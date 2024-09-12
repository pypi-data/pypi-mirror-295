import datetime

import kcontrol as K
import cpsar.wsgirun as W
import cpsar.report
import cpsar.runtime as R

from cpsar.controls import PharmacyFilterListBox
from cpsar import sales

class Report(cpsar.report.WSGIReport):
    label = 'Pharmacy Paid Transactions'
    def form_params(self):
        self.params = [
            ('Group Number', sales.ClientListBox('group_number')),
            ('Report Code', K.TextBox('report_code')),
            ('Posting Date After', K.DatePicker('posting_date_after',
                     defaultValue=datetime.date.today()-datetime.timedelta(2),
                     required=True
                     )),
            ('Posting Date Before', K.DatePicker('posting_date_before',
                     defaultValue=datetime.date.today(), required=True))
        ]

    sql = """
        SELECT trans.trans_id,
               trans.group_number,
               trans.pharmacy_nabp,
               trans.batch_date,
               trans.rx_number,
               patient.first_name || ' ' || patient.last_name AS patient,
               trans.refill_number || ' (' || trans.refill_number %% 20 || ')' AS refill_number,
               history.pharmacy_payment_date,
               drug.name as drug_name
        FROM trans
        JOIN drug using(drug_id)
        JOIN history using(history_id)
        JOIN patient ON trans.patient_id = patient.patient_id
        WHERE history.pharmacy_payment_date BETWEEN
              %(posting_date_after)s AND %(posting_date_before)s
              AND trans.group_number %(gn_frag)s
    ORDER BY trans.trans_id
    """

application = Report().wsgi()
