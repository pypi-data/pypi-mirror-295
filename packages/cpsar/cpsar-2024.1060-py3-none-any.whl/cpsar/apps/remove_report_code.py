import cpsar.runtime as R
import cpsar.ws as W

class Program(W.GProgram):
    @property
    def group_number(self):
        return self.fs.getvalue('group_number')

    @property
    def report_code(self):
        return self.fs.getvalue('rc')

    def main(self):
        self._delete_report_code()
        R.log.info('Removed Report Code %s from %s',
                   self.report_code, self.group_number)
        R.flash('Removed Report Code %s' % self.report_code)
        self._res.redirect("/view_client?group_number=%s", self.group_number)

    def _delete_report_code(self):
        cursor = R.db.cursor()
        cursor.execute("""
            DELETE FROM client_report_code 
            WHERE group_number=%s AND report_code=%s
            """, (self.group_number, self.report_code))
        R.db.commit()

application = Program.app
