import decimal

import cpsar.runtime as R
import cpsar.ws as W

from cpsar.util import insert_sql

class Program(W.GProgram):
    def main(self):
        fs = self.fs
        group_number = fs.getvalue('group_number')
        distribution_account = fs.getvalue('distribution_account')
        amount = fs.getvalue('amount')
        percent = fs.getvalue('percent')
        tx_type = fs.getvalue('tx_type')
        show_on_invoice = bool(fs.getvalue('show_on_invoice'))
        addon = bool(fs.getvalue('addon'))
        add_to_running_total = bool(fs.getvalue('add_to_running_total'))
        try:
            priority = int(fs.getvalue('priority'))
        except (ValueError, TypeError) as e:
            priority = 1
        try:
            max_cost = decimal.Decimal(fs.getvalue('max_cost', ''))
        except decimal.InvalidOperation:
            max_cost = None
        try:
            min_cost = decimal.Decimal(fs.getvalue('min_cost', ''))
        except decimal.InvalidOperation:
            min_cost = None

        if max_cost and min_cost and min_cost >= max_cost:
            R.error("max cost must be more than min cost")
        if not group_number:
            R.error('Missing group number')
        if not tx_type:
            R.error('Missing TX Type')
        if not distribution_account:
            R.error('Missing distribution account')
        if not amount and not percent:
            R.error('Missing amount or percent')
        if amount and percent:
            R.error('Can only take amount or percent, not both')

        if R.has_errors():
            for e in R.get_errors():
                self._res.error(e)
            return

        sql = insert_sql("distribution_rule", {
            "group_number": group_number,
            "tx_type": tx_type,
            "distribution_account": distribution_account,
            "amount": amount,
            "percent": percent,
            "min_cost": min_cost,
            "max_cost": max_cost,
            "addon": addon,
            "add_to_running_total": add_to_running_total,
            "priority": priority,
            "show_on_invoice": show_on_invoice
            })
        cursor = R.db.cursor()
        cursor.execute(sql)
        R.db.commit()

        if amount:
            msg = 'Added fixed amount distribution Rule to %s: %s, %s, %s' % (
                    group_number, tx_type, distribution_account, amount)
        else:
            msg = 'Added percent distribution Rule to %s: %s, %s, %s' % (
                    group_number, tx_type, distribution_account, percent)
        R.log.info(msg)
        self._res.redirect('/view_client?group_number=%s&m=x', group_number)

application = Program.app
