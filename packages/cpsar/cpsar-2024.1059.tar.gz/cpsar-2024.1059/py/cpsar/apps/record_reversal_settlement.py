import cpsar.ajson as json
import cpsar.runtime as R
import cpsar.txlib as txlib
import cpsar.ws as W

class Program(W.GProgram):
    def main(self):
        
        fs = self.fs
        self._res.content_type = 'application/json'

        errors = []

        check_no = fs.getvalue("check_no")
        prs_id = fs.getvalue("prs_id")
        if not check_no:
            errors.append("no check no")
        if not prs_id:
            errors.append("no prs_id")

        entry_date = fs.getvalue('entry_date')
        if not entry_date:
            raise ValueError('boom')
            entry_date = None

        if not errors:
            self.settle_pending_reversal(prs_id, check_no, entry_date)
            R.db.commit()
        self._res.write(json.write({'errors': errors}))

    def settle_pending_reversal(self, prs_id, cno, entry_date):
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT trans.trans_id,
                   pending_reversal_settlement.amount,
                   reversal.reversal_id
            FROM pending_reversal_settlement
            JOIN reversal USING(reversal_id)
            JOIN trans USING(trans_id)
            WHERE pending_reversal_settlement.prs_id = %s
            """,
            (prs_id,))
        if not cursor.rowcount:
            return
        trans_id, amount, reversal_id = cursor.fetchone()
        txlib.add_reversal_settlement(reversal_id, cno, amount, trans_id,
                                      entry_date)
        cursor.execute("""
            DELETE FROM pending_reversal_settlement
            WHERE prs_id=%s
            """, (prs_id,))

application  = Program.app
