""" Change the TX Type of the given transaction. First implemented for compounds
from CPS.
"""

from cpsar.wsgirun import json, wsgi
import cpsar.runtime as R
import cpsar.txlib as T

@wsgi
@json
def application(req, res):
    trans_id = req.get('trans_id')
    tx_type = req.get('tx_type')

    if not trans_id:
        res.error('No trans_id given')
    if not tx_type:
        res.error('No tx type given')

    if res.has_error():
        return

    T.change_tx_type(trans_id, tx_type)
    res['tx_type'] = tx_type
    R.db.commit()
