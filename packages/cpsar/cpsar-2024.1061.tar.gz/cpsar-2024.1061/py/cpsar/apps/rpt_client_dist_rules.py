import cpsar.runtime as R
import cpsar.report

class Report(cpsar.report.WSGIReport):
    label = 'Client Distribution Rules'
    def record_fields(self):
        return [
            'group_number',
            'tx_type',
            'distribution_account',
            'amount',
            'percent',
            'create_time'
        ]

    def records(self):
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT group_number, tx_type, distribution_account, amount, 
                   percent, create_time
            FROM distribution_rule
            ORDER BY group_number, tx_type, distribution_account
            """)
        return cursor

application = Report().wsgi()
