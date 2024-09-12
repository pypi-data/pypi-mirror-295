import datetime
import decimal

import cpsar.runtime as R
import cpsar.util as U
import cpsar.ws as W

from cpsar import txlib

class Program(W.GProgram):
    """ Add an adjudication Woff an amount from a transaction
    """
    def main(self):
        fs = self.fs
        trans_id = fs.getvalue('trans_id')

        try:
            amount = U.parse_currency(fs.getvalue('amount', ''))
        except U.ParseError:
            self._res.error("Invalid amount given")
            return

        if amount <= 0:
            return self._res.error("please enter a positive amount")
        note = fs.getvalue('note')
        reversal_id = fs.getvalue('reversal_id')

        if not trans_id or not reversal_id:
            return self._res.error("No transaction or reversal id given")

        try:
            entry_date = U.parse_american_date(fs.getvalue('entry_date', ''))
        except U.ParseError:
            entry_date = datetime.datetime.now()

        try:
            txlib.add_adjudication(trans_id, reversal_id, amount, entry_date, note)
            R.db.commit()
            R.flash("Adjudication added")
        except txlib.BusinessError as e:
            R.flash(e)

        self._res.redirect(self._req.referer)

application = Program.app




