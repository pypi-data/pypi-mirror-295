""" HCFA form generation system

"""
from past.builtins import cmp
from builtins import input
from builtins import str
from builtins import map
from past.builtins import basestring
from builtins import object
import logging
import sys

from copy import copy
from decimal import Decimal
from itertools import count
from math import floor
from pprint import pprint, pformat
from textwrap import dedent

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch

import cpsar.pg as pg
import cpsar.runtime as R
import cpsar.util as util

from cpsar.hcfa1500 import hcfa1500

default_data = {
        'patient_name': '',
        'patient_dob_mm': '',
        'patient_dob_dd': '',
        'patient_dob_yyyy': '',
        'patient_sex_m': '',
        'patient_sex_f': '',
        'insured_type_other': 'X',
        'insured_id_number': '',
        'insured_named': '',
        'patient_relationship_self': 'X',
        'patient_address_street': '',
        'patient_address_city': '',
        'patient_address_state': '',
        'patient_address_zip_code': '',
        'patient_phone_area_code': '',
        'patient_phone': '',
        'insured_policy_group_number': '',
        'insured_dob_mm': '',
        'insured_dob_dd': '',
        'insured_dob_yyyy': '',
        'insured_sex_male': '',
        'insured_sex_female': '',
        'doi_mm': '',
        'doi_dd': '',
        'doi_yyyy': '',
        'referring_provider_name': '',
        'referring_provider_npi': '',
        'referring_provider_dea': '',
        'dos_from_mm_1': '',
        'dos_from_dd_1': '',
        'dos_from_yy_1': '',
        'dos_to_mm_1': '',
        'dos_from_mm_2': '',
        'dos_from_mm_3': '',
        'dos_from_mm_4': '',
        'dos_from_mm_5': '',
        'dos_from_mm_6': '',
        'dos_from_dd_2': '',
        'dos_from_dd_3': '',
        'dos_from_dd_4': '',
        'dos_from_dd_5': '',
        'dos_from_dd_6': '',
        'dos_from_yy_2': '',
        'dos_from_yy_3': '',
        'dos_from_yy_4': '',
        'dos_from_yy_5': '',
        'dos_from_yy_6': '',
        'dos_to_mm_2': '',
        'dos_to_mm_3': '',
        'dos_to_mm_4': '',
        'dos_to_mm_5': '',
        'dos_to_mm_6': '',
        'dos_to_dd_1': '',
        'dos_to_dd_2': '',
        'dos_to_dd_3': '',
        'dos_to_dd_4': '',
        'dos_to_dd_5': '',
        'dos_to_dd_6': '',
        'dos_to_yy_1': '',
        'dos_to_yy_2': '',
        'dos_to_yy_3': '',
        'dos_to_yy_4': '',
        'dos_to_yy_5': '',
        'dos_to_yy_6': '',
        'pos_1': '',
        'pos_2': '',
        'pos_3': '',
        'pos_4': '',
        'pos_5': '',
        'pos_6': '',
        'service_1': '',
        'pos_6': '',
        'service_2': '',
        'service_3': '',
        'service_4': '',
        'service_5': '',
        'service_6': '',
        'modifier_1': '',
        'modifier_2': '',
        'modifier_3': '',
        'modifier_4': '',
        'modifier_5': '',
        'modifier_6': '',
        'charge_dollar_1': '',
        'charge_cent_1': '',
        'charge_dollar_2': '',
        'charge_dollar_3': '',
        'charge_dollar_4': '',
        'charge_dollar_5': '',
        'charge_dollar_6': '',
        'charge_cent_2': '',
        'charge_cent_3': '',
        'charge_cent_4': '',
        'charge_cent_5': '',
        'charge_cent_6': '',
        'rendering_provider_npi_1': '',
        'rendering_provider_npi_2': '',
        'rendering_provider_npi_3': '',
        'rendering_provider_npi_4': '',
        'rendering_provider_npi_5': '',
        'rendering_provider_npi_6': '',
        'federal_tax_id_number': '63-1040950',
        'ein': 'X',
        'accept_assignment_yes': 'X',
        'total_charge_dollar': '',
        'total_charge_cent': '',
        'balance_due_dollar': '',
        'balance_due_cent': '',
        'service_facility_1': '',
        'service_facility_2': '',
        'service_facility_3': '',
        'billing_provider_1': 'CORPORATE PHARMACY SERV., INC.',
        'billing_provider_2': 'P.O. BOX 1950',
        'billing_provider_3': 'GADSDEN, AL 35902',
        'billing_provider_phone_area_code': '800',
        'billing_provider_phone': '568-3784',
        'service_facility_npi': '',
        'billing_provider_npi': '1437194933',
        'reserved_for_local_use': '',
        'is_there_another_health_benefit_plan_no': 'X',
        'insured_plan_name': '',
        'days_or_units_1': '',
        'days_or_units_2': '',
        'days_or_units_3': '',
        'days_or_units_4': '',
        'days_or_units_5': '',
        'days_or_units_6': '',
        'invoice_line': 'Please reference invoice #%s when submitting '
                        'payment'
}

