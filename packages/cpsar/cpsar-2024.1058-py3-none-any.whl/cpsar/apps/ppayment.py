from __future__ import division
from past.utils import old_div
import re
import itertools
import decimal
import sys

import cpsar.runtime as R
import cpsar.wsgirun as W

from cpsar import pg
from cpsar import txlib
from cpsar import util
from cpsar.wsgirun import json, mako

reg = W.PathDispatch()

@reg
@mako('ppayment.tmpl')
def index(req, res):
    res['payment_types'] = _all_payment_types()

def _all_payment_types():
    cursor = R.db.dict_cursor()
    # The COALESCE in the ORDER BY makes those with no group numbers appear
    # at the top
    cursor.execute("""
        SELECT
         group_number, 
         ptype_id, 
         type_name,
         default_ref_no,
         type_name
            || COALESCE(' *' || substring(default_ref_no from length(default_ref_no)-3), '')
            AS caption
        FROM payment_type
        WHERE expiration_date IS NULL OR expiration_date < NOW()
        ORDER BY COALESCE(group_number, '--'), ptype_id ASC
        """)
    return itertools.groupby(cursor, lambda x: x['group_number'])

@reg
@json
def trans_search(req, res):
    def eq(key, field, values):
        return ["%s = %%s" % field], [values[key]]

    def inteq(key, field, values):
        try:
            v = int(values[key])
        except ValueError:
            return [], []
        return ["%s = %%s" % field], [v]

    def ilike(key, field, values):
        return ["%s ILIKE %%s" % field], [values[key]]

    def client_report_code(key, field, values):
        return ["""client.group_number in (select group_number
                        from client_report_code where report_code=%s)
                    or client.report_code = %s"""], [values[key], values[key]]

    cursor = R.db.dict_cursor()
    cond_fields = [
        ('group_number', 'trans.group_number', eq),
        ('group_auth', 'trans.group_auth', inteq),
        ('patient_last_name', 'patient.last_name', ilike),
        ('patient_first_name', 'patient.first_name', ilike),
        ('invoice_id', 'trans.invoice_id', inteq),
        ('rx_number', 'history.rx_number', inteq),
        ('report_code', 'client.report_code', client_report_code),
        ('payer_code', 'history.payer_code', eq),
        ('invoice_line_no', 'trans.line_no', inteq),
        ('batch_date', 'trans.batch_date', eq),
        ('invoice_date', 'invoice.create_date', eq),
        ('hbs_order_number', 'history.hbs_order_number', inteq)
        ]

    cond_sql = ["trans.balance > 0"]
    cond_values = []

    for skey, field, proc in cond_fields:
        if req.params.get(skey):
            sql, vals = proc(skey, field, req.params)
            cond_sql.extend(sql)
            cond_values.extend(vals)

    if not cond_values:
        res['transactions'] = []
        return
    
    cond_values = tuple(cond_values)
    sql = """
        SELECT trans.batch_date,
               trans.rx_date,
               trans.group_number,
               trans.group_auth,
               trans.invoice_id,
               trans.line_no,
               trans.trans_id,
               trans.rx_number,
               history.payer_code,
               (trans.balance * 100)::int AS balance,
               patient.patient_id,
               patient.first_name as patient_first_name,
               patient.last_name as patient_last_name,
               drug.name as drug_name
        FROM trans
        LEFT JOIN invoice USING(invoice_id)
        JOIN patient ON
             trans.patient_id = patient.patient_id
        JOIN history ON
             trans.history_id = history.history_id
        JOIN client ON history.group_number = client.group_number
        LEFT JOIN drug ON
             trans.drug_id = drug.drug_id
        WHERE %s
        ORDER BY trans.invoice_id, trans.line_no
        """ % (" AND ".join(cond_sql))
    cursor.execute(sql, cond_values)

    res['sql'] = sql
    res['transactions'] = [dict(c) for c in cursor]

