import kcontrol as K

import cpsar.wsgirun as W
import cpsar.report

from cpsar import sales

class Report(cpsar.report.WSGIReport):
    label = "Collections Report"
    def form_params(self):
        self.params = [
            ('Group Number', sales.ClientListBox('group_number')),
            ('Report Code', K.TextBox('report_code')),
            ('Age', K.TextBox('age', required=True, defaultValue='30'))
        ]

    def query_args(self):
        a = super(Report, self).query_args()
        age = self.req.params.get("age")
        a['age'] = f"'{age} days'"
        return a

    def record_fields(self):
        return [
        "Trans #",
        "Invoice #",
        "Group #",
        "Invoice Date",
        "Patient Name",
        "Patient DOB",
        "Patient SSN",
        "Patient DOI",
        "Claim #",
        "Rx Date",
        "Rx Number",
        "Drug Name",
        "Pharmacy Name",
        "State Fee Schedule",
        "Total",
        "Amount Due",
        "Age"
    ]

    sql = """
        select
            trans.trans_id,
            trans.invoice_id,
            trans.group_number,
            trans.batch_date,
            patient.first_name || '' || patient.last_name,
            patient.dob,
            patient.ssn,
            trans.doi,
            coalesce(claim.claim_number, trans.claim_number),
            trans.rx_date,
            trans.rx_number,
            drug.name,
            pharmacy.name,
            trans.state_fee,
            trans.total,
            trans.balance,
            extract('Day' from now() - trans.batch_date)::int
        from trans
        join patient using(patient_id)
        join history using(history_id)
        join claim using(claim_id)
        join drug on history.drug_id = drug.drug_id
        join pharmacy on pharmacy.pharmacy_id = history.pharmacy_id
        where
            trans.group_number %(gn_frag)s and
            trans.balance != 0 and
            now() - trans.batch_date > %(age)s
        order by trans.trans_id
        """

application = Report().wsgi()

