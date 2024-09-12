import cpsar.runtime as R
import cpsar.ws as W

class Program(W.GProgram):
    """Manages the client, removes a fee dispense rule"""
    def main(self):
        fs = self.fs
        
        id = fs.getvalue('cdfm_id')
        if not id:
            self._res.error("no id")
            return

        cursor = R.db.cursor()
        cursor.execute("""
            SELECT group_number, tx_type, amount
            FROM client_dispense_fee_rule
            WHERE cdfm_id=%s
            """, (id,))

        if not cursor.rowcount:
            self.res.error("")
            return

        group_number, tx_type, amount = cursor.fetchone()
        cursor.execute("""
            DELETE 
            FROM client_dispense_fee_rule
            WHERE cdfm_id=%s
            """, (id,))

        R.log.info('Removed dispense fee rule override from %s: %s -> %s',  
                 group_number, tx_type, amount)
        R.db.commit()
        self._res.redirect("/view_client?group_number=%s", group_number)

application = Program.app
