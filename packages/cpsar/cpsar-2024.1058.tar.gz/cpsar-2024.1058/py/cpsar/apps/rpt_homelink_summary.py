import cpsar.pg
import cpsar.report
import cpsar.runtime as R
import kcontrol

class Report(cpsar.report.WSGIReport):
    label = 'Homelink Commission Summary'

    query_css = """
        TD { font-size: 11pt; }
    """
    def form_params(self):
        self.params = [
            ('Start Date', kcontrol.DatePicker('start_date')), 
            ('End Date',   kcontrol.DatePicker('end_date'))
        ]

    @property
    def start_date(self):
        return self.req.get('start_date')

    @property
    def end_date(self):
        return self.req.get('end_date')

    def record_fields(self):
        return ['group number', 'client', 
                'type',  'script count', 'commission']

    def records(self):
        cursor = R.db.cursor()

        ## Create a commission table that does not include transactions
        ## that have a net 0 effect over the given time frame. This takes
        ## care of reversals.
        sql = """
         CREATE TEMPORARY TABLE d_distribution AS
          SELECT trans_id, amount
          FROM distribution WHERE
            distribution.distribution_date::date BETWEEN
                %(start_date)s AND %(end_date)s AND
                distribution_account = 'homelink' AND
                  trans_id IN (
                    SELECT trans_id
                    FROM distribution
                    WHERE distribution.distribution_date::date BETWEEN
                        %(start_date)s AND %(end_date)s AND
                        distribution_account = 'homelink'
                    GROUP BY trans_id
                    HAVING SUM(amount) != 0
            )
        """ % self.query_args()
        cursor.execute(sql)

        cursor.execute("""
            SELECT trans.group_number,
                   client.client_name,
                   drug.brand,
                   COUNT(DISTINCT d_distribution.trans_id),
                   SUM(d_distribution.amount)
            FROM d_distribution
            JOIN trans ON d_distribution.trans_id = trans.trans_id
            JOIN client ON trans.group_number = client.group_number
            JOIN drug ON trans.drug_id = drug.drug_id
            GROUP BY trans.group_number, client.client_name, drug.brand
            ORDER BY trans.group_number, drug.brand
            """)


        for rec in cursor:
            yield rec

        cursor.execute("""
            SELECT 'TOTAL',
                   '',
                   '', 
                   COUNT(DISTINCT trans_id),
                   SUM(d_distribution.amount)
            FROM d_distribution 
            """ % self.query_args())
        yield cursor.fetchone()

application = Report().wsgi()
