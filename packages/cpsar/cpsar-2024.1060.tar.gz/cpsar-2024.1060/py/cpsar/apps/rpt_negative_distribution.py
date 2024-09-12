import cpsar.report
import kcontrol

class Report(cpsar.report.WSGIReport):
    label = 'Negative CPS Distributions'

    def form_params(self):
        self.params = [
            ('Start Date Processed', kcontrol.DatePicker('start_date')), 
            ('End Date Processed',   kcontrol.DatePicker('end_date')),
            ('Amount', kcontrol.TextBox('amount', value='10.00'))
        ]

    sql = """
    SELECT trans.group_number, 
           trans.drug_ndc_number,
           trans.quantity,
           pharmacy_nabp,
           drug.name,
           trans.total,
           patient.first_name,
           patient.last_name,
           trans.trans_id,
           trans.rx_number,
           trans.refill_number,
           trans.rx_date,
           trans.invoice_id,
           distribution.amount AS cps_distribution
    FROM distribution
    JOIN trans USING(trans_id)
    JOIN drug USING(drug_id)
    JOIN pharmacy USING(pharmacy_id)
    JOIN patient USING(patient_id)
    JOIN history USING(history_id)
    WHERE  history.date_processed BETWEEN %(start_date)s AND %(end_date)s
      AND distribution.distribution_account = 'cps'
      AND distribution.amount < 0
      AND ABS(distribution.amount) >= %(amount)s

      ORDER BY trans.trans_id
    """

application = Report().wsgi()
