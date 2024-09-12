""" Fix the savings for all transactions for a group. Useful after the
savings formula has changed.
"""
import cpsar.runtime as R
import cpsar.txlib as T

from cpsar.wsgirun import wsgi

@wsgi
def application(req, res):
    gn = req.params.get('group_number')
    if not gn:
        res.body = 'Invalid Param'
        return

    cursor = R.db.cursor()
    cursor.execute("""
        SELECT trans_id
        FROM trans
        WHERE group_number = %s
        """, (gn,))

    txs = [c for c, in cursor]
    list(map(T.check_savings, txs))
    R.db.commit()
    res.body = 'Updated %s records.' % len(txs)

