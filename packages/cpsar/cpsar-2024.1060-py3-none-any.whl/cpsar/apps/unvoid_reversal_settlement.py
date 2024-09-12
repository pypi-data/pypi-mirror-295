from cpsar import txlib
from cpsar.runtime import db, flash
from cpsar.wsgirun import wsgi

@wsgi
def application(req, res):
    settlement_id = req.params.get('settlement_id')
    if not settlement_id:
        return res.error("no settlement_id given")
    txlib.unvoid_reversal_settlement(settlement_id)
    db.commit()
    flash("Reversal settlement %s unvoided", settlement_id)
    res.redirect(req.referer)
