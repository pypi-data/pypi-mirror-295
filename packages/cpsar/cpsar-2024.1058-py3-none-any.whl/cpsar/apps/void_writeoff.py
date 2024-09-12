""" Void out a writeoff """
from cpsar.runtime import db, flash
from cpsar.wsgirun import wsgi, HTTPNotFound
from cpsar import txlib
from cpsar.util import parse_american_date, ParseError

@wsgi
def application(req, res):
    writeoff_id = req.params.get('writeoff_id', '').strip()
    if not writeoff_id:
        return res.error("no writeoff_id given")
    void_date = req.params.get("void_date", "").strip()
    try:
        void_date = parse_american_date(void_date)
    except ParseError:
        return res.error("Invalid void date %s" % void_date)
    txlib.void_writeoff(writeoff_id, void_date)
    db.commit()
    flash("writeoff voided")
    res.redirect(req.referer)
