import datetime
import os

import kcontrol

import cpsar.pg
import cpsar.report
import cpsar.runtime as R
import cpsar.sales

from cpsar.controls import GroupNumberListBox
from cpsar.controls import PharmacyFilterListBox

class Report(cpsar.report.WSGIReport):
    label = 'A/R Summary Aging'
    def form_params(self):
        self.params = [
            ('Group Number', GroupNumberListBox('group_number', blankOption=True)),
            ('Report Code', kcontrol.TextBox('report_code')),
            ('Pharmacy Filter', PharmacyFilterListBox()),
            ('As Of', kcontrol.DatePicker('as_of',
                        required=True,
                        defaultValue=datetime.datetime.now())),
            ('Payment Date', kcontrol.DatePicker('payment_date'))
        ]

    csv_exportable = True

    def query_args(self):
        args = super(Report, self).query_args()

        if not args.get('payment_date'):
            args['payment_date'] = args['as_of']

        args['date_frag'] = ' <= %(as_of)s' % args
        if self.req.get('pharmacy_filter') == "C":
            f = "pharmacy.nabp = '%s' AND trans.compound_code = '2'"
            args['pharmacy_nabp_frag'] = f % R.CPS_NABP_NBR
        elif self.req.get('pharmacy_filter') == "M":
            f = "pharmacy.nabp = '%s' AND trans.compound_code = '1'"
            args['pharmacy_nabp_frag'] = f % R.CPS_NABP_NBR
        elif self.req.get('pharmacy_filter') == "R":
            f = "pharmacy.nabp <> '%s'" 
            args['pharmacy_nabp_frag'] = f % R.CPS_NABP_NBR
        else:
            args['pharmacy_nabp_frag'] = "TRUE"
        return args

    def client_name(self):
        if not self.req.get('group_number') and \
           not self.req.get('report_code'):
            return 'All'
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT client.client_name, client.group_number
            FROM client
            JOIN requested_group USING(group_number)
            ORDER BY client.client_name
        """)
        return ", ".join("%s - %s" % c for c in cursor)

    def record_fields(self):
        return ['Client', 'Current 0-15', '16-30', '31-60',
                '61-90', '91+', 'TOTAL']

    def records(self):
        # Get the data
        args = self.query_args()
        cursor = R.db.dict_cursor()
        self._create_requested_group_table()

        # Build a temporary table of transactions as they existed
        # as of the given date

        sql = """
        CREATE TEMPORARY TABLE trans_as_of AS
            SELECT client.client_name,
                   trans.trans_id,
                   trans.group_number,
                   trans.create_date,
                   trans.total,
                   trans.total + COALESCE(debits.amount, 0)
                               - COALESCE(payments.amount, 0) 
                               - COALESCE(adjudications.amount, 0)
                               - COALESCE(writeoffs.amount, 0) 
                               - COALESCE(rebate_credits.amount, 0)
                               - COALESCE(rebill_credits.amount, 0) AS balance,
                   %(as_of)s::date - trans.create_date::date AS age,
                   CASE
                    WHEN
                        %(as_of)s::date - trans.create_date::date
                        BETWEEN 0 and 15 THEN 0
                    WHEN
                        %(as_of)s::date - trans.create_date::date
                        BETWEEN 16 and 30 THEN 15
                    WHEN 
                        %(as_of)s::date - trans.create_date::date
                        BETWEEN 31 AND 60 THEN 30
                    WHEN
                        %(as_of)s::date - trans.create_date::date
                        BETWEEN 61 AND 90 THEN 60
                    WHEN
                        %(as_of)s::date - trans.create_date::date
                        > 90 THEN 90
                   END AS age_bucket
            FROM trans
            JOIN patient ON
                trans.patient_id = patient.patient_id
            JOIN client ON
                trans.group_number = client.group_number
            JOIN pharmacy USING(pharmacy_id)
            JOIN requested_group ON client.group_number = requested_group.group_number
            LEFT JOIN (
                SELECT trans_id, SUM(amount) AS amount
                FROM trans_payment
                WHERE entry_date::date <= %(payment_date)s
                GROUP BY trans_id
            ) AS payments ON trans.trans_id = payments.trans_id
            LEFT JOIN (
                SELECT trans_id, SUM(amount) AS amount
                FROM trans_adjudication
                WHERE entry_date::date <= %(payment_date)s
                  AND (void_date IS NULL OR void_date > %(as_of)s)
                GROUP BY trans_id
            ) AS adjudications ON trans.trans_id = adjudications.trans_id
            LEFT JOIN (
                SELECT trans_id, SUM(amount) AS amount
                FROM trans_writeoff
                WHERE entry_date::date <= %(payment_date)s
                  AND (void_date IS NULL OR void_date > %(as_of)s)
                GROUP BY trans_id
            ) AS writeoffs ON trans.trans_id = writeoffs.trans_id
            LEFT JOIN (
                SELECT trans_id, SUM(amount) AS amount
                FROM rebill_credit
                WHERE entry_date::date <= %(payment_date)s
                GROUP BY trans_id
            ) AS rebill_credits ON trans.trans_id = rebill_credits.trans_id
            LEFT JOIN (
                SELECT trans_id, SUM(amount) AS amount
                FROM rebate_credit 
                WHERE entry_date::date <= %(payment_date)s
                  AND (void_date IS NULL OR void_date > %(as_of)s)
                GROUP BY trans_id
            ) AS rebate_credits ON trans.trans_id = rebate_credits.trans_id
            LEFT JOIN (
                SELECT trans_id, SUM(amount) AS amount
                FROM trans_debit
                WHERE entry_date::date <= %(payment_date)s
                GROUP BY trans_id
            ) AS debits ON trans.trans_id = debits.trans_id
            WHERE
               %(pharmacy_nabp_frag)s AND
               trans.group_number %(gn_frag)s AND
               trans.create_date::date %(date_frag)s AND
               trans.total + COALESCE(debits.amount, 0)
                           - COALESCE(payments.amount, 0) 
                           - COALESCE(adjudications.amount, 0)
                           - COALESCE(writeoffs.amount, 0)
                           - COALESCE(rebate_credits.amount, 0)
                           - COALESCE(rebill_credits.amount, 0) <> 0
        """ % args

        cursor.execute(sql)

        cursor.execute("""
            SELECT group_number || ' ' || client_name, age_bucket, SUM(balance)
            FROM trans_as_of
            GROUP BY group_number, client_name, age_bucket
            ORDER BY group_number, age_bucket
        """)

        # Do our own crosstab
        records = {}
        for client, age, balance in cursor:
            records.setdefault(client, {'total': 0})
            records[client][age] = balance
            records[client]['total'] += balance
        keys = list(records.keys())
        keys.sort()
        cols = [0, 15, 30, 60, 90, 'total']
        def build_row(k, rec):
            return [k] + [rec.get(c, 0) for c in cols]
        records = [build_row(k, records[k]) for k in keys]

        gtotals = ['Total', 0, 0, 0, 0, 0, 0]

        for rec in records:
            yield rec
            for i in range(1, 7):
                gtotals[i] += rec[i]
        yield gtotals

    def _create_requested_group_table(self):
        args = self.query_args()
        cursor = R.db.dict_cursor()
        if args['report_code']:
            cursor.execute("""
              CREATE TEMP TABLE requested_group AS
              SELECT group_number
              FROM client_report_code
              WHERE report_code=%s
              """ % args['report_code'])
        elif args['gn_frag']:
            cursor.execute("""
              CREATE TEMP TABLE requested_group AS
              SELECT group_number
              FROM client
              WHERE group_number %s
              """ % args['gn_frag'])
        else:
            cursor.execute("""
              CREATE TEMP TABLE requested_group AS
              SELECT group_number
              FROM client""")

application = Report().wsgi()
