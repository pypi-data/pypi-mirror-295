from cpsar import txlib
from cpsar.runtime import db, flash
from cpsar.wsgirun import wsgi

@wsgi
def application(req, res):
    puc_id = int(req.params.get('puc_id'))
    cursor = db.cursor()

    cursor.execute("""
        SELECT trans_id
        FROM overpayment
        WHERE puc_id=%s
        """, (puc_id,))
    if not cursor.rowcount:
        res.error("ID %s not found" % pic_id)
        return

    trans_id, = cursor.fetchone()
    txlib.revoke_overpayment(puc_id)
    db.commit()
    res.redirect("/view_trans?trans_id=%s&m=ud", trans_id)
