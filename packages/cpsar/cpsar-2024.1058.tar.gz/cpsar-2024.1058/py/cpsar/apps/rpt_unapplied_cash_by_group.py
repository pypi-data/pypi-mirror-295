import datetime

import cpsar.wsgirun as W
import cpsar.report

from cpsar import sales
from cpsar import controls

class Report(cpsar.report.WSGIReport):
    label = "Current Unapplied Cash by Group Summary"
    def form_params(self):
        self.params = [
            ('Start Entry Date', controls.DatePicker('start_date')), 
            ('End Entry Date',   controls.DatePicker('end_date')),
            ('As Of Date',  controls.DatePicker('as_of', value=datetime.date.today()))
        ]

    sql = """
     SELECT group_number, client_name, type, SUM(balance) AS balance
     FROM (
        SELECT client.group_number,
               client.client_name,
               'Over Payments' AS type,
               overpayment_as_of.balance
        FROM overpayment_as_of(%(as_of)s)
        JOIN trans USING(trans_id)
        JOIN client USING(group_number)
        WHERE overpayment_as_of.entry_date::date BETWEEN
            %(start_date)s AND %(end_date)s

        UNION ALL

        SELECT client.group_number,
               client.client_name,
               'Paid Reversals' AS type,
               reversal_as_of.balance
        FROM reversal_as_of(%(as_of)s)
        JOIN client USING(group_number)
        JOIN trans USING(trans_id)
        WHERE reversal_as_of.entry_date BETWEEN
            %(start_date)s AND %(end_date)s
      ) AS x
      WHERE balance != 0
      GROUP BY group_number, client_name, type
      ORDER BY SUM(balance) DESC
    """
 
application = Report().wsgi()

