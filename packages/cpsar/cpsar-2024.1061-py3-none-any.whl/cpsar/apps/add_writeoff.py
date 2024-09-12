import datetime

import cpsar.runtime as R
import cpsar.txlib
import cpsar.ws as W
import cpsar.util as U

class Program(W.GProgram):
    """ Write off an amount from a transaction """
    def main(self):
        fs = self.fs
        trans_id = fs.getvalue('trans_id')
        if not trans_id:
            self._res.redirect("/")
        try:
            amount = U.parse_currency(fs.getvalue('amount', ''))
        except U.ParseError:
            R.flash("Invalid amount %s" % fs.getvalue('amount', ''))
            self._res.redirect("/view_trans?trans_id=%s", trans_id)
            return

        note = fs.getvalue('note')
        try:
            entry_date = U.parse_american_date(self.fs.getvalue("entry_date"))
        except U.ParseError:
            entry_date = datetime.datetime.now()
        try:
            cpsar.txlib.add_writeoff(trans_id, amount, entry_date, note)
            R.db.commit()
            R.flash("Writeoff Added")
        except cpsar.txlib.BusinessError as e:
            R.flash(e)
        self._res.redirect("/view_trans?trans_id=%s", trans_id)

application = Program.app
