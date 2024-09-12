import cpsar.wsgirun as W

from cpsar.runtime import db, flash
from cpsar import txlib

application = app = W.MethodDispatch()

@app.get
@W.mako("settle_overpayment.tmpl")
def show_form(req, tmpl):
    puc_id = req.params.get('puc_id')
    if not puc_id:
        return tmpl.error("no puc_id given")
    cursor = db.dict_cursor()
    cursor.execute("SELECT * FROM overpayment WHERE puc_id=%s", (puc_id,))
    tmpl.update(cursor.fetchone())

@app.post
def form_submit_handler(req, res):
    puc_id = req.params.get('puc_id')
    check_no = req.params.get('check_no')
    if not puc_id:
        return res.error("no puc_id given")
    if not check_no:
        return res.error("no check number given")

    cursor = db.cursor()
    cursor.execute("""
        SELECT trans_id
        FROM overpayment
        WHERE puc_id=%s
        """, (puc_id,))
    trans_id, = cursor.fetchone()

    entry_date = req.params.get('entry_date')

    txlib.add_overpayment_settlement(puc_id, check_no, entry_date)
    db.commit()
    flash("Settled overpayment %s with check %s", puc_id, check_no)
    res.redirect("/view_trans?trans_id=%s", trans_id)
