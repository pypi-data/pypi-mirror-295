import cpsar.wsgirun as W

from cpsar.runtime import db, flash
from cpsar import txlib

@W.wsgi
def application(req, res):
    settlement_id = req.params.get('settlement_id')
    if not settlement_id:
        return res.error("no settlement_id given")
    txlib.void_reversal_settlement(settlement_id)
    db.commit()
    flash("Reversal settlement %s voided", settlement_id)
    res.redirect(req.referer)
