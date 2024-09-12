""" Summary Cash Receipt Report
@summary:  Written for Nancy
"""
import datetime
import kcontrol as K

import cpsar.wsgirun as W
import cpsar.report
import cpsar.runtime as R

from cpsar import sales
from cpsar.controls import PharmacyFilterListBox

class Report(cpsar.report.WSGIReport):
    label = "Summary Cash Receipt Report"
    summary = """Provides a list of all checks received from clients over a specified
    time frame. This includes payments and overpayments.
    """

    def form_params(self):
        self.params = [
            ('Group Number', sales.ClientListBox('group_number')),
            ('Report Code', K.TextBox('report_code')),
            ('Pharmacy Filter', PharmacyFilterListBox('pharmacy')),
            ('Payment Date After', K.DatePicker('payment_date_after',
                     defaultValue=datetime.date.today()-datetime.timedelta(2)   )),
            ('Payment Date Before', K.DatePicker('payment_date_before',
                     defaultValue=datetime.date.today()))
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
    WITH payments_by_group AS (
        SELECT trans.group_number,
               trans.trans_id,
               trans.batch_date,
               trans_payment.entry_date::date AS payment_date,
               amount,
               'payment' AS payment_applied_type
        FROM trans_payment
        JOIN trans USING(trans_id)
        WHERE trans_payment.entry_date::date BETWEEN
            %(payment_date_after)s AND %(payment_date_before)s
            AND trans.group_number %(gn_frag)s
            AND trans_payment.puc_id IS NULL
            AND trans_payment.credit_group_number IS NULL
            AND trans.pharmacy_nabp %(nabp_frag)s
        UNION ALL
        SELECT trans.group_number,
               trans.trans_id,
               trans.batch_date,
               overpayment.entry_date::date AS payment_date,
               amount,
               'overpayment' AS payment_applied_type
        FROM overpayment
        JOIN trans USING(trans_id)
        WHERE overpayment.entry_date::date BETWEEN
            %(payment_date_after)s AND %(payment_date_before)s
            AND trans.group_number %(gn_frag)s
            AND trans.pharmacy_nabp %(nabp_frag)s
      )
    SELECT group_number AS "Group Number",
           payment_date AS "Payment Date",
           batch_date AS "Batch Date",
           payment_applied_type AS "Payment Applied Type",
           COUNT(*) AS "Receipt Count",
           format_currency(SUM(amount)) AS Amount
    FROM payments_by_group
    GROUP BY group_number, payment_date, batch_date, payment_applied_type
    UNION ALL
    SELECT 'zzTotal', NULL, NULL,NULL, COUNT(*), format_currency(SUM(amount))
    FROM payments_by_group
    ORDER BY "Group Number", "Payment Date", "Batch Date"
    """
 
application = Report().wsgi()
