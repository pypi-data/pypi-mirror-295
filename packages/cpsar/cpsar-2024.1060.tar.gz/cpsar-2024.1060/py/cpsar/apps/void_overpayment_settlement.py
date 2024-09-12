""" Void out an overpayment settlement. """
from cpsar.runtime import db, flash
from cpsar.wsgirun import wsgi, HTTPNotFound
from cpsar import txlib

@wsgi
def application(req, res):
    puc_settle_id = req.params.get('puc_settle_id').strip()
    if not puc_settle_id:
        return res.error("no puc_settle_id given")
    txlib.void_overpayment_settlement(puc_settle_id)
    db.commit()
    flash("Overpayment settlement voided")
    res.redirect(req.referer)
