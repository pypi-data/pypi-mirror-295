""" Keep lookup library
Each object provides a lookup of values based on key values which are loaded
from the relational database. These are simple memory caching mechanisms to
save repeatedly lookups from the database.
"""
import logging

import cpsar.runtime as R

log = logging.getLogger()

class PatientLookup(dict):
    def __init__(self):
        cursor = R.db.cursor()
        log.debug('Populating patient key lookup')
        cursor.execute("""
            SELECT patient_id, group_number, to_char(dob, 'YYYYMMDD'), ssn
            FROM patient""")
        for pid, gn, dob, ssn in cursor:
            self[(gn, dob, ssn)] = pid

class DrugLookup(dict):
    def __init__(self):
        log.debug('Populating drug key lookup')
        cursor = R.db.cursor()
        cursor.execute("SELECT drug_id, ndc_number FROM drug")
        for id, ndc in cursor:
            self[ndc] = id

class PharmacyLookup(dict):
    def __init__(self):
        log.debug('Populating pharmacy key lookup')
        cursor = R.db.cursor()
        cursor.execute("SELECT nabp, pharmacy_id FROM pharmacy")
        for nabp, id in cursor:
            self[nabp] = id

class DoctorLookup(dict):
    def __init__(self):
        log.debug('Populating doctor key lookup')
        cursor = R.db.cursor()
        cursor.execute("SELECT doc_key, doctor_id FROM doctor_key")
        for key, doctor_id in cursor:
            self[key] = doctor_id

class HistoryLookup(dict):
    def __init__(self):
        log.debug('Populating history key lookup')
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT group_number, group_auth, history_id
            FROM history """)
        for gn, ga, id in cursor:
            self[(gn, ga)] = id

class TransLookup(dict):
    def __init__(self):
        log.debug('Populating trans key lookup')
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT group_number, group_auth, trans_id
            FROM trans""")
        for gn, ga, id in cursor:
            self[(gn, ga)] = id

class ClaimLookup(dict):
    def __init__(self):
        log.debug('Populating claim key lookup')
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT patient_id, to_char(doi, 'YYMMDD'), claim_id
            FROM claim
            """)
        for pid, doi, id in cursor:
            self[(pid, doi)] = id
