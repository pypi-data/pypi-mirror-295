import datetime

import kcontrol as K
import cpsar.wsgirun as W
import cpsar.report
import cpsar.runtime as R

from cpsar.controls import PharmacyFilterListBox
from cpsar import sales

class Report(cpsar.report.WSGIReport):
    label = 'Cash Receipts By Invoice'
    def form_params(self):
        self.params = [
            ('Group Number', sales.ClientListBox('group_number')),
            ('Report Code', K.TextBox('report_code')),
            ('Pharmacy Filter', PharmacyFilterListBox('pharmacy')),
            ('Posting Date After', K.DatePicker('posting_date_after',
                     defaultValue=datetime.date.today()-datetime.timedelta(2)   )),
            ('Posting Date Before', K.DatePicker('posting_date_before',
                     defaultValue=datetime.date.today()))
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
    WITH all_payments AS (
        SELECT trans.invoice_id,
               trans.tx_type,
               trans.group_number,
               trans.pharmacy_nabp,
               trans.batch_date,
               patient.first_name || ' ' || patient.last_name AS patient_name,
               trans_payment.entry_date::date AS payment_date,
               payment_type.type_name,
               trans_payment.ref_no,
               trans_payment.username,
               trans_payment.amount,
               'payment' AS payment_applied_type
        FROM trans_payment
        JOIN trans USING(trans_id)
        JOIN payment_type USING(ptype_id)
        JOIN patient ON trans.patient_id = patient.patient_id
        WHERE trans_payment.entry_date::date BETWEEN
              %(posting_date_after)s AND %(posting_date_before)s
              AND trans.group_number %(gn_frag)s
              AND trans_payment.puc_id IS NULL
              AND trans_payment.credit_group_number IS NULL
              AND trans.pharmacy_nabp %(nabp_frag)s
        UNION ALL
        SELECT trans.invoice_id,
               trans.tx_type,
               trans.group_number,
               trans.pharmacy_nabp,
               trans.batch_date,
               patient.first_name || ' ' || patient.last_name AS patient_name,
               overpayment.entry_date::date AS payment_date,
               payment_type.type_name,
               overpayment.ref_no,
               overpayment.username,
               overpayment.amount,
               'overpayment' AS payment_applied_type
        FROM overpayment
        JOIN trans USING(trans_id)
        JOIN payment_type USING(ptype_id)
        JOIN patient USING(patient_id)
        WHERE overpayment.entry_date::date BETWEEN
            %(posting_date_after)s and %(posting_date_before)s
            AND trans.group_number %(gn_frag)s
            AND trans.pharmacy_nabp %(nabp_frag)s
    )
    SELECT invoice_id AS "Invoice ID",
           tx_type AS "TX Type",
           group_number AS "Group Number",
           pharmacy_nabp AS "Pharmacy NABP",
           batch_date AS "Batch Date",
           patient_name AS "Patient Name",
           payment_applied_type AS "Payment Applied Type",
           MAX(payment_date) AS "Most Recent Payment Date",
           array_to_string(array_accum(DISTINCT type_name), ', ') AS "Type",
           array_to_string(array_accum(DISTINCT ref_no), ', ') AS "Reference No",
           array_to_string(array_accum(DISTINCT username), ', ') AS "Usernames",
           '' AS "_",
           COUNT(*) AS "Payments",
           format_currency(SUM(amount)) AS "Amount"
    FROM all_payments
    GROUP BY "Invoice ID", "TX Type", "Group Number", "Pharmacy NABP", "Batch Date",
             "Patient Name", "Payment Applied Type", "_"
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
           'TOTAL',
           COUNT(*),
           format_currency(sum(all_payments.amount))
     FROM all_payments
    ORDER BY "_", "Invoice ID", "Most Recent Payment Date"
    """

application = Report().wsgi()
