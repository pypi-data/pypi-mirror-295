""" Report which will show all adjustments to transactions including
debit notes, reversal credit notes, rebill credit notes and write
offs
"""
import csv
import datetime

import cpsar.report
import cpsar.runtime as R
import cpsar.util as U
import cpsar.ws as W
import cpsar.sagel as S
import kcontrol as K

class Program(W.HTTPMethodMixIn, W.MakoProgram):
    ## Submitted Form Value Properties

    def do_get(self):
        params = ReportParams(self._req)
        params.update_form_store()
        self._set_default_tmpl_args()

    def do_post(self):
        self._set_default_tmpl_args()
        params = ReportParams(self._req)
        params.update_form_store()
        cursor = R.db.cursor()

        if params.group_number:
            create_group_table_for_group_number(params.group_number)
        elif params.report_code:
            create_group_table_for_report_code(params.report_code)
        else:
            create_group_table_for_all()

        create_report_table()
        for record_type in params.record_types:
            insert_report_records(record_type,
                params.from_entry_date,
                params.to_entry_date)
        if params.patient_first_name:
            delete_patient_by_first_name(params.patient_first_name)
        if params.patient_last_name:
            delete_patient_by_last_name(params.patient_last_name)
        if params.pharmacy_filter == 'M':
            delete_non_mailorder_records()
        elif params.pharmacy_filter == 'R':
            delete_non_retail_records()

        record_fields = fields_for_record(params.grouping, params.fields)
        records = report_records(params.grouping)
        if params.export_csv:
            self._send_csv_file(record_fields, records)
        else:
            self.tmpl['record_fields'] = record_fields
            self.tmpl['records'] = records

        delete_report_table()
        delete_group_table()

    def _set_default_tmpl_args(self):
        self.tmpl['fields'] = fields()
        self.tmpl['groupings'] = groupings()
        
    ## Report Running Methods
    def _send_csv_file(self, fields, records):
        self._res.content_type = 'text/csv'
        h = self._res.headers
        self.mako_auto_publish = False
        h.add("Expires", "0")
        h.add("Content-Transfer-Encoding", "binary")
        h.add("Pragma", "public")
        h.add("Content-Disposition", "attachment; filename=trans_adjustments.csv")
        writer = csv.writer(self._res)
        writer.writerow([f[1] for f in fields])
        for rec in records:
            writer.writerow([rec[f] for f, c in fields])

def create_group_table_for_all():
    cursor = R.db.cursor()
    cursor.execute("""
      CREATE TEMP TABLE report_group AS
        SELECT group_number FROM client
    """)

def create_group_table_for_report_code(report_code):
    cursor = R.db.cursor()
    cursor.execute("""
      CREATE TEMP TABLE report_group AS
        SELECT DISTINCT group_number
        FROM client_report_code
        WHERE report_code=%s
    """, (report_code,))

def create_group_table_for_group_number(group_number):
    cursor = R.db.cursor()
    cursor.execute("""
      CREATE TEMP TABLE report_group (group_number VARCHAR);
      INSERT INTO report_group VALUES(%s);
      """, (group_number,))

def delete_group_table():
    cursor = R.db.cursor()
    cursor.execute("DROP TABLE report_group")

def create_report_table():
    cursor = R.db.cursor()
    cursor.execute("""
    CREATE TEMP TABLE report (
        adjustment_type varchar,
        adjust_id varchar,
        amount decimal(10, 2),
        entry_date date,
        entry_month varchar,
        entry_note text,
        trans_id bigint,
        invoice_id bigint,
        line_no int,
        patient_name varchar,
        patient_first_name varchar,
        patient_last_name varchar,
        batch_date date,
        group_number varchar,
        client_name varchar,
        rx_number int,
        rx_date date,
        tx_type char(2),
        claim_number varchar,
        username varchar,
        pharmacy varchar,
        nabp varchar,
        drug_name varchar,
        doctor_npi_number varchar,
        doctor_name varchar,
        compound_code char,
        adj_trans_id bigint,
        adj_invoice_id bigint,
        void_date date,
        total decimal,
        ref_no text,
        puc_id bigint,
        payment_type_name text
    )
    """)

def delete_report_table():
    cursor = R.db.cursor()
    cursor.execute("DROP TABLE report")

