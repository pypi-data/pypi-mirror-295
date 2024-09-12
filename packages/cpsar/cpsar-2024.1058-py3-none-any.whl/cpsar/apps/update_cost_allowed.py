#!/usr/bin/env python
import decimal

from cpsar.runtime import db, flash
from cpsar.txlib import BusinessError, check, Transaction, update_cost_allowed
from cpsar.ws import GProgram

class Program(GProgram):
    def main(self):
        fs = self.fs
        cursor = db.cursor()

        trans_id = fs.getvalue('trans_id')
        t = Transaction(trans_id)
        if not t.record:
            return self._res.redirect("/")

        try:
            cost_allowed = decimal.Decimal(fs.getvalue('cost_allowed'))
        except (decimal.InvalidOperation, TypeError):
            flash("Invalid cost allowed given")
            return self._res.redirect("/view_trans?trans_id=%s", trans_id)

        try:
            update_cost_allowed(t, cost_allowed)
        except BusinessError as e:
            flash(e)
            return self._res.redirect("/view_trans?trans_id=%s", trans_id)

        check(trans_id)
        db.commit()
        flash("Cost allowed updated successfully")
        self._res.redirect("/view_trans?trans_id=%s", trans_id)

application = Program.app
