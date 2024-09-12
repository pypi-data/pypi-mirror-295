""" Summary Cash Receipt Report specially modified for group GROUPH
"""
import csv
import datetime

import cpsar.report
import cpsar.runtime as R
import cpsar.util as U
import cpsar.ws as W
import kcontrol as K

from cpsar import sales

class Program(W.MakoProgram):

    ## Things needed by query_form.tmpl
    label = "Group Health Cash Receipt Report"
    summary = """Provides a list of all checks received from clients over a specified
    time frame. This includes payments and overpayments.
    """
    form_resources = ''
    script_name = '/rpt_gh_cash_receipt'
    csv_exportable = True
    query_css = ''
    debug = False
    def print_params(self):
        p = []
        for key, value in self._req.params.items():
            if value and not key.startswith('_q'):
                p.append("%s: %s" % (key, value))
        return " ".join(p)

    _record_fields = ()
    record_fields = lambda self: self._record_fields
    legend = lambda self: ''

    ## Submitted Form Value Properties
    @property
    def payment_date_before(self):
        return self._date_form_val('payment_date_before')

    @property
    def payment_date_after(self):
        return self._date_form_val('payment_date_after')

    @property
    def payer_code(self):
        return self._req.params.get('payer_code')

    @property
    def grouping(self):
        val = self._req.params.get('grouping')
        if val in ['detail', 'summary', 'hbs_order_number']:
            return val
        else:
            return 'detail'

    def main(self):
        """ Entry Point """
        if self._req.params.get('_q_submit'):
            cursor = self._report_cursor()
            if self._req.params.get('_q_csv'):
                self._send_csv_file(cursor)
            else:
                self._send_mako_html(cursor)
        else:
            self._send_form()

    ## Form Methods
    def _send_form(self):
        self._set_params()
        self.tmpl.template_name = 'query_form.tmpl'
        return

    def _set_params(self):
        self.params = [
            ('Payer Code', K.TextBox('payer_code')),
            ('Payment Date After', K.DatePicker('payment_date_after',
                     defaultValue=datetime.date.today()-datetime.timedelta(2)   )),
            ('Payment Date Before', K.DatePicker('payment_date_before',
                     defaultValue=datetime.date.today())),
            ('Grouping', K.ListBox('grouping', values=[
                ('detail', 'Detail'),
                ('summary', 'Summary'),
                ('hbs_order_number', 'HBS Order Number')]))
        ]

    ## Report Running Methods
    def _report_cursor(self):
        if self.payer_code:
            create_constrained_payer_code_table(self.payer_code)
        else:
            create_unconstrained_payer_code_table()

        create_payment_table(self.payment_date_after, self.payment_date_before)

        if self.grouping == 'detail':
            return self._detail_report_cursor()
        elif self.grouping == 'summary':
            return self._summary_report_cursor()
        elif self.grouping == 'hbs_order_number':
            return self._hbs_order_report_cursor()

    def _send_mako_html(self, cursor):
        self._assign_record_fields_from_cursor(cursor)
        self.tmpl.template_name = 'query_show_sql.tmpl'
        self.tmpl['cursor'] = cursor
        self.tmpl['duration'] = ''

    def _send_csv_file(self, cursor):
        self._res.content_type = 'text/csv'
        h = self._res.headers
        self.mako_auto_publish = False
        h.add("Expires", "0")
        h.add("Content-Transfer-Encoding", "binary")
        h.add("Pragma", "public")
        h.add("Content-Disposition", "attachment; filename=gh_cash_receipt.csv")
        writer = csv.writer(self._res)
        writer.writerow([c[0] for c in cursor.description])
        for rec in cursor:
            writer.writerow(rec)

    def _detail_report_cursor(self):
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT trans_id,
               tx_type,
               payer_code,
               hbs_order_number,
               batch_date,
               rx_number, 
               patient_first_name || ' ' || patient_last_name AS patient,
               refill_number,
               payment_date,
               type_name,
               ref_no,
               username,
               amount,
               compound_code,
               drug_name,
               overpayment_or_payment AS type
            FROM payment
            ORDER BY payment_date
        """)
        return cursor

    def _summary_report_cursor(self):
        cursor = R.db.cursor()
        cursor.execute('''
            SELECT payer_code,
                   batch_date,
                   SUM(amount) AS amount
            FROM payment
            GROUP BY payer_code, batch_date
            ORDER BY batch_date, payer_code
            ''')
        return cursor

    def _hbs_order_report_cursor(self):
        cursor = R.db.cursor()
        cursor.execute('''
          SELECT hbs_order_number,
                 payer_code,
                 payment_date,
                 type_name,
                 SUM(amount) AS amount
          FROM payment
          GROUP BY hbs_order_number, payer_code, payment_date, type_name
          ORDER BY hbs_order_number, payment_date
          ''')
        return cursor

    def _assign_record_fields_from_cursor(self, cursor):
        self._record_fields = [c[0] for c in cursor.description]

    ## Utility Methods
    def _date_form_val(self, field):
        val = self._req.params.get(field)
        try:
            return U.parse_american_date(val)
        except U.ParseError:
            return None


        for v in self.params:
            key = v[1].name
            if self.req.get(key):
                args[key] = cpsar.pg.qstr(str(self.req.get(key)))
            else:
                args[key] = None
        gn = self.client_requested_group_numbers()


    def query_args(self):
        args = super(Report, self).query_args()
        phcy = self.req.get('pharmacy')
        payer_code = self.req.get('payer_code')
        if payer_code:
            args['payer_code_frag'] = " = '%s'" % cpsar.pg.qstr(payer_code)
        else:
            args['payer_code_frag'] = " IS NOT NULL"
        return args

    sql = """
    WITH payments_by_payer_code AS (
        SELECT 
           history.payer_code,
           payment_type.type_name,
           trans_payment.ref_no,
           trans.trans_id,
           trans.batch_date,
           trans_payment.entry_date::date AS payment_date,
           trans_payment.amount
        FROM trans_payment
        JOIN trans USING(trans_id)
        JOIN payment_type USING(ptype_id)
        WHERE trans_payment.entry_date::date BETWEEN
            %(payment_date_after)s AND %(payment_date_before)s
            AND history.payer_code %(payer_code_frag)s
            AND trans_payment.puc_id IS NULL
            AND trans_payment.credit_group_number IS NULL
            AND trans.group_number = 'GROUPH'
        UNION ALL
        SELECT
           history.payer_code,
           payment_type.type_name,
           overpayment.ref_no,
           trans.trans_id,
           trans.batch_date,
           overpayment.entry_date::date AS payment_date,
           overpayment.amount
        FROM overpayment
        JOIN trans USING(trans_id)
        JOIN trans_payment USING(puc_id)
        LEFT JOIN payment_type USING(ptype_id)
        WHERE overpayment.entry_date::date BETWEEN
            %(payment_date_after)s AND %(payment_date_before)s
            AND history.payer_code %(payer_code_frag)s
            AND trans.group_number = 'GROUPH'
      )
    SELECT payer_code AS AS "Payer Code",
           payment_date AS "Payment Date",
           payment_type AS "Payment Type",
           batch_date AS "Batch Date",
           COUNT(*) AS "Receipt Count",
           format_currency(SUM(amount)) AS Amount
    FROM payments_by_payer_code
    GROUP BY payer_code, payment_date, batch_date
    UNION ALL
    SELECT 'zzTotal', NULL, NULL, COUNT(*), format_currency(SUM(amount))
    FROM payments_by_group
    ORDER BY "Group Number", "Payment Date", "Batch Date"
    """

def create_constrained_payer_code_table(payer_code):
    cursor = R.db.cursor()
    cursor.execute('''CREATE TEMP TABLE payer_code_constraint AS
        SELECT %s::varchar AS payer_code
        ''', (payer_code,))

def create_unconstrained_payer_code_table():
    cursor = R.db.cursor()
    cursor.execute('''
        CREATE TEMP TABLE payer_code_constraint AS
        SELECT DISTINCT history.payer_code
        FROM history
        WHERE group_number='GROUPH'
    ''')

def create_payment_table(payment_date_after, payment_date_before):
    cursor = R.db.cursor()
    cursor.execute('''
    CREATE TEMP TABLE payment (
        trans_id BIGINT,
        tx_type CHAR(2),
        payment_id BIGINT,
        payment_date DATE,
        amount DECIMAL(10, 2),
        type_name VARCHAR,
        ref_no VARCHAR,
        overpayment_or_payment VARCHAR,
        batch_date DATE,
        hbs_order_number BIGINT,
        rx_number BIGINT,
        refill_number INT,
        payer_code VARCHAR,
        patient_first_name VARCHAR,
        patient_last_name VARCHAR,
        drug_name varchar,
        compound_code char,
        username VARCHAR);

    /* Regular payments */
    INSERT INTO payment (trans_id, payment_id, payment_date, amount,
                         type_name, ref_no, username, drug_name, compound_code, overpayment_or_payment)
    SELECT 
       trans_payment.trans_id,
       trans_payment.payment_id,
       trans_payment.entry_date::date,
       trans_payment.amount,
       payment_type.type_name,
       trans_payment.ref_no,
       trans_payment.username,
       drug.name as drug_name,
       trans.compound_code,
       'payment'
    FROM trans_payment
    JOIN trans USING(trans_id)
    JOIN drug USING(drug_id)
    JOIN payment_type USING(ptype_id)
    WHERE trans_payment.entry_date::date BETWEEN
        %(payment_date_after)s AND %(payment_date_before)s
        AND trans_payment.puc_id IS NULL
        AND trans_payment.credit_group_number IS NULL
        AND trans.group_number = 'GROUPH';

    /* Overpayments */
    INSERT INTO payment (trans_id, payment_date, amount, type_name,
                         ref_no, username, compound_code, drug_name, overpayment_or_payment)
    SELECT
       overpayment.trans_id,
       overpayment.entry_date::date,
       overpayment.amount,
       payment_type.type_name,
       overpayment.ref_no,
       overpayment.username,
       trans.compound_code,
       drug.name as drug_name,
       'overpayment'
    FROM overpayment
    JOIN trans USING(trans_id)
    JOIN drug using(drug_id)
    JOIN payment_type USING(ptype_id)
    WHERE overpayment.entry_date::date BETWEEN
        %(payment_date_after)s AND %(payment_date_before)s
        AND trans.group_number = 'GROUPH';

    /* Common data fields for all kinds of payments */

    UPDATE payment SET
        batch_date=trans.batch_date,
        hbs_order_number=history.hbs_order_number,
        rx_number=history.rx_number,
        refill_number=history.refill_number,
        payer_code=history.payer_code,
        patient_first_name=patient.first_name,
        patient_last_name=patient.last_name,
        tx_type=trans.tx_type
    FROM history, trans, patient
    WHERE payment.trans_id = trans.trans_id AND
         history.history_id = trans.history_id AND
         history.patient_id = patient.patient_id;
    ''', {'payment_date_after': payment_date_after,
          'payment_date_before': payment_date_before})

application = Program.app
