
"""
search term for string
"""
from cpsar import pg
import cpsar.runtime as R
import cpsar.ws as W
import cpsar.util as U

class Program(W.MakoProgram):
    search_results = []
    sql = None

    def main(self):
        self._compute_search_results()

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
        self._fetch_search_results()
        self._drop_search_results_table()

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
        cursor.execute("DROP TABLE search_results")

    def _delete_filtered_search_results(self):
        cursor = R.db.cursor()
        if not self.fs.getvalue('report_code'):
            return
        cursor.execute("""
          DELETE FROM search_results
          WHERE NOT EXISTS (
            SELECT 1 FROM client_report_code
            WHERE client_report_code.group_number =
                  search_results.group_number
              AND client_report_code.report_code = %s
          )""", (self.fs.getvalue('report_code'),))

    @property
    def _limit(self):
        try:
            return min(int(self.fs.getvalue('limit')), 5000)
        except (ValueError, TypeError):
            return 5000

    @property
    def _sort_field(self):
        return self.fs.getvalue('sort_by', 'srid')

    @property
    def _sort_order(self):
        return self.fs.getvalue('sort_order', 'ASC')

    @property
    def _order_by(self):
        return "%s %s" % (self._sort_field, self._sort_order)

    def _limit_results(self):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            DELETE FROM search_results
            WHERE trans_id NOT IN
                (SELECT trans_id
                 FROM search_results
                 ORDER BY %s %s
                 LIMIT %%s)
            """ % (self._sort_field, self._sort_order), (self._limit,))

    def _fetch_search_results(self):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT * FROM search_results
            ORDER BY %s
            """ % (self._order_by))

        self.search_results = list(cursor)

    @property
    def _create_table_sql(self):
        return """
            CREATE TEMPORARY TABLE search_results AS
            SELECT DISTINCT
                state_report_entry.srid,
                state_report_entry.control_number,
                state_report_bill.bill_id,
                state_report_bill.bill_number,
                state_report_file.sr_file_id,
                state_report_file.send_time,
                trans.trans_id,
                trans.group_number,
                trans.paid_date as cps_paid_date,
                history.reverse_date,
                history.pharmacy_payment_date,
                trans.sr_mark,
                coalesce(state_report_bill.patient_first_name, patient.first_name) as patient_first_name,
                coalesce(state_report_bill.patient_last_name, patient.last_name) as patient_last_name
            from state_report_entry
            left join state_report_bill using(bill_id)
            join state_report_file on state_report_entry.sr_file_id = state_report_file.sr_file_id
            left join trans on coalesce(state_report_entry.trans_id, state_report_bill.trans_id) = trans.trans_id
            left join history on trans.history_id = history.history_id
            left join patient on trans.patient_id = patient.patient_id
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
        p.value_equal_term('state_report_file.sr_file_id'),
        p.send_date_after(),
        p.send_date_before(),

        p.value_equal_term('state_report_bill.bill_id'),
        p.value_equal_term('state_report_bill.claim_number'),
        p.value_equal_term('state_report_bill.claim_freq'),
        p.search_term('state_report_bill.patient_first_name'),
        p.search_term('state_report_bill.patient_last_name'),

        p.value_equal_term('state_report_entry.srid'),
        p.value_equal_term('state_report_entry.control_number'),

        p.value_equal_term('trans.trans_id'),
        p.value_equal_term('trans.patient_id'),
    ]

class _GivenSearchParams(object):
    def __init__(self, fs):
            self._fs = fs

# Generic terms
    def value_equal_term(self, name):
        val = self._fs.getvalue(name)
        if not val:
            return []
        return ['%s=%s' % (name, pg.qstr(val))]

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

# Specific terms
    def send_date_after(self):
        val = self._fs.getvalue('state_report_file.send_date_after')
        if not val:
            return []
        return ["state_report_file.send_time::date >= %s" % pg.qstr(val)]

    def send_date_before(self):
        val = self._fs.getvalue('state_report_file.send_date_before')
        if not val:
            return []
        return ["state_report_file.send_time::date <= %s" % pg.qstr(val)]

application = Program.app
