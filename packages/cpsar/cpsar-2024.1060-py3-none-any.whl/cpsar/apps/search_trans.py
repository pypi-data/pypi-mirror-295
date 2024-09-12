"""
search term for string
"""
from cpsar import pg
import cpsar.runtime as R
import cpsar.ws as W
import cpsar.util as U

class Program(W.MakoProgram):
    search_results = []
    search_totals = None
    sql = None

    def main(self):
        self._compute_search_results()
        if len(self.search_results) == 1:
            trans_id = self.search_results[0]['trans_id']
            self._res.redirect('/view_trans?trans_id=%s', trans_id)
            return

    @property
    def _search_performed(self):
        if where_conditions(self.fs):
            return self.fs.getvalue('action') == 'Search'
        return False

    def _compute_search_results(self):
        if not self._search_performed:
            return 
        self._create_search_results_table()
        if R.has_errors():
            return
        self._delete_filtered_search_results()
        self._limit_results()
        self._compute_search_totals()
        self._fetch_search_results()
        self._drop_search_results_table()

    def _compute_search_totals(self):
        cursor = R.db.dict_cursor()
        sql = """
            SELECT 
                SUM(SearchResults.total) as total,
                SUM(SearchResults.adjustments) as adjustments,
                SUM(SearchResults.paid) AS paid,
                SUM(SearchResults.balance) as balance
            FROM SearchResults """
        cursor.execute(sql)
        self.search_totals = pg.one(cursor)

    def _create_search_results_table(self):
        cursor = R.db.cursor()
        self.sql = self._create_table_sql
        try:
            cursor.execute(self.sql)
        except pg.DataError as e:
            R.error(e)
            R.db.rollback()

    def _drop_search_results_table(self):
        cursor = R.db.cursor()
        cursor.execute("DROP TABLE SearchResults")

    def _delete_filtered_search_results(self):
        cursor = R.db.cursor()
        if not self.fs.getvalue('report_code'):
            return
        cursor.execute("""
          DELETE FROM SearchResults
          WHERE NOT EXISTS (
            SELECT 1 FROM client_report_code
            WHERE client_report_code.group_number =
                  SearchResults.group_number
              AND client_report_code.report_code = %s
          )""", (self.fs.getvalue('report_code'),))

    @property
    def _limit(self):
        try:
            return min(int(self.fs.getvalue('limit')), 1000)
        except (ValueError, TypeError):
            return 1000

    @property
    def _sort_field(self):
        return self.fs.getvalue('sort_by', 'last_name')

    @property
    def _sort_order(self):
        return self.fs.getvalue('sort_order', 'ASC')

    @property
    def _order_by(self):
        return "%s %s" % (self._sort_field, self._sort_order)

    def _limit_results(self):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            DELETE FROM SearchResults
            WHERE trans_id NOT IN
                (SELECT trans_id
                 FROM SearchResults
                 ORDER BY %s %s
                 LIMIT %%s)
            """ % (self._sort_field, self._sort_order), (self._limit,))

    def _fetch_search_results(self):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT * FROM SearchResults
            ORDER BY %s
            """ % (self._order_by))

        self.search_results = list(cursor)

    @property
    def _create_table_sql(self):
        return """
            CREATE TEMPORARY TABLE SearchResults AS
            SELECT DISTINCT trans.trans_id,
                   trans.batch_date,
                   trans.group_number,
                   trans.group_auth,
                   trans.paid_date,
                   patient.patient_id,
                   patient.first_name,
                   patient.last_name,
                   trans.rx_date,
                   max_credit.credit_date,
                   drug.name AS drug_name,
                   drug.ndc_number,
                   trans.rx_number,
                   trans.claim_number,
                   trans.invoice_id,
                   trans.line_no,
                   trans.total,
                   trans.adjustments,
                   trans.balance,
                   trans.paid_amount AS paid,
                   trans.settled_amount,
                   trans.adjuster1_email,
                   trans.adjuster2_email,
                   history.payer_code,
                   date_part('day', NOW() - trans.create_date)::int AS age,
                   reversal.balance as reversal_balance
            FROM trans
            LEFT JOIN patient ON
             trans.patient_id = patient.patient_id
            LEFT JOIN drug ON
             trans.drug_id = drug.drug_id
            LEFT JOIN invoice ON
             trans.invoice_id = invoice.invoice_id
            LEFT JOIN client ON
             trans.group_number = client.group_number
            LEFT JOIN reversal ON
             trans.trans_id = reversal.trans_id
            LEFT JOIN reversal_settlement ON
             reversal.reversal_id = reversal_settlement.reversal_id
            LEFT JOIN overpayment ON
             trans.trans_id = overpayment.trans_id
            Left JOIN history ON
             trans.history_id = history.history_id
            Left JOIN pharmacy ON
                trans.pharmacy_id = pharmacy.pharmacy_id 
            LEFT JOIN (
                SELECT trans_id, MAX(entry_date)::date AS credit_date
                FROM (
                    SELECT trans_adjudication.trans_id,
                           trans_adjudication.entry_date
                    FROM trans_adjudication
                    UNION ALL
                    SELECT trans_writeoff.trans_id,
                           trans_writeoff.entry_date
                    FROM trans_writeoff
                ) AS all_credits
                GROUP BY trans_id
            ) AS max_credit ON trans.trans_id = max_credit.trans_id
            %s """ % (where_conditions(self.fs))

    def search(self):
        cursor = R.db.dict_cursor()

