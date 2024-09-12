import kcontrol as K

import cpsar.sales
import cpsar.runtime as R
import cpsar.report

from cpsar.sales import ClientListBox, ReportCodeListBox

class Report(cpsar.report.WSGIReport):
    label = 'Rebates'
    csv_file_name = 'rebates.csv'

    def form_params(self):
        self.params = [
            ('Start Rebate Date', K.DatePicker('start_date')), 
            ('End Rebate Date',   K.DatePicker('end_date')),
            ('Group Number', ClientListBox('group_number')),
            ('Report Code', ReportCodeListBox('report_code')),
            ('Only Show Rebates With Client Amount?', K.CheckBox('has_client_amount')),
            ('Only Show Rebates With Client Balance?', K.CheckBox('has_client_balance'))
        ]

    def validate_form_input(self):
        if not self.req.params.get('start_date'):
            R.error("No start date selected")
        if not self.req.params.get('end_date'):
            R.error("No end date selected")

    def records(self):
        cursor = self.cursor = R.db.mako_cursor('ar/rpt_rebates.sql')
        qargs = self.query_args()
        cursor.execute_template(**qargs)
        return cursor

application = Report().wsgi()

