""" Formulary Services Module

This module allows for programs to determine whether or not a 
particular drug is on the formulary for a particular patient.
"""
from __future__ import print_function
from builtins import range
import re

import cpsar.runtime as R
import cpsar.shell as S

## Public Interface
def patient_has_drug(patient, drug):
    """ Is the given drug on formulary for the given
    patient? The records must have fields for the
    patient and drug tables respectively.
    """
    if _drug_on_patient_drug_list(drug, patient):
        return True
    if not patient['uses_group_formulary']:
        return False
    return _drug_on_group_formulary(drug, patient['group_number'])

## Testing Interface
class Program(S.Command):
    def do_on(self, args):
        patient_id, ndc_number = args.split()
        patient = _patient_by_id(patient_id)
        drug = _drug_by_ndc(ndc_number)
        print(patient_has_drug(patient, drug))

    def do_speed(self, args):
        patient_id, ndc_number = args.split()
        patient = _patient_by_id(patient_id)
        drug = _drug_by_ndc(ndc_number)
        for i in range(1000):
            patient_has_drug(patient, drug)

## Implementation
def _drug_on_patient_drug_list(drug, patient):
    cursor = R.db.dict_cursor()
    cursor.execute("""
        SELECT gpi_regexp
        FROM patient_drug_list
        WHERE patient_id = %s
        """, (patient['patient_id'],))

    for gpi_regex, in cursor:
        if re.compile(gpi_regex).match(drug['gpi_code']):
            return True
    return False

def _drug_on_group_formulary(drug, group_number):
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT uses_formulary, formulary
        FROM client
        WHERE group_number=%s
        """, (group_number,))
    uses_formulary, formulary = cursor.fetchone()
    if not uses_formulary:
        return False
    # If no formulary is on file for the client, we lookup a
    # formulary specific to the group number
    if not formulary:
        formulary = group_number
    cursor.execute("""
        SELECT gpi_regexp
        FROM group_formulary
        WHERE name=%s
        """, (formulary,))
    for gpi_regexp, in cursor:
        if re.compile(gpi_regexp).match(drug['gpi_code']):
            return True
    return False

def _drug_by_ndc(ndc):
    cursor = R.db.dict_cursor()
    cursor.execute("""
        SELECT *
        FROM drug
        WHERE ndc_number=%s
        """, (ndc,))
    if not cursor.rowcount:
        raise ValueError("NDC # %s not found" % ndc)
    return cursor.fetchone()

def _patient_by_id(patient_id):
    cursor = R.db.dict_cursor()
    cursor.execute("""
        SELECT *
        FROM patient
        WHERE patient_id=%s
        """, (patient_id,))
    if not cursor.rowcount:
        raise ValueError("Unknown patient id %s" % patient_id)
    return cursor.fetchone()

if __name__ == '__main__':
    Program().run()
