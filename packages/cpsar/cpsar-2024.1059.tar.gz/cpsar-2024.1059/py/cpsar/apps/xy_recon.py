import datetime

import cpsar.runtime as R
from cpsar import util
from cpsar import ws

class Program(ws.PIMixIn, ws.MakoProgram):
    @property
    def send_date_start(self):
        d = util.parse_date(self.fs.getvalue('send_date_start'))
        if not d:
            return datetime.date.today() - datetime.timedelta(days=1)
        return d

    @property
    def send_date_end(self):
        d = util.parse_date(self.fs.getvalue('send_date_end'))
        if not d:
            return datetime.date.today()
        return d

    @ws.publish
    def index(self):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            select state_report_entry.*, bishop_bsr.*,
                load_file.name as incoming_file_name,
                state_report_file.file_name as outgoing_file_name
            from state_report_entry
            join state_report_bill using(bill_id)
            join state_report_file on state_report_bill.sr_file_id = state_report_file.sr_file_id
            left join bishop_bsr on state_report_entry.bill_id = bishop_bsr.bill_id
            left join load_file on bishop_bsr.file_id = load_file.file_id
            where state_report_file.send_time between %s and %s
        """, (self.send_date_start, self.send_date_end))

        self.tmpl['entries'] = list(cursor)

    @ws.publish
    def mark(self):
        srid = self.fs.getvalue('srid')
        cursor = R.db.cursor()
        cursor.execute("""
            update state_report_entry set reconciled=not reconciled
            where srid=%s
            """, (srid,))
        R.db.commit()
        self.mako_auto_publish = False
        self._res.write_json({
            'errors': []
        })

application = Program.app
