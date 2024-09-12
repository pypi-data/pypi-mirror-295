import cpsar.report
import kcontrol

class Report(cpsar.report.WSGIReport):
    label = 'Sales Totals'

    def form_params(self):
        self.params = [
            ('Start Date', kcontrol.DatePicker('start_date')), 
            ('End Date',   kcontrol.DatePicker('end_date'))
        ]

    sql = """
    SELECT client.group_number, 
           t.total_scripts,
           t.total_sales,
           a.total_adjudications,
           w.total_writeoffs,
           t.total_sales - a.total_adjudications
                         - w.total_writeoffs AS balance,
           c.total_commission,
           p.pharmacies_paid,
           cps.net_income,
           cpharm.cps_total,
           u.undistributed
    FROM client
    FULL OUTER JOIN (
        SELECT
            trans.group_number,
            COUNT(trans.*) as total_scripts,
            SUM(trans.total) as total_sales
        FROM trans
        WHERE create_date BETWEEN %(start_date)s AND %(end_date)s
        GROUP BY trans.group_number
    ) AS t ON
        client.group_number = t.group_number
    FULL OUTER JOIN (
        SELECT
            trans.group_number,
            SUM(trans_adjudication.amount) as total_adjudications
        FROM trans
        JOIN trans_adjudication ON 
            trans.trans_id = trans_adjudication.trans_id
        WHERE trans_adjudication.entry_date BETWEEN 
                %(start_date)s AND %(end_date)s
          AND (trans_adjudication.void_date IS NULL OR
               trans_adjudication.void_date > %(end_date)s)
        GROUP BY trans.group_number
    ) AS a ON
        client.group_number = a.group_number
    FULL OUTER JOIN (
        SELECT
            trans.group_number,
            SUM(trans_writeoff.amount) as total_writeoffs
        FROM trans
        JOIN trans_writeoff ON 
            trans.trans_id = trans_writeoff.trans_id
        WHERE trans_writeoff.entry_date BETWEEN 
          %(start_date)s AND %(end_date)s
          AND (void_date IS NULL OR void_date > %(end_date)s)
        GROUP BY trans.group_number
    ) AS w ON
        client.group_number = w.group_number
    FULL OUTER JOIN (
        SELECT
            trans.group_number,
            SUM(distribution.amount) as total_commission
        FROM trans
        JOIN distribution ON
            trans.trans_id = distribution.trans_id AND
            distribution.distribution_date
                BETWEEN %(start_date)s AND %(end_date)s AND
                distribution.distribution_account NOT IN
                    ('cps', 'pharmacy', 'eho')
        GROUP BY trans.group_number
    ) AS c ON
        client.group_number = c.group_number
    FULL OUTER JOIN (
        SELECT
            trans.group_number,
            SUM(distribution.amount) as pharmacies_paid 
        FROM trans
        JOIN distribution ON
            trans.trans_id = distribution.trans_id AND
            distribution.distribution_date
                BETWEEN %(start_date)s AND %(end_date)s AND
                distribution.distribution_account IN
                    ('pharmacy', 'eho')
        GROUP BY trans.group_number
    ) AS p ON
        client.group_number = p.group_number
    FULL OUTER JOIN (
        SELECT
            trans.group_number,
            SUM(distribution.amount) as net_income
        FROM trans
        JOIN distribution ON
            trans.trans_id = distribution.trans_id AND
            distribution.distribution_date
                BETWEEN %(start_date)s AND %(end_date)s AND
                distribution.distribution_account = 'cps'
        GROUP BY trans.group_number
    ) AS cps ON
        client.group_number = cps.group_number
    FULL OUTER JOIN (
        SELECT trans.group_number,
               SUM(trans.total) as cps_total
        FROM trans
        JOIN pharmacy ON
            trans.pharmacy_id = pharmacy.pharmacy_id AND
            pharmacy.nabp = '0123682' AND
            trans.create_date BETWEEN %(start_date)s AND %(end_date)s
        GROUP BY trans.group_number
    ) AS cpharm ON
        client.group_number = cpharm.group_number
    FULL OUTER JOIN (
        SELECT trans.group_number,
               COUNT(trans.trans_id) as undistributed
        FROM trans
        WHERE
            trans.distributed_amount <> trans.paid_amount AND
            trans.paid_date BETWEEN %(start_date)s AND %(end_date)s
        GROUP BY trans.group_number
    ) AS u ON
        client.group_number = u.group_number 
    UNION ALL
    SELECT NULL, 
           (SELECT
                COUNT(trans.*) as total_scripts
            FROM trans
            WHERE create_date BETWEEN
                %(start_date)s AND %(end_date)s
           ),
           (SELECT
               SUM(trans.total) as total_scripts
            FROM trans
            WHERE create_date BETWEEN
                %(start_date)s AND %(end_date)s
           ),
           (SELECT
                SUM(trans_adjudication.amount) as total_adjudications
            FROM trans_adjudication 
            WHERE entry_date BETWEEN
                %(start_date)s AND %(end_date)s
              AND (trans_adjudication.void_date IS NULL OR
                   trans_adjudication.void_date > %(end_date)s)
           ),
           (SELECT
                SUM(amount) as total_writeoffs
            FROM trans_writeoff 
            WHERE entry_date BETWEEN %(start_date)s AND %(end_date)s
              AND (void_date IS NULL OR void_date > %(end_date)s)
           ),
           NULL,
           (SELECT
                SUM(distribution.amount) as total_commission
            FROM distribution
            WHERE
                distribution_date BETWEEN
                    %(start_date)s AND %(end_date)s AND
                distribution_account NOT IN
                    ('cps', 'pharmacy', 'eho')
           ),
           (SELECT
                SUM(distribution.amount) as total_commission
            FROM distribution
            WHERE
                distribution_date BETWEEN
                    %(start_date)s AND %(end_date)s AND
                distribution_account IN
                    ('pharmacy', 'eho')
           ),
           (SELECT
                SUM(distribution.amount) as total_commission
            FROM distribution
            WHERE
                distribution_date BETWEEN
                    %(start_date)s AND %(end_date)s AND
                distribution_account = 'cps'
           ),
           (
        SELECT SUM(trans.total) as cps_total
        FROM trans
        JOIN pharmacy ON
            trans.pharmacy_id = pharmacy.pharmacy_id AND
            pharmacy.nabp = '0123682' AND
            trans.paid_date BETWEEN %(start_date)s AND %(end_date)s
            ),
        NULL

    ORDER BY group_number ASC 
    """

application = Report().wsgi()
