#!/usr/bin/env python
""" Program to add Pinnacle transactions from PK data. We use our locally cached
data from PK that is loaded into PostgreSQL daily.
"""
import datetime
import decimal
import time

import cpsar.runtime as R
import cpsar.util as U
from cpsar import cobol
from cpsar.wsgirun import mako, wsgi, json, PathDispatch

reg = PathDispatch()

@reg
@mako("import_pk.tmpl")
def index(req, res):
    res['pharmacy_id'] = _cps_pharmacy_id()
    res['pharmacy_nabp'] = R.CPS_NABP_NBR
    res['drug_ndc'] = _drug_ndc()
    res['drug_id'] = _drug_id()

def _drug_ndc(): return '00000000000'
def _drug_id():
    cursor = R.db.cursor()
    cursor.execute("SELECT drug_id FROM drug WHERE ndc_number=%s",
        (_drug_ndc(),))
    return cursor.fetchone()[0]

def _cps_pharmacy_id():
    cursor = R.db.cursor()
    cursor.execute("SELECT pharmacy_id FROM pharmacy WHERE nabp=%s",
        (R.CPS_NABP_NBR,))
    return cursor.fetchone()[0]

@reg
def pk_lookup(req, res):
    try:
        rx_number = int(req.get('pk_rx_number'))
    except (ValueError, TypeError):
        res.write("No rx number given")
        return
    group_number = req.get('group_number')
    if not group_number:
        res.write("no group given")
        return

    cursor = R.db.dict_cursor()
    cursor.execute("""
        SELECT
            pc_rxfill.rxfill_id,
            pc_rxfill.patient_price,
            to_char(pc_rxfill.fill_date, 'MM/DD/YYYY') AS fill_date,
            pc_patient.patient_id AS pc_patient_id,
            pc_patient.firstname, 
            pc_patient.lastname,
            pc_patient.cardnumber1,
            to_char(pc_patient.birthdate, 'MM/DD/YYYY') AS birthdate,
            patient.patient_id,
            pk_trans_sup.trans_id
        FROM pc_rxfill
        JOIN pc_rxmain USING (rxmain_id)
        JOIN pc_patient USING(patient_id)
        LEFT JOIN pc_sales_person ON pc_rxfill.sales_person_id
                = pc_sales_person.sales_person_id
        LEFT JOIN pk_trans_sup USING(rxfill_id)
        LEFT JOIN patient ON
            patient.dob = pc_patient.birthdate AND
            patient.ssn = pc_patient.patient_id::text AND
            patient.group_number =  %s
        WHERE pc_rxfill.rx_number = %s
        ORDER BY fill_date DESc
        """, (group_number, rx_number))
    if not cursor.rowcount:
        res.write("No results found")
        return

    res.write("""<table class='grid'><thead><tr>
        <th>rxfill_id</th>
        <th>Fill Date</th>
        <th>Name</th>
        <th>Patient ID</th>
        <th>DOB</th>
        <th>PK Cardholder #</th>
        <th>Price</th>
        <th></th>
    </tr></thead>""")
    for rec in cursor:
        res.write("""<tr>
          <td class='rxfill_id'>%(rxfill_id)s</td>
          <td>%(fill_date)s</td>
          <td>%(firstname)s %(lastname)s</td>
          <td><span class='patient_id'>%(pc_patient_id)s</span></td>
          <td>%(birthdate)s</td>
          <td>%(cardnumber1)s</td>
          <td><span class='price'>%(patient_price)s</span></td>
        """ % rec)
        if rec['trans_id']:
            link = "<a href='/view_trans?trans_id=%(trans_id)s' target='_blank'> " % rec
            res.write("<td>Existing trans: %s%s</a></td>" % (link, rec['trans_id']))
        elif not rec['patient_id']:
            if rec['birthdate']:
                res.write("""<td>Patient not on file in %s
                    <input type='button' class='add_patient' value='Add patient' />
                    </td>
                """ % group_number)
            else:
                res.write("<td>Cannot add patient with no DOB on file</td>")
        else:
            res.write("<td><input type='button' class='use_pk' value='Load' /></td>")
        res.write("</tr>")
    res.write("</table>")

