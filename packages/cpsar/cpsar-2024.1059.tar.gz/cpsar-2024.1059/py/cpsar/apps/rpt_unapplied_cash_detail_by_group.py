import datetime
import cpsar.runtime as R

from cpsar import controls
from cpsar import report
from cpsar import sales
from cpsar import pg

class Report(report.WSGIReport):
    label = "Unapplied Cash Report - Detail by Group"
    def form_params(self):
        self.params = [
            ('Group Number', sales.ClientListBox('group_number')),
            ('Report Code', controls.TextBox('report_code')),
            ('Pharmacy Filter', controls.PharmacyFilterListBox('pharmacy')),
            ('Start Entry Date', controls.DatePicker('start_date')),
            ('End Entry Date',   controls.DatePicker('end_date')),
            ('As Of Date',   controls.DatePicker('as_of', value=datetime.date.today()))
        ]

    def validate_form_input(self):
        g = lambda s: self.req.get(s).strip()
        if not g('start_date'):
            R.error("Start date required")
        if not g('end_date'):
            R.error("End date required")
        if not g('group_number') and not g('report_code'):
            R.error("Group Number or Report Code required")

    def query_args(self):
        args = super(Report, self).query_args()
        phcy = self.req.get('pharmacy')
        if phcy == "C":
            args['nabp_frag'] = "= %s AND trans.compound_code = '2'" % \
                pg.qstr(R.CPS_NABP_NBR)
        elif phcy == "M":
            args['nabp_frag'] = "= %s AND trans.compound_code = '1'" % \
                pg.qstr(R.CPS_NABP_NBR)
        elif phcy == "R":
            args['nabp_frag'] = '<> %s' % pg.qstr(R.CPS_NABP_NBR)
        else:
            args['nabp_frag'] = "IS NOT NULL"
        return args


    _record_fields = []
    def record_fields(self):
        return self._record_fields

    def records(self):
        cursor = R.db.dict_cursor()
        self.expanded_sql = self.sql % self.query_args()
        cursor.execute(self.expanded_sql)
        self._record_fields = [c[0] for c in cursor.description]

        if self.csv_export:
            return cursor

        x = []
        for rec in map(dict, cursor):
            tmpl = "<a href='/patient?patient_id=%s'>%s</a>"
            rec['first_name'] = tmpl % (rec['patient_id'], rec['first_name'])
            rec['last_name'] = tmpl % (rec['patient_id'], rec['last_name'])
            x.append([rec[c] for c in self._record_fields])
        return x

    sql = """
    SELECT trans.trans_id,
           trans.invoice_id || '-' || trans.line_no as invoice_no,
           trans.batch_date,
           NULL as reversal_date,
           overpayment.entry_date::date,
           client.client_name,
           client.group_number,
           trans.claim_number,
           trans.rx_date,
           'OP' AS type,
           patient.first_name,
           patient.last_name,
           patient.dob,
           patient.ssn,
           patient.status,
           patient.patient_id,
           trans.doi,
           drug.name AS drug_name,
           trans.compound_code,
           trans.quantity,
           payment_type.type_name,
           overpayment.ref_no,
           overpayment.balance AS balance,
           overpayment.note
    FROM overpayment_as_of(%(as_of)s) as overpayment
    JOIN trans USING(trans_id)
    JOIN client USING(group_number)
    JOIN payment_type USING(ptype_id)
    JOIN patient USING(patient_id)
    JOIN drug USING(drug_id)
    WHERE overpayment.entry_date::date BETWEEN
            %(start_date)s AND %(end_date)s
          AND trans.group_number %(gn_frag)s
          AND trans.pharmacy_nabp %(nabp_frag)s
          AND overpayment.balance != 0
    UNION ALL
    SELECT trans.trans_id,
           trans.invoice_id || '-' || trans.line_no as invoice_no,
           trans.batch_date,
           reversal.reversal_date,
           reversal.entry_date::date,
           client.client_name,
           client.group_number,
           trans.claim_number,
           trans.rx_date,
           'PR' AS type,
           patient.first_name,
           patient.last_name,
           patient.dob,
           patient.ssn,
           patient.status,
           patient.patient_id,
           trans.doi,
           drug.name AS drug_name,
           trans.compound_code,
           trans.quantity,
           array_to_string(tp.type_name, ', '),
           array_to_string(tp.ref_no, ', '),
           reversal.balance AS balance,
           '' AS note
    FROM reversal_as_of(%(as_of)s::date) as reversal
    JOIN client USING(group_number)
    JOIN trans USING(trans_id)
    JOIN patient USING(patient_id)
    JOIN drug USING(drug_id)
    LEFT JOIN (
        SELECT trans_id, 
               array_accum(DISTINCT payment_type.type_name) AS type_name,
               array_accum(DISTINCT ref_no) AS ref_no
        FROM trans_payment
        JOIN payment_type USING(ptype_id)
        GROUP BY trans_id
    ) AS tp ON tp.trans_id = trans.trans_id

    WHERE reversal.entry_date BETWEEN %(start_date)s AND %(end_date)s
          AND reversal.group_number %(gn_frag)s
          AND trans.pharmacy_nabp %(nabp_frag)s
          AND reversal.balance != 0 
    ORDER BY trans_id
    """
 
application = Report().wsgi()
