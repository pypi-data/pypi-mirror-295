from cpsar.runtime import db, flash
from cpsar import txlib
import cpsar.ws as W

class Program(W.GProgram):
    def main(self):
        cursor = db.cursor()
        req = self._req
        res = self._res

        trans_id = int(req.params.get('trans_id'))
        cursor.execute("""
            SELECT ack_code 
                FROM state_report_entry
            WHERE trans_id=%s
            """, (trans_id,))

        assert cursor.rowcount == 1
        if cursor.fetchone()[0] == 'R':
            # If it's a reject resend using same entry_id
            txlib.resend_state_report_rejection(trans_id)
        else:
            # If not a reject cancel orig and resend with new entry id
            txlib.cancel_state_report_entries(trans_id)
            txlib.mark_for_state_reporting(trans_id)
        db.commit()

        #Ensure sr reporting isn't frozen
        cursor.execute("""
            SELECT freeze_sr_entry
                FROM trans
            WHERE trans_id=%s
            """, (trans_id,))

        assert cursor.rowcount == 1
        if not cursor.fetchone()[0]:
            flash('Transaction successful resending rejection')
        else:
            flash('Transaction not successful state reporting is frozen')
        res.redirect("/view_trans?trans_id=%s", trans_id)

application = Program.app
