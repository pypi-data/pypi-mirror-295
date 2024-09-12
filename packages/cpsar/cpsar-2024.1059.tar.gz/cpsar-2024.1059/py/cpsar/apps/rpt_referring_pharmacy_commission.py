import collections
import csv

import kcontrol

import cpsar.sales
import cpsar.runtime as R
import cpsar.report

class Report(cpsar.report.WSGIReport):
    label = 'Referring Pharmacy Commission'

    sql_tmpl_file = 'rpt_referring_pharmacy_commission.tmpl'
    csv_exportable = False

    def form_params(self):
        self.params = [
            ('Start Distribution Date', kcontrol.DatePicker('start_date')), 
            ('End Distribution Date',   kcontrol.DatePicker('end_date'))
        ]

    def validate_form_input(self):
        if not self.req.params.get('start_date'):
            R.error("No start date selected")
        if not self.req.params.get('end_date'):
            R.error("No end date selected")

    def records(self):
        return ''

    def pharmacies(self):
        cursor = R.db.dict_cursor()
        g = self.req.get
        cursor.execute("""
            SELECT pharmacy.name,
                   distribution.distribution_account AS nabp,
                   pharmacy.address_1,
                   pharmacy.address_2,
                   pharmacy.city,
                   pharmacy.state,
                   pharmacy.zip_code,
                   patient.first_name || ' ' || patient.last_name AS patient_name,
                   patient.dob AS patient_dob,
                   trans.rx_date,
                   trans.rx_number,
                   trans.refill_number,
                   trans.quantity,
                   doctor.name AS doctor_name,
                   distribution.distribution_date,
                   distribution.distribution_account,
                   distribution.amount
            FROM distribution
            JOIN trans USING(trans_id)
            JOIN patient USING(patient_id)
            LEFT JOIN pharmacy ON
                distribution.distribution_account = pharmacy.nabp
            JOIN history USING(history_id)
            LEFT JOIN doctor ON history.doctor_id = doctor.doctor_id
            WHERE distribution_date BETWEEN %s AND %s
              AND distribution.referring_pharmacy = TRUE
            ORDER BY distribution_account
        """, (g('start_date'), g('end_date')))

        pharmacies = collections.OrderedDict()
        phcy_fields = ['name', 'nabp', 'address_1','address_2',
                       'city', 'state', 'zip_code']
        dist_fields = ['patient_name', 'patient_dob', 'rx_date',
                       'refill_number', 'quantity', 'doctor_name',
                       'rx_number', 'distribution_date', 'amount']
        for rec in cursor:
            phcy = pharmacies.get(rec['nabp'])
            if not phcy:
                phcy = dict((f, rec[f]) for f in phcy_fields)
                phcy['distributions'] = []
                phcy['total_count'] = 0
                phcy['total_amount'] = 0
                pharmacies[rec['nabp']] = phcy
            dist = dict((f, rec[f]) for f in dist_fields)
            phcy['distributions'].append(dist)
            phcy['total_count'] += 1
            phcy['total_amount'] += dist['amount']
        return pharmacies.values()

    def csv(self):
        self.res.content_type = 'text/csv'

        h = self.res.headers
        h.add("Expires", "0")
        h.add("Content-Transfer-Encoding", "binary")
        h.add("Pragma", "public")
        h.add("Content-Disposition", "attachment; filename=%s" %
                                     self.csv_file_name)
        cursor = self.records()
        writer = csv.writer(self.res)
        preamble = self.preamble()
        if preamble is not None:
            writer.writerow(preamble)
        writer.writerow([
            '', '', 'Mail Order Brand', '', 'Mail Order Generic', '',
            'Retail Brand', '', 'Retail Generic', '', 'Other', ''])
        writer.writerow(['number', 'group']
          + ['count', 'amount'] * 5
          + ['count_total', 'subtotal', 'reversals_and_writeoffs', 'total'])

        for rec in cursor:
            writer.writerow(rec)

application = Report().wsgi()