def insert_report_records(record_type, from_date, to_date):
    type_procedures = {
        'adjudications': insert_adjudication_records,
        'writeoffs': insert_writeoff_records,
        'rebill_credits': insert_rebill_credit_records,
        'rebate_credits': insert_rebate_credits_records,
        'debit': insert_debit_records,
        'payments': insert_payment_records
    }
    if record_type not in type_procedures:
        return
    type_procedures[record_type](from_date, to_date)

def insert_payment_records(from_date, to_date):
    cursor = R.db.cursor()
    cursor.execute("""
      INSERT INTO report
      SELECT 'PY',
             'PY' || trans_payment.payment_id,
             -trans_payment.amount,
             trans_payment.entry_date::date,
             to_char(trans_payment.entry_date, 'YYYY-MM MON'),
             trans_payment.note,
             trans_payment.trans_id,
             trans.invoice_id,
             trans.line_no,
             patient.first_name || ' ' || patient.last_name,
             patient.first_name as patient_first_name,
             patient.last_name as patient_last_name,
             trans.batch_date,
             trans.group_number,
             client.client_name,
             trans.rx_number,
             trans.rx_date,
             trans.tx_type,
             claim.claim_number,
             trans_payment.username,
             pharmacy.name,
             pharmacy.nabp,
             drug.name,
             trans.doctor_npi_number,
             doctor.name,
             trans.compound_code,
             NULL AS adj_trans_id,
             NULL AS adj_invoid_id,
             NULL AS void_date,
             trans.total,
             trans_payment.ref_no,
             trans_payment.puc_id,
             payment_type.type_name AS payment_type_name
        FROM trans_payment
        JOIN trans USING(trans_id)
        JOIN client USING(group_number)
        JOIN report_group USING(group_number)
        JOIN patient USING(patient_id)
        JOIN pharmacy USING(pharmacy_id)
        JOIN drug USING(drug_id)
        JOIN history USING(history_id)
        LEFT JOIN claim USING(claim_id)
        LEFT JOIN doctor ON history.doctor_id = doctor.doctor_id
        LEFT JOIN payment_type USING(ptype_id)
        WHERE trans_payment.entry_date::date BETWEEN %s AND %s
    """, (from_date, to_date))

def insert_adjudication_records(from_date, to_date):
    cursor = R.db.cursor()
    cursor.execute("""
      INSERT INTO report
      SELECT 'ADJ',
             'ADJ' || trans_adjudication.adjudication_id,
             -trans_adjudication.amount,
             trans_adjudication.entry_date::date,
             to_char(trans_adjudication.entry_date, 'YYYY-MM MON'),
             trans_adjudication.note,
             trans_adjudication.trans_id,
             trans.invoice_id,
             trans.line_no,
             patient.first_name || ' ' || patient.last_name,
             patient.first_name as patient_first_name,
             patient.last_name as patient_last_name,
             trans.batch_date,
             trans.group_number,
             client.client_name,
             trans.rx_number,
             trans.rx_date,
             trans.tx_type,
             claim.claim_number,
             trans_adjudication.username,
             pharmacy.name,
             pharmacy.nabp,
             drug.name,
             trans.doctor_npi_number,
             doctor.name,
             trans.compound_code,
             source.trans_id,
             source.invoice_id,
             trans_adjudication.void_date,
             trans.total,
             NULL AS ref_no,
             NULL AS puc_id,
             NULL AS payment_type_name
        FROM trans_adjudication
        JOIN trans USING(trans_id)
        JOIN client USING(group_number)
        JOIN report_group USING(group_number)
        JOIN patient USING(patient_id)
        JOIN pharmacy USING(pharmacy_id)
        JOIN drug USING(drug_id)
        JOIN history USING(history_id)
        LEFT JOIN claim USING(claim_id)
        LEFT JOIN doctor ON history.doctor_id = doctor.doctor_id
        JOIN reversal ON trans_adjudication.reversal_id = reversal.reversal_id
        JOIN trans AS source ON reversal.trans_id = source.trans_id
        WHERE trans_adjudication.entry_date::date BETWEEN %s AND %s
    """, (from_date, to_date))

