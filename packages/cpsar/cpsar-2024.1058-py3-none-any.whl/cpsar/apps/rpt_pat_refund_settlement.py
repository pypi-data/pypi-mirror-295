""" This report was requested by Lindsay for MRM to show patients that
have had refunds in three months in a row. We implemented it as 2 months
in a row because we've never seen one with three months in a row.
"""
import datetime as DT
import kcontrol as K

import cpsar.wsgirun as W
import cpsar.runtime as R

from cpsar import report
from cpsar import pg
from cpsar import sales
from cpsar import util

class Report(report.WSGIReport):
    label = "Patient Refund Settlement Report"
    def form_params(self):
        self.params = [
            ('Group Number', sales.ClientListBox('group_number')),
            ('Report Code', K.TextBox('report_code')),
            ('As Of',   K.DatePicker('as_of'))
        ]

    def query_args(self):
        as_of = self.req.get('as_of')
        if as_of:
            try:
                ao = util.parse_american_date(as_of)
            except util.ParseError:
                ao = DT.date.today()
        else:
            ao = DT.date.today()

        # Gross way of going two months back
        fom = DT.datetime(ao.year, ao.month, 1)
        lom = fom - DT.timedelta(days=1)
        fom = DT.datetime(lom.year, lom.month, 1)
        ## Third month
        #lom = fom - DT.timedelta(days=1)
        #fom = DT.datetime(lom.year, lom.month, 1)

        args = super(Report, self).query_args()
        args['as_of'] = pg.qstr(ao)
        args['start_date'] = pg.qstr(fom)
        return args

    sql = """
with os as (
    select overpayment_settlement.*
    from overpayment_settlement
    join overpayment using(puc_id)
    join trans using(trans_id)
    where overpayment_settlement.check_no not like 'WO%%'
      and overpayment_settlement.void_date is null
      and overpayment_settlement.entry_date between %(start_date)s and %(as_of)s
      and trans.group_number %(gn_frag)s
      ),
pat_by_mo as (
    select trans.patient_id, date_trunc('month', os.entry_date) as month
    from os
    join overpayment using(puc_id)
    join trans using(trans_id)
    group by trans.patient_id, month),
spat as (
    select pat_by_mo.patient_id
    from pat_by_mo
    group by pat_by_mo.patient_id
    having count(*) >= 2)
select client.group_number, client.client_name, patient.first_name,
       patient.last_name, patient.dob, patient.ssn, trans.claim_number,
       trans.trans_id, trans.invoice_id, drug.name as drug_name, trans.rx_date,
       os.check_no, os.entry_date as settle_date, os.amount
from os
join overpayment using(puc_id)
join trans using(trans_id)
join client on trans.group_number = client.group_number
join drug using(drug_id)
join spat on trans.patient_id = spat.patient_id
join patient on trans.patient_id = patient.patient_id
order by client.group_number, patient.last_name, patient.first_name, trans.trans_id;
    """

application = Report().wsgi()