###############################
def where_conditions(fs):
    cond_string = " AND ".join(sum(where_exprs(fs), []))
    if cond_string == '':
        return ''
    else:
        return "WHERE %s" % cond_string

def where_exprs(fs):
    p = _GivenSearchParams(fs)
    return [
        p.value_equal_term('trans.trans_id'),        
        p.date_equal_term('trans.batch_date'),
        p.date_equal_term('trans.rx_date'),
        p.search_term('trans.paid'),
        p.tx_status_term(),
        p.tx_reconciled_term(),
        p.tx_invoice_id(),
        p.search_term('trans.pharmacy_nabp'),        
        p.value_equal_term('trans.patient_id'),
        p.email_term(),
        p.tx_report_status(),
        p.search_term('trans.group_number'),
        p.value_equal_term('trans.group_auth'),
        p.search_term('trans.claim_number'),
        p.create_date_after('trans.create_date_after'),
        p.create_date_before('trans.create_date_before'),
        p.tx_rebill_term(),
        p.value_equal_term('trans.processing_fee'),
        p.tx_has_settlement_term(),
        p.value_equal_term('trans.rx_number'),
        p.tx_reversal_exists(), 
        p.tx_reversal_balanced_term(),
        p.value_equal_term('reversal.reversal_id'),
        p.value_equal_term('client.invoice_processor_code'),
        p.search_term('patient.first_name'),
        p.search_term('patient.last_name'),
        p.search_term('patient.jurisdiction'),
        p.value_equal_term('overpayment.puc_id'),
        p.tx_overpayment_overpaid(),
        p.search_term('history.payer_code'),
        p.value_equal_term('history.pharmacy_payment_date'),
        p.tx_type_term()
    ]

class _GivenSearchParams(object):
    def __init__(self, fs):
            self._fs = fs

# Generic terms
    def search_term(self, name):
        val = self._fs.getvalue(name)
        if not val:
            return []
        return ['%s ILIKE %s' % (name, pg.qstr(val))]

    def bool_null_term(self, name):
        val = self._fs.getvalue(name)
        if not val:
            return []
        if val  == 'Y':
            return ['%s IS NOT NULL' % name]
        else:
            return ['%s IS NULL' % name]

    def date_equal_term(self, name):
        val = self._fs.getvalue(name)
        if not val:
            return []
        return ['%s=%s' % (name, pg.qstr(val))]

    def create_date_after(self, name):
        val = self._fs.getvalue('trans.create_date_after')
        if not val:
            return []
        return ["trans.create_date::date >= %s" % pg.qstr(val)]

    def create_date_before(self, name):
        val = self._fs.getvalue('trans.create_date_before')
        if not val:
            return []
        return ["trans.create_date::date <= %s" % pg.qstr(val)]

