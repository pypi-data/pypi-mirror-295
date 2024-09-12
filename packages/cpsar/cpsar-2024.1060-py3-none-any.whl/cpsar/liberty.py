""" Support library for interfacing with the liberty pharmacy system """
import base64
import datetime
import decimal
import io
import json
import math
import time

import requests

import cpsar.runtime as R
from cpsar import util
from cpsar import pg

try:
    import urllib3
    urllib3.disable_warnings()
except (ImportError, AttributeError):
    pass

# production credentials
username = 'corppharm'
password = '3h^4jL@8Ts'
npi = '1437194933'
api_key = '8241127'
customer_header = b'1437194933:8241127'
base_url = 'https://api.libertysoftware.com'

ZERO = decimal.Decimal("0.00")

class API(object):

    def __init__(self):
        self.load_insurance_codes()

    def load_insurance_codes(self):
        """ List of insurance codes we are to import """
        cursor = R.db.cursor()
        cursor.execute("""
            select insurance_code, group_number
            from client_liberty_insurance_code
        """)
        self.insurance_codes = dict((i, g) for i, g in cursor)

    def refresh(self):
        """ Refresh the cache index. This operation fetches all of
        the prescriptions for the last year into the cache table for
        quick listing.
        """
        cursor = R.db.cursor()
        if not pg.table_exists(R.db, "liberty_cache", "bd"):
            cursor.execute("""
                create table bd.liberty_cache (
                    rx_date date,
                    rx_number int,
                    refill_number int,
                    details jsonb
                )""")
        else:
            cursor.execute("truncate bd.liberty_cache")

        year_ago = datetime.date.today() - datetime.timedelta(days=365)
        start = datetime.date(2020, 8, 1)

        for rx in self.all_since(max(start, year_ago)):
            if not rx.get('Fill'):
                continue
            dispense_date = rx['Fill'].get('DispenseDate')
            if not dispense_date:
                continue
            cursor.execute(util.insert_sql("liberty_cache", {
                "rx_date": dispense_date,
                "rx_number": rx.get('ScriptNumber'),
                'details': json.dumps(rx)
            }))

    def script_details(self, rx_number, refill_number):
        rurl = api_url("/prescription/%s/%s" % (rx_number, refill_number))
        r = api_get(rurl)
        try:
            script = r.json()
        except:
            return None

        def _currency_value(v):
            """ The currency fields come in as floats from JSON. We have to
            stringify/quantize into decimal. """
            return util.count_money(decimal.Decimal(str(v)))

        if 'Fill' not in script:
            return None
        fill = script['Fill']
        primary_insurance = fill['Primary']
        insurance_code = primary_insurance['Id'].strip()

        group_number = self.insurance_codes.get(insurance_code)
        patient = script['Patient']

        # This is the cost allowed that comes back from the insurance. We don't use this.
        cost = decimal.Decimal(fill['Cost'])

        prescriber = script['Prescriber']
        cursor = R.db.cursor()
        cursor.execute("""
            select patient_id
            from patient
            where group_number=%s and dob=%s and ssn=%s
            """, (group_number, patient['BirthDate'], patient['Id']))
        patient_id = next(cursor)[0] if cursor.rowcount else ''

        cursor.execute("""
            select drug_id
            from drug
            where ndc_number=%s
            """, (fill['DrugDispensed']['NDC'],))
        drug_id = next(cursor)[0] if cursor.rowcount else ''

        # How much the insurance is going to pay
        insurance_pay = _currency_value(primary_insurance['InsurancePay'])

        # How much the patient is going to pay. We don't store this as a copay
        # because we want to actually collect the money and report it in AR.
        patient_pay = _currency_value(fill['PatientPay'])

        # How much the total bill for the prescription is for.
        cost_allowed = insurance_pay + patient_pay

        return {
            'group_number': group_number,
            'pat_first_name': patient['Name']['FirstName'],
            'pat_last_name': patient['Name']['LastName'],
            'sex': '2' if patient['Gender'] == 'F' else '1',
            'address_1': patient['Address']['Street1'],
            'address_2': patient['Address']['Street2'],
            'city': patient['Address']['City'],
            'state': patient['Address']['State'],
            'zip_code': patient['Address']['Zip'],
            'dob': util.parse_date2(patient['BirthDate']),
            'cardholder_number': patient['Id'],
            'patient_id': patient_id,
            'pharmacy_nabp': R.CPS_NABP_NBR,
            'rx_date': fill['DispenseDate'],
            'ndc': fill['DrugDispensed']['NDC'],
            'drug_id': drug_id,
            'drug_name': fill['DrugDispensed']['Name'],
            'gpi_code': fill['DrugDispensed'].get('GPI', ''),  # This isn't provided if the script is a compound
            'rx_number': script['ScriptNumber'],
            'refill_number': fill['RefillNumber'],
            'date_written': script['WrittenDate'],
            'daw': fill['DAW'],
            'quantity': fill['DispenseQuantity'],
            'days_supply': fill['DaysSupply'],
            'compound_code': '1' if fill['DrugDispensed']['IsCompound'] == 0 else '2',
            'cost_allowed': cost_allowed,
            'dispense_fee': ZERO,
            'processing_fee': ZERO,
            'copay': ZERO,
            'dea': prescriber['DEA'],
            'doctor_name': "%s %s" % (prescriber['Name']['FirstName'], prescriber['Name']['LastName']),
            'date_entered': time.strftime("%Y-%m-%d"),
            'awp': _currency_value(fill['AWP']),
            'state_fee': _currency_value(fill['AWP'])
        }

    def all_since(self, date):
        """ Get all scripts since the given date. This will make multiple queries based on
        page number, so it shouldn't be done all of the time. """
        sdate = date.strftime("%m/%d/%Y")
        rurl = api_url("/prescriptions?StartDate=%s&Page=1" % sdate)
        r = api_get(rurl)
        j = r.json()

        record_count = int(j['RecordCount'])
        page_size = int(j['PageSize'])

        page_count = int(math.ceil(float(record_count) / page_size))

        #print "Record count:", record_count
        #print "Page size:", page_size
        #print "Page count:", page_count

        for x in j['Scripts']:
            yield x
        for page_no in range(2, page_count+2):
            rurl = api_url("/prescriptions?StartDate=%s&Page=%s" % (sdate, page_no))
            #print page_no
            r = api_get(rurl)
            j = r.json()
            for x in j['Scripts']:
                yield x

    def unimported_since(self, date, end_date):
        """ List of all prescriptions that have not been imported into the back end since
        the given date.
        """

        cursor = R.db.cursor()
        cursor.execute("""
            select details
            from liberty_cache
            where rx_date between %s  and %s order by rx_date""", (date, end_date))

        pending_scripts = []
        for script, in cursor:
            if isinstance(script, str):
                script = json.loads(script)
            fill = script['Fill']
            primary_insurance = fill['Primary']
            if not primary_insurance:
                continue
            insurance_code = primary_insurance['Id'].strip()
            patient = script['Patient']

            group_number = self.insurance_codes.get(insurance_code)
            if not group_number:
                continue
            pending_scripts.append({
                'patient_name': " ".join([patient['Name']['FirstName'], patient['Name']['LastName']]),
                'dob': util.parse_date2(patient['BirthDate']),
                'group_number': group_number,
                'cardholder_number': patient['Id'].strip(),
                'rx_date': fill['DispenseDate'],
                'ndc': script['DrugPrescribed']['NDC'],
                'insurance_code': insurance_code,
                'compound_code': '1' if fill['DrugDispensed']['IsCompound'] == 0 else '2',
                'rx_number': script['ScriptNumber'],
                'refill_number': fill['RefillNumber'],
                'drug_name': fill['DrugDispensed']['Name'],
                'dispense_date': fill['DispenseDate'],
                'status_code': fill['StatusCode'],
                'cost': fill['Cost'],
                'awp': fill['AWP']
            })

        # Create temp table to do lookups of patients, transactions and drugs
        cursor = R.db.cursor()
        cursor.execute("""
            create temp table pat_lookup (
                group_number varchar,
                dob date,
                ssn varchar,
                rx_number int,
                refill_number int,
                ndc varchar)
                on commit delete rows""")
        buf = io.StringIO()
        for s in pending_scripts:
            if not s['dob']:
                continue
            buf.write(",".join([
                s['group_number'],
                s['dob'].strftime("%Y-%m-%d"),
                s['cardholder_number'],
                str(s['rx_number']),
                str(s['refill_number']),
                s['ndc']]))
            buf.write("\n")

        # Populate patient_id ans trans_id. Go through the trouble to not have N+1 queries.
        buf.seek(0)
        cursor.copy_from(buf, "pat_lookup", sep=",")
        cursor.execute("""
            alter table pat_lookup add column patient_id bigint;
            alter table pat_lookup add column trans_id bigint;
            alter table pat_lookup add column drug_id bigint;
            alter table pat_lookup add column drug_name varchar;
            update pat_lookup set patient_id=patient.patient_id
            from patient
            where pat_lookup.group_number = patient.group_number
              and pat_lookup.ssn = patient.ssn
              and pat_lookup.dob = patient.dob;

            update pat_lookup set trans_id=trans.trans_id
            from trans
            where trans.group_number = pat_lookup.group_number
              and trans.rx_number = pat_lookup.rx_number
              and trans.refill_number = pat_lookup.refill_number;

            update pat_lookup set drug_id=drug.drug_id, drug_name=drug.name
            from drug
            where pat_lookup.ndc = drug.ndc_number;
            """)
        cursor.execute("""
            select group_number, dob, ssn, patient_id
            from pat_lookup
            where patient_id is not null""")
        pat_lookup = dict(((c[0], c[1], c[2]), c[3]) for c in cursor)
        cursor.execute("""
            select group_number, rx_number, refill_number, trans_id
            from pat_lookup
            where trans_id is not null""")
        trans_lookup = dict(((c[0], c[1]), c[2]) for c in cursor)
        cursor.execute("""
            select ndc, drug_id, drug_name
            from pat_lookup
            where drug_id is not null""")
        drug_lookup = dict((c[0], (c[1], c[2])) for c in cursor)
        cursor.execute("drop table pat_lookup")
        for s in pending_scripts:
            s['patient_id'] = pat_lookup.get((s['group_number'], s['dob'], s['cardholder_number']), '')
            s['trans_id'] = trans_lookup.get((s['group_number'], s['rx_number'], s['refill_number']), '')
            s['drug_id'], s['drug_name'] = drug_lookup.get(s['ndc'], ['', s['drug_name']])
        return pending_scripts

class RecordSet(object):
    record_count = 0
    page_size = 50
    def __init__(self):
        self.records = []

def api_url(part):
    return '%s/%s' % (base_url, part)

def api_get(url):
    headers = {
        'Customer' : base64.b64encode(customer_header)
    }
    return requests.get(url, headers=headers,  auth=(username, password), verify=False)
