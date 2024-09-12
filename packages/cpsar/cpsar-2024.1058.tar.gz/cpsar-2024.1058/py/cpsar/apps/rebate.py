""" Main controller file for all rebate-related operations. Most of
these messages are sent from the view trans screen """
import datetime
import decimal
import time
import cpsar.runtime as R
import cpsar.rebate as RB

import cpsar.txlib as T
import cpsar.wsgirun as W

reg = W.PathDispatch()

@reg
def void_credit(req, res):
    try:
        credit_id = int(req.get('rebate_credit_id'))
    except TypeError:
        return res.not_found('Credit %s' % credit_id)
    credit = RB.credit_by_id(credit_id)
    if not credit:
        return res.not_found('Credit %s' % credit_id)

    try:
        credit.void(datetime.date.today())
    except RB.BusinessError as e:
        return res.error(e)

    R.flash("Rebate credit voided") 
    R.db.commit()
    res.redirect("/view_trans?trans_id=%s", credit.trans_id)

@reg
def unvoid_credit(req, res):
    try:
        credit_id = int(req.get('rebate_credit_id'))
    except TypeError:
        return res.not_found('Credit %s' % credit_id)
    credit = RB.credit_by_id(credit_id)
    if not credit:
        return res.not_found('Credit %s' % credit_id)

    try:
        credit.unvoid()
    except RB.BusinessError as e:
        return res.error(e)

    R.flash("Rebate credit unvoided") 
    R.db.commit()
    res.redirect("/view_trans?trans_id=%s", credit.trans_id)

@reg
def revoke_credit(req, res):
    try:
        credit_id = int(req.get('rebate_credit_id'))
    except TypeError:
        return res.not_found('Credit %s' % credit_id)
    credit = RB.credit_by_id(credit_id)
    if not credit:
        return res.not_found('Credit %s' % credit_id)

    try:
        credit.revoke()
    except RB.BusinessError as e:
        return res.error(e)

    R.flash("Rebate credit revoked") 
    R.db.commit()
    res.redirect("/view_trans?trans_id=%s", credit.trans_id)

@reg
def add_rebate_credit(req, res):
    rebate_id = req.get('rebate_id')
    rebate = RB.by_id(rebate_id)
    if not rebate:
        return res.not_found('Rebate not found: %s' % rebate_id)

    amount = req.get('amount')
    if not amount:
        return res.error('No amount given')
    try:
        amount = decimal.Decimal(amount)
    except decimal.InvalidOperation:
        return res.error("Invalid amount %s given" % amount)

    trans_id = req.get('trans_id')
    try:
        rebate.credit_trans(trans_id, amount, R.username())
    except RB.BusinessError as e:
        return res.error(e)

    R.flash("Rebate credit applied") 
    R.db.commit()
    res.redirect("/view_trans?trans_id=%s", trans_id)

application = reg.get_wsgi_app()
