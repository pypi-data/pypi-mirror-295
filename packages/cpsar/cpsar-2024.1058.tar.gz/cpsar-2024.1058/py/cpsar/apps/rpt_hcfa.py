import csv


from cpsar import controls
from cpsar import pg
from cpsar import report
from cpsar import sales
import cpsar.runtime as R

class Report(report.WSGIReport):
    label = 'HCFA Export'

    csv_file_name = 'hcfa_export.csv'

    def form_params(self):
        self.params = [
            ('Group Number', sales.ClientListBox('group_number')),
            ('Report Code', controls.TextBox('report_code')),
            ('Start Batch Date', controls.DatePicker('start_date')),
            ('End Batch Date',   controls.DatePicker('end_date')),
            ('First Name', controls.TextBox('first_name')),
            ('Last Name', controls.TextBox('last_name')),
            ('Include Transactions with Zero Balance', controls.CheckBox('zero_balance_trans'))
        ]

    def validate_form_input(self):
        g = self.req.get
        if not g('group_number') and not g('report_code'):
            R.error("Group number or report code required")
        if not self.req.params.get('start_date'):
            R.error("No start date selected")
        if not self.req.params.get('end_date'):
            R.error("No end date selected")

    def query_args(self):
        args = super(Report, self).query_args()
        gv = self.fs.getvalue
        if gv('first_name'):
            args['first_name'] = pg.qstr("%s%%" % gv('first_name'))
        else:
            args['first_name'] = None
        if gv('last_name'):
            args['last_name'] = pg.qstr("%s%%" % gv('last_name'))
        else:
            args['last_name'] = None
        return args

    def records(self):
        if R.has_errors():
            return []
        cursor = R.db.mako_cursor('ar/rpt_hcfa.sql')
        args = super(Report, self).query_args()
        cursor.execute_template(**args)
        self.cursor = cursor
        return cursor

    def csv(self):
        self.res.content_type = 'application/csv'

        h = self.res.headers
        h.add("Expires", "0")
        h.add("Content-Transfer-Encoding", "binary")
        h.add("Pragma", "public")
        h.add("Content-Disposition", "attachment; filename=%s" %
                                     self.csv_file_name)
        cursor = self.records()
        writer = csv.writer(self.res)
        writer.writerow([c[0] for c in cursor.description[1:]])
        last_invoice_id = None
        for rec in cursor:
            if rec[0] != last_invoice_id:
                last_invoice_id = rec[0]
                writer.writerow(rec[1:])
            else:
                writer.writerow(['']*69 + list(rec[70:]))

application = Report().wsgi()
