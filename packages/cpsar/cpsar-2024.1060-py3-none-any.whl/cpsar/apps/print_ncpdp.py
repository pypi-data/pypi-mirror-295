
from cpsar import print_invoice
import cpsar.ncpdp as N 
import cpsar.pg as P
import cpsar.runtime as R
import cpsar.util as util
import cpsar.ws as W

class Program(W.GProgram):

    def main(self):
        trans_ids = self.fs.getlist('trans_id')
        invoice_id = self.fs.getvalue('invoice_id')

        f = print_invoice.Factory()
        ifactory = f.invoice_factory()
        invoice = ifactory.for_invoice_id(invoice_id)
        

        if trans_ids:
            self.generate_trans_batch(trans_ids)
        elif invoice_id:
            self._generate_single_invoice(invoice)

    def _generate_single_invoice(self, invoice):
        """ Generate the PDF for a single invoice. """
        trans_ids = []
        for line_item in invoice.items:
            trans_ids.append(line_item.trans_id)

        trans_data = ncpdp_transaction_data(trans_ids)
        write_pdf_to_response(invoice, trans_data, self._res)

def ncpdp_transaction_data(trans_ids):
    """ Provide a list of all transactions records to put on the NCPDP form
    for the given list of trans_ids
    """
    cursor = R.db.dict_cursor()
    frag = ", ".join(map(P.qstr, trans_ids))
    cursor.execute("""
        SELECT
            trans.group_number,
            trans.batch_date,
            patient.first_name,
            patient.last_name,
            patient.address_1 AS patient_address,                  
            patient.city AS patient_city,
            patient.state AS patient_state,
            patient.zip_code AS patient_zip_code,
            patient.phone AS patient_phone,
            patient.dob,
            patient.ssn,
            trans.doi,
            patient.patient_id,
            patient.sex,
            trans.invoice_id,
            soj.abbr AS jurisdiction,
            trans.claim_number,
            client.client_name,
            client.address_1 AS client_address,
            client.city AS client_city,
            client.state client_state,
            client.zip_code client_zip_code,
            pharmacy.npi,
            pharmacy.name AS pharmacy_name,
            pharmacy.address_1 AS pharmacy_address,
            pharmacy.city AS pharmacy_city,
            pharmacy.state AS pharmacy_state,
            pharmacy.zip_code AS pharmacy_zip_code,
            pharmacy.phone AS pharmacy_phone,
            trans.doctor_dea_number,
            doctor.name AS doctor_name,
            doctor.doctor_id,
            trans.rx_number,
            trans.refill_number,
            trans.date_written, 
            trans.rx_date,
            trans.quantity,
            trans.days_supply,
            trans.daw,
            drug.name AS drug_name,
            trans.total AS total,
            trans.compound_code,
            'AWP: $' || coalesce(trans.awp, '0.00') || '  SFS: $' || coalesce(trans.state_fee, '0.00') AS awp_sfs       -- AWP and SFS
        FROM trans
        JOIN patient USING(patient_id)
        JOIN client ON trans.group_number = client.group_number
        JOIN pharmacy USING (pharmacy_id)
        JOIN doctor USING (doctor_id)
        JOIN drug USING (drug_id)
        JOIN soj USING(jurisdiction)
        WHERE trans.trans_id IN (%s)
        ORDER BY trans.group_number, patient.last_name, patient.first_name,
                 trans.patient_id, trans.invoice_id,
                 trans.pharmacy_id
        """ % frag)
    for tx in map(dict, cursor):
        yield tx

def write_pdf_to_response(invoice, trans_data, res):
    trans_ids =[]
    res.content_type = 'application/pdf'
    canvas = N.make_canvas(res)
    drawer = N.ncpdp11(my_canvas=canvas)
    ingredients_per_page = 7

    # for every item being printed on the invoice
    #for line_item in invoice_items: 
    for idx, rec in enumerate(trans_data):
        # isolate our ingredients
        line_item = invoice.items[idx]
        ingredients = [i for i in line_item.ingredients]

        # seperate its ingredients into sets <= ingredients_per_page
        ingredient_sets = [ingredients[i:i+ingredients_per_page] 
                for i in range(0, len(ingredients), ingredients_per_page)]

        # map ingredients to form data field names
        form_ingredient_data = N.make_ncpdp_ingredient(ingredient_sets)

        current_page = 1
        for ingredient_set in form_ingredient_data:
            # We need to re collect the records for each record set
            drawer.ds.clear()

            # map line item data to form data field names
            form_data = N.make_ncpdp_record(rec)

            # Pull the totals out so we can override them for all pages but the last
            totals = { 'usual_customary_charge': form_data['usual_customary_charge'],
                       'gross_amount': form_data['gross_amount'],
                       'net_amount': form_data['net_amount'],
                       'awp_sfs': form_data['awp_sfs']}

            form_data['usual_customary_charge'] = ''
            form_data['gross_amount'] = ''
            form_data['net_amount'] = ''
            form_data['awp_sfs'] = 'See next page'

            # Only apply totals to the last page
            if current_page == len(ingredient_sets):
                form_data['usual_customary_charge'] = totals['usual_customary_charge']
                form_data['gross_amount'] = totals['gross_amount']
                form_data['net_amount'] = totals['net_amount']
                form_data['awp_sfs'] = totals['awp_sfs']
            
            current_page += 1
            drawer.ds = form_data

            for key, val in ingredient_set.items():
                drawer.ds["%s" % key] = val 

            drawer.show_background = True
            drawer.draw()
    canvas.save()

application = Program.app
