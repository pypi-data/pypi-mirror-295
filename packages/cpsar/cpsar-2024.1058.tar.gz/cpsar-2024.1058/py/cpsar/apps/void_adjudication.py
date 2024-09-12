""" Void out an adjudication """
from cpsar.runtime import db, flash
from cpsar.wsgirun import wsgi, HTTPNotFound
from cpsar import txlib
from cpsar.util import parse_american_date, ParseError

@wsgi
def application(req, res):
    adjudication_id = req.params.get('adjudication_id', '').strip()
    if not adjudication_id:
        return res.error("no adjudication_id given")
    entry_date = req.params.get("void_adj_date", "").strip()
    try:
        entry_date = parse_american_date(entry_date)
    except ParseError:
        return res.error("Invalid entry date %s" % entry_date)
    try:
        txlib.void_adjudication(adjudication_id, entry_date)
    except txlib.BusinessError as e:
        flash(e)
        res.redirect(req.referer)
        return

    db.commit()
    flash("Adjudication voided")
    res.redirect(req.referer)
