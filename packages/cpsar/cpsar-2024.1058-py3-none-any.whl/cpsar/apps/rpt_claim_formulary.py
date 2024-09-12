
import datetime

import kcontrol as K
import cpsar.wsgirun as W
import cpsar.report
import cpsar.runtime as R

from cpsar.controls import PharmacyFilterListBox
from cpsar import sales

class Report(cpsar.report.WSGIReport):
    label = 'Patient Claim Formulary Export'
    def form_params(self):
        self.params = [
            ('Group Number', sales.ClientListBox('group_number')),
            ('Report Code', K.TextBox('report_code')),
        ]

    query_css = """
    """

    sql = """
    select patient.group_number,
           patient.first_name,
           patient.last_name,
           patient.ssn,
           patient.dob,
           patient.sex,
           claim.doi,
           claim.claim_number,
           doi_formulary.drug_name,
           doi_formulary.gpi_code
    from doi_formulary
    join claim using(claim_id)
    join patient using(patient_id)
    join client using(group_number)
    where patient.group_number %(gn_frag)s
    order by patient.group_number,
             patient.last_name,
             patient.first_name
    """

application = Report().wsgi()
