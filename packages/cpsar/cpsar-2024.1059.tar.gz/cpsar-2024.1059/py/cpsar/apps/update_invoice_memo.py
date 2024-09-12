#!/usr/bin/env python
import decimal

from cpsar.runtime import db, flash
from cpsar.txlib import BusinessError, check, Transaction, update_cost_allowed
from cpsar.ws import GProgram

class Program(GProgram):
    def main(self):
        invoice_id = int(self.fs.getvalue('invoice_id', 0))
        if not invoice_id:
            return
        memo = self.fs.getvalue('memo')
        cursor = db.cursor()
        cursor.execute("UPDATE invoice SET memo=%s WHERE invoice_id=%s",
            (memo, invoice_id))
        db.commit()

application = Program.app