@reg
@json
def add_patient(req, res):
    try:
        rxfill_id = int(req.get("rxfill_id"))
    except (ValueError, TypeError):
        res.error("no rxfill id given")
        return
    group_number = req.get("group_number")
    if not group_number:
        res.error("no group number given")
        return
    cursor = R.db.dict_cursor()
    cursor.execute("""
     INSERT INTO patient (group_number, dob, ssn, first_name, last_name, name, ctime)
     SELECT %s,
        pc_patient.birthdate,
        pc_patient.patient_id::text,
        pc_patient.firstname, 
        pc_patient.lastname,
        pc_patient.firstname || ' ' || pc_patient.lastname,
        NOW()
        FROM pc_rxfill
        JOIN pc_rxmain USING (rxmain_id)
        JOIN pc_patient USING(patient_id)
        LEFT JOIN pc_sales_person ON pc_rxfill.sales_person_id
                = pc_sales_person.sales_person_id
        WHERE pc_rxfill.rxfill_id = %s
    """, (group_number, rxfill_id))
    if cursor.rowcount == 0:
        res.error('no rxfill with id %s' % rxfill_id)
    R.db.commit()

@reg
@json
def pk_data(req, res):
    try:
        rxfill_id = int(req.get("rxfill_id"))
    except (ValueError, TypeError):
        res.error("invalid rxfill id")
        return
    group_number = req.get("group_number")
    if not group_number:
        res.error("no group given")
        return
    cursor = R.db.dict_cursor()
    cursor.execute("""
    SELECT
        rxfill_id,
        nextval('grouph_auth_nbr_seq') AS group_auth,
        to_char(pc_rxfill.fill_date, 'MM/DD/YYYY') AS fill_date,
        pc_rxfill.rx_number,
        to_char(pc_rxmain.date_written, 'MM/DD/YYYY') AS date_written,
        pc_rxmain.daw,
        pc_rxfill.quantity,
        pc_rxfill.days_supply,
        pc_rxfill.patient_price,
        20 as shipping_price,
        pc_rxfill.pharmacy_cost,
        pc_doctor.dea,
        pc_doctor.firstname || ' ' || pc_doctor.lastname AS doctor_name,
        to_char(pc_rxfill.date_entered, 'MM/DD/YYYY') AS date_entered,
        patient.patient_id,
        patient.first_name,
        patient.last_name,
        patient.ssn,
        to_char(patient.dob, 'MM/DD/YYYY') AS dob,
        pc_sales_person.lastname AS referring_nabp
    FROM pc_rxfill
    JOIN pc_rxmain USING(rxmain_id)
    JOIN pc_patient ON pc_patient.patient_id = pc_rxmain.patient_id
    LEFT JOIN pc_sales_person ON pc_rxfill.sales_person_id
            = pc_sales_person.sales_person_id
    LEFT JOIN pc_doctor ON pc_rxmain.doctor_id = pc_doctor.doctor_id
    LEFT JOIN patient ON
        patient.group_number = %s AND
        patient.dob = pc_patient.birthdate AND
        patient.ssn = pc_patient.patient_id::text
    WHERE pc_rxfill.rxfill_id=%s
    """, (group_number, rxfill_id))

    rec = dict(cursor.fetchone())

    # refill_number
    cursor.execute("""
        SELECT rxfill_id
        FROM pc_rxfill
        WHERE rx_number=%s
        ORDER BY pc_rxfill.fill_date, rxfill_id
        """, (rec['rx_number'],))
    rec['refill_number'] = 0
    for idx, srec in enumerate(cursor):
        if srec['rxfill_id'] == rxfill_id:
            rec['refill_number'] = idx
            break

    res.update(rec)
    res['group_number'] = group_number

