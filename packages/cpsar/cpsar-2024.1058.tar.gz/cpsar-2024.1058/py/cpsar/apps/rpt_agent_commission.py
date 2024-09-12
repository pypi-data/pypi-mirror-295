import csv

import kcontrol

import cpsar.report
import cpsar.runtime as R
import cpsar.sales

class Report(cpsar.report.WSGIReport):
    label = 'Agent Commission'

    sql_tmpl_file = 'rpt_agent_commission.tmpl'
    csv_file_name = 'agent_commission.csv'

    def form_params(self):
        self.params = [
            ('Start Date', kcontrol.DatePicker('start_date', required=True)),
            ('End Date',   kcontrol.DatePicker('end_date', required=True)),
            ('Account', cpsar.sales.DistributionAccountListBox('account'))
        ]

    def validate_form_input(self):
        if not self.req.params.get('account'):
            R.error("No account selected")
        if not self.req.params.get('start_date'):
            R.error("No start date selected")
        if not self.req.params.get('end_date'):
            R.error("No end date selected")

    def records(self):
        cursor = R.db.cursor()

        g = self.req.get
        args = {
            'start_date': g('start_date'),
            'end_date': g('end_date'),
            'account': g('account')
        }
        cursor.execute_file('ar/rpt_agent_commission.sql', args)
        cursor.execute("SELECT * FROM report ORDER BY group_number")
        for r in cursor: yield r
        cursor.execute("SELECT * FROM total")
        yield cursor.fetchone()
        cursor.execute("DROP TABLE report, total, sdistribution")

    def csv(self):
        self.res.content_type = 'text/csv'

        h = self.res.headers
        h.add("Expires", "0")
        h.add("Content-Transfer-Encoding", "binary")
        h.add("Pragma", "public")
        h.add("Content-Disposition", "attachment; filename=%s" %
                                     self.csv_file_name)
        cursor = self.records()
        writer = csv.writer(self.res)
        preamble = self.preamble()
        if preamble is not None:
            writer.writerow(preamble)
        writer.writerow([
            '', '', 'Mail Order Brand', '', 'Mail Order Generic', '',
            'Retail Brand', '', 'Retail Generic', '', 'Other', ''])
        writer.writerow(['number', 'group']
          + ['count', 'amount'] * 5
          + ['count_total', 'subtotal', 'reversals_and_writeoffs', 'total'])

        for rec in cursor:
            writer.writerow(rec)

application = Report().wsgi()
