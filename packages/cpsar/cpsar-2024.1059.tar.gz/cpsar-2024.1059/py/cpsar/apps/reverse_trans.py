import datetime

import cpsar.runtime as R
from cpsar import txlib
import cpsar.util as U
import cpsar.ws as W

class Program(W.GProgram):
    ## Form Data
    @property
    def trans_id(self):
        try:
            return int(self.fs.getvalue('trans_id'))
        except (TypeError, ValueError):
            return None

    @property
    def reversal_date(self):
        try:
            return U.parse_american_date(self.fs.getvalue('reversal_date', ''))
        except U.ParseError:
            return datetime.date.today()

    ## Action Handlers
    def main(self):
        if not self.trans_id:
            self._res.write("No transaction")
            return 

        txlib.add_reversal(self.trans_id, self.reversal_date)
        if R.has_errors():
            for error in R.get_errors():
                self._res.write("<div>%s</div>" % error)
            return
        R.db.commit()
        R.flash("Reversal added")
        self._res.redirect("/view_trans?trans_id=%s", self.trans_id)

application =  Program.app
