#!/usr/bin/env python
""" Report written for Nancy to display all the processor activity at EHO
for CPS for a given day. This is so Nancy can compare and match that up with
what they have in HBS.
"""
import os
import datetime

import cpsar.runtime as R
import cpsar.report
import kcontrol

yesterday = datetime.date.today() - datetime.timedelta(days=1)

class Report(cpsar.report.WSGIReport):
    label = 'Daily Processor Totals at EHO for Pharmacy'
    params = [
      ('Process Date', kcontrol.DatePicker('process_date', value=yesterday)),
      ('Pharmacy NABP',   kcontrol.TextBox('nabp', value=R.CPS_NABP_NBR))
    ]

    def record_fields(self):
        return [
            'Process Time',
            'RX #',
            'Refill #',
            'RX Date',
            'Group #',
            'First Name',
            'Last Name',
            'NDC #',
            'Drug',
            'Qty',
            'D/S',
            'Cost Allowed',
            'Dispense Fee',
            'Sales Tax',
            'Reverse Date'
        ]

    sql = """
        SELECT to_char(history.date_processed, 'HH12:MI AM') AS process_time,
               history.rx_number,
               history.refill_number::int %% 20 AS refill_number,
               history.rx_date,
               history.group_number,
               patient.first_name,
               patient.last_name,
               fmt_ndc(drug.ndc_number),
               drug.name,
               history.quantity,
               history.days_supply,
               history.cost_allowed,
               history.dispense_fee,
               history.sales_tax,
               to_char(history.reverse_date, 'MM/DD/YYYY')
        FROM history
        JOIN patient USING(patient_id)
        JOIN drug USING(drug_id)
        JOIN pharmacy USING(pharmacy_id)
        WHERE history.date_processed::date = %(process_date)s AND
              pharmacy.nabp = %(nabp)s
        ORDER BY history.date_processed ASC
    """

    def _records(self):
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT history.group_number,
                   history.group_auth,
                   cost_allowed + dispense_fee + sales_tax - eho_network_copay 
            FROM history
            JOIN heldback ON history.history_id = heldback.history_id
            WHERE heldback.batch_date BETWEEN %(start_date)s AND
                                              %(end_date)s
            """ % self.query_args())
        for x in cursor: yield x

        cursor.execute("""
            SELECT 'TOTAL', '',
                   SUM(cost_allowed + dispense_fee + sales_tax - eho_network_copay)
            FROM history
            JOIN heldback ON history.history_id = heldback.history_id
            WHERE heldback.batch_date BETWEEN %(start_date)s AND
                                              %(end_date)s
            """ % self.query_args())
        yield cursor.fetchone()

application = Report().wsgi()

