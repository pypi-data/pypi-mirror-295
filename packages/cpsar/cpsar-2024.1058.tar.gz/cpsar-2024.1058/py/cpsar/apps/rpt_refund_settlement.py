""" The refund settlement report rshows all of the refunds issued over a
period of time for a sponsor. The report shows both settlements for
reversals and overpayments. We do not include voided settlements in this
report.
"""
import kcontrol as K

import cpsar.wsgirun as W
import cpsar.report
import cpsar.runtime as R

from cpsar.controls import PharmacyFilterListBox
from cpsar import sales

class Report(cpsar.report.WSGIReport):
    label = "Refund Settlement Report"
    def form_params(self):
        self.params = [
            ('Group Number', sales.ClientListBox('group_number')),
            ('Report Code', K.TextBox('report_code')),
            ('Pharmacy Filter', PharmacyFilterListBox('pharmacy')),
            ('Start Refund Date', K.DatePicker('start_date')), 
            ('End Refund Date',   K.DatePicker('end_date'))
        ]

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
    SELECT 
           client.group_number,
           client.client_name,
           trans.trans_id,
           trans.invoice_id || '-' || trans.line_no as invoice_no,
           trans.claim_number,
           trans.pharmacy_nabp,
           trans.rx_date,
           trans.rx_number,
           'OP' AS type,
           patient.first_name,
           patient.last_name,
           patient.ssn,
           patient.dob,
           fmt_ndc(drug.ndc_number) AS ndc,
           drug.name AS drug_name,
           trans.quantity,
           overpayment.balance AS "OP/PR Amount",
           overpayment_settlement.entry_date::date AS refund_date,
           overpayment_settlement.check_no AS refund_check_no,
           overpayment_settlement.amount AS refund_amount
    FROM overpayment
    JOIN trans USING(trans_id)
    JOIN client USING(group_number)
    JOIN patient USING(patient_id)
    JOIN drug USING(drug_id)
    JOIN overpayment_settlement USING(puc_id)
    WHERE overpayment_settlement.entry_date::date BETWEEN
            %(start_date)s AND %(end_date)s
          AND overpayment_settlement.void_date IS NULL
          AND trans.group_number %(gn_frag)s
          AND trans.pharmacy_nabp %(nabp_frag)s
    UNION ALL
    SELECT client.group_number,
           client.client_name,
           trans.trans_id,
           trans.invoice_id || '-' || trans.line_no as invoice_no,
           trans.claim_number,
           trans.pharmacy_nabp,
           trans.rx_date,
           trans.rx_number,
           'PR' AS type,
           patient.first_name,
           patient.last_name,
           patient.ssn,
           patient.dob,
           fmt_ndc(drug.ndc_number) AS ndc,
           drug.name AS drug_name,
           trans.quantity,
           reversal.balance,
           reversal_settlement.entry_date::date,
           reversal_settlement.check_no,
           reversal_settlement.amount
    FROM reversal
    JOIN client USING(group_number)
    JOIN trans USING(trans_id)
    JOIN patient USING(patient_id)
    JOIN drug USING(drug_id)
    JOIN reversal_settlement USING(reversal_id)
    WHERE reversal_settlement.entry_date
            BETWEEN %(start_date)s AND %(end_date)s
          AND reversal_settlement.void_date IS NULL
          AND reversal.group_number %(gn_frag)s
          AND trans.pharmacy_nabp %(nabp_frag)s
    ORDER BY trans_id
    """
 
application = Report().wsgi()

