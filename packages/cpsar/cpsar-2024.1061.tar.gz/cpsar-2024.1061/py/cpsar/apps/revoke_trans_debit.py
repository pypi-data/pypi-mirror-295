import decimal

import cpsar.txlib
import cpsar.runtime as R
import cpsar.util as U
import cpsar.ws as W

class Program(W.GProgram):
    """ Revoke a debit to a transaction """
    def main(self):
        debit_id = self.fs.getvalue("debit_id")
        if not debit_id:
            self._res.error("no debit_id given")
            return

        cursor = R.db.cursor()
        cursor.execute("SELECT trans_id FROM trans_debit WHERE debit_id=%s",
            (debit_id,))
        if not cursor.rowcount:
            self._res.error("debit %s not found" % debit_id)
            return

        trans_id, = cursor.fetchone()
        cpsar.txlib.revoke_debit(debit_id)
        R.db.commit()
        R.flash("Debit revoked")
        self._res.redirect("/view_trans?trans_id=%s",  trans_id)

application = Program.app




