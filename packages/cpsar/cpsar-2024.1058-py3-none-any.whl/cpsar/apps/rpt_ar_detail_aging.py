""" Master Aging Report for Blue Diamond. The report reflects the amount in A/R
that is posted to CPS's transactions since Gerald got in the game.

This report contains lines of the following types:

CL: A transaction billed by CPS to it's client. Only shows if the tranasction
    has not been fulled paid. Positively affects the balance.
PY: A payment applied to a transaction from a check, credit card, direct
    deposit or an outstanding overpayment credit. Negatively affects the balance.
AD: a reversal credit applied to a transaction. Negatively affects the balance.
WO: A write off of an amount from a transaction. Negatively affects the balance.
RB: Rebate credit
RC: For transactions that are rebilled, the rebill credit on the original
    transaction. Negatively affects the balance.
DB: A debit of an amount to a transaction.
RB: Rebate credit applied to trans

If the "Show Unapplied Cash" check box is checked, the following line items are
also included:

RV: An outstanding reversal credit that has not been applied
RB: An outstanding rebill credit balance
CK/DD/CC: An outstanding unapplied cash balance
"""
import csv
import datetime
from decimal import Decimal
import sys

from cpsar.controls import GroupNumberListBox
from cpsar.controls import PharmacyFilterListBox
import cpsar.pg
import cpsar.report
import cpsar.runtime as R
import kcontrol

import cpsar.util as U

