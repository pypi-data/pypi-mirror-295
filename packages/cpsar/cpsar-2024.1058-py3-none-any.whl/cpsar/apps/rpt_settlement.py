""" Report to procduce a list of all settlements that have occured over a
specific date range.

"""
import kcontrol as K

import cpsar.wsgirun as W
import cpsar.report

from cpsar import sales

class Report(cpsar.report.WSGIReport):
    label = "Settlement Report"
    summary = """Provides a list of all checks paid back to clients
    over the specified time-frame.
    """

    def form_params(self):
        self.params = [
            ('Group Number', sales.ClientListBox('group_number')),
            ('Start Entry Date', K.DatePicker('start_date')), 
            ('End Entry Date',   K.DatePicker('end_date'))
        ]

    sql = """
        SELECT
           trans.trans_id,
           'CK' || check_no AS ref,
           'PR' AS type,
           to_char(reversal_settlement.entry_date, 'mm/dd/yy') AS entry_date,
           to_char(reversal_settlement.entry_date, 'HH:MM AM') AS entry_time,
           reversal_settlement.amount,
           reversal_settlement.username
        FROM reversal_settlement
        JOIN reversal USING(reversal_id)
        JOIN trans USING(trans_id)
        WHERE
            trans.group_number %(gn_frag)s
            AND reversal_settlement.entry_date::date
                BETWEEN %(start_date)s AND %(end_date)s
            AND reversal_settlement.void_date IS NULL
        UNION ALL
        SELECT
            trans.trans_id,
            'CK' || overpayment_settlement.check_no,
            'OP',
           to_char(overpayment_settlement.entry_date, 'mm/dd/yy') AS entry_date,
           to_char(overpayment_settlement.entry_date, 'HH:MM AM') AS entry_time,
           overpayment_settlement.amount,
           overpayment.username
        FROM overpayment_settlement
        JOIN overpayment USING(puc_id)
        JOIN trans USING(trans_id)
        WHERE
            trans.group_number %(gn_frag)s
            AND overpayment_settlement.entry_date::date
                BETWEEN %(start_date)s AND %(end_date)s
            AND overpayment_settlement.void_date IS NULL
        ORDER BY entry_date, entry_time
    """
 
application = Report().wsgi()
