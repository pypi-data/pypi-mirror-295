import cpsar.report

class Report(cpsar.report.WSGIReport):
    label = 'Monthly Sales Totals'

    sql = """
    SELECT
        to_char(trans.batch_date, 'YYYY-MM') AS m,
        to_char(trans.batch_date, 'YYYY MON') AS month,
        trans.group_number,
        SUM(trans.total) as total
    FROM trans
    GROUP BY month, trans.group_number, m
    ORDER BY m DESC, group_number ASC
    """

application = Report().wsgi()
