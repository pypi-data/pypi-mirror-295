""" Void out an adjudication """
from cpsar.runtime import db, flash
from cpsar.wsgirun import wsgi, HTTPNotFound
from cpsar import txlib

@wsgi
def application(req, res):
    adjudication_id = req.params.get('adjudication_id', '').strip()
    if not adjudication_id:
        return res.error("no adjudication_id given")
    txlib.unvoid_adjudication(adjudication_id)
    db.commit()
    flash("Adjudication unvoided")
    res.redirect(req.referer)
