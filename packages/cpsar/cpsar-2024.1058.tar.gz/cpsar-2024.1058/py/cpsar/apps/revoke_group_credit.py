import cpsar.runtime as R
import cpsar.ws as W
from cpsar import txlib

class Program(W.GProgram):
    def main(self):
        gcid = self.fs.getvalue('gcid')
        cursor = R.db.real_dict_cursor()
        cursor.execute("select source_reversal_id, amount from group_credit where gcid=%s", (gcid,))
        if not cursor.rowcount:
            return self._redirect()
        gcr = next(cursor)

        cursor.execute("""
            delete from group_credit
            where gcid=%s
            """, (gcid,))

        if gcr['source_reversal_id']:
            cursor.execute("""
                update reversal set balance = balance + %s
                where reversal_id=%s
                """, (gcr['amount'], gcr['source_reversal_id']))

        cursor.execute("""
            REFRESH MATERIALIZED VIEW group_ledger;
            REFRESH MATERIALIZED VIEW group_ledger_balance;
        """)

        cursor.execute("""
            select trans_id from reversal where reversal_id=%s
            """, (gcr['source_reversal_id'],))

        trans_id = next(cursor)['trans_id']

        txlib.check_transfered_amount(trans_id)
        txlib.check_balance(trans_id)
        txlib.check_distributed_amount(trans_id)
        R.db.commit()
        self._redirect()

    def _redirect(self):
        r = self.fs.getvalue('r') or '/'
        self._res.redirect(r)

application = Program.app
