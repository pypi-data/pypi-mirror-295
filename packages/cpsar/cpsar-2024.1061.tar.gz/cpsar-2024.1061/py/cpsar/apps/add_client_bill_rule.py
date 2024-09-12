import logging
import os

import cpsar.controls as C
import cpsar.runtime as R
import cpsar.ws as W

log = None

class Program(W.GProgram):
    def main(self):
        fs = self.fs
        group_number = fs.getvalue('group_number')
        rule_type = fs.getvalue("rule_type")
        tx_type = fs.getvalue('tx_type')
        amount = fs.getvalue('amount')

        if not group_number:
            R.error('Missing group number')
        if not tx_type:
            R.error('Missing TX Type')
        if not C.client_bill_rule_label(rule_type):
            R.error("Invalid bill ruile")
        if tx_type in ('AP', 'CF') and not amount:
            R.error('Missing amount')

        # Bomb out
        if R.has_errors():
            for e in R.get_errors():
                self._res.error(e)
            return

        cursor = R.db.cursor()
        if amount:
            amount = amount.replace('$', '')

        cursor.execute("""
            UPDATE client_bill_rule SET amount=%s
            WHERE group_number=%s AND
                  tx_type=%s AND
                  rule_type=%s
            """, (amount, group_number, tx_type, rule_type))
        if not cursor.rowcount:
            sql = """INSERT INTO client_bill_rule (
                     group_number, 
                     rule_type,
                     tx_type, 
                     amount)
                     VALUES (%s, %s, %s, %s)
                    """
            cursor.execute(sql, (group_number, rule_type, tx_type, amount))
        
        msg = 'Added Bill Rule %s: %s;%s -> %s' % (
                group_number, rule_type, tx_type, amount)
        R.db.commit()
        self._res.redirect('/view_client?group_number=%s', group_number)

application = Program.app