def groups_with_hcfa_set():
    """ Provide a list of all groups with the PRINT HCFA FORM flag """
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT group_number
        FROM client
        WHERE print_hcfa_1500 = TRUE
        ORDER BY group_number
        """)
    return [c[0] for c in cursor]

def batches_to_process(groups):
    """ Provide a list of all batch dates that have transactions
    that have not had HCFA's generated for them.
    """
    gn_frag = ", ".join(pg.qstr(g) for g in groups)
    cursor = R.db.cursor()
    cursor.execute("""
      SELECT batch_date
      FROM (
        SELECT DISTINCT batch_date
        FROM trans
        WHERE group_number IN (%s)
        ) AS X
      LEFT JOIN hcfa_1500_print_history USING(batch_date)
      WHERE hcfa_1500_print_history.batch_date IS NULL
      ORDER BY batch_date
        """ % gn_frag)
    return [b[0] for b in cursor]

def gen_batch_pdf(batch_date, group_numbers):
    """ Generate a PDF file for the given batch_date for all of the group
    numbers provided.
    """
    logging.debug("Generating HCFA file for batch %s", batch_date)
    fname = "hcfa-%s.pdf" % batch_date.strftime("%Y%m%d")
    fpath = R.dpath("invoice", "hcfa", fname)
    canvas = make_canvas(fpath)
    drawer = hcfa1500(my_canvas=canvas)
    drawer.show_background = False

    for gn in group_numbers:
        trans = get_trans_set(gn, batch_date)
        trans = list(sorted(group_trans_set(trans), key=lambda x: x[0]['invoice_id']))
        for t in trans:
            drawer.ds = make_hcfa_record(t)
            logging.info("Rendering for %s %s",
                         t[0]['first_name'], t[0]['last_name'])
            for x in t:
                logging.debug("Line %s", x['drug_name'])
            drawer.draw()
    canvas.save()

def record_batch_gen_history(batch_date):
    """ Record the fact that we have generated the HCFA for the given batch
    date so we won't do it again.
    """
    cursor = R.db.cursor()
    cursor.execute(
        "INSERT INTO hcfa_1500_print_history (batch_date) VALUES (%s)",
        (batch_date,))

def unrecord_batch_gen_history(batch_date):
    cursor = R.db.cursor()
    cursor.execute("DELETE FROM hcfa_1500_print_history WHERE batch_date=%s",
                    (batch_date,))

def gen_group_pdf(group_number, batch_date, fpath, show_background=False):
    """ Generate a PDF file for the given group number and batch date
    containing HCFA forms for all of the transactions.
    """
    trans = get_trans_set(group_number, batch_date)
    sets = group_trans_set(trans)
    canvas = make_canvas(fpath)
    drawer = hcfa1500(my_canvas=canvas)
    drawer.show_background = show_background
    for t in sets:
        drawer.ds = make_hcfa_record(t)
        logging.info("Rendering for %s %s", 
                     t[0]['first_name'], t[0]['last_name'])
        for x in t:
            logging.debug("Line %s", x['drug_name'])
        drawer.draw()
    canvas.save()

def make_canvas(fpath):
    """ Create the reportlab canvas that we are going to use. 
    """
    page_width = hcfa1500.page_width * 72
    page_height = hcfa1500.page_height * 72
    return Canvas(fpath, pagesize=(page_width, page_height))

def get_trans_set(group_number, batch_date):
    """ Provide a list of all transactions that need to be on the
    HCFA form for the given group_number and batch_date)
    """
    cursor = R.db.dict_cursor()
    def execute(sql, a):
        import cpsar.pg
        sql %= tuple(map(pg.qstr, a))
        logging.debug(sql)
        cursor.execute(sql)

    execute("""
        SELECT client.print_multiplier_invoice,
               client.print_nonmultiplier_invoice,
               client.invoice_multiplier
        FROM client
        WHERE group_number=%s
        """, (group_number,))
    client = cursor.fetchone()

    execute("""
        SELECT
            trans.total, 
            trans.doi,
            trans.invoice_id,
            trans.trans_id,
            trans.group_number,
            claim.claim_number,
            history.rx_date,
            history.quantity,
            client.billing_name,
            patient.ssn,
            patient.dob,
            patient.first_name,
            patient.last_name,
            patient.sex,
            patient.address_1 AS patient_address_1,
            patient.address_2 AS patient_address_2,
            patient.city AS patient_city,
            patient.state AS patient_state,
            patient.zip_code AS patient_zip_code,
            patient.phone AS patient_phone,
            pharmacy.name AS pharmacy_name,
            pharmacy.nabp AS pharmacy_nabp,
            pharmacy.npi AS pharmacy_npi,
            pharmacy.address_2 AS pharmacy_address_2,
            pharmacy.city AS pharmacy_city,
            pharmacy.state AS pharmacy_state,
            pharmacy.zip_code AS pharmacy_zip_code,
            doctor.name AS doctor_name,
            history.doctor_npi_number AS doctor_npi_number,
            history.doctor_dea_number AS doctor_dea_number,
            drug.ndc_number,
            drug.name AS drug_name
        FROM trans
        JOIN client USING(group_number)
        JOIN patient USING(patient_id)
        JOIN drug USING(drug_id)
        JOIN pharmacy USING(pharmacy_id)
        JOIN history USING(history_id)
        LEFT JOIN claim USING(claim_id)
        LEFT JOIN doctor ON history.doctor_id = doctor.doctor_id
        WHERE trans.group_number = %s AND trans.batch_date = %s
        ORDER BY trans.group_number, patient.last_name, patient.first_name,
                 trans.patient_id, trans.invoice_id,
                 trans.pharmacy_id
        """, (group_number, batch_date))

    factor = client['invoice_multiplier']
    for tx in map(dict, cursor):
        if client['print_multiplier_invoice']:
            tx['total'] = util.count_money(factor * tx['total'])
        yield tx

def group_trans_set(txs):
    """ Group together the list of transactions into pages. The
    pages are based on the DOI and there can only be 6 transactions
    per page.
    """
    bucket = []
    for tx in txs:
        if _cmp_trans(tx, bucket):
            bucket.append(tx)
            logging.debug("Added tx on invoice %s to bucket", tx['invoice_id'])
        else:
            logging.debug("Grouped %s tx's for %s", len(bucket), bucket[0]['invoice_id'])
            for item in _chop_tx_set(bucket):
                yield item
            bucket = [tx]
    if bucket:
        logging.debug("Grouped %s tx's for %s", len(bucket), bucket[0]['invoice_id'])
        for item in _chop_tx_set(bucket):
            yield item

def make_hcfa_record(txset):
    """ For the set of given transactions, create a data source that can be
    passed to the HCFA form generator. The length of the transactions must
    be 6 or less. This procedure defines the mapping between our backend
    database and the fields on a HCFA form.
    """
    assert 0 < len(txset) <= 6
    head = txset[0]
    rec = copy(default_data)
    rec['patient_name'] = "%(last_name)s, %(first_name)s" % head
    rec['patient_dob_mm'] = head['dob'].strftime("%m")
    rec['patient_dob_dd'] = head['dob'].strftime("%d")
    rec['patient_dob_yyyy'] = head['dob'].strftime("%Y")
    if head['sex'] == '1':
        rec['patient_sex_m'] = 'X'
        rec['insured_sex_male'] = 'X'
    else:
        rec['patient_sex_f'] = 'X'
        rec['insured_sex_female'] = 'X'
    rec['insured_id_number'] = head['ssn']
    rec['insured_named'] = "%(last_name)s, %(first_name)s" % head
    rec['patient_address_street'] = head['patient_address_1']
    rec['patient_address_city'] = head['patient_city']
    rec['patient_address_state'] = head['patient_state']
    rec['patient_address_zip_code'] = head['patient_zip_code']
    rec['patient_phone'] = head['patient_phone']
    rec['insured_policy_group_number'] = head['claim_number']
    rec['insured_dob_mm'] = head['dob'].strftime("%m")
    rec['insured_dob_dd'] = head['dob'].strftime("%d")
    rec['insured_dob_yyyy'] = head['dob'].strftime("%Y")
    if head['doi']:
        rec['doi_mm'] = head['doi'].strftime("%m")
        rec['doi_dd'] = head['doi'].strftime("%d")
        rec['doi_yyyy'] = head['doi'].strftime("%Y")
        rec['reserved_for_local_use'] = head['doi'].strftime("%m/%d/%Y")
    rec['referring_provider_name'] = head['doctor_name']
    rec['referring_provider_npi'] = head['doctor_npi_number']
    rec['referring_provider_dea'] = head['doctor_dea_number']

    total = Decimal("0.0")
    subs = txsubset(rec, txset)
    for sub in subs:
        subs.set("dos_from_mm", sub['rx_date'].strftime("%m"))
        subs.set("dos_from_dd", sub['rx_date'].strftime("%d"))
        subs.set("dos_from_yy", sub['rx_date'].strftime("%y"))
        subs.set("dos_to_mm", sub['rx_date'].strftime("%m"))
        subs.set("dos_to_dd", sub['rx_date'].strftime("%d"))
        subs.set("dos_to_yy", sub['rx_date'].strftime("%y"))
        subs.set("pos", "01")
        subs.set("service", sub['drug_name'])
        subs.set("modifier", sub['ndc_number'])
        subs.set("days_or_units", sub['quantity'])

        charge_d, charge_c = split_currency(sub['total'])
        subs.set("charge_dollar", charge_d)
        subs.set("charge_cent", charge_c)
        subs.set("rendering_provider_npi", sub['pharmacy_npi'])
        total += sub['total']

    total_d, total_c = split_currency(total)
    rec['total_charge_dollar'] = total_d
    rec['total_charge_cent'] = total_c
    rec['balance_due_dollar'] = total_d
    rec['balance_due_cent'] = total_c
    rec['service_facility_1'] = head["pharmacy_name"]
    rec['service_facility_2'] = head['pharmacy_address_2']
    rec['service_facility_3'] = "%(pharmacy_city)s, %(pharmacy_state)s %(pharmacy_zip_code)s" % head
    rec['service_facility_npi'] = head["pharmacy_npi"]
    rec['insured_plan_name'] = head['billing_name']
    rec['invoice_line'] %= head['invoice_id']
    return rec

def pause(m, *a):
    import sys
    if not isinstance(m, basestring):
        m = str(m)
    else:
        m %= a
    sys.stderr.write(m + "\n")
    input("Continue")

class txsubset(object):
    """ Provides a clean interface for setting values based on the 
    numeric field numbers which are maintained internally. 
    """
    def __init__(self, out, txset):
        self.out = out
        self.txset = txset
        self.idx = -1

    def __iter__(self):
        return self

    def __next__(self):
        self.idx += 1
        try:
            return self.txset[self.idx]
        except IndexError:
            raise StopIteration

    def set(self, key, value):
        key = "%s_%s" % (key, self.idx+1)
        self.out[key] = value

def split_currency(x):
    """ Split a decimal currency value into dollars and cents. """
    dollar = int(floor(x))
    cents = x - dollar
    cents = int(cents * 100)
    return dollar, "%02d" % cents

def _cmp_trans(a, b, _keys=
               ['group_number', 'ssn', 'dob', 'doi', 'pharmacy_npi']):
    """ Return true if transaction a is for the same claim as trans b. """
    if not b:
        return True
    return list(map(a.__getitem__, _keys)) == list(map(b[0].__getitem__, _keys))

def _chop_tx_set(items):
    """ We can only have 6 transactions per page, so we break them up
    if there is more.
    """
    bucket = []
    items = list(items)
    while items:
        if len(bucket) == 6:
            yield bucket
            bucket = []
        bucket.append(items.pop(0))
    if bucket:
        yield bucket

if __name__ == '__main__':
    Program().run()
