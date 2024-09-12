from decimal import Decimal
import datetime

import cpsar.runtime as R
import cpsar.ws as W
from cpsar import txlib
from cpsar import util

class Program(W.GProgram):
    def main(self):
        reversal_id = self.fs.getvalue('reversal_id')
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT trans.group_number, reversal.*
            FROM reversal
            JOIN trans USING(trans_id)
            WHERE reversal_id=%s
            """, (reversal_id, ))
        reversal = cursor.fetchone()
        assert reversal
        trans_id = reversal['trans_id']
        credit_amount = reversal['balance']

        if not reversal['balance']:
            R.error("Reversal does not have a balance")
            self._res.redirect("/view_trans?trans_id=%s", reversal['trans_id'])
            return

        cursor.execute("""
            INSERT INTO group_credit (
                source_reversal_id, amount, entry_date, username, group_number
            ) VALUES (%s, %s, NOW(), %s, %s)
            """, (reversal_id, credit_amount, R.session['username'], reversal['group_number']))

        cursor.execute("""
            UPDATE reversal SET balance=0 WHERE reversal_id=%s
            """, (reversal_id,))

        cursor.execute("""
            REFRESH MATERIALIZED VIEW group_ledger;
            REFRESH MATERIALIZED VIEW group_ledger_balance;
        """)

        # Create negative distributions to match
        distributions = R.db.dict_cursor()
        distributions.execute("""
            SELECT distribution_account, amount
            FROM distribution
            WHERE trans_id=%s AND amount > 0 AND distribution_date IS NOT NULL
            """, (trans_id,))
        distributions = list(distributions)
        distributed_total = sum(d['amount'] for d in distributions)

        if credit_amount == distributed_total:
            for distribution in distributions:
                amount = -distribution['amount']
                account = distribution['distribution_account']
                ndist = R.db.cursor()
                ndist.execute(util.insert_sql('distribution', {
                    'trans_id': trans_id,
                    'distribution_account': account,
                    'amount': amount
#                    'distribution_date': datetime.datetime.now()
                }))

                amount = "%.02f" % Decimal(amount)
                txlib.log(trans_id, "Added distribution of %s to %s" % (amount, account))
        else:
            R.error('Credit amount %s != distributed total %s', credit_amount, distributed_total)

        txlib.check_transfered_amount(trans_id)
        txlib.check_balance(trans_id)
        txlib.check_distributed_amount(trans_id)
        R.db.commit()
        self._res.redirect("/view_trans?trans_id=%s&m=cr", trans_id)

application = Program.app