class Report(cpsar.report.WSGIReport):
    label = 'A/R Detail Aging'
    sql_tmpl_file = 'rpt_ar_detail_aging.tmpl'
    csv_exportable = True

    form_resources = """
    <script src='/js/jquery-1.4.2.min.js'></script>
    <script src='/js/rpt_aging_detail.js'></script>
    <script src='/repo/js/kcontrol/calendar.js'></script>
    <script src='/repo/js/kcontrol/lang/calendar-en.js'></script>
    <script src='/repo/js/kcontrol/calendar-setup.js'></script>
    <link type='text/css' rel='stylesheet'
          href='/repo/css/kcontrol/calendar.css' />"""

    def form_params(self):
        self.params = [
            ('Group Number', GroupNumberListBox('group_number', blankOption=True)),
            ('Report Code', kcontrol.TextBox('report_code')),
            ('Pharmacy Filter', PharmacyFilterListBox()),
            ('Adjuster', kcontrol.Dropdown('adjuster_email')),
            ('As Of', kcontrol.DatePicker('as_of',
                        required=True,
                        defaultValue=datetime.datetime.now())),
            ('Current', kcontrol.Number('current', defaultValue=15)),
            ('First', kcontrol.Number('first', defaultValue=30)),
            ('Second', kcontrol.Number('second', defaultValue=60)),
            ('Third', kcontrol.Number('third', defaultValue=90)),
            ('Show Unapplied Cash?', kcontrol.CheckBox('show_uc', default=True)),
            ('Show Age?', kcontrol.CheckBox('show_age'))
        ]

    @property
    def show_age(self):
        return self.req.get('show_age')

    def query_args(self):
        args = super(Report, self).query_args()
        args['date_frag'] = ' <= %(as_of)s' % args

        if args['adjuster_email']:
            args['adj_frag'] = "trans.adjuster1_email = %s" % \
                                    args['adjuster_email']
        else:
            args['adj_frag'] = 'TRUE'

        if self.req.get('pharmacy_filter') == "C":
            f = "pharmacy.nabp = '%s' AND trans.compound_code = '2'" % R.CPS_NABP_NBR
            args['pharmacy_nabp_frag'] = f
        elif self.req.get('pharmacy_filter') == "M":
            f = "pharmacy.nabp = '%s' AND trans.compound_code = '1'" % R.CPS_NABP_NBR
            args['pharmacy_nabp_frag'] = f
        elif self.req.get('pharmacy_filter') == "R":
            args['pharmacy_nabp_frag'] = "pharmacy.nabp <> '%s'" % R.CPS_NABP_NBR
        else:
            args['pharmacy_nabp_frag'] = "TRUE"

        return args

    @property
    def showing_mailorder(self):
        return self.req.get('pharmacy_filter') != 'R'

    @property
    def showing_retail(self):
        return self.req.get('pharmacy_filter') != 'M'

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

    def adjuster_name(self):
        args = self.query_args()
        if not args['adjuster_email']:
            return
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT first_name || ' ' || last_name || ' - ' || email
            FROM user_info
            JOIN requested_group USING(group_number)
            WHERE email=%(adjuster_email)s
            """ % args)
        return cursor.fetchone()[0]

    def records(self):
        # Get the data
        args = self.query_args()
        cursor = R.db.dict_cursor()

        # Build constraint table
        self._create_requested_group_table()

        # Build a temporary table of transactions as they existed
        # as of the given date
        # raise ValueError(self.query_args())
        self._create_selected_trans_table()
        self._create_debit_as_of_table()
        self._create_payment_as_of_table()
        self._create_adjudication_as_of_table()
        self._create_writeoff_as_of_table()
        self._create_trans_as_of_table()

        sql = """
 SELECT trans_as_of.group_number,
        rx_date,
        payer_code,
        trans_as_of.patient_id, 
        first_name,
        last_name,
        trans_as_of.trans_id,
        'CL' AS doc_type, 
        invoice_id || '-' || line_no || ' CLM #:' || trans_as_of.claim_number
       AS doc_no, 
        trans_as_of.create_date::date AS doc_date,
        %(as_of)s::date - trans_as_of.create_date::date AS age,
        '' AS applied_type,
        to_char(trans_as_of.create_date + '15 days', 'MM/DD/YYYY')
            || ' ' ||
            CASE WHEN claim.status IS NULL THEN 'OPEN' ELSE
                'CLOSED' END 
            AS applied_no,
        trans_as_of.total AS amount
 FROM trans_as_of
 LEFT JOIN claim ON
    trans_as_of.patient_id = claim.patient_id AND
    trans_as_of.doi = claim.doi
 UNION ALL
 SELECT trans_as_of.group_number,
        rx_date,
        payer_code,
        patient_id,
        first_name,
        last_name,
        trans_as_of.trans_id,
        '' AS doc_type,
        '' AS doc_no,
        entry_date::date AS doc_date,
        %(as_of)s::date - trans_as_of.create_date::date AS age,
        'PY' AS applied_type,
        payment_type.type_name
          || COALESCE(': ' || trans_payment.ref_no, '') AS applied_no,
        -trans_payment.amount
 FROM trans_payment
 JOIN trans_as_of ON trans_as_of.trans_id = trans_payment.trans_id
 JOIN payment_type USING(ptype_id)
 WHERE trans_payment.entry_date::date %(date_frag)s
 UNION ALL
 SELECT trans_as_of.group_number,
        rx_date,
        payer_code,
        patient_id,
        first_name,
        last_name,
        trans_as_of.trans_id,
        '' AS doc_type,
        '' AS doc_no,
        entry_date::date AS doc_date,
        %(as_of)s::date - trans_as_of.create_date::date AS age,
        'AD' AS applied_type,
        adjudication_id::varchar AS applied_no,
        -trans_adjudication.amount
 FROM trans_adjudication
 JOIN trans_as_of USING(trans_id)
 WHERE trans_adjudication.entry_date %(date_frag)s AND
    (void_date IS NULL OR void_date > %(as_of)s)
 UNION ALL
 SELECT trans_as_of.group_number,
        rx_date,
        payer_code,
        patient_id,
        first_name,
        last_name,
        trans_as_of.trans_id,
        '' AS doc_type,
        '' AS doc_no,
        entry_date::date AS doc_date,
        %(as_of)s::date - trans_as_of.create_date::date AS age,
        'RB' AS applied_type,
        rebate_credit.rebate_credit_id::varchar AS applied_no,
        -rebate_credit.amount
 FROM rebate_credit
 JOIN trans_as_of USING(trans_id)
 WHERE entry_date::date %(date_frag)s
   AND (void_date IS NULL OR void_date > %(as_of)s)

 UNION ALL
 SELECT trans_as_of.group_number,
        rx_date,
        payer_code,
        patient_id,
        first_name,
        last_name,
        trans_as_of.trans_id,
        'DB' AS doc_type,
        invoice_id || '-' || line_no || ' CLM #:' || trans_as_of.claim_number
         AS doc_no, 
        entry_date::date AS doc_date,
        %(as_of)s::date - trans_as_of.create_date::date AS age,
        '' AS applied_type,
        trans_debit.debit_id::varchar AS applied_no,
        trans_debit.amount
 FROM trans_debit
 JOIN trans_as_of USING(trans_id)
 WHERE entry_date::date %(date_frag)s
 UNION ALL
 SELECT trans_as_of.group_number,
        rx_date,
        payer_code,
        patient_id,
        first_name,
        last_name,
        trans_as_of.trans_id,
        '' AS doc_type,
        '' AS doc_no,
        entry_date::date AS doc_date,
        %(as_of)s::date - trans_as_of.create_date::date AS age,
        'WO' AS applied_type,
        trans_writeoff.writeoff_id::varchar AS applied_no,
        -trans_writeoff.amount
 FROM trans_writeoff
 JOIN trans_as_of USING(trans_id)
 WHERE entry_date::date %(date_frag)s
   AND (void_date IS NULL OR void_date > %(as_of)s)
 UNION ALL
 SELECT trans_as_of.group_number,
        rx_date,
        payer_code,
        patient_id,
        first_name,
        last_name,
        trans_as_of.trans_id,
        '' AS doc_type,
        '' AS doc_no,
        entry_date::date AS doc_date,
        %(as_of)s::date - trans_as_of.create_date::date AS age,
        'RC' AS applied_type,
        rebill_credit.rebill_credit_id::text AS applied_no,
        -rebill_credit.amount
