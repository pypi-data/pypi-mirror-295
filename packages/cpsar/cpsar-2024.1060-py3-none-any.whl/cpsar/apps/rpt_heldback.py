import cpsar.runtime as R
import cpsar.report
import kcontrol

class HeldbackBatchListBox(kcontrol.ListBox):
    def __init__(self, *a, **k):
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT DISTINCT batch_date, batch_date
            FROM heldback
            ORDER BY batch_date DESC
            """)
        kcontrol.ListBox.__init__(self, values=list(cursor), *a, **k)

class Report(cpsar.report.WSGIReport):
    label = 'Held Back Transactions'
    params = [
        ('Start Batch Date', kcontrol.DatePicker('start_date')), 
        ('End Batch Date',   kcontrol.DatePicker('end_date'))
    ]

    def record_fields(self):
        return ['Group', 'Claim Ref #', 'Amount (Not including PF)']

    def records(self):
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT history.group_number,
                   history.group_auth,
                   cost_allowed + dispense_fee + sales_tax - eho_network_copay 
            FROM history
            JOIN heldback ON history.history_id = heldback.history_id
            WHERE heldback.batch_date BETWEEN %(start_date)s AND
                                              %(end_date)s
            """ % self.query_args())
        for x in cursor: yield x

        cursor.execute("""
            SELECT 'TOTAL', '',
                   SUM(cost_allowed + dispense_fee + sales_tax - eho_network_copay)
            FROM history
            JOIN heldback ON history.history_id = heldback.history_id
            WHERE heldback.batch_date BETWEEN %(start_date)s AND
                                              %(end_date)s
            """ % self.query_args())
        yield cursor.fetchone()

application = Report().wsgi()
