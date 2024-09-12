import cpsar.controls as C
import cpsar.runtime as R

from cpsar import report
from cpsar import sales

class Report(report.WSGIReport):
    label = 'Pending Distributions'

    def form_params(self):
        self.params = [
            ('Group Number', sales.ClientListBox('group_number')),
            ('Start Entry Date', C.DatePicker('start_date')), 
            ('End Entry Date',   C.DatePicker('end_date')),
            ('Account', sales.DistributionAccountListBox('account'))
        ]

    def validate_form_input(self):
        f = self.req.params.get
        if not f('group_number'):
            R.error("no group number given")
        if not f("account"):
            R.error("No account selected")
        if not f("start_date"):
            R.error("No start date selected")
        if not f("end_date"):
            R.error("No end date selected")

    sql = """
    SELECT trans.trans_id,
           distribution.distribution_id,
           distribution.entry_date,
           distribution.amount,
           distribution.distribution_date
    FROM distribution
    JOIN trans USING(trans_id)
    WHERE distribution.entry_date BETWEEN %(start_date)s AND %(end_date)s
      AND distribution.distribution_account = %(account)s
      AND trans.group_number = %(group_number)s
      ORDER BY distribution_id
    """

application = Report().wsgi()
