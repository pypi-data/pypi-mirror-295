#!/usr/bin/env python
from __future__ import absolute_import
import csv
import datetime
import decimal
import json as _json
import time

import cpsar.runtime as R
import cpsar.util as U

from cpsar import cobol
from cpsar import liberty
from cpsar import pg
from cpsar import txtype
from cpsar.wsgirun import mako, wsgi, json, PathDispatch

reg = PathDispatch()

ZERO = decimal.Decimal("0.00")

@reg
@mako("import_liberty.tmpl")
def index(req, res):
    res['pharmacy_id'] = _cps_pharmacy_id()
    res['pharmacy_nabp'] = R.CPS_NABP_NBR
    res['distribution_accounts'] = _distribution_accounts()
    res['load_date'] = R.session.get('load_date', datetime.date.today().strftime("%Y-%m-%d"))
    res['lookup_end_date'] = R.session.get('lookup_end_date', datetime.date.today().strftime("%Y-%m-%d"))

def _distribution_accounts():
    cursor = R.db.cursor()
    cursor.execute("SELECT name FROM distribution_account ORDER BY name")
    return [c[0] for c in cursor]

def _cps_pharmacy_id():
    cursor = R.db.cursor()
    cursor.execute("SELECT pharmacy_id FROM pharmacy WHERE nabp=%s",
        (R.CPS_NABP_NBR,))
    return cursor.fetchone()[0]

@reg
def cache_summary(req, res):
    cursor = R.db.cursor()
    cursor.execute("""
        select rx_date, count(*)::text from liberty_cache
        group by rx_date
        order by rx_date
        """)
    res.csv_header("liberty_summary.csv")
    wr = csv.writer(res)
    wr.writerow(['rx_date', 'count'])
    for c in cursor:
        wr.writerow(list(c))

@reg
def download_cache(req, res):
    cursor = R.db.cursor()
    cursor.execute("""
        select details from liberty_cache
        order by rx_date
        """)
    res.content_type = 'application/json'
    cache = [c for c, in cursor]
    res.write(_json.dumps(cache))

@reg
def rx_lookup(req, res):
    start_date = U.parse_date(req.get('lookup_start_date'))
    if not start_date:
        start_date = datetime.date.today() - datetime.timedelta(days=7)

    end_date = U.parse_date(req.get('lookup_end_date'))
    if not end_date:
        end_date = datetime.date.today()

    R.session['load_date'] = start_date.strftime("%Y-%m-%d")
    R.session['lookup_end_date'] = end_date.strftime("%Y-%m-%d")
    R.session.save()

    api = liberty.API()
    prescriptions = api.unimported_since(start_date, end_date)
    if not prescriptions:
        res.write("No results found")
        return

    res.write("""<table class='grid'><thead><tr>
        <th>Rx Date</th>
        <th>Rx #</th>
        <th>Group #</th>
        <th>Name</th>
        <th>Patient ID</th>
        <th>DOB</th>
        <th>Cardholder #</th>
        <th>Cpd</th>
        <th>Drug</th>
        <th>Status</th>
        <th>Cost</th>
        <th colspan='2'></th>
    </tr></thead>""")
    for rec in prescriptions:
#        if rec['status_code'] not in ('PickedUp', 'Shipped'):
#            continue
        res.write("""<tr>
          <td>%(rx_date)s</td>
          <td class='script_id'>%(rx_number)s-%(refill_number)s</td>
          <td class='group_number'>%(group_number)s</td>
          <td>%(patient_name)s</td>
          <td><span class='patient_id'>%(patient_id)s</span></td>
          <td>%(dob)s</td>
          <td>%(cardholder_number)s</td>
          <td>%(compound_code)s</td>
          <td><span class='drug_id'>%(drug_id)s</span>:
              <span class='ndc'>%(ndc)s</span>:
              <span class='drug_name'>%(drug_name)s</span>
          </td>
          <td>%(status_code)s</td>
          <td><span class='cost'>%(cost)s</span></td>
        """ % rec)
        if rec['trans_id']:
            link = "<a href='/view_trans?trans_id=%(trans_id)s' target='_blank'> " % rec
            res.write("<td>Existing trans: %s%s</a></td>" % (link, rec['trans_id']))
        elif not rec['patient_id']:
            if rec['dob']:
                res.write("""
                <td><input type='button' class='add_patient' value='Add Patient' /></td>
                <td>Patient not on file in %s</td>
                """ % rec['group_number'])
            else:
                res.write("<td></td><td>Cannot add patient with no DOB on file</td>")
        elif not rec['drug_id']:
                res.write("""
                <td>
                    <select class='add_brand_generic'>
                        <option value='G'>Generic</option>
                        <option value='B'>Brand</option>
                    </select>
                    <input type='button' class='add_drug' value='Add Drug' />
                </td>
                <td>Drug NDC #%s not on file</td>""" % rec['ndc'])
        else:
            res.write("<td><input type='button' class='load_rx' value='Load' /></td><td></td>")
        res.write("</tr>")
    res.write("</table>")

