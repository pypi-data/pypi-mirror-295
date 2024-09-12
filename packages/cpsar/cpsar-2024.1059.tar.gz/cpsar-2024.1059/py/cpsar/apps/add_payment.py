import datetime
import time

import cpsar.runtime as R
import cpsar.txlib
import cpsar.util as U
import cpsar.ws as W

class Program(W.GProgram):
    """ Add a payment to a transaction
    """

    ## Form Data
    @property
    def trans_id(self):
        try:
            return int(self.fs.getvalue('trans_id'))
        except (TypeError, ValueError):
            return None

    @property
    def ref_no(self):
        return self.fs.getvalue('ref_no')

    @property
    def ptype_id(self):
        return self.fs.getvalue('ptype_id')

    @property
    def amount(self):
        try:
            return U.parse_currency(self.fs.getvalue('amount', ''))
        except U.ParseError:
            return None

    @property
    def entry_date(self):
        try:
            return U.parse_american_date(self.fs.getvalue('entry_date', ''))
        except U.ParseError:
            return datetime.date.today()

    @property
    def note(self):
        return self.fs.getvalue("note") or None

    @property
    def balance(self):
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT balance FROM trans where trans_id=%s
            """, (self.trans_id,))
        return cursor.fetchone()[0]

    ## Action Handlers
    def main(self):
        if not self.trans_id or not self.amount:
            self._res.write("No transaction or amount given")
            return 

        # Automatically figure out how much to apply as a payment
        # and/or overpayment
        if self.amount > self.balance:
            payment_amount = self.balance
            overpayment_amount = self.amount - self.balance

            if payment_amount > 0:
                self._add_payment(payment_amount)

            self._add_overpayment(overpayment_amount)
        else:
            self._add_payment(self.amount)

        if R.has_errors():
            for error in R.get_errors():
                self._res.write("<div>%s</div>" % error)
            return
        R.db.commit()
        self._res.redirect("/view_trans?trans_id=%s", self.trans_id)

    def _add_payment(self, amount):
        cpsar.txlib.add_payment(
            self.trans_id,
            self.ptype_id,
            self.ref_no,
            amount,
            self.entry_date,
            self.note)

    def _add_overpayment(self, amount):
        cpsar.txlib.add_overpayment(
            self.trans_id,
            self.ptype_id,
            self.ref_no,
            amount,
            self.entry_date,
            self.note)

application =  Program.app