def insert_writeoff_records(from_date, to_date):
    cursor = R.db.cursor()
    cursor.execute("""
      INSERT INTO report
      SELECT 'WO',
             'WO' || trans_writeoff.writeoff_id,
             -trans_writeoff.amount,
             trans_writeoff.entry_date::date,
             to_char(trans_writeoff.entry_date, 'YYYY-MM MON'),
             trans_writeoff.note,
             trans_writeoff.trans_id,
             trans.invoice_id,
             trans.line_no,
             patient.first_name || ' ' || patient.last_name,
             patient.first_name as patient_first_name,
             patient.last_name as patient_last_name,
             trans.batch_date,
             trans.group_number,
             client.client_name,
             trans.rx_number,
             trans.rx_date,
             trans.tx_type,
             claim.claim_number,
             trans_writeoff.username,
             pharmacy.name,
             pharmacy.nabp,
             drug.name,
             trans.doctor_npi_number,
             doctor.name,
             trans.compound_code,
             NULL,
             NULL,
             trans_writeoff.void_date,
             trans.total,
             NULL AS ref_no,
             NULL AS puc_id,
             NULL AS payment_type_name
        FROM trans_writeoff
        JOIN trans USING(trans_id)
        JOIN client USING(group_number)
        JOIN report_group USING(group_number)
        JOIN patient USING(patient_id)
        JOIN pharmacy USING(pharmacy_id)
        JOIN drug USING(drug_id)
        JOIN history USING(history_id)
        LEFT JOIN doctor ON history.doctor_id = doctor.doctor_id
        LEFT JOIN claim USING(claim_id)
        WHERE trans_writeoff.entry_date::date BETWEEN %s AND %s
    """, (from_date, to_date))

def insert_debit_records(from_date, to_date):
    cursor = R.db.cursor()
    cursor.execute("""
      INSERT INTO report
      SELECT 'DB',
             'DB' || trans_debit.debit_id,
             trans_debit.amount,
             trans_debit.entry_date::date,
             to_char(trans_debit.entry_date, 'YYYY-MM MON'),
             trans_debit.note,
             trans_debit.trans_id,
             trans.invoice_id,
             trans.line_no,
             patient.first_name || ' ' || patient.last_name,
             patient.first_name as patient_first_name,
             patient.last_name as patient_last_name,
             trans.batch_date,
             trans.group_number,
             client.client_name,
             trans.rx_number,
             trans.rx_date,
             trans.tx_type,
             claim.claim_number,
             trans_debit.username,
             pharmacy.name,
             pharmacy.nabp,
             drug.name,
             trans.doctor_npi_number,
             doctor.name,
             trans.compound_code,
             NULL,
             NULL,
             NULL,
             trans.total,
             NULL AS ref_no,
             NULL AS puc_id,
             NULL AS payment_type_name
        FROM trans_debit
        JOIN trans USING(trans_id)
        JOIN client USING(group_number)
        JOIN report_group USING(group_number)
        JOIN patient USING(patient_id)
        JOIN pharmacy USING(pharmacy_id)
        JOIN drug USING(drug_id)
        JOIN history USING(history_id)
        LEFT JOIN claim USING(claim_id)
        LEFT JOIN doctor ON history.doctor_id = doctor.doctor_id
        WHERE trans_debit.entry_date::date BETWEEN %s AND %s
    """, (from_date, to_date))

def insert_rebill_credit_records(from_date, to_date):
    cursor = R.db.cursor()
    cursor.execute("""
      INSERT INTO report
      SELECT 'RC',
             'RC' || rebill_credit.rebill_credit_id,
             -rebill_credit.amount,
             rebill_credit.entry_date::date,
             to_char(rebill_credit.entry_date, 'YYYY-MM MON'),
             NULL,
             rebill_credit.trans_id,
             trans.invoice_id,
             trans.line_no,
             patient.first_name || ' ' || patient.last_name,
             patient.first_name as patient_first_name,
             patient.last_name as patient_last_name,
             trans.batch_date,
             trans.group_number,
             client.client_name,
             trans.rx_number,
             trans.rx_date,
             trans.tx_type,
             claim.claim_number,
             rebill_credit.username,
             pharmacy.name,
             pharmacy.nabp,
             drug.name,
             trans.doctor_npi_number,
             doctor.name,
             trans.compound_code,
             NULL,
             NULL,
             NULL,
             trans.total,
             NULL AS ref_no,
             NULL AS puc_id,
             NULL AS payment_type_name
        FROM rebill_credit
        JOIN trans USING(trans_id)
        JOIN client USING(group_number)
        JOIN report_group USING(group_number)
        JOIN patient USING(patient_id)
        JOIN pharmacy USING(pharmacy_id)
        JOIN drug USING(drug_id)
        JOIN history USING(history_id)
        LEFT JOIN claim USING(claim_id)
        LEFT JOIN doctor ON history.doctor_id = doctor.doctor_id
        WHERE rebill_credit.entry_date::date BETWEEN %s AND %s
    """, (from_date, to_date))