@reg
@json
def add_script_patient(req, res):
    script_id = req.get('script_id') or ''
    rx_number, _, refill_number = script_id.partition('-')
    try:
        rx_number = int(rx_number)
        refill_number = int(refill_number)
    except (ValueError, TypeError):
        res.error("invalid script_id %s" % script_id)
        return

    api = liberty.API()
    s = api.script_details(rx_number, refill_number)
    if not s:
        res.error("Could not load script %s:%s" % (rx_number, refill_number))
        return
    group_number = s["group_number"]
    if not group_number:
        res.error("no group number given")
        return
    cursor = R.db.dict_cursor()
    sql = U.insert_sql("patient", {
        'group_number': s['group_number'],
        'dob': s['dob'],
        'ssn': s['cardholder_number'],
        'first_name': s['pat_first_name'],
        'last_name': s['pat_last_name'],
        'name': "%s %s" % (s['pat_first_name'], s['pat_last_name']),
        'address_1': s['address_1'][:30],
        'address_2': s['address_2'][:30],
        'source': 'liberty',
        'city': s['city'],
        'state': s['state'],
        'zip_code': s['zip_code']
    }) + " ON CONFLICT (group_number, dob, ssn) DO NOTHING RETURNING *"
    cursor.execute(sql)
    if not cursor.rowcount:
        cursor.execute("""
            select * from patient where group_number=%s and dob=%s and ssn=%s
            """, (s['group_number'], s['dob'], s['cardholder_number']))
    res.update(next(cursor))
    R.db.commit()

@reg
@json
def add_script_drug(req, res):
    script_id = req.get('script_id') or ''
    rx_number, _, refill_number = script_id.partition('-')
    try:
        rx_number = int(rx_number)
        refill_number = int(refill_number)
    except (ValueError, TypeError):
        res.error("invalid script_id %s" % script_id)
        return

    brand = req.get('brand')
    if brand not in ('B', 'G', 'C'):
        res.error("Invalid Brand %r. Expected B, G or C" % brand)
        return

    api = liberty.API()
    s = api.script_details(rx_number, refill_number)
    if not s:
        res.error("Could not load script %s:%s" % (rx_number, refill_number))
        return
    cursor = R.db.dict_cursor()
    sql = U.insert_sql("drug", {
        'ndc_number': s['ndc'],
        'name': s['drug_name'],
        'gpi_code': s['gpi_code'],
        'source': 'liberty',
        'brand': brand,
    }) + " ON CONFLICT (ndc_number) DO NOTHING RETURNING *"
    cursor.execute(sql)
    if not cursor.rowcount:
        cursor.execute("""
            select * from drug where ndc_number=%s
            """, (s['ndc'],))
    res.update(next(cursor))
    R.db.commit()

def brand(drug_id):
    if not drug_id:
        return 'G'
    cursor = R.db.cursor()
    cursor.execute("""
        select brand from drug where drug_id=%s""", (drug_id,))
    if cursor.rowcount:
        return next(cursor)[0]
    else:
        return 'G'

def ndc_number(drug_id):
    if not drug_id:
        return ''
    cursor = R.db.cursor()
    cursor.execute("""
        select ndc_number from drug where drug_id=%s""", (drug_id,))
    if cursor.rowcount:
        return next(cursor)[0]
    else:
        return ''

