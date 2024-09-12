import datetime

import kcontrol as K
import cpsar.wsgirun as W
import cpsar.report
import cpsar.runtime as R

from cpsar.controls import PharmacyFilterListBox
from cpsar import sales

class Report(cpsar.report.WSGIReport):
    label = 'Detailed Cash Receipts'
    def form_params(self):
        self.params = [
            ('Group Number', sales.ClientListBox('group_number')),
            ('Report Code', K.TextBox('report_code')),
            ('Pharmacy Filter', PharmacyFilterListBox('pharmacy')),
            ('Posting Date After', K.DatePicker('posting_date_after',
                     defaultValue=datetime.date.today()-datetime.timedelta(2),
                     required=True
                     )),
            ('Posting Date Before', K.DatePicker('posting_date_before',
                     defaultValue=datetime.date.today(), required=True))
        ]

    query_css = """
        TD.data11 { text-align: right; }
    """

    def query_args(self):
        args = super(Report, self).query_args()
        phcy = self.req.get('pharmacy')
        if phcy == "C":
            args['nabp_frag'] = "= %s AND trans.compound_code = '2'" % \
                cpsar.pg.qstr(R.CPS_NABP_NBR)
        elif phcy == "M":
            args['nabp_frag'] = "= %s AND trans.compound_code = '1'" % \
                cpsar.pg.qstr(R.CPS_NABP_NBR)
        elif phcy == "R":
            args['nabp_frag'] = '<> %s' % cpsar.pg.qstr(R.CPS_NABP_NBR)
        else:
            args['nabp_frag'] = "IS NOT NULL"
        return args

    sql = """
    WITH payments_by_trans_id AS (
        SELECT trans.trans_id,
               trans.tx_type,
               trans.group_number,
               trans.pharmacy_nabp,
               trans.batch_date,
               rx_number, 
               patient.first_name || ' ' || patient.last_name AS patient,
               refill_number || ' (' || refill_number %% 20 || ')' AS refill_number,
               trans_payment.entry_date::date AS payment_date,
               payment_type.type_name,
               drug.name as drug_name,
               trans_payment.ref_no,
               trans_payment.username,
               trans_payment.amount,
               trans.compound_code,
               'payment' as payment_applied_type
        FROM trans_payment
        JOIN trans USING(trans_id)
        JOIN payment_type USING(ptype_id)
        JOIN drug USING(drug_id)
        JOIN patient ON trans.patient_id = patient.patient_id
        WHERE trans_payment.entry_date::date BETWEEN
              %(posting_date_after)s AND %(posting_date_before)s
              AND trans.group_number %(gn_frag)s
              AND trans_payment.puc_id IS NULL
              AND trans_payment.credit_group_number IS NULL
              AND trans.pharmacy_nabp %(nabp_frag)s
        UNION ALL
        SELECT trans.trans_id,
               trans.tx_type,
               trans.group_number,
               trans.pharmacy_nabp,
               trans.batch_date,
               trans.rx_number, 
               patient.first_name || ' ' || patient.last_name AS patient,
               refill_number || ' (' || refill_number %% 20 || ')' AS refill_number,
               overpayment.entry_date::date AS payment_date,
               payment_type.type_name,
               drug.name as drug_name,
               overpayment.ref_no,
               overpayment.username,
               overpayment.amount,
               trans.compound_code,
               'overpayment' AS payment_applied_type
        FROM overpayment
        JOIN trans USING(trans_id)
        JOIN drug using(drug_id)
        JOIN payment_type USING(ptype_id)
        JOIN patient USING(patient_id)
        WHERE overpayment.entry_date::date BETWEEN
            %(posting_date_after)s and %(posting_date_before)s
            AND trans.group_number %(gn_frag)s
            AND trans.pharmacy_nabp %(nabp_frag)s
    )
    SELECT trans_id as "Trans ID",
           tx_type AS "Type",
           group_number AS "Group Number",
           drug_name AS "Drug Name",
           pharmacy_nabp AS "Pharmacy NABP",
           batch_date AS "Batch Date",
           rx_number AS "RX Number",
           patient AS "Patient Name",
           refill_number AS "Refill Number",
           payment_date AS "Payment Date",
           type_name AS "Type",
           ref_no AS "Reference No",
           username AS "Username",
           payment_applied_type AS "Payment Applied Type",
           compound_code as "Compound Code",
           '' AS "_",
           format_currency(amount) AS "Amount"
    FROM payments_by_trans_id
    UNION ALL
    SELECT NULL,
           NULL,
           NULL,
           NULL,
           NULL,
           NULL,
           NULL,
           NULL,
           NULL,
           NULL,
           NULL,
           NULL,
           NULL,
           NULL,
           NULL,
           'TOTAL',
           format_currency(sum(payments_by_trans_id.amount))
     FROM payments_by_trans_id
    ORDER BY "_", "Trans ID", "Payment Date"
    """

application = Report().wsgi()
