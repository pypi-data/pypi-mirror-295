import datetime
import cpsar.wsgirun as W
from itertools import repeat

from cpsar.runtime import db, flash, username
from cpsar import txlib

application = app = W.MethodDispatch()

@app.get
@W.mako("settle_rebates.tmpl")
def show_form(req, tmpl):
    _set_form_passthru(req, tmpl)

@app.post
def form_submit_handler(req, res):
    if req.get('post'):
        return post_settlement(req, res)
    else:
        return review_rebates(req, res)

@W.mako("settle_rebates.tmpl")
def review_rebates(req, tmpl):
    _set_form_passthru(req, tmpl)
    group_number = req.get('group_number')
    quarter_date = req.get('quarter_date')
    if not group_number:
        return tmpl.error('no group number')
    if not quarter_date:
        return tmpl.error('no quarter_date')
    tmpl['rebates'] = available_rebates(group_number, quarter_date)
    tmpl['rebate_total'] = rebate_sum(tmpl['rebates'])

@W.json
def post_settlement(req, jres):
    check_number = req.get('check_number')
    if not check_number:
        return jres.error("no check number")
    settle_date = req.get('settle_date') or datetime.date.today()
    rebate_ids = req.params.getall("rebate_id")
    apply_amounts = req.params.getall("apply_amount")
    settlements = zip(
        rebate_ids,
        repeat(check_number),
        apply_amounts,
        repeat(settle_date),
        repeat(username()))

    if not settlements:
        return jres.error("no rebates matching selection")

    cursor = db.mako_dict_cursor("ar/settle_rebates.sql")
    cursor.apply_rebate_settlements(settlements)
    if cursor.rowcount:
        for rebate in cursor:
            args = (rebate['rebate_id'], rebate['error_msg'])
            jres.error("rebate %s: %s" % args)
    else:
        flash("Settlements created")
        db.commit()

def available_rebates(group_number, quarter_date):
    cursor = db.mako_dict_cursor("ar/settle_rebates.sql")
    cursor.available_rebates(group_number, quarter_date)
    return list(cursor)

def rebate_sum(rebates):
    return sum(r['client_balance'] for r in rebates)

def _set_form_passthru(req, tmpl):
    tmpl['group_number'] = req.get('group_number')
    tmpl['quarter_date'] = req.get('quarter_date')

