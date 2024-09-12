import psycopg2
import cpsar.runtime as R
import cpsar.ws as W

from cpsar.util import insert_sql

class Program(W.GProgram):
    @property
    def group_number(self):
        return self.fs.getvalue('group_number')

    @property
    def report_code(self):
        return self.fs.getvalue('rc')

    @property
    def internal(self):
        return bool(self.fs.getvalue('internal'))

    def main(self):
        try:
            self._add_report_code()
        except psycopg2.IntegrityError as e:
            R.error("Could not add report code: %s", e)

        if R.has_errors():
            for e in R.get_errors():
                self._res.write("<div>%s</div>" % e)
            return

        R.log.info('Added Report Code %s to %s',
                   self.report_code, self.group_number)
        R.flash('Added Report Code %s', self.report_code)
        self._res.redirect("/view_client?group_number=%s", self.group_number)

    def _add_report_code(self):
        cursor = R.db.cursor()
        cursor.execute(insert_sql("client_report_code", {
            "group_number": self.group_number,
            "report_code": self.report_code,
            "internal": self.internal
        }))
        R.db.commit()

application = Program.app
