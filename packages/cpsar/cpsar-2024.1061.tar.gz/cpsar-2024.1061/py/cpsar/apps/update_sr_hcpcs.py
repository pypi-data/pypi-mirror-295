import cpsar.runtime as R
from cpsar.wsgirun import wsgi
from cpsar.wsgirun import json

@wsgi
def application(req, res):
    ndc = req.get('ndc_number')
    if not ndc:
        R.flash("no ndc")
        res.redirect(req.referer)
        return
    hcpcs = req.get('sr_hcpcs_code') or None
    cur = R.db.cursor()
    cur.execute("""
        update drug set sr_hcpcs_code=%s
        where ndc_number=%s
        """, (hcpcs, ndc))
    R.db.commit()
    R.flash("HCPCS Code Updated Successfully")
    res.redirect(req.referer)

