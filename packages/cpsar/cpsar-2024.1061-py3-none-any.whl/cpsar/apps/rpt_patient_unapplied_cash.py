import kcontrol as K

import cpsar.wsgirun as W
import cpsar.report

from cpsar import sales

class Report(cpsar.report.WSGIReport):
    label = "Patient Unapplied Cash"
    def form_params(self):
        self.params = [
            ('Group Number', sales.ClientListBox('group_number')),
            ('Start Entry Date', K.DatePicker('start_date')), 
            ('End Entry Date',   K.DatePicker('end_date'))
        ]

    sql = """
        SELECT patient.group_number,
               patient.first_name,
               patient.last_name,
               patient.ssn,
               patient.dob,
               overpayment.puc_id,
               NULL AS reversal_id,
               overpayment.amount,
               overpayment.balance,
               'OP' AS type,
               trans.trans_id::text,
               trans.claim_number AS claim_number,
               trans.invoice_id AS invoice_id,
               trans.drug_ndc_number,
               drug.name,
               to_char(trans.rx_date, 'MM/DD/YYYY'),
               NULL AS reversal_date,

               to_char(trans.batch_date, 'MM/DD/YYYY'),
               to_char(trans.create_date, 'MM/DD/YYYY'),
               to_char(overpayment.entry_date, 'MM/DD/YYYY') AS entry_date,
               to_char(overpayment.entry_date, 'HH12:MI AM') 

        FROM overpayment
        JOIN trans USING (trans_id)
        JOIN drug USING(drug_id)
        JOIN patient ON trans.patient_id = patient.patient_id
        WHERE
            overpayment.balance != 0 AND
            patient.group_number %(gn_frag)s AND
            overpayment.entry_date BETWEEN %(start_date)s AND %(end_date)s
        UNION ALL
        SELECT trans.group_number, 
               patient.first_name, 
               patient.last_name, 
               patient.ssn,
               patient.dob,
               NULL,
               reversal.reversal_id::text, 
               reversal.total AS amount, 
               reversal.balance, 
               'REV', 
               trans.trans_id::text, 
               trans.claim_number,
               trans.invoice_id,
               drug.ndc_number,
               drug.name AS ndc_desc,
               to_char(trans.rx_date, 'MM/DD/YYYY'),
               to_char(reversal.reversal_date, 'MM/DD/YYYY') AS reversal_date,
               to_char(trans.batch_date, 'MM/DD/YYYY') AS trans_batch_date,
               to_char(trans.create_date, 'MM/DD/YYYY') AS trans_create_date,
               to_char(reversal.reversal_date, 'MM/DD/YYYY') AS entry_date,
               '' AS entry_time
        FROM reversal
        JOIN trans USING(trans_id)
        JOIN patient USING(patient_id)
        JOIN drug USING(drug_id)
        WHERE reversal.balance != 0 AND
              trans.group_number %(gn_frag)s AND
              reversal.entry_date BETWEEN %(start_date)s AND %(end_date)s

        ORDER BY last_name, first_name, entry_date
        """
 
application = Report().wsgi()