@reg
@json
def unapplied_cash_search(req, res):
    def eq(key, field, values):
        return ["%s = %s" % (field, pg.qstr(values[key]))]
    
    def inteq(key, field, values):
        try:
            v = int(values[key])
        except ValueError:
            return []
        return ["%s = %s" % (field, v)]

    def ilike(key, field, values):
        return ["%s ILIKE %s" % (field, pg.qstr(values[key]))]

    def client_report_code(key, field, values):
        v = pg.qstr(values[key])
        return ["""client.group_number in (select group_number
                        from client_report_code where report_code=%s)
                    or client.report_code = %s""" % (v, v)]

    cursor = R.db.dict_cursor()
    cond_fields = [
        ('group_number', 'trans.group_number', eq),
        ('group_auth', 'trans.group_auth', inteq),
        ('patient_last_name', 'patient.last_name', ilike),
        ('patient_first_name', 'patient.first_name', ilike),
        ('invoice_id', 'trans.invoice_id', inteq),
        ('rx_number', 'trans.rx_number', inteq),
        ('report_code', 'client.report_code', client_report_code),
        ('payer_code', 'history.payer_code', eq),
        ('invoice_line_no', 'trans.line_no', inteq),
        ('batch_date', 'trans.batch_date', eq),
        ('invoice_date', 'invoice.create_date', eq),
        ('hbs_order_number', 'history.hbs_order_number', inteq)
        ]
    cond_sql = []

    for skey, field, proc in cond_fields:
        if req.params.get(skey):
            sql = proc(skey, field, req.params)
            cond_sql.extend(sql)

    if not cond_sql:
        res['records'] = []
        return

    cond = (" AND ".join(cond_sql))

    sql = """
        WITH selected_patient AS (
            SELECT trans.patient_id, trans.group_number
            FROM trans
            JOIN patient USING(patient_id)
            JOIN history USING(history_id)
            JOIN invoice ON trans.invoice_id = invoice.invoice_id
            join client on history.group_number = client.group_number
            WHERE %s
        )
        SELECT
               (overpayment.balance*100)::int AS balance,
               overpayment.ptype_id,
               overpayment.ref_no,
               overpayment.puc_id,
               payment_type.type_name,
               NULL AS reversal_id,
               patient.first_name,
               patient.last_name,
               patient.group_number
        FROM overpayment
        JOIN trans USING(trans_id)
        JOIN selected_patient USING(patient_id)
        JOIN patient USING(patient_id)
        JOIN history USING(history_id)
        LEFT JOIN payment_type USING(ptype_id)
        WHERE overpayment.balance != 0

        UNION
        SELECT
               (reversal.balance*100)::int AS balance,
               NULL AS ptype_id,
               'TX:' || reversal.trans_id AS ref_no,
               NULL AS puc_id,
               'REV' AS type_name,
               reversal.reversal_id AS reversal_id,
               patient.first_name,
               patient.last_name,
               patient.group_number

        FROM reversal
        JOIN trans USING(trans_id)
        JOIN selected_patient USING(patient_id)
        JOIN patient USING(patient_id)
        JOIN history USING(history_id)
        WHERE reversal.balance != 0

        UNION
        SELECT
                (group_ledger_balance.balance*100)::int,
                NULL as ptype_id,
                'GROUP:' || group_ledger_balance.group_number as ref_no,
                NULL as puc_id,
                'GROUPC' as type_name,
                NULL as reversal_id,
                NULL,
                NULL,
                group_ledger_balance.group_number
        FROM group_ledger_balance
        WHERE group_ledger_balance.balance > 0
        """ % (cond,)
    try:
        cursor.execute(sql)
    except pg.DataError as e:
        res['errors'] = [str(e)]
        res['records'] = []
        return

    res['records'] = [dict(c) for c in cursor]

## BEGIN POST PAYMENT
@reg
@json
def post(req, res):
    fields = [
        'ptype_id',
        'ref_no',
        'trans_id',
        'entry_date',
        'amount',
        'overpayment',
        'puc_id',
        'reversal_id',
        'type'
    ]

    # Turn the arrays of individual values given in the POST data into a 
    # list of dictionaries that we can iterate over like any other kind of
    # record we are used to dealing with.
    separated_values = list(map(req.params.getall, fields))
    str_records = [dict(list(zip(fields, list_record)))
                   for list_record in zip(*separated_values)]

    # Convert POST string data into appropriate python data types
    records = []
    for payment in str_records:
        try:
            payment['trans_id'] = int(payment['trans_id'])
        except (TypeError, ValueError):
            res.error("Invalid trans_id %s" % payment['trans_id'])
            continue
        try:
            payment['amount'] = old_div(decimal.Decimal(payment['amount']),100)
            payment['amount'] = util.count_money(payment['amount'])
        except decimal.InvalidOperation:
            res.error("Invalid amount %s" % payment['amount'])
            continue
        try:
            payment['puc_id'] = int(payment['puc_id'])
        except (TypeError, ValueError):
            payment['puc_id'] = None
        try:
            payment['reversal_id'] = int(payment['reversal_id'])
        except (TypeError, ValueError):
            payment['reversal_id'] = None
        if payment['overpayment'] == "Y":
            payment["overpayment"] = True
        else:
            payment["overpayment"] = False
        records.append(payment)

    if res.has_error():
        return

    for payment in records:
        try:
            _add_payment(payment, req, res)
        except txlib.BusinessError as e:
            res.error(e)

    res['records'] = records
    if not res.has_error():
        R.db.commit()

def _add_payment(payment, req, res):
    if not payment['amount']:
        res.error('no amount')
        return
    if payment['type'] == 'GROUPC':
        m = re.match("^GROUP:(.+)$", payment['ref_no'])
        if not m:
            res.error("Invalid group credit ref number submitted %s" % payment['ref_no'])
            return
        group_number, = m.groups()
        txlib.add_group_credit_payment(
            payment['trans_id'],
            payment['amount'],
            group_number,
            R.session['username']
        )
    elif payment['puc_id']:
        txlib.add_overpayment_payment(
            payment['trans_id'],
            payment['puc_id'],
            payment['amount'],
            payment['entry_date'])
    elif payment['reversal_id']:
        txlib.add_adjudication(payment['trans_id'],
            payment['reversal_id'],
            payment['amount'],
            payment['entry_date'], 
            '')
    elif payment['overpayment']:
        txlib.add_overpayment(
            payment['trans_id'],
            payment['ptype_id'],
            payment['ref_no'],
            payment['amount'],
            payment['entry_date'])
    else:
        txlib.add_payment(
            payment['trans_id'],
            payment['ptype_id'],
            payment['ref_no'],
            payment['amount'],
            payment['entry_date'])


## END POST PAYMENT

application = reg.get_wsgi_app()
