from cpsar.runtime import db, flash
from cpsar.wsgirun import wsgi, HTTPNotFound
from cpsar import txlib

@wsgi
def application(req, res):
    puc_settle_id = req.params.get('puc_settle_id').strip()
    if not puc_settle_id:
        raise HTTPNotFound()

    # Get the trans_id so we can redirect back to the
    # trans screen
    cursor = db.cursor()
    cursor.execute("""
        SELECT trans_id
        FROM overpayment
        WHERE puc_id=(
            SELECT puc_id
            FROM overpayment_settlement
            WHERE puc_settle_id=%s)
        """, (puc_settle_id,))

    if cursor.rowcount != 1:
        raise HTTPNotFound(puc_settle_id)

    trans_id, = cursor.fetchone()
    txlib.revoke_overpayment_settlement(puc_settle_id)
    db.commit()
    flash("Overpayment settlement revoked")
    res.redirect("/view_trans?trans_id=%s", trans_id)
