import cpsar.report
import kcontrol

class Report(cpsar.report.WSGIReport):
    label = 'Partial Balances'

    sql = """
    SELECT  
        trans.trans_id,
        trans.batch_date,
        trans.invoice_id,
        trans.group_number,
        trans.total,
        trans.adjustments,
        trans.balance
    FROM trans
    WHERE balance > 0 AND balance <> total
    ORDER BY trans.trans_id
    """

application = Report().wsgi()
