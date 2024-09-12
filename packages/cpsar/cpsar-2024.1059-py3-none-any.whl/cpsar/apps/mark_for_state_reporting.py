from cpsar.runtime import db, flash
from cpsar import txlib
import cpsar.ws as W

class Program(W.GProgram):
    def main(self):
        req = self._req
        res = self._res

        trans_id = int(req.params.get('trans_id'))
        txlib.mark_for_state_reporting(trans_id)
        db.commit()

        flash('Transaction successful marked for state reporting')
        res.redirect("/view_trans?trans_id=%s", trans_id)

application = Program.app