# Specific terms
    def tx_type_term(self):
        tx_type = self._fs.getvalue('trans.tx_type')
        if not tx_type:
            return []
        if tx_type == 'retail':
            return ["trans.tx_type LIKE 'R%'"]
        elif tx_type == 'mail_order':
            return ["trans.tx_type LIKE 'M%' AND history.compound_code !='2'"]
        elif tx_type == 'compound':
            return ["history.compound_code ='2'"]

    def tx_reconciled_term(self):
        tx_reconciled = self._fs.getvalue('trans.reconciled')
        if not tx_reconciled:
            return []
        if tx_reconciled == 'no':
            return ['trans.distributed_amount <> trans.paid_amount - trans.settled_amount']
        elif tx_reconciled == 'yes':
            return ["trans.distributed_amount = trans.paid_amount - trans.settled_amount"]
        return ["trans.paid_amount <> 0"]

    def tx_status_term(self):
        tx_statuses = self._fs.getlist('trans.status')
        if not tx_statuses:
            return []
        age_frag = "date_part('day', NOW()- trans.create_date)::int"
        p = []

        for status in tx_statuses:
            if status == 'collect':
                p.append('(%s > 30 AND trans.balance > 0)' % age_frag)
            elif status == 'overdue':
                p.append('(%s BETWEEN 16 AND 30 '
                         'AND trans.balance > 0)' % age_frag)
            elif status == 'current':
                p.append('(%s <= 15 '
                         'AND trans.balance > 0)' % age_frag)
            elif status == 'paid':
                p.append('(trans.balance = 0)')
            elif status == 'overpaid':
                p.append('(trans.balance < 0)')
        if p:
            return ["(%s)" % " OR\n\t\t".join(p)]

    def tx_invoice_id(self):
        tx_invoice_id = self._fs.getvalue('trans.invoice_id')
        if not tx_invoice_id:
            return []

        if tx_invoice_id.count('-') == 1:
            invoice_id, line_no = tx_invoice_id.split('-')
            return ["""
                trans.invoice_id = %s AND
                trans.line_no = %s""" % (invoice_id, line_no)]
        else:
            try:
                int(tx_invoice_id)
                return ['trans.invoice_id=%s' % tx_invoice_id]
            except ValueError:
                R.error("Invalid invoice id %s" % tx_invoice_id)
                return []

    def tx_rebill_term(self):
        rebill = self._fs.getvalue('trans.rebill')
        if not rebill:
            return []
        if self._fs.getvalue('trans.rebill') == 'on':
            return ['trans.rebill = True']
        else:
            return ['trans.rebill = False']

    def tx_has_settlement_term(self):
        val = self._fs.getvalue('trans.has_settlement')
        if not val:
            return []

        if val == 'Y':
            return ['trans.settled_amount = 0']
        elif val == 'N':
            return ['trans.settled_amount <> 0']
        else:
            return []

    def tx_reversal_balanced_term(self):
        val = self._fs.getvalue('reversal.balanced')
        if not val:
            return []
        if self._fs.getvalue(val) == 'Y':
            return ['reversal.balance <> 0']
        else:
            return ['reversal.balance = 0']

    def value_equal_term(self, name):
        val = self._fs.getvalue(name)
        if not val:
            return []
        return ['%s=%s' % (name, pg.qstr(val))]

    def email_term(self):
        val = self._fs.getvalue('trans.email')
        if not val:
            return []
        return["""(
            trans.adjuster1_email ILIKE %s OR
            trans.adjuster2_email ILIKE %s)""" % ( pg.qstr(val), pg.qstr(val))]

    def tx_report_status(self):
        val = self._fs.getvalue('trans.report_status')
        if not val:
            return []
        if val != 'N':
            return ["trans.report_status = '%s'" % val]
        else:
            return ['trans.report_status IS NOT NULL']

    def tx_reversal_exists(self):
        val = self._fs.getvalue('reversal.exists')
        if not val:
            return []
        if val  == 'Y':
            return ['reversal.trans_id IS NOT NULL']
        else:
            return ['reversal.trans_id IS NULL']

    def tx_overpayment_overpaid(self):
        val = self._fs.getvalue('overpayment.overpaid')
        if not val:
            return []
        if val  == 'Y':
            return ['overpayment.puc_id IS NOT NULL']
        else:
            return ['overpayment.puc_id IS NULL']

application = Program.app
