from decimal import Decimal

import cpsar.runtime as R
import cpsar.ws as W

class Program(W.GProgram):
    """ Management of Client Record - Remove 
    distribution rule from the given client."""

    def main(self):
        fs = self.fs
        id = fs.getvalue('cbram_id')
        if not id:
            self._res.error('no id')
            return

        cursor = R.db.cursor()
        cursor.execute("""
            SELECT group_number, rule_type, tx_type, amount
            FROM client_bill_rule
            WHERE cbram_id=%s
            """, (id,))

        if not cursor.rowcount:
            self._res.error('')
            return

        group_number, rule_type, tx_type, amount = cursor.fetchone()
        cursor.execute("""
            DELETE 
            FROM client_bill_rule
            WHERE cbram_id=%s
            """, (id,))

        R.log.info('Removed bill rule from %s: %s;%s -> %s',  
                 group_number, rule_type, tx_type, amount)
        R.db.commit()
        self._res.redirect("/view_client?group_number=%s", group_number)

application = Program.app