@reg
@json
def load_rx(req, res):
    script_id = req.get('script_id') or ''
    rx_number, _, refill_number = script_id.partition('-')
    try:
        rx_number = int(rx_number)
        refill_number = int(refill_number)
    except (ValueError, TypeError):
        res.error("invalid script_id %s" % script_id)
        return

    api = liberty.API()
    script = api.script_details(rx_number, refill_number)
    if not script:
        res.error("Could not load script %s:%s" % (rx_number, refill_number))
        return

    group_number = script["group_number"]
    if not group_number:
        res.error("no group given")
        return
    res.update(script)

    pricing = R.pricing_module(group_number)
    pricing.use_db()

    tx = pricing.Transaction.for_record({
            'group_number': group_number,
            'cost_allowed': res['cost_allowed'],
            'dispense_fee': res['dispense_fee'],
            'processing_fee': res['processing_fee'],
            'sales_tax': ZERO,
            'eho_network_copay': ZERO,
            'brand': brand(res['drug_id']),
            'compound_code': res['compound_code'],
            'awp': res['awp'],
            'state_fee': res['awp'],
            'nabp': res['pharmacy_nabp'],
            'ndc': ndc_number(res['drug_id'])
        })

    res['client_price'] = tx.total
    res['tx_type'] = tx.rx.tx_type
    """
    store = pricing2.PreloadPgStore()
    inq = pricing2.Inquiry()
    inq.group_number = res['group_number']
    inq.pharmacy_nabp = res['pharmacy_nabp']
    inq.cost_allowed = res['cost_allowed']
    inq.dispense_fee = res['dispense_fee']
    inq.processing_fee = res['processing_fee']
    inq.copay = res['copay']
    res['client_price'] = pricing2.client_price(inq, store)
    res['tx_type'] = inq.tx_type(store)
    """