FROM rebill_credit
JOIN trans_as_of ON trans_as_of.trans_id = rebill_credit.trans_id
WHERE entry_date::date %(date_frag)s
        """

        if self.req.get('show_uc'):
            self._create_reversal_as_of_table()
            self._create_overpayment_as_of_table()
            sql += """
             UNION ALL
             SELECT reversal_as_of.group_number,
                    trans.rx_date,
                    history.payer_code,
                    patient.patient_id,
                    patient.first_name,
                    patient.last_name,
                    trans.trans_id,
                    'RV' AS doc_type,
                    reversal_as_of.reversal_id::varchar AS doc_no,
                    reversal_as_of.entry_date::date AS doc_date,
                    %(as_of)s::date - reversal_as_of.entry_date::date AS age,
                    'CL' AS applied_type,
                    trans.invoice_id || '-' || trans.line_no AS applied_no, 
                    -reversal_as_of.balance
             FROM reversal_as_of
             JOIN trans USING(trans_id)
             JOIN patient USING(patient_id)
             JOIN history USING(history_id)
             WHERE reversal_as_of.balance != 0
             UNION ALL
             SELECT trans.group_number,
                    trans.rx_date,
                    history.payer_code,
                    patient.patient_id,
                    patient.first_name,
                    patient.last_name,
                    trans.trans_id,
                    overpayment_as_of.type_name AS doc_type,
                    overpayment_as_of.ref_no AS doc_no,
                    overpayment_as_of.entry_date::date AS doc_date,
                    %(as_of)s::date - overpayment_as_of.entry_date::date AS age,
                    'OV' AS applied_type,
                    trans.invoice_id || '-' || trans.line_no AS applied_no,
                    -overpayment_as_of.balance
             FROM overpayment_as_of
             JOIN trans USING(trans_id)
             JOIN patient USING(patient_id)
             JOIN history USING(history_id)
             WHERE overpayment_as_of.balance != 0
             UNION ALL
             SELECT trans_as_of.group_number,
                    trans_as_of.rx_date,
                    trans_as_of.payer_code,
                    patient.patient_id,
                    patient.first_name,
                    patient.last_name,
                    trans_as_of.trans_id,
                    'RB' AS doc_type,
                    rebill.rebill_id::text AS doc_no,
                    rebill.entry_date::date AS doc_date,
                    %(as_of)s::date - rebill.entry_date::date AS age,
                    '' AS applied_type,
                    '' AS applied_no,
                    -rebill.balance
            FROM rebill
            JOIN trans_as_of USING(trans_id)
            JOIN patient USING(patient_id)
            WHERE rebill.entry_date::date %(date_frag)s
                AND rebill.balance != 0
            """
        sql += "ORDER BY patient_id, trans_id, doc_date"
        cursor.execute(sql % args)
        # Build up a list of patient dicts with list of tx

        # Build up a data structure of groups which contain patients
        # which contain transactions
        groups = {}

        for rec in cursor:
            group = groups.setdefault(
                rec['group_number'],
                {'group_number': rec['group_number'],
                 'patients':  {},
                 'total': Decimal("0.0"),
                 'totals': [],
                 'percent_totals': []})
            patient = group['patients'].setdefault(rec['patient_id'], {
                'first_name': rec['first_name'],
                'last_name': rec['last_name'],
                'total_past_due': Decimal("0.0"),
                'tx': []
            })
            patient['tx'].append(dict(rec))

        # Turn groups into list. Sort by group_number
        groups = self.groups = list(groups.values())
        groups.sort(key=lambda x: x['group_number'])

        # Turn patients into list. Sort by last_name, first_name
        for group in groups:
            patients = list(group['patients'].values())
            patients.sort(key=lambda x: (x['last_name'], x['first_name']))
            group['patients'] = patients

        # Build up list of date ranges which will be used to put
        # values in particular buckets.
        as_of = U.parse_american_date(self.req.get('as_of'))
        self.as_of = as_of.strftime("%m/%d/%Y")
        def term(name):
            try:
                return int(self.req.get(name, '0'))
            except ValueError:
                return 0
        cur = term('current')
        first = term('first')
        second = term('second')
        third = term('third')

        # Create table header caption values. We don't have a header for
        # the "current" column
        self.amount_headers = []
        if first:
            self.amount_headers.append((cur+1, first))
        if second:
            self.amount_headers.append((first+1, second))
        if third:
            self.amount_headers.append((second+1, third))
        try:
            self.amount_headers.append((self.amount_headers[-1][1],))
        except IndexError:
            R.error("Enter at least two date ranges")
            return

        # Create a list of dates that limit the totals in each column
        # The list can be of dynamic length, depending on what the user
        # provides
        ranges = [cur]
        if first:
            ranges.append(first)
        if second:
            ranges.append(second)
        if third:
            ranges.append(third)
        ranges.append(999999)

        # Initialize the grand totals
        grand_totals = self.grand_totals = [Decimal('0.00')] * len(ranges)
        self.grand_total = Decimal("0.0")

        # Initialize the group totals
        for group in groups:
            group['totals'] = [Decimal('0.00')] * len(ranges)
        
        # Initialize the patient totals
        for group in groups:
            for patient in group['patients']:
                patient['totals'] = [Decimal('0.00')] * len(ranges)

        # We have to go through each transaction and decide which column the
        # amount goes in. Along the way, we will also increment the
        # corresponding patient totals, group totals and grand totals.
        # When this block is finished, each transaction will have a list of
        # amounts, one of which will have the amount based on the tx age
        # and the columns of the patient totals, group totals and grand totals
        # will be filled out.
        for group in groups:
            for patient in group['patients']:
                for tx in patient['tx']:
                    tx['amounts'] = [''] * len(ranges)

                    # find the column. This algorithm could be better
                    # written.
                    for idx, cnt in enumerate(ranges):
                        if tx['age'] <= cnt:
                            break
                    amount = tx['amount']

                    # At one time, the total past due did not include the
                    # "CURRENT" column. Now it does so there is no logic.
                    tx['amounts'][idx] = amount
                    tx['total_past_due'] = amount
                    patient['totals'][idx] += amount
                    patient['total_past_due'] += amount
                    group['totals'][idx] += amount
                    group['total'] += amount
                    grand_totals[idx] += amount
                    self.grand_total += amount

        # Calculate the group percentage totals
        for group in groups:
            # Deal with divide by zero
            total = max(group['total'], Decimal("0.0001"))
            group['percent_totals'] = [g/total for g in group['totals']]

        # Calculate the grand total percentages
        grand_total = max(self.grand_total, Decimal('.0001'))
        self.grand_percent_totals = [g/grand_total for g in grand_totals]

    def record_fields_new(self):
        return ['group_number',
            'first_name',
            'last_name',
            'trans',
            'age',
            'due date / applied no',
            'applied type',
            'doc date',
            'doc no',
            'doc type',
            'current']

    def csv_new(self):
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
        writer.writerow(self.record_fields())
        for rec in cursor:
            writer.writerow(rec)

    def csv(self):
        h = self.res.headers
        self.res.content_type = "application/csv"
        h.add("Expires", "0")
        h.add("Content-Transfer-Encoding", "binary")
        h.add("Pragma", "public")
        h.add("Content-Disposition", "attachment; filename=%s" %
                                     self.csv_file_name)
        writer = csv.writer(self.res)
        self.records()

        wr = writer.writerow

        # Write Header Line
        header = [
            'group_number',
            'first_name',
            'last_name',
            'trans',
            'age',
            'due date / applied no',
            'applied type',
            'doc date',
            'doc no',
            'doc type',
            'current']

        # Generate variable column header labels
        for i in self.amount_headers:
            if len(i) == 2:
                header.append("%s to %s" % tuple(i))
            else:
                header.append("Over %s" % i[0])
        header.append('total')
        wr(header)

        # Write Transaction Lines
        for group in self.groups:
            for p in group['patients']:
                for tx in p['tx']:
                    record = [
                        group['group_number'],
                        p['first_name'],
                        p['last_name'],
                        tx['trans_id'],
                        tx['age'],
                        tx['applied_no'],
                        tx['applied_type'],
                        tx['doc_date'],
                        tx['doc_no'],
                        tx['doc_type']
                        ]
                    for amt in tx['amounts']:
                        record.append(str(amt))
                    record.append(str(tx['total_past_due']))
                    wr(record)

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

    def _create_reversal_as_of_table(self):
        """ Create a reversal_as_of SQL temp table whose balance is based
        off of the trans_payments and settlements as they existed  the
        as_of date given by the user.
        """
        cursor = R.db.cursor()
        cursor.execute("""
          CREATE TEMP TABLE reversal_as_of AS
            SELECT reversal.reversal_id,
                   reversal.group_number,
                   reversal.group_auth,
                   reversal.entry_date::date AS entry_date,
                   reversal.trans_id,
                   reversal.total,
                   reversal.total
                   - COALESCE(trans_adjudication_as_of.amount, 0)
                   - COALESCE(reversal_settlement_as_of.amount, 0)
                   - COALESCE(group_credit_as_of.amount, 0)
                   AS balance
            FROM reversal
            JOIN selected_trans USING(trans_id)
            LEFT JOIN (
                SELECT reversal_id, SUM(amount) AS amount
                FROM trans_adjudication
                WHERE entry_date::date %(date_frag)s
                  AND (void_date IS NULL OR void_date > %(as_of)s)
                GROUP BY reversal_id
            ) AS trans_adjudication_as_of
            ON reversal.reversal_id = trans_adjudication_as_of.reversal_id
            LEFT JOIN (
                SELECT reversal_id, SUM(amount) AS amount
                FROM reversal_settlement
                WHERE entry_date::date %(date_frag)s
                  AND (void_date IS NULL OR void_date > %(as_of)s)
                GROUP BY reversal_id
            ) AS reversal_settlement_as_of
            ON reversal.reversal_id = reversal_settlement_as_of.reversal_id
            LEFT JOIN (
                SELECT source_reversal_id as reversal_id,
                       SUM(group_credit.amount) AS amount
                FROM group_credit
                WHERE entry_date::date %(date_frag)s
                GROUP BY source_reversal_id
            ) AS group_credit_as_of
            ON reversal.reversal_id = group_credit_as_of.reversal_id
            WHERE reversal.entry_date %(date_frag)s
        """ % self.query_args())

    def _create_overpayment_as_of_table(self):
        """ Create an overpayment table with a balance as of a certain date.
        Balance calculated using the overpayment total, unvoided overpayment
        settlement amounts and trans payments using the overpayment
        """
        cursor = R.db.cursor()
        cursor.execute("""
          CREATE TEMP TABLE overpayment_as_of AS
            SELECT overpayment.puc_id,
                   overpayment.username,
                   overpayment.amount,
                   payment_type.type_name,
                   overpayment.ref_no,
                   overpayment.entry_date,
                   overpayment.amount
                   - COALESCE(trans_payment_as_of.amount, 0)
                   - COALESCE(overpayment_settlement_as_of.amount, 0)
                   AS balance,
                   overpayment.trans_id,
                   overpayment.note
            FROM overpayment
            JOIN payment_type USING(ptype_id)
            JOIN selected_trans USING(trans_id)
            LEFT JOIN (
                SELECT puc_id, SUM(amount) AS amount
                FROM trans_payment
                WHERE puc_id IS NOT NULL
                  AND entry_date::date %(date_frag)s
                GROUP BY puc_id
            ) AS trans_payment_as_of
            ON overpayment.puc_id = trans_payment_as_of.puc_id
            LEFT JOIN (
                SELECT puc_id, SUM(amount) AS amount
                FROM overpayment_settlement
                WHERE entry_date %(date_frag)s
                  AND ( void_date IS NULL OR
                        NOT ( void_date %(date_frag)s ))
                GROUP BY puc_id
            ) AS overpayment_settlement_as_of
            ON overpayment.puc_id = overpayment_settlement_as_of.puc_id
            WHERE
              overpayment.entry_date::date %(date_frag)s
        """ % self.query_args())

    def _create_selected_trans_table(self):
        """ Create a table that has all of the trans id's the user has
        selected as report paramters. This table stores the results of
        that matching logic for many other queries to inner join on.
        """
        cursor = R.db.cursor()
        cursor.execute("""
        CREATE TEMP TABLE selected_trans AS
          SELECT trans.trans_id
          FROM trans
          JOIN requested_group USING(group_number)
          JOIN client USING(group_number)
          JOIN pharmacy USING(pharmacy_id)
          WHERE
              %(adj_frag)s AND
              %(pharmacy_nabp_frag)s AND
              trans.create_date::date %(date_frag)s
        """ % self.query_args())
        
    def _create_debit_as_of_table(self):
        cursor = R.db.cursor()
        cursor.execute("""
        CREATE TABLE debit_as_of AS
            SELECT trans_debit.trans_id, sum(trans_debit.amount) AS amount
            FROM trans_debit
            JOIN selected_trans USING(trans_id)
            WHERE entry_date::date %(date_frag)s
            GROUP BY trans_debit.trans_id
        """ % self.query_args())

    def _create_payment_as_of_table(self):
        cursor = R.db.cursor()
        cursor.execute("""
        CREATE TEMP TABLE payment_as_of AS
          SELECT trans_payment.trans_id, SUM(trans_payment.amount) AS amount
          FROM trans_payment
          JOIN selected_trans USING(trans_id)
          WHERE entry_date::date %(date_frag)s
          GROUP BY trans_payment.trans_id
        """ % self.query_args())

    def _create_adjudication_as_of_table(self):
        cursor = R.db.cursor()
        cursor.execute("""
        CREATE TEMP TABLE adjudication_as_of AS
          SELECT trans_adjudication.trans_id,
                 SUM(trans_adjudication.amount) AS amount
          FROM trans_adjudication
          JOIN selected_trans USING(trans_id)
          WHERE entry_date::date %(date_frag)s AND
            (void_date IS NULL OR void_date > %(as_of)s)
          GROUP BY trans_adjudication.trans_id
        """ % self.query_args())

    def _create_writeoff_as_of_table(self):
        cursor = R.db.cursor()
        cursor.execute("""
        CREATE TEMP TABLE writeoff_as_of AS
          SELECT trans_writeoff.trans_id,
                 SUM(trans_writeoff.amount) AS amount
          FROM trans_writeoff
          JOIN selected_trans USING(trans_id)
          WHERE entry_date::date %(date_frag)s
            AND (void_date IS NULL OR void_date > %(as_of)s)
          GROUP BY trans_writeoff.trans_id
        """ % self.query_args())

    def _create_trans_as_of_table(self):
        """ Create a trans_as_of SQL temp table whose total is based off of
        payments, adjudications and writeoffs as they existed on the 
        user provided as_of date.
        """
        cursor = R.db.cursor()
        cursor.execute("""
        CREATE TEMPORARY TABLE trans_as_of AS
            SELECT trans.trans_id,
                   history.payer_code,
                   trans.rx_date,
                   trans.patient_id,
                   trans.doi,
                   patient.first_name,
                   patient.last_name,
                   trans.group_number,
                   trans.invoice_id,
                   COALESCE(trans.claim_number, '') AS claim_number,
                   trans.line_no,
                   trans.create_date,
                   trans.total,
                   trans.total - COALESCE(payment_as_of.amount, 0) 
                               - COALESCE(adjudication_as_of.amount, 0)
                               - COALESCE(writeoff_as_of.amount, 0)
                               + COALESCE(debit_as_of.amount, 0) AS balance
            FROM trans
            JOIN selected_trans USING(trans_id)
            JOIN patient USING(patient_id)
            JOIN pharmacy USING(pharmacy_id)
            JOIN client ON trans.group_number = client.group_number
            JOIN history using(history_id)
            LEFT JOIN payment_as_of
                ON trans.trans_id = payment_as_of.trans_id
            LEFT JOIN adjudication_as_of
                ON trans.trans_id = adjudication_as_of.trans_id
            LEFT JOIN writeoff_as_of
                ON trans.trans_id = writeoff_as_of.trans_id
            LEFT JOIN debit_as_of
                ON trans.trans_id = debit_as_of.trans_id
            WHERE
               trans.total - COALESCE(payment_as_of.amount, 0) 
                           - COALESCE(adjudication_as_of.amount, 0)
                           - COALESCE(writeoff_as_of.amount, 0)
                           + COALESCE(debit_as_of.amount, 0) <> 0; 
        """ % self.query_args())

application = Report().wsgi()
