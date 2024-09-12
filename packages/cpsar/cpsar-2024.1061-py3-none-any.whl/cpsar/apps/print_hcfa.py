import os

import cpsar.hcfa as H
import cpsar.invoice as I
import cpsar.pg as P
import cpsar.runtime as R
import cpsar.ws as W
import cpsar.util as U

class Program(W.GProgram):

    def main(self):
        trans_ids = self.fs.getlist('trans_id')
        invoice_id = self.fs.getvalue('invoice_id')

        if trans_ids:
            self.generate_trans_batch(trans_ids)
        elif invoice_id:
            self.generate_single_invoice(invoice_id)

    def generate_single_invoice(self, invoice_id):
        """ Generate the PDF for a single invoice. """
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT trans_id
            FROM trans
            WHERE invoice_id=%s""",
            (invoice_id,))

        trans_ids = [c for c, in cursor]
        trans_data = hcfa_transaction_data(trans_ids)
        write_pdf_to_response(trans_data, self._res)

    def generate_trans_batch(self, trans_ids):
        """ Generate a PDF file for invoices with the given set of
        transactions. This procedure was written to provide invoice
        generation from the trans search page.
        """
        trans_data = hcfa_transaction_data(sorted(trans_ids))
        write_pdf_to_response(trans_data, self._res)

def hcfa_transaction_data(trans_ids):
    """ Provide a list of all transactions records to put on the HCFA form
    for the given list of trans_ids
    """
    cursor = R.db.dict_cursor()

    frag = ", ".join(map(P.qstr, trans_ids))

    cursor.execute("""
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
            client.print_multiplier_invoice,
            client.print_nonmultiplier_invoice,
            client.invoice_multiplier,
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
        WHERE trans.trans_id IN (%s)
        ORDER BY trans.group_number, patient.last_name, patient.first_name,
                 trans.patient_id, trans.invoice_id,
                 trans.pharmacy_id
        """ % frag)

    for tx in map(dict, cursor):
        factor = tx['invoice_multiplier']
        if tx['print_multiplier_invoice']:
            tx['total'] = U.count_money(factor * tx['total'])
        yield tx

def write_pdf_to_response(trans_data, res):
    sets = H.group_trans_set(trans_data)
    res.content_type = 'application/pdf'
    canvas = H.make_canvas(res)
    drawer = H.hcfa1500(my_canvas=canvas)
    for t in sets:
        drawer.ds = H.make_hcfa_record(t)
        drawer.show_background = False
        drawer.draw()
    canvas.save()

application = Program.app