@reg
@json
def add(req, res):
    ## Internal Utility
    def _date_value(field_name):
        if not req.get(field_name): return None
        try:
            return U.parse_date(req.get(field_name))
        except U.ParseError:
            res.error('Invalid date %s for %s', req.get(field_name), field_name)
    def _currency_value(field_name):
        if not req.get(field_name):
            return decimal.Decimal("0.00")
        try:
            return decimal.Decimal(req.get(field_name))
        except decimal.InvalidOperation:
            res.error('Invalid currency value %s for %s', req.get(field_name), field_name)

    cursor = R.db.dict_cursor()

    # Group Number
    group_number = req.get('group_number')
    if not group_number:
        res.error("no group # given")

    # Group Auth/Claim Reference Number
    cursor.execute("select nextval('grouph_auth_nbr_seq') as group_auth")
    group_auth, = next(cursor)
    cursor.execute("""
      SELECT history_id FROM history
      WHERE group_number=%s AND group_auth=%s
      """, (group_number, group_auth))
    if cursor.rowcount:
        res.error('group_auth %s already found for %s: assigned to HY %s',
                  group_auth, group_number, cursor.fetchone()['history_id'])
        return

    # Patient ID
    try:
        patient_id = int(req.get('patient_id'))
    except ValueError:
        res.error('Invalid patient_id %s', req.get('patient_id'))
        return
    cursor.execute("SELECT * FROM patient WHERE patient_id=%s", (patient_id,))
    if not cursor.rowcount:
        res.error('No patient with id %s found', patient_id)
        return
    prec = cursor.fetchone()
    patient_dob = prec['dob']
    patient_ssn = prec['ssn']
    
    # Drug ID
    try:
        drug_id = int(req.get('drug_id'))
    except (TypeError, ValueError) as e:
        res.error('Invalid drug_id %s', req.get('drug_id'))
        return
    cursor.execute('SELECT * FROM drug where drug_id=%s', (drug_id,))
    if not cursor.rowcount:
        res.error('No drug with id %s found', drug_id)
        return
    drec = cursor.fetchone()
    drug_ndc_number = drec['ndc_number']
    brand = drec['brand']

    # Pharmacy ID
    try:
        pharmacy_id = int(req.get('pharmacy_id'))
    except ValueError:
        res.error('Invalid pharmacy_id', req.get('pharmacy_id'))
        return
    cursor.execute('SELECT * FROM pharmacy WHERE pharmacy_id=%s', (pharmacy_id,))
    if not cursor.rowcount:
        res.error('No pharmacy with id %s found', pharmacy_id)
        return
    pharmacy_nabp = cursor.fetchone()['nabp']

    # Doctor ID
    doctor_name = req.get('doctor_name')
    doctor_id = None
    dea = req.get('doctor_dea_number')
    npi = req.get('doctor_npi_number')

    if dea:
        cursor.execute("""
          SELECT doctor_id FROM doctor_key WHERE doc_key=%s
          """, (dea,))
        if cursor.rowcount:
            doctor_id = cursor.fetchone()['doctor_id']
        else:
            doctor_id = doctor_id_for_new(dea, req.get('doctor_name'))
    elif npi:
        cursor.execute("""
          SELECT doctor_id FROM doctor_key WHERE doc_key=%s
          """, (npi,))
        if cursor.rowcount:
            doctor_id = cursor.fetchone()['doctor_id']

    rx_date = _date_value('rx_date')
    date_written = _date_value('date_written')

    batch_date = _date_value('batch_date')
    if not batch_date:
        res.error('missing required batch date')
        return

    # Quantity
    try:
        quantity = decimal.Decimal(req.get('quantity'))
    except decimal.InvalidOperation:
        res.error('Invalid quantity %s', req.get('quantity'))
        return

    # Day's Supply
    try:
        days_supply = int(req.get('days_supply'))
    except ValueError:
        res.error('Invalid days supply')
        return

    # Compound Code
    compound_code = req.get('compound_code')
    if compound_code not in ('1', '2'):
        res.error('Invalid compound code %r', compound_code)
        return

    # DAW
    daw = req.get('daw')
    if len(daw) > 1:
        res.error('DAW must be 1 character')
        return

    # Rx Number/ Refill #
    try:
        rx_number = int(req.get('rx_number'))
    except ValueError:
        res.error('Invalid rx_number %s', rx_number)
        return
    try:
        refill_number = int(req.get('refill_number'))
    except ValueError:
        res.error('Invalid refill_number %s', refill_number)
        return

    # Invoice ID/Line No
    invoice_id, line_no = next_invoice(batch_date, patient_id)

    # Batch file
    batch_file_name = "liberty-%s" % batch_date.strftime("%Y%m%d")
    cursor.execute("""
      SELECT batch_file_id FROM batch_file
      WHERE file_name=%s
      """, (batch_file_name,))
    if cursor.rowcount:
        batch_file_id = cursor.fetchone()[0]
    else:
        cursor.execute(U.insert_sql("batch_file", {
            'batch_date': batch_date,
            'file_name': batch_file_name
        }, ['batch_file_id']))
        batch_file_id = cursor.fetchone()[0]

    usual_customary = _currency_value('usual_customary')
    cost_submitted = _currency_value('cost_submitted')

    ###########################################################################
    # Pricing
    pricing = R.pricing_module(group_number)
    pricing.use_db()

    tx = pricing.Transaction.for_record({
            'group_number': group_number,
            'cost_allowed': _currency_value('cost_allowed'),
            'dispense_fee': _currency_value('dispense_fee'),
            'processing_fee': _currency_value('processing_fee'),
            'sales_tax': 0,
            'eho_network_copay': _currency_value('eho_network_copay'),
            'brand': brand,
            'compound_code': compound_code,
            'awp': _currency_value('awp'),
            'state_fee': _currency_value('state_fee'),
            'sales_tax': _currency_value('sales_tax'),
            'nabp': pharmacy_nabp,
            'ndc': drug_ndc_number
        })

    hy = pricing.History(tx)
    #res['client_price'] = tx.total
    #res['tx_type'] = tx.rx.tx_type

    client_price = _currency_value('client_price')

    """
    store = pricing2.PreloadPgStore()
    inq = pricing2.Inquiry()
    inq.cost_allowed =  _currency_value('cost_allowed')
    inq.dispense_fee = _currency_value('dispense_fee')
    inq.processing_fee = _currency_value('processing_fee')
    inq.awp = _currency_value('awp')
    inq.state_fee = _currency_value('state_fee')
    inq.sales_tax = _currency_value('sales_tax')
    inq.compound_code = compound_code
    inq.copay = _currency_value('eho_network_copay')
    inq.group_number = group_number
    inq.brand_code = brand
    inq.pharmacy_nabp = pharmacy_nabp
    client_price = _currency_value('client_price')
    """

    if res.has_error():
        return

    ## history record
    hrec = {
        'group_number': group_number,
        'group_auth': group_auth,
        'patient_id': patient_id,
        'pharmacy_id': pharmacy_id,
        'doctor_id': doctor_id,
        'drug_id': drug_id,
        'rx_date': rx_date,
        'rx_number': rx_number,
        'date_written': date_written,
        'daw': daw,
        'quantity': quantity,
        'days_supply': days_supply,
        'compound_code': compound_code,
        'refill_number': refill_number,
        'cost_submitted': tx.cost_allowed,
        # Sponsor Cost Allowed
        'sponsor_cost_allowed': tx.pbm.cost_allowed,
        'sponsor_dispense_fee': tx.pbm.dispense_fee,
        # PBM Cost Allowed
        'cost_allowed': hy.cost_allowed,
        'dispense_fee': hy.dispense_fee,
        'processing_fee': tx.processing_fee,
        'sales_tax': tx.sales_tax,
        'eho_network_copay': tx.copay,
        'usual_customary': usual_customary,
        'state_fee': tx.rx.state_fee,
        'awp': tx.rx.awp,
        'date_processed': datetime.datetime.now(),
        'doctor_dea_number': dea,
        'doctor_npi_number': npi,
        'tx_type': tx.rx.tx_type,
        'ctime': datetime.datetime.now()
    }
    cursor.execute(U.insert_sql('history', hrec, ['*']))
    hrec = cursor.fetchone()
    history_id = hrec['history_id']
    res['hrec'] = dict(hrec)

    # trans record
    trec = dict(
        batch_date = batch_date,
        create_date = batch_date,
        batch_file_id = batch_file_id,
        group_number = group_number,
        group_auth = group_auth,
        invoice_id = invoice_id,
        line_no = line_no,
        patient_dob = patient_dob,
        patient_cardholder_nbr = patient_ssn,
        patient_id = patient_id,
        pharmacy_nabp = pharmacy_nabp,
        pharmacy_id = pharmacy_id,
        doctor_dea_number = dea,
        doctor_npi_number = npi,
        drug_ndc_number = drug_ndc_number,
        drug_id = drug_id,
        rx_date = rx_date,
        rx_number = rx_number,
        date_written = date_written,
        daw = daw,
        quantity = quantity,
        days_supply = days_supply,
        compound_code = compound_code,
        refill_number = refill_number,
        cost_allowed = tx.cost_allowed,
        dispense_fee = tx.dispense_fee,
        processing_fee = tx.processing_fee,
        eho_network_copay = tx.copay,
        total = tx.total,

        cost_submitted = cost_submitted,
        usual_customary = usual_customary,
        state_fee = tx.rx.state_fee,
        awp = tx.rx.awp,
        tx_type = tx.rx.tx_type,
        history_id = history_id)

    trec['balance'] = trec['total']
    trec['savings'] = trec['awp'] - trec['total']

    cursor.execute(U.insert_sql('trans', trec, ['*']))
    res['trec'] = dict(cursor.fetchone())
    trans_id = res['trec']['trans_id']

    upsert_invoice(invoice_id)

    for d in tx.distributions:
        account, amount = d[:2]
        cursor.execute(U.insert_sql('distribution', dict(
            trans_id=trans_id,
            distribution_account=account,
            amount=amount
        )))

    R.db.commit()