@reg
@json
def lookup_invoice_id(req, res):
    try:
        batch_date = U.parse_american_date(req.get('batch_date'))
    except U.ParseError:
        return
    try:
        patient_id = int(req.get('patient_id'))
    except ValueError:
        return

    cursor = R.db.cursor()
    cursor.execute("""
        SELECT MAX(invoice_id), MAX(line_no)+1
        FROM trans
        WHERE batch_date=%s AND patient_id=%s
        """, (batch_date, patient_id))

    res['invoice_id'], res['line_no'] = cursor.fetchone()
    if res['invoice_id']:
        return

    cursor.execute("SELECT MAX(invoice_id)+1 FROM trans")
    res['invoice_id'] = cursor.fetchone()[0]
    res['line_no'] = 1

@reg
@json
def add(req, res):
    ## Internal Utility
    def _date_value(field_name):
        if not req.get(field_name): return None
        try:
            return U.parse_american_date(req.get(field_name))
        except U.ParseError:
            res.error('Invalid date %s for %s', req.get(field_name), field_name)
    def _currency_value(field_name):
        if not req.get(field_name):
            return decimal.Decimal("0.00")
        try:
            return decimal.Decimal(req.get(field_name))
        except decimal.InvalidOperation:
            res.error('Invalid currency value %s for %s', req.get(field_name), field_name)

    cursor = R.db.dict_cursor()

    try:
        rxfill_id = int(req.get('rxfill_id'))
    except ValueError:
        res.error('invalid rxfill_id %s', req.get('rxfill_id'))
        return

    # Referring pharmacy. They are storing the NABP in the sales person
    # lastname field.
    cursor.execute("""
        SELECT pc_sales_person.lastname
        FROM pc_rxfill
        LEFT JOIN pc_sales_person ON pc_rxfill.sales_person_id
                = pc_sales_person.sales_person_id
        WHERE rxfill_id=%s
        """, (rxfill_id,))
    if not cursor.rowcount:
        res.error('No fill in PK software with rxfill_id of %s', rxfill_id)
        return
    rec = cursor.fetchone()


    # Group Number
    group_number = req.get('group_number')
    if not group_number:
        res.error("no group # given")


    # Referring NABP
    referring_nabp = req.get('referring_nabp') or ''
    if len(referring_nabp) > 20:
        res.error('The referring NABP is longer than 20 characters from the PK'
                  ' sales person table')
    if group_number == 'GROUPPRC' and not referring_nabp:
        res.error('referring NABP required for GROUPRC for distributon')

    # Group Auth
    try:
        group_auth = int(req.get('group_auth'))
    except ValueError:
        res.error('Invalid group_auth %s', req.get('group_auth'))
        return
    cursor.execute("""
      SELECT history_id FROM history
      WHERE group_number=%s AND group_auth=%s
      """, (group_number, group_auth))
    if cursor.rowcount:
        res.error('group_auth %s already found for %s: assigned to HY %s',
                  group_auth, group_number, cursor.fetchone()['history_id'])
        return

    # Patient ID
    try:
        patient_id = int(req.get('patient_id'))
    except ValueError:
        res.error('Invalid patient_id %s', req.get('patient_id'))
        return
    cursor.execute("SELECT * FROM patient WHERE patient_id=%s", (patient_id,))
    if not cursor.rowcount:
        res.error('No patient with id %s found', patient_id)
        return
    prec = cursor.fetchone()
    patient_dob = prec['dob']
    patient_ssn = prec['ssn']
    
    # Drug ID
    try:
        drug_id = int(req.get('drug_id'))
    except ValueError:
        res.error('Invalid drug_id %s', req.get('drug_id'))
        return
    cursor.execute('SELECT * FROM drug where drug_id=%s', (drug_id,))
    if not cursor.rowcount:
        res.error('No drug with id %s found', drug_id)
        return
    drug_ndc_number = cursor.fetchone()['ndc_number']

    # Pharmacy ID
    try:
        pharmacy_id = int(req.get('pharmacy_id'))
    except ValueError:
        res.error('Invalid pharmacy_id', req.get('pharmacy_id'))
        return
    cursor.execute('SELECT * FROM pharmacy WHERE pharmacy_id=%s', (pharmacy_id,))
    if not cursor.rowcount:
        res.error('No pharmacy with id %s found', pharmacy_id)
        return
    pharmacy_nabp = cursor.fetchone()['nabp']

    # Doctor ID
    doctor_name = req.get('doctor_name')
    doctor_id = None
    dea = req.get('doctor_dea_number')
    npi = req.get('doctor_npi_number')
    
    if dea:
        cursor.execute("""
          SELECT doctor_id FROM doctor_key WHERE doc_key=%s
          """, (dea,))
        if cursor.rowcount:
            doctor_id = cursor.fetchone()['doctor_id']
        else:
            doctor_id = doctor_id_for_new(dea, req.get('doctor_name'))
    elif npi:
        cursor.execute("""
          SELECT doctor_id FROM doctor_key WHERE doc_key=%s
          """, (npi,))
        if cursor.rowcount:
            doctor_id = cursor.fetchone()['doctor_id']

    rx_date = _date_value('rx_date')
    date_written = _date_value('date_written')

    batch_date = _date_value('batch_date')
    if not batch_date:
        res.error('missing required batch date')
        return

    # Quantity
    try:
        quantity = decimal.Decimal(req.get('quantity'))
    except decimal.InvalidOperation:
        res.error('Invalid quantity %s', req.get('quantity'))
        return

    # Day's Supply
    try:
        days_supply = int(req.get('days_supply'))
    except ValueError:
        res.error('Invalid days supply')
        return

    # Compound Code
    compound_code = req.get('compound_code')
    if compound_code not in ('1', '2'):
        res.error('Invalid compound code %r', compound_code)
        return

    # DAW
    daw = req.get('daw')
    if len(daw) > 1:
        res.error('DAW must be 1 character')
        return

    # Rx Number/ Refill #
    try:
        rx_number = int(req.get('rx_number'))
    except ValueError:
        res.error('Invalid rx_number %s', rx_number)
        return
    try:
        refill_number = int(req.get('refill_number'))
    except ValueError:
        res.error('Invalid refill_number %s', refill_number)
        return

    # Invoice ID/Line No
    try:
        invoice_id = int(req.get('invoice_id'))
    except ValueError:
        res.error('Invalid invoice_id %s', req.get('invoice_id'))
        return
    try:
        line_no = int(req.get('line_no'))
    except ValueError:
        res.error('Invalid line_no %s', req.get('line_no'))
        return
    cursor.execute("""
        SELECT trans_id FROM trans
        WHERE invoice_id=%s AND line_no=%s
        """, (invoice_id, line_no))
    if cursor.rowcount:
        res.error("Invoice/Line %s:%s already assigned to trans %s",
            invoice_id, line_no, cursor.fetchone()['trans_id'])
        return
    cursor.execute("""
        SELECT patient_id FROM trans
        WHERE invoice_id=%s
        """, (invoice_id,))
    if cursor.rowcount:
        opid = cursor.fetchone()['patient_id']
        if opid != patient_id:
            res.error("Invoice ID %s is already assigned to another patient "
                "with ID %s", invoice_id, opid)
            return

    cost_submitted = _currency_value('cost_submitted')
    cost_allowed = _currency_value('cost_allowed')
    dispense_fee = _currency_value('dispense_fee')
    processing_fee = _currency_value('processing_fee')
    pharmacy_cost = _currency_value('pharmacy_cost')
    sales_tax = _currency_value('sales_tax')
    eho_network_copay = _currency_value('eho_network_copay')
    usual_customary = _currency_value('usual_customary')
    savings = _currency_value('savings')
    state_fee = _currency_value('state_fee')
    awp = _currency_value('awp')

    drug_cost = _currency_value('drug_cost')
    labor_cost = _currency_value('labor_cost')
    shipping_cost = _currency_value('shipping_cost')

    if res.has_error():
        return

    total = cost_allowed + dispense_fee + processing_fee + sales_tax - eho_network_copay

    # Batch file
    batch_file_name = "pk-cmpd-%s" % batch_date.strftime("%Y%m%d")
    cursor.execute("""
      SELECT batch_file_id FROM batch_file
      WHERE file_name=%s
      """, (batch_file_name,))
    if cursor.rowcount:
        batch_file_id = cursor.fetchone()[0]
    else:
        cursor.execute(U.insert_sql("batch_file", {
            'batch_date': batch_date,
            'file_name': batch_file_name
        }, ['batch_file_id']))
        batch_file_id = cursor.fetchone()[0]

    ## history record
    hrec = {
        'group_number': group_number,
        'group_auth': group_auth,
        'patient_id': patient_id,
        'pharmacy_id': pharmacy_id,
        'doctor_id': doctor_id,
        'drug_id': drug_id,
        'rx_date': rx_date,
        'rx_number': rx_number,
        'date_written': date_written,
        'daw': daw,
        'quantity': quantity,
        'days_supply': days_supply,
        'compound_code': compound_code,
        'refill_number': refill_number,
        'cost_submitted': cost_submitted,
        'cost_allowed': cost_allowed,
        'dispense_fee': dispense_fee,
        'processing_fee': processing_fee,
        'sales_tax': sales_tax,
        'eho_network_copay': eho_network_copay,
        'usual_customary': usual_customary,
        'state_fee': state_fee,
        'awp': awp,
        'date_processed': datetime.datetime.now(),
        'doctor_dea_number': dea,
        'doctor_npi_number': npi,
        'tx_type': req.get('tx_type'),
        'ctime': datetime.datetime.now()
    }
    cursor.execute(U.insert_sql('history', hrec, ['*']))
    hrec = cursor.fetchone()
    history_id = hrec['history_id']
    res['hrec'] = dict(hrec)

    # trans record
    trec = dict(
        batch_date = batch_date,
        create_date = batch_date,
        batch_file_id = batch_file_id,
        group_number = group_number,
        group_auth = group_auth,
        invoice_id = invoice_id,
        line_no = line_no,
        patient_dob = patient_dob,
        patient_cardholder_nbr = patient_ssn,
        patient_id = patient_id,
        pharmacy_nabp = pharmacy_nabp,
        pharmacy_id = pharmacy_id,
        doctor_dea_number = dea,
        doctor_npi_number = npi,
        drug_ndc_number = drug_ndc_number,
        drug_id = drug_id,
        rx_date = rx_date,
        rx_number = rx_number,
        date_written = date_written,
        daw = daw,
        quantity = quantity,
        days_supply = days_supply,
        compound_code = compound_code,
        refill_number = refill_number,
        cost_submitted = cost_submitted,
        cost_allowed = cost_allowed,
        dispense_fee = dispense_fee,
        sales_tax = sales_tax,
        eho_network_copay = eho_network_copay,
        processing_fee = processing_fee,
        usual_customary = usual_customary,
        state_fee = state_fee,
        total = total,
        balance = total,
        awp = awp,
        savings = savings,
        tx_type = req.get('tx_type'),
        history_id = history_id)
    
    cursor.execute(U.insert_sql('trans', trec, ['*']))
    res['trec'] = dict(cursor.fetchone())
    trans_id = res['trec']['trans_id']

    upsert_invoice(invoice_id)

    def add_distribution(account, amount, referring_pharmacy=False):
        cursor.execute(U.insert_sql('distribution', dict(
            trans_id=trans_id,
            distribution_account=account,
            amount=amount,
            referring_pharmacy=referring_pharmacy
        )))

    if group_number == 'GROUPPRC':
        # 80 dollar distribution for whatever NABP the sales person
        # the referring pharmacy NABP
        # rest of it goes to CPS
        # add a field to the distribution that is flagged as "Referring Pharmacy"
        add_distribution(referring_nabp, 80, True)
        add_distribution('cps', total - 80)
    elif group_number == 'HELIOS':
        # Glenn and Randy get %5 of the markup (pharmacy cost - )
        markup = total - pharmacy_cost - shipping_cost
        if markup > 0:
            glenn = markup * decimal.Decimal(".05")
            randy = glenn
            add_distribution("glencox", glenn)
            add_distribution("randy_beckham", randy)
            total = total - glenn - randy
            add_distribution("cps", total)
    elif group_number == 'GROUPMJO':
        markup = total - pharmacy_cost - shipping_cost
        if markup > 0:
            glenn = markup * decimal.Decimal(".10")
            total = total - glenn
            add_distribution('glencox', glenn)
        add_distribution('cps', total)
    elif group_number == 'ALIUS':
        if total < decimal.Decimal("15.00"):
            raise ValueError('ALIUS transaction with total under 15.00')
        fifteen = decimal.Decimal('15.00')
        add_distribution("bailey", fifteen)
        add_distribution("cps", total - fifteen)
    elif group_number == 'WAM':
        if total < decimal.Decimal("1.00"):
            raise ValueError('WAM transaction with total under 1.00')
        fifteen = decimal.Decimal('1.00')
        add_distribution("bailey", fifteen)
        add_distribution("cps", total - fifteen)
    elif group_number == 'GROUPSPL':
        markup = total - pharmacy_cost - shipping_cost
        if markup > 0:
            glenn = markup * decimal.Decimal(".10")
            total = total - glenn
            add_distribution('glencox', glenn)
        add_distribution('cps', total)
    elif group_number == 'GROUPMSQ':
        markup = total - pharmacy_cost - shipping_cost
        if markup > 0:
            glenn = markup * decimal.Decimal(".10")
            total = total - glenn
            add_distribution('glencox', glenn)
        add_distribution('cps', total)
    else:       # group_number == 'GROUPH'
        add_distribution('cps', total)

    cursor.execute(U.insert_sql('pk_trans_sup', dict(
        trans_id=trans_id,
        rxfill_id=rxfill_id,
        drug_cost=drug_cost,
        labor_cost=labor_cost,
        shipping_cost=shipping_cost,
        referring_nabp=referring_nabp,
        pharmacy_cost=pharmacy_cost
    )))
    R.db.commit()

