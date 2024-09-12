import decimal

import cpsar.txlib
import cpsar.runtime as R
import cpsar.util as U
import cpsar.ws as W

class Program(W.GProgram):
    """ Add a debit to a transaction """
    def main(self):
        trans_id = self.fs.getvalue('trans_id')
        if not trans_id:
            self._res.error("No trans_id given")
            return

        try:
            amount = U.parse_currency(self.fs.getvalue('amount', ''))
        except U.ParseError:
            self._res.error("Invalid amount given")
            return

        if amount <= 0:
            self._res.error("please enter a positive amount")
            return

        note = self.fs.getvalue('note')
        try:
            entry_date = U.parse_american_date(self.fs.getvalue("entry_date"))
        except ParseError:
            self._res.error("Invalid entry date %s" %
                            self.fs.getvalue("entry_date"))
            return

        cpsar.txlib.add_debit(trans_id, amount, entry_date, note)
        R.db.commit()
        R.flash("Debit added")
        self._res.redirect("/view_trans?trans_id=%s",  trans_id)

application = Program.app




