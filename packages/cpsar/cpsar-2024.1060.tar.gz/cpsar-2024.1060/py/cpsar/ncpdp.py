""" NCPDP form generation system
"""

import datetime
import sys

from copy import copy
from pprint import pprint, pformat
from textwrap import dedent

from reportlab.pdfgen.canvas import Canvas

import cpsar.pg as pg
import cpsar.runtime as R
import cpsar.util as util

from cpsar.ncpdp11 import ncpdp11

default_ingredient_data = {
        'product_name_1': '',
        'product_name_2': '',
        'product_name_3': '',
        'product_name_4': '',
        'product_name_5': '',
        'product_name_6': '',
        'product_name_7': '',
        'product_id_1': '',
        'product_id_2': '',
        'product_id_3': '',
        'product_id_4': '',
        'product_id_5': '',
        'product_id_6': '',
        'product_id_7': '',
        'product_type_1': '',
        'product_type_2': '',
        'product_type_3': '',
        'product_type_4': '',
        'product_type_5': '',
        'product_type_6': '',
        'product_type_7': '',
        'product_qty_1': '',
        'product_qty_2': '',
        'product_qty_3': '',
        'product_qty_4': '',
        'product_qty_5': '',
        'product_qty_6': '',
        'product_qty_7': '',
        'product_cost_1': '',
        'product_cost_2': '',
        'product_cost_3': '',
        'product_cost_4': '',
        'product_cost_5': '',
        'product_cost_6': '',
        'product_cost_7': '',
        'product_basis_1': '',
        'product_basis_2': '',
        'product_basis_3': '',
        'product_basis_4': '',
        'product_basis_5': '',
        'product_basis_6': '',
        'product_basis_7': '',
        }

default_data = {
        'indicator': 'WC',
        'patient_id_type': '99',
        'employer_name': 'Wal-mart',
        'pharmacy_id_type': '01',
        'doctor_id_type': '',
        'payee_tin': '631040950',
        'payee_id_type': '11', 
        'payee_name':  'Corporate Pharmacy Sevices',
        'payee_address': 'P.O. Box 1950',
        'payee_city': 'Gadsden',
        'payee_state': 'AL',
        'payee_zip_code': '35902', 
        'payee_phone': '800-568-3784',
        'sex': '',
        'employer_address': '',
        'employer_city': '',
        'employer_state': '',
        'employer_zip_code': '',
        'employer_phone': '',
        'employer_contact': '',
        'doctor_address': '',
        'doctor_city': '',
        'doctor_state': '',
        'doctor_zip_code': '',
        'doctor_phone': '',
        'jurisdiction_1': '',
        'jurisdiction_2': '',
        'jurisdiction_3': '',
        'jurisdiction_4': '',
        'jurisdiction_5': '',
        'rx_service_type': '1',
        'rx_origin': '0',
        'rx_classification': '',
        'product_id': '',
        'product_id_type': '',
        'pa_number': '',
        'pa_type': '',
        'other_coverage': '',
        'delay_reason': '',
        'other_payer_id': '',
        'other_payer_id_type': '',
        'other_payer_date': '',
        'other_payer_rejects': '',
        'dur_reason': '',
        'dur_service': '',
        'dur_result': '',
        'level_of_effort': '',
        'procedure_modifier': '',
        'dosage_form_description_code': '',
        'dispensing_unit_form_indicator': '',
        'route_of_administration': '',
        'ingredient_component_count': '',
        'basis_of_cost': '',
        'ingredient_cost': '',
        'dispensing_fee': '',
        'other_amount': '',
        'sales_tax': '',
        'patient_paid_amount': '',
        'other_payer_amount': '',
        'other_payer_patient_resp_amount': '',
        'doctor_first_name': '',
        'usual_customary_charge': '', 
}

def cmp_data_fmt(quantity, compound_code):
    cmp_data = {}
    cmp_data['strength'] =  ''
    cmp_data['measurement'] =  ''

    if int(compound_code) == 2:
        cmp_data['strength'] =  quantity
        cmp_data['measurement'] =  'GM'
    return cmp_data


def date_fmt(date):
    return date.strftime("%m-%d-%Y")


