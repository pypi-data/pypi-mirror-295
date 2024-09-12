import csv
import sys

import cpsar.pg
import cpsar.runtime as R
import cpsar.report
import cpsar.wsgirun as W
import kcontrol

class Report(cpsar.report.WSGIReport):
    label = 'Companion Comission Report'
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
            'scsaf_paid',
            'eho',
            'cps',
            'comp',
            'pharmacy',
            'net',
            'count']

    def records(self):
        args = self.query_args()
        cursor = R.db.cursor()

        cursor.execute("""
            CREATE TEMP TABLE groups_with_comp_distributions AS (
                SELECT DISTINCT group_number
                FROM distribution_rule
                WHERE distribution_account = 'comp'
            )
        """)

        cursor.execute("""
            CREATE TEMPORARY TABLE ctrans AS
            SELECT trans.trans_id, 
                   distribution_date, 
                   distribution_account,
                   distribution.amount
            FROM trans
            JOIN distribution ON trans.trans_id=distribution.trans_id
            JOIN groups_with_comp_distributions ON trans.group_number =
                 groups_With_comp_distributions.group_number
            WHERE NOT (group_auth BETWEEN 86579 AND 92263 OR
                       group_auth BETWEEN 94623 AND 95828) AND
                  distribution_date BETWEEN %(start_date)s AND %(end_date)s
            """ % args)

        cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM ctrans")
        args['scsaf_paid'] = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM ctrans
            WHERE distribution_account = 'eho'
            """)
        args['eho'] = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM ctrans
            WHERE distribution_account = 'cps'
            """)
        args['cps'] = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM ctrans
            WHERE distribution_account = 'comp'
            """)
        args['comp'] = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM ctrans
            WHERE distribution_account = 'pharmacy'
            """)
        args['pharmacy'] = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COALESCE(COUNT(DISTINCT trans_id), 0)
            FROM ctrans
            """)
        args['count'] = cursor.fetchone()[0]

        args['net'] = args['scsaf_paid'] - args['eho'] - args['cps'] - \
                      args['comp'] - args['pharmacy']

        cursor.execute("DROP TABLE ctrans")
        return args

    def csv(self):
        self.res.content_type = 'application/csv'
        self.res.headers["Content-Disposition"] = "attachment; filename=companion_commission.csv"
        writer = csv.writer(self.res)
        preamble = self.preamble()
        if preamble is not None:
            writer.writerow(preamble)
        writer.writerow(self.record_fields())
        r = self.records()
        writer.writerow([r[f] for f in self.record_fields()])

    def _mako_record(self):
        tmpl = 'rpt_companion_commission.tmpl'
        mako = W.MakoRecord(self.req, self.res, tmpl_name=tmpl)
        mako.update({
            'q': self,
            'sql' : self.expanded_sql})

        rec = self.records()
        for k in self.currency_keys:
            v = rec[k]
            mako['%s_fmt' % k] = cpsar.pg.format_currency(v)
        mako.update(rec)
        return mako

    sql_tmpl_file = 'rpt_companion_commission.tmpl'

application = Report().wsgi()