def insert_rebate_credits_records(from_date, to_date):
    cursor = R.db.cursor()
    cursor.execute("""
      INSERT INTO report
      SELECT 'RB',
             'RB' || rebate_credit.rebate_credit_id,
             -rebate_credit.amount,
             rebate_credit.entry_date::date,
             to_char(rebate_credit.entry_date, 'YYYY-MM MON'),
             NULL,
             rebate_credit.trans_id,
             trans.invoice_id,
             trans.line_no,
             patient.first_name || ' ' || patient.last_name,
             patient.first_name as patient_first_name,
             patient.last_name as patient_last_name,
             trans.batch_date,
             trans.group_number,
             client.client_name,
             trans.rx_number,
             trans.rx_date,
             trans.tx_type,
             claim.claim_number,
             rebate_credit.username,
             pharmacy.name,
             pharmacy.nabp,
             drug.name,
             trans.doctor_npi_number,
             doctor.name,
             trans.compound_code,
             NULL,
             NULL,
             NULL,
             trans.total,
             NULL AS ref_no,
             NULL AS puc_id,
             NULL AS payment_type_name
        FROM rebate_credit
        JOIN trans USING(trans_id)
        JOIN client USING(group_number)
        JOIN report_group USING(group_number)
        JOIN patient USING(patient_id)
        JOIN pharmacy USING(pharmacy_id)
        JOIN drug USING(drug_id)
        JOIN history USING(history_id)
        LEFT JOIN claim USING(claim_id)
        LEFT JOIN doctor ON history.doctor_id = doctor.doctor_id
        WHERE rebate_credit.entry_date::date BETWEEN %s AND %s
    """, (from_date, to_date))

## Grouping of tra
def groupings():
    return [('detail', 'Detail'), ('month_group', 'Month/Group')]

def report_records(grouping):
    if grouping == 'month_group':
        return _report_records_by_month_group()
    else: 
        return _detailed_report_records()

def _detailed_report_records():
    cursor = R.db.dict_cursor()
    cursor.execute("SELECT * FROM report ORDER BY entry_date, adjust_id")
    return list(cursor)

def _report_records_by_month_group():
    agg = S.aggregator()
    agg_fnames = [f for f, c in entry_month_fields() if f not in ["count", "amount"]]
    agg_fields = tuple(map(S.field, agg_fnames))
    agg.add_level(agg_fields, (S.count("count"), S.sum("amount")))
    records = agg.transform(_detailed_report_records(), False)
    records = [f for f in records if f['_type'] == 'ah']
    sort_key = lambda x:(x['entry_month'], x['group_number'], x['adjustment_type'])
    return sorted(records, key=sort_key)

## Fields available on report
def fields_for_record(grouping, names):
    if grouping == 'month_group':
        return entry_month_fields()

    f = []
    for field, caption in fields():
        if field in names:
            f.append((field, caption))
    return f

def entry_month_fields():
    return [
        ("entry_month", "Entry Month"),
        ("adjustment_type", "Type"),
        ("group_number", "Group Number"),
        ("client_name", "Client Name"),
        ("count", "Count"),
        ("amount", "Amount")
    ]

