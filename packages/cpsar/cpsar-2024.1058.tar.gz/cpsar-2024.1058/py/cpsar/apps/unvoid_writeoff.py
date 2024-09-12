""" Void out an writeoff """
from cpsar.runtime import db, flash
from cpsar.wsgirun import wsgi, HTTPNotFound
from cpsar import txlib

@wsgi
def application(req, res):
    writeoff_id = req.params.get('writeoff_id', '').strip()
    if not writeoff_id:
        return res.error("no writeoff_id given")
    txlib.unvoid_writeoff(writeoff_id)
    db.commit()
    flash("writeoff unvoided")
    res.redirect(req.referer)
