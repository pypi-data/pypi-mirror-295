import cpsar.report
import cpsar.runtime as R
import kcontrol

class Report(cpsar.report.WSGIReport):
    label = 'Commission Comparison'
    params = [
        ('Start Date', kcontrol.DatePicker('start_date')), 
        ('End Date',   kcontrol.DatePicker('end_date'))
    ]

    query_css = """
        TD.data2 { text-align: right; }
    """

    @property
    def start_date(self):
        return self.req.get('start_date')

    @property
    def end_date(self):
        return self.req.get('end_date')

    def record_fields(self):
        return ['Account', 'Amount']

    sql = """
        SELECT distribution_account, SUM(amount)
        FROM distribution
        JOIN trans ON
            distribution.trans_id = trans.trans_id AND
              NOT (trans.group_number = '56600' AND 
                   (group_auth BETWEEN 86579 AND 92263 OR
                    group_auth BETWEEN 94623 AND 95828))
        WHERE distribution_date BETWEEN %(start_date)s AND %(end_date)s
            AND distribution_account != 'pharmacy'
        GROUP BY distribution_account
        UNION ALL
        SELECT '*TOTAL', SUM(amount)
        FROM distribution
        JOIN trans ON
            distribution.trans_id = trans.trans_id AND
              NOT (trans.group_number = '56600' AND 
                   (group_auth BETWEEN 86579 AND 92263 OR
                    group_auth BETWEEN 94623 AND 95828))
        WHERE distribution_date BETWEEN %(start_date)s AND %(end_date)s
            AND distribution_account != 'pharmacy'
        ORDER BY distribution_account
    """

application = Report().wsgi()