def fields():
    return [
    ('adjustment_type', 'Type'),
    ('adjust_id', 'ID'),
    ('amount', 'Amount'),
    ('entry_date', 'Entry Date'),
    ('entry_note', 'Entry Note'),
    ('trans_id', 'Trans #'),
    ('invoice_id', 'Invoice #'),
    ('line_no', 'Line #'),
    ('patient_name', 'Patient'),
    ('batch_date', 'Batch Date'),
    ('group_number', 'Group #'),
    ('client_name', 'Client Name'),
    ('rx_number', 'RX #'),
    ('rx_date', 'RX Date'),
    ('tx_type', 'Tx Type'),
    ('claim_number', 'Claim #'),
    ('pharmacy', 'Pharmacy'),
    ('nabp', 'NABP #'),
    ('drug_name', 'Drug'),
    ('doctor_npi_number', 'Doctor NPI #'),
    ('doctor_name', 'Doctor Name'),
    ('compound_code', 'Compound Code'),
    ('adj_trans_id', 'Adj Trans #'),
    ('adj_invoice_id', 'Adj Invoice #'),
    ('username', 'Entered By'),
    ('void_date', 'Void Date'),
    ('total', 'Tx Total'),
    ('ref_no', 'Ref #'),
    ('puc_id', 'PUC #'),
    ('payment_type_name', 'Payment Type')
    ]

## Pharmacy Filtering
def delete_non_mailorder_records():
    cursor = R.db.cursor()
    cursor.execute("""
      DELETE FROM report
      WHERE nabp != %s
    """, (R.CPS_NABP_NBR,))

def delete_patient_by_last_name(last_name):
    cursor = R.db.cursor()
    cursor.execute("""
        delete from report where patient_last_name != %s
        """, (last_name.upper(),))

def delete_patient_by_first_name(first_name):
    cursor = R.db.cursor()
    cursor.execute("""
        delete from report where patient_first_name != %s
        """, (first_name.upper(),))

def delete_non_retail_records():
    cursor = R.db.cursor()
    cursor.execute("""
      DELETE FROM report
      WHERE nabp = %s
    """, (R.CPS_NABP_NBR,))

## Parameters for the report
class ReportParams(object):
    def __init__(self, req):
        self._req = req

    @property
    def group_number(self):
        return self._req.params.get('group_number')

    @property
    def report_code(self):
        if self.group_number:
            return None
        else:
            return self._req.params.get('report_code')

    @property
    def from_entry_date(self):
        val = self._date_form_val('from_entry_date')
        if val:
            return val
        today = datetime.date.today()
        first_day_of_month = datetime.date(today.year, today.month, 1)
        last_day_of_last_month = first_day_of_month - datetime.timedelta(days=1)
        first_day_of_last_month = datetime.date(
            last_day_of_last_month.year,
            last_day_of_last_month.month, 1)
        return first_day_of_last_month 

    @property
    def to_entry_date(self):
        val = self._date_form_val('to_entry_date')
        if val:
            return val

        today = datetime.date.today()
        first_day_of_month = datetime.date(today.year, today.month, 1)
        last_day_of_last_month = first_day_of_month - datetime.timedelta(days=1)
        return last_day_of_last_month

    @property
    def patient_first_name(self):
        return self._req.params.get('patient_first_name', '').strip()

    @property
    def patient_last_name(self):
        return self._req.params.get('patient_last_name', '').strip()

    @property
    def record_types(self):
        return self._req.params.getall('record_types')

    @property
    def fields(self):
        return self._req.params.getall('fields')

    @property
    def export_csv(self):
        return bool(self._req.params.get('export_csv'))

    @property
    def pharmacy_filter(self):
        return self._req.params.get('pharmacy')

    @property
    def grouping(self):
        grp = self._req.params.get('grouping')
        for name, cap in groupings():
            if grp == name:
                return grp
        return 'detail'

    def update_form_store(self):
        K.store.update({
            'group_number': self.group_number,
            'report_code': self.report_code,
            'from_entry_date': self.from_entry_date,
            'to_entry_date': self.to_entry_date,
            'record_types': self.record_types,
            'patient_first_name': self.patient_first_name,
            'patient_last_name': self.patient_last_name,
            'fields': self.fields,
            'export_csv': self.export_csv,
            'grouping': self.grouping
        })
        
    ## Utility
    def _date_form_val(self, field):
        val = self._req.params.get(field)
        try:
            return U.parse_american_date(val)
        except (TypeError, U.ParseError):
            return None


application = Program.app
