import kcontrol as K

import cpsar.sales
import cpsar.runtime as R
import cpsar.report

from cpsar.sales import ClientListBox, ReportCodeListBox

class Report(cpsar.report.WSGIReport):
    label = 'Brands With No Rebate'
    csv_file_name = 'unrebated.csv'

    def form_params(self):
        self.params = [
            ('Start Date Processed', K.DatePicker('start_date')), 
            ('End Date Processed',   K.DatePicker('end_date')),
            ('Group Number', ClientListBox('group_number')),
            ('Report Code', ReportCodeListBox('report_code')),
        ]

    def validate_form_input(self):
        if not self.req.params.get('start_date'):
            R.error("No start date selected")
        if not self.req.params.get('end_date'):
            R.error("No end date selected")

    def records(self):
        cursor = self.cursor = R.db.mako_cursor('ar/rpt_unrebated.sql')
        qargs = self.query_args()
        cursor.execute_template(**qargs)
        return cursor

application = Report().wsgi()

