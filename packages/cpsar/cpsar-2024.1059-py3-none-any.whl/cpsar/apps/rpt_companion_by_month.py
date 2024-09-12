import csv

import cpsar.runtime as R
import cpsar.report
import kcontrol

class Report(cpsar.report.WSGIReport):
    label = 'Companion Comission Summary by Month'
    params = [
        ('Start Date', kcontrol.DatePicker('start_date')), 
        ('End Date',   kcontrol.DatePicker('end_date'))
    ]

    currency_keys = [
        'scsaf_paid',
        'eho',
        'cps',
        'comp',
        'net',
        'pharmacy'
    ]

    def record_fields(self):
        return [
            'Date',
            'Scripts Balanced',
            'Total',
            'CPS Fee',
            'Companion',
            'Pharmacy Remittance'
        ]

    query_css = """
        .data2 {
            text-align: right;
        }
        .data3 {
            text-align: right;
        }
        .data4 {
            text-align: right;
        }
        .data5 {
            text-align: right;
        }
        .data6 {
            text-align: right;
        }
    """

    def records(self):
        args = self.query_args()
        cursor = R.db.cursor()
        cursor.execute("""
CREATE TABLE dist_by_month AS
SELECT x.month,
       x.month_num,
       x.account,
       x.amount_sum,
       cnt.trans_count
FROM (
  SELECT to_char(distribution.distribution_date, 'YYYY MON') AS month,
         to_char(distribution.distribution_date, 'YYYY MM') as month_num,
         distribution.distribution_account AS account,
         SUM(distribution.amount) AS amount_sum
  FROM distribution
  JOIN trans ON distribution.trans_id = trans.trans_id AND
       trans.group_number = '56600' AND 
       NOT (group_auth BETWEEN 86579 AND 92263 OR
            group_auth BETWEEN 94623 AND 95828)
  WHERE distribution.distribution_date BETWEEN %(start_date)s AND %(end_date)s
  GROUP BY month, month_num, distribution_account
) AS x
JOIN (
  SELECT to_char(distribution_date, 'YYYY MM') AS month_num,
           COUNT(DISTINCT distribution.trans_id) AS trans_count
  FROM distribution
  JOIN trans ON distribution.trans_id = trans.trans_id AND
         trans.group_number = '56600' AND 
       NOT (group_auth BETWEEN 86579 AND 92263 OR
            group_auth BETWEEN 94623 AND 95828)
  WHERE distribution_date BETWEEN %(start_date)s AND %(end_date)s
  GROUP BY month_num
) AS cnt ON cnt.month_num = x.month_num
        """ % self.query_args())

        cursor.execute("""
            SELECT dist.month, 
                   dist.trans_count AS scripts_balanced,
                   format_currency(dist.month_total),
                   format_currency(cps.total),
                   format_currency(comp.total),
                   format_currency(pharm.total + eho.total)
            FROM (
                SELECT month,
                       month_num, 
                       trans_count, 
                       SUM(amount_sum) AS month_total
                FROM dist_by_month
                GROUP BY month, month_num, trans_count
            ) AS dist

            LEFT JOIN (
                SELECT month_num, SUM(amount_sum) AS total
                FROM dist_by_month
                WHERE account = 'cps'
                GROUP BY month_num
            ) AS cps ON dist.month_num = cps.month_num

            LEFT JOIN (
                SELECT month_num, SUM(amount_sum) AS total
                FROM dist_by_month
                WHERE account = 'comp'
                GROUP BY month_num
            ) AS comp ON dist.month_num = comp.month_num

            LEFT JOIN (
                SELECT month_num, SUM(amount_sum) AS total
                FROM dist_by_month
                WHERE account = 'pharmacy'
                GROUP BY month_num
            ) AS pharm ON dist.month_num = pharm.month_num

            LEFT JOIN (
                SELECT month_num, SUM(amount_sum) AS total
                FROM dist_by_month
                WHERE account = 'eho'
                GROUP BY month_num
            ) AS eho ON dist.month_num = eho.month_num

            ORDER BY dist.month_num""" % args)

        for rec in cursor:
            yield rec

        cursor.execute("""
            select 'TOTAL', 
                   (SUM(trans_count) / 4)::int,
                   format_currency(SUM(amount_sum))
            FROM dist_by_month
            """)

        rec = list(cursor.fetchone())
        cursor.execute("""
            SELECT format_currency(SUM(amount_sum))
            FROM dist_by_month
            WHERE account = 'cps'
            """)
        rec.extend(list(cursor.fetchone()))

        cursor.execute("""
            SELECT format_currency(SUM(amount_sum))
            FROM dist_by_month
            WHERE account = 'comp'
            """)
        rec.extend(list(cursor.fetchone()))

        cursor.execute("""
            SELECT format_currency(SUM(amount_sum))
            FROM dist_by_month
            WHERE account IN ('pharmacy', 'eho')
            """)
        rec.extend(list(cursor.fetchone()))

        yield rec

    def csv(self):
        self.res.content_type = 'application/csv'
        h = self.res.headers
        h.add("Expires", "0")
        h.add("Content-Transfer-Encoding", "binary")
        h.add("Pragma", "public")
        cod = "attachment; filename=companion_commission.csv"
        h.add("Content-Disposition", cod)

        writer = csv.writer(self.res)
        preamble = self.preamble()
        if preamble is not None:
            writer.writerow(preamble)
        writer.writerow(self.record_fields())
        for r in self.records():
            writer.writerow(r)

application = Report().wsgi()