def upsert_invoice(invoice_id):
    cursor = R.db.cursor()
    total, balance, item_count = _invoice_aggregates(invoice_id)
    cursor.execute("""
      UPDATE invoice SET total = %s, balance = %s, item_count = %s
      WHERE invoice_id = %s
      RETURNING *
      """, (total, balance, item_count, invoice_id))
    if cursor.rowcount > 0:
        return

    cursor.execute("""
      SELECT patient_id, group_number, batch_date, 
             batch_date + INTERVAL '15 days'
      FROM trans
      WHERE invoice_id=%s
      LIMIT 1
      """, (invoice_id,))
    if not cursor.rowcount:
        return
    patient_id, group_number, batch_date, due_date = cursor.fetchone()
    cursor.execute(U.insert_sql('invoice', dict(
      invoice_id=invoice_id,
      patient_id=patient_id,
      group_number=group_number,
      batch_date=batch_date,
      due_date=due_date,
      total=total,
      adjustments=0,
      balance=balance,
      item_count=item_count
    )))

def _invoice_aggregates(invoice_id):
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT SUM(total), SUM(balance), COUNT(*)
        FROM trans WHERE invoice_id=%s
        """, (invoice_id,))
    return [c or 0 for c in cursor.fetchone()]

def doctor_id_for_new(dea, name):
    record = {'name': name}
    result = cobol.query('corp-docfm2', record)
    doctor_id = result['results'][0]['doctor_id']
    record = {'doctor_id': doctor_id, 'doc_key': dea}
    cobol.query('corp-doc-key-set', record)
    time.sleep(1)
    return doctor_id

application = reg.get_wsgi_app()
