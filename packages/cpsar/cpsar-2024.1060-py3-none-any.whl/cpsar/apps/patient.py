""" CPSAR WSGI PATH_INFO Application Skeleton
"""
import datetime
import decimal
import io
import functools

import xlsxwriter

from cpsar import pg
from cpsar import txlib
import cpsar.runtime as R
from cpsar.wsgirun import json
from cpsar.wsgirun import mako, MakoRecord
from cpsar.wsgirun import PathDispatch
import cpsar.util as U

reg = PathDispatch()

def patres(proc):
    """ Patient view decorator. Ensure the patient exists and populate
    the response with patient information from the database.
    """
    def inner(req, tmpl):
        patient_id = req.params.get('patient_id', '').strip()
        if not patient_id:
            return tmpl.error("Invalid param")

        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT *
            FROM patient
            WHERE patient_id=%s
            """, (patient_id,))

        if not cursor.rowcount:
            return tmpl.not_found()

        patient = cursor.fetchone()
        tmpl['patient'] = patient
        proc(req, tmpl, patient_id)
    functools.update_wrapper(inner, proc)
    return inner

@reg
@mako('patient.tmpl')
@patres
def index(req, tmpl, patient_id):
    cursor = R.db.dict_cursor()
    cursor.execute("""
        SELECT trans.*, drug.name AS drug_name, history.date_processed,
               pharmacy.name AS pharmacy_name
        FROM trans
        JOIN drug USING(drug_id)
        JOIN history USING(history_id)
        JOIN pharmacy ON trans.pharmacy_id = pharmacy.pharmacy_id
        WHERE trans.patient_id=%s
        ORDER BY trans.trans_id DESC
        """, (patient_id,))
    tmpl['transactions'] = pg.all(cursor)

    cursor.execute("""
        SELECT username, entry_date, message
        FROM patient_log
        WHERE patient_id=%s
        """, (patient_id,))
    tmpl['logs'] = pg.all(cursor)

@reg
@mako('patient_history.tmpl')
@patres
def history(req, tmpl, patient_id):
    """ Show the user a list of all history records for the user. """
    cursor = R.db.dict_cursor()
    cursor.execute("""
        SELECT history_id, group_number, group_auth, rx_number
        FROM history
        WHERE patient_id = %s
        """, (patient_id,))
    tmpl['history'] = pg.all(cursor)

@reg
@mako('patient_uc.tmpl')
@patres
def uc(req, tmpl, patient_id):
    """ Show the user a list of all unapplied cash. """
    cursor = R.db.dict_cursor()
    cursor.execute("""
        SELECT overpayment.balance,
               overpayment.amount,
               overpayment.entry_date::date AS entry_date,
               overpayment.puc_id,
               payment_type.type_name,
               overpayment.ref_no,
               overpayment.trans_id,
               username
        FROM overpayment
        JOIN trans USING(trans_id)
        JOIN payment_type USING(ptype_id)
        WHERE trans.patient_id=%s AND overpayment.balance != 0
        UNION ALL
        SELECT reversal.balance,
               reversal.total,
               reversal.entry_date,
               reversal.reversal_id,
               'REV',
               reversal.reversal_id::text,
               reversal.trans_id,
               ''
        FROM reversal
        JOIN trans USING(trans_id)
        WHERE trans.patient_id=%s AND reversal.balance != 0

        ORDER BY entry_date
        """, (patient_id, patient_id))
    tmpl['unapplied_cash'] = pg.all(cursor)

@reg
@mako('patient_sale_of_account.tmpl')
@patres
def sale_of_account(req, tmpl, patient_id):
    """ Show the user the form to pick the params for the rx history
    report.
    """
    pass

@reg
@mako('patient_credit_memo.tmpl')
@patres
def credit_memo(req, tmpl, patient_id):
    """ show the credit memo report form """
    tmpl['start_entry_date'] = _last_monday()
    tmpl['end_entry_date'] = _last_sunday()
    tmpl['as_of'] = datetime.date.today()

###############################################################################
@reg
@mako('patient_credit_memo_report.tmpl')
@patres
def credit_memo_submit(req, tmpl, patient_id):
    start_entry_date = req.params.get('start_entry_date')
    end_entry_date = req.params.get('end_entry_date')
    as_of = req.params.get('as_of')
    cursor = R.db.dict_cursor()
    cursor.execute_file("ar/patient_credit_memo_report.sql", {
        'patient_id': patient_id,
        'start_entry_date': req.params.get('start_entry_date'),
        'end_entry_date': req.params.get('end_entry_date'),
        'as_of': req.params.get('as_of')
    })

    tmpl['report'] = list(cursor)

    cursor.execute("SELECT * FROM client WHERE group_number=%s",
        (tmpl['patient']['group_number'],))
    tmpl['client'] = cursor.fetchone()

    cursor.execute("""
        SELECT DISTINCT claim_number
        FROM claim
        JOIN patient USING(patient_id)
        WHERE patient.patient_id = %s
        """, (patient_id,))

    tmpl['claim_numbers'] = ','.join([c['claim_number'] or '' for c in cursor])

def _last_monday():
    today = datetime.date.today()
    return today - datetime.timedelta(days=today.weekday(), weeks=1)

def _last_sunday():
    today = datetime.date.today()
    return today - datetime.timedelta(days=today.weekday()+1)

###############################################################################
@reg
def gen_sale_of_account(req, res):
    """ Send the report to the user in MS Excel. """
    tmpl = MakoRecord(req, res, 'patient_gen_sale_of_account.tmpl')

    patient_id = req.params.get('patient_id', '').strip()
    if not patient_id:
        res.status = 404
        return
    cursor = R.db.dict_cursor()
    cursor.execute("""
        SELECT *
        FROM patient
        WHERE patient_id=%s
        """, (patient_id,))

    if not cursor.rowcount:
        res.status = 404
        return

    patient = cursor.fetchone()
    tmpl['patient'] = patient

    start_date = req.params.get('start_date')
    end_date = req.params.get('end_date')
    if not start_date or not end_date:
        return tmpl.error('Missing start or end date')

    if req.params.get('show_paid_reversal'):
        extra_where = """
        reversal_id IS NULL OR
        (reversal_id IS NOT NULL AND trans.paid_amount > 0)
        """
    else:
        extra_where = "reversal_id IS NULL"

    cursor = R.db.dict_cursor()

    cursor.execute("""
        select group_number, client_name, address_1, address_2, city, state, 
               zip_code
        from client
        where group_number=(
            select group_number
            from patient
            where patient_id=%s)
        """, (patient_id,))
    tmpl['client'] = dict(cursor.fetchone())
    for k, v in tmpl['client'].items():
        if v is None:
            tmpl['client'][k] = ''

    cursor.execute(f"""
        SELECT trans.rx_date, pharmacy.name AS pharmacy_name,
               drug.ndc_number, trans.rx_number, trans.refill_number %% 20 as refill_number,
               drug.name AS drug_name,
               trans.days_supply,
               trans.quantity,
               trans.total,
               doctor.name AS doctor_name,
               client.invoice_multiplier
        FROM trans
        JOIN client USING(group_number)
        LEFT JOIN reversal ON trans.trans_id = reversal.trans_id
        JOIN drug USING(drug_id)
        JOIN pharmacy ON trans.pharmacy_id = pharmacy.pharmacy_id
        LEFT JOIN doctor USING(doctor_id)
        WHERE trans.patient_id=%s AND
            rx_date BETWEEN %s AND %s
            AND {extra_where}
        ORDER BY trans.trans_id ASC
        """, (patient_id, start_date, end_date))

    tmpl['start_date'] = start_date
    tmpl['end_date'] = end_date

    transactions = pg.all(cursor)
    grand_total = decimal.Decimal("0.0")
    for trans in transactions:
        for k, v in trans.items():
            if v is None:
                trans[k] = ''

        if req.params.get("use_multiplier"):
            trans['total'] = trans['total'] * trans['invoice_multiplier']
            trans['total'] = U.count_money(trans['total'])
            trans['total_fmt'] = pg.format_currency(trans['total'])
        grand_total += trans['total']

    tmpl['transactions'] = transactions
    tmpl['grand_total'] = grand_total
    tmpl['grand_total_fmt'] = pg.format_currency(grand_total)
    tmpl['client']['grand_total_fmt'] = tmpl['grand_total_fmt']

    if req.params.get("format") == "xlsx":
        buf = generate_patient_report(tmpl['patient'], tmpl['client'], tmpl['transactions'], start_date, end_date)
        res.content_type = 'application/vnd.ms-excel'
        res.headers.add("Content-Disposition", "attachment; filename=rx_history.xlsx")
        res.write(buf.getvalue())
    else:
        return tmpl()

def generate_patient_report(patient, client, transactions, start_date, end_date):
    # Create an in-memory output file for the new workbook.
    output = io.BytesIO()

    # Create a new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    # Define some formats to use in the workbook.
    bold = workbook.add_format({'bold': True})
    date_format = workbook.add_format({'num_format': 'mm/dd/yyyy'})
    currency_format = workbook.add_format({'num_format': '$#,##0.00'})

    worksheet.set_column('A:A', 15)  # Date
    worksheet.set_column('B:B', 20)  # Pharmacy
    worksheet.set_column('C:C', 10)  # Rx #
    worksheet.set_column('D:D', 10)  # Refill #
    worksheet.set_column('E:E', 30)  # Drug
    worksheet.set_column('F:F', 5)   # DS
    worksheet.set_column('G:G', 5)   # Qty
    worksheet.set_column('H:H', 10)  # Amount
    worksheet.set_column('I:I', 20)  # NDC and Doctor

    # Write headers
    worksheet.write('A1', 'Corporate Pharmacy Services', bold)
    worksheet.write('A2', '319 Broad Street', bold)
    worksheet.write('A3', 'Gadsden, AL 35901', bold)
    worksheet.write('A5', f'Record of Sale of Account:', bold)
    worksheet.write('E5', f'From: {start_date} To: {end_date}', bold)

    # Write patient and client info
    worksheet.write('A7', f"Patient: {patient['first_name']} {patient['last_name']}")
    worksheet.write('B7', f"Birth Date: {patient['dob'].strftime('%m/%d/%Y')}", date_format)
    worksheet.write('E7', f"Client: {client['client_name']} {client['group_number']}")

    worksheet.write('A8', f"{patient['address_1']} {patient['address_2'] or ''}")
    worksheet.write('E8', f"{client['address_1']} {client['address_2'] or ''}")

    worksheet.write('A9', f"{patient['city']}, {patient['state']} {patient['zip_code']}")
    worksheet.write('E9', f"{client['city']}, {client['state']} {client['zip_code']}")

    # Write table headers
    headers = ['Date', 'Pharmacy', 'Rx #', 'Refill #', 'Drug', 'DS', 'Qty', 'Amount']
    for col_num, header in enumerate(headers):
        worksheet.write(11, col_num, header, bold)

    # Write transactions
    row_num = 12
    for transaction in transactions:
        worksheet.write(row_num, 0, transaction['rx_date'].strftime('%m/%d/%Y'), date_format)
        worksheet.write(row_num, 1, transaction['pharmacy_name'])
        worksheet.write(row_num, 2, transaction['rx_number'])
        worksheet.write(row_num, 3, transaction['refill_number'])
        worksheet.write(row_num, 4, transaction['drug_name'])
        worksheet.write(row_num, 5, transaction['days_supply'])
        worksheet.write(row_num, 6, transaction['quantity'])
        worksheet.write(row_num, 7, transaction['total_fmt'], currency_format)

        row_num += 1
        worksheet.write(row_num, 1, f"NDC: {transaction['ndc_number']}", bold)
        worksheet.write(row_num, 2, f"DR: {transaction['doctor_name']}", bold)
        row_num += 1

    # Write total
    worksheet.write(row_num, 6, 'Total:', bold)
    worksheet.write(row_num, 7, client['grand_total_fmt'], currency_format)

    # Final lines for signatures
    worksheet.write(row_num + 3, 1, 'Signed by R.Ph:', bold)
    worksheet.write(row_num + 5, 1, 'License #:', bold)
    worksheet.write(row_num + 7, 1, 'Federal Tax ID:', bold)

    # Close the workbook
    workbook.close()

    # Get the value of the BytesIO buffer and rewind the buffer to the beginning
    output.seek(0)

    return output

@reg
@mako('patient_card_print_log.tmpl')
@patres
def card_print_log(req, tmpl, patient_id):
    cursor = R.db.dict_cursor()
    cursor.execute("""
        SELECT *
        FROM card_print_log
        WHERE patient_id=%s
        ORDER BY print_time DESC
        """, (patient_id,))
    tmpl['card_print_log'] = pg.all(cursor)

@reg
@json
def revoke_uc(req, res):
    """ Delete the unapplied cash record from the system. This is only
    allowed if the balance of the record is the same as the amount,
    AKA the UC record has not been applied to any transactions.
    """
    puc_id = req.params.get('puc_id')
    if not puc_id:
        return res.not_found()

    try:
        txlib.revoke_overpayment(puc_id)
    except ValueError as e:
        res['errors'] = [str(e)]
        return

    R.db.commit()

application = reg.get_wsgi_app()