def next_invoice(batch_date, patient_id):
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT MAX(invoice_id), MAX(line_no)+1
        FROM trans
        WHERE batch_date=%s AND patient_id=%s
        """, (batch_date, patient_id))

    invoice_id, line_no = cursor.fetchone()
    if invoice_id:
        return (invoice_id, line_no)

    cursor.execute("SELECT MAX(invoice_id)+1 FROM trans")
    return cursor.fetchone()[0], 1


def upsert_invoice(invoice_id):
    cursor = R.db.cursor()
    total, balance, item_count = _invoice_aggregates(invoice_id)
    cursor.execute("""
      UPDATE invoice SET total = %s, balance = %s, item_count = %s
      WHERE invoice_id = %s
      RETURNING *
      """, (total, balance, item_count, invoice_id))
    if cursor.rowcount > 0:
        return

    cursor.execute("""
      SELECT patient_id, group_number, batch_date, 
             batch_date + INTERVAL '15 days'
      FROM trans
      WHERE invoice_id=%s
      LIMIT 1
      """, (invoice_id,))
    if not cursor.rowcount:
        return
    patient_id, group_number, batch_date, due_date = cursor.fetchone()
    cursor.execute(U.insert_sql('invoice', dict(
      invoice_id=invoice_id,
      patient_id=patient_id,
      group_number=group_number,
      batch_date=batch_date,
      due_date=due_date,
      total=total,
      adjustments=0,
      balance=balance,
      item_count=item_count
    )))

def _invoice_aggregates(invoice_id):
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT SUM(total), SUM(balance), COUNT(*)
        FROM trans WHERE invoice_id=%s
        """, (invoice_id,))
    return [c or 0 for c in cursor.fetchone()]

def doctor_id_for_new(dea, name):
    record = {'name': name}
    result = cobol.query('corp-docfm2', record)
    doctor_id = result['results'][0]['doctor_id']
    record = {'doctor_id': doctor_id, 'doc_key': dea}
    cobol.query('corp-doc-key-set', record)
    time.sleep(1)
    return doctor_id

application = reg.get_wsgi_app()
