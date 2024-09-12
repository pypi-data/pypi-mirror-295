#!/usr/bin/env python
""" CPSAR WSGI Application Skeleton
"""
import cpsar.runtime as R

from cpsar import pg
from cpsar import txlib
from cpsar.wsgirun import mako
from cpsar.wsgirun import wsgi
from cpsar.wsgirun import PathDispatch

reg = PathDispatch()

@reg
@mako("void_settlement_check_form.tmpl")
def index(req, res):
   pass

@reg
@mako("void_settlement_check_review.tmpl")
def review(req, res):
    check_no = req.get("check_no")
    if not check_no:
        return res.error("No check no given")
    _get_settlement_records(check_no, res)

@reg
@mako("void_settlement_check_review.tmpl")
def commit(req, res):
    cursor = R.db.dict_cursor()
    check_no = req.get("check_no")
    if not check_no:
        return res.error("No check no given")

    cursor.execute("""
        SELECT puc_settle_id
        FROM overpayment_settlement
        WHERE check_no=%s AND void_date IS NULL
        """, (check_no,))
    for puc_settle_id, in cursor:
        txlib.void_overpayment_settlement(puc_settle_id)

    cursor.execute("""
        SELECT settlement_id
        FROM reversal_settlement
        WHERE check_no=%s AND void_date IS NULL
        """, (check_no,))
    for settlement_id, in cursor:
        txlib.void_reversal_settlement(settlement_id)

    _get_settlement_records(check_no, res)
    res['voided'] = True
    R.db.commit()

def _get_settlement_records(check_no, res):
    """ Get all of the settlement records for the check number and
    populate the mako response object. """
    cursor = R.db.dict_cursor()
    cursor.execute("""
        SELECT
            overpayment.trans_id,
            overpayment_settlement.puc_settle_id AS key,
            'PUC #' || overpayment.puc_id  AS ref,
            overpayment_settlement.amount,
            overpayment_settlement.entry_date,
            overpayment_settlement.void_date
        FROM overpayment_settlement
        JOIN overpayment USING(puc_id)
        WHERE check_no=%s
        UNION ALL
        SELECT 
            reversal.trans_id,
            reversal_settlement.settlement_id AS key,
            'REV #' || reversal.reversal_id AS ref,
            reversal_settlement.amount,
            reversal_settlement.entry_date,
            reversal_settlement.void_date
        FROM reversal_settlement
        JOIN reversal USING(reversal_id)
        WHERE check_no=%s
        ORDER BY entry_date
    """, (check_no, check_no))
    res['settlements'] = pg.all(cursor)
    res['total'] = sum(x['amount'] for x in res['settlements'])
    res['total_fmt'] = pg.format_currency(res['total'])
    res['check_no'] = check_no

application = reg.get_wsgi_app()
