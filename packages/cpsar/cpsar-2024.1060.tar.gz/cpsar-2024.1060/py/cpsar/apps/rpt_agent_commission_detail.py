import cpsar.report
import cpsar.runtime as R
import cpsar.sales
import kcontrol

class Report(cpsar.report.WSGIReport):
    label = 'Agent Commission Detail'

    query_css = """
        TD { font-size: 11pt; }
    """
    def form_params(self):
        self.params = [
            ('Group Number', cpsar.sales.ClientListBox('group_number')),
            ('Report Code', kcontrol.TextBox('report_code')),
            ('Start Date', kcontrol.DatePicker('start_date', required=True)), 
            ('End Date',   kcontrol.DatePicker('end_date', required=True)),
            ('Account', cpsar.sales.DistributionAccountListBox('account'))]

    def record_fields(self):
        return ['trans #', 'group number', 'pharmacy_name',
                'first_name', 'last_name', 'drug', 'type', 'rx_date', 'trans_total', 'distribution date', 'awp', 'mac',
                'savings', 'commission']

    def records(self):
        cursor = R.db.cursor()
        if not self.req.get('account'):
            return

        cursor.execute("""
            SELECT trans.trans_id,
                   trans.group_number,
                   pharmacy.name as pharmacy_name,
                   patient.first_name,
                   patient.last_name,
                   drug.name,
                   trans.tx_type,
                   trans.rx_date,
                   trans.total as trans_total,
                   distribution.distribution_date::date,
                   trans.awp as awp,
                   history.cost_allowed + history.sales_tax + history.dispense_fee
                    - history.eho_network_copay as mac,
                   trans.savings as savings,
                   distribution.amount
            FROM distribution
            JOIN trans ON
                trans.trans_id = distribution.trans_id AND
                trans.group_number %(gn_frag)s
            JOIN patient ON
                trans.patient_id = patient.patient_id
            JOIN history ON
                trans.history_id = history.history_id
            JOIN pharmacy ON
                trans.pharmacy_id = pharmacy.pharmacy_id
            JOIN drug ON
                trans.drug_id = drug.drug_id
            WHERE distribution.distribution_date::date BETWEEN
                %(start_date)s AND %(end_date)s AND
                distribution.distribution_account = %(account)s AND
                  NOT (trans.group_number = '56600' AND 
                       (trans.group_auth BETWEEN 86579 AND 92263 OR
                        trans.group_auth BETWEEN 94623 AND 95828))

            ORDER BY trans.trans_id
            """ % self.query_args())

        for rec in cursor:
            yield rec

        cursor.execute("""
            SELECT 'TOTAL',
                   '',
                   '',
                   '',
                   '',
                   '',
                   '',
                   '',
                   '',
                   '',
                   SUM(trans.total),
                   '',
                   SUM(trans.savings),
                   SUM(distribution.amount)
            FROM distribution 
            JOIN trans ON
                trans.trans_id = distribution.trans_id AND
                trans.group_number %(gn_frag)s
            JOIN drug ON
                trans.drug_id = drug.drug_id
            WHERE distribution.distribution_date BETWEEN
                %(start_date)s AND %(end_date)s AND
                distribution.distribution_account = %(account)s AND
                  NOT (trans.group_number = '56600' AND 
                       (group_auth BETWEEN 86579 AND 92263 OR
                        group_auth BETWEEN 94623 AND 95828))
            """ % self.query_args())
        yield cursor.fetchone()

application = Report().wsgi()
