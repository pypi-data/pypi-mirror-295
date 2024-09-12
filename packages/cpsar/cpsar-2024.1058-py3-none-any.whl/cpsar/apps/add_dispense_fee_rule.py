import cpsar.runtime as R
import cpsar.ws as W

class Program(W.GProgram):

    def main(self):
        fs = self.fs
        cursor = R.db.cursor()

        group_number = fs.getvalue('group_number')
        tx_type = fs.getvalue('tx_type')
        amount = fs.getvalue('amount')

        if not group_number:
            R.error('Missing group number')
        if not tx_type:
            R.error('Missing TX Type')
        if not amount:
            R.error('Missing amount')

        if R.has_errors():
            self._res.error('')
            for e in R.get_errors():
                self._res("%s", e)
            return

        if amount:
            amount = amount.replace('$', '')

        cursor.execute("""
            UPDATE client_dispense_fee_rule SET amount=%s
            WHERE group_number=%s AND
                  tx_type=%s
            """, (amount, group_number, tx_type))
        if not cursor.rowcount:
            sql = """INSERT INTO client_dispense_fee_rule (
                     group_number, 
                     tx_type, 
                     amount)
                     VALUES (%s, %s, %s)
                    """
            cursor.execute(sql, (group_number, tx_type, amount))
        
        msg = 'Added Dispense Fee Override Rule to %s: %s -> %s' % (
                group_number, tx_type, amount)
        R.log.info(msg)
        R.db.commit()
        self._res.redirect("/view_client?group_number=%s", group_number)

application = Program.app