def find_doc_key(doc_id):
    """ If we didn't find the doc dea on the doctor table look in
    the doctor_key table use the dea or npi found there"""
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT 
            doc_key,
            modify_datetime
        FROM doctor_key 
        WHERE doctor_id = %s""" % doc_id)
    doc_keys = cursor.fetchall()
    dea_numbers = [(date, key) for key, date in doc_keys if not key.isdigit()]
    npi_numbers = [(date, key) for key, date in doc_keys if key.isdigit()]
    newest_dea = newest_key(dea_numbers)
    newest_npi = newest_key(npi_numbers)
    doc_data = {}
    if newest_dea is not None:
        doc_data['doctor_key'] = newest_dea
        doc_data['doctor_key_type'] = '12'
    if newest_dea is None and newest_npi is not None:
        doc_data['doctor_key'] = newest_npi
        doc_data['doctor_key_type'] = '01'
    return doc_data


def newest_key(keys):
    if keys: 
        return sorted(keys)[-1][1]
    else:
        return None


def make_canvas(fpath):
    """ Create the reportlab canvas that we are going to use. 
    """
    page_width = ncpdp11.page_width * 72
    page_height = ncpdp11.page_height * 72
    return Canvas(fpath, pagesize=(page_width, page_height))


def make_ncpdp_ingredient(txset):
    # an ingredient_set is the set of ingredients per page
    ingredient_data= []
    for id, ingredient_sets in enumerate(txset):
        rec = copy(default_ingredient_data)
        for idx, ingredient in enumerate(ingredient_sets):
            index = str(idx+1)
            rec['product_name_%s' % index ] = ingredient.drug_name 
            rec['product_id_%s' % index ] = ingredient.ndc_number
            rec['product_type_%s' % index ] = '03'
            rec['product_qty_%s' % index ] = ingredient.qty
            rec['product_cost_%s' % index ] = ingredient.cost
            rec['product_basis_%s' % index ] = '01'
        ingredient_data.append(rec)
    return ingredient_data


def make_ncpdp_record(txset):
    """ 
    For the set of given transactions, create a data source that can be
    passed to the NCPDP form generator. The length of the transactions must
    be 7 or less. This procedure defines the mapping between our backend
    database and the fields on a NCPDP form.
    """

    rec = copy(default_data)
    rec['date_of_billing'] = date_fmt(txset['batch_date']) #Batch_date
    rec['patient_last'] = txset['last_name'] 
    rec['patient_first'] = txset['first_name'] 
    rec['patient_address'] = txset['patient_address']
    rec['patient_city'] = txset['patient_city']
    rec['patient_state'] = txset['patient_state']
    rec['patient_zip_code'] = txset['patient_zip_code']
    rec['patient_phone'] = txset['patient_phone']
    rec['dob'] = date_fmt(txset['dob'])
    rec['doi'] = date_fmt(txset['doi'])
    rec['patient_id'] = txset['ssn']
    rec['sex'] = txset['sex']
    rec['invoice_id'] = txset['invoice_id']
    rec['jurisdiction'] = txset['jurisdiction']
    rec['claim_number'] = txset['claim_number']
    rec['client_name'] = txset['client_name']
    rec['client_address'] = txset['client_address']
    rec['client_city'] = txset['client_city']
    rec['client_state'] = txset['client_state']
    rec['client_zip_code'] = txset['client_zip_code']
    rec['pharmacy_npi'] = txset['npi']
    rec['pharmacy_name'] = txset['pharmacy_name']
    rec['pharmacy_address'] = txset['pharmacy_address']
    rec['pharmacy_city'] = txset['pharmacy_city']
    rec['pharmacy_zip_code'] = txset['pharmacy_zip_code']
    rec['pharmacy_state'] = txset['pharmacy_state']
    rec['pharmacy_zip_code'] = txset['pharmacy_zip_code']
    rec['pharmacy_phone'] = txset['pharmacy_phone']

    doc_dea = txset['doctor_dea_number']
    doc_id_type = '12'
    if doc_dea in (None, ''):
        doc_data = find_doc_key(txset['doctor_id'])
        doc_dea = doc_data['doctor_key']
        doc_id_type = doc_data['doctor_key_type']

    rec['doctor_dea_number'] = doc_dea 
    rec['doctor_id_type'] = doc_id_type
    rec['doctor_last_name'] = txset['doctor_name']

    rec['rx_number'] = txset['rx_number']
    rec['refill_number'] = txset['refill_number']
    rec['daw'] = txset['daw']
    rec['rx_date'] = date_fmt(txset['rx_date'])
    rec['quantity'] = txset['quantity']
    rec['days_supply'] = txset['days_supply']
    rec['daw'] = txset['daw']
    rec['drug_name'] = txset['drug_name']
    cmp_data = {}
    cmp_data = cmp_data_fmt(txset['quantity'], txset['compound_code'])
    rec['drug_strength'] = cmp_data['strength']
    rec['unit_of_measure'] = cmp_data['measurement']

    rec['usual_customary_charge'] = txset['total']
    rec['gross_amount'] = txset['total']
    rec['net_amount'] = txset['total']
    rec['awp_sfs'] = txset['awp_sfs']

    return rec

if __name__ == '__main__':
    Program().run()
