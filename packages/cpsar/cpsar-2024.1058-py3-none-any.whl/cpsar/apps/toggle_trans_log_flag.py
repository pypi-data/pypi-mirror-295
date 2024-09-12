import cpsar.runtime as R
import cpsar.ws as W

class Program(W.GProgram):
    def main(self):
        fs = self.fs
        cursor = R.db.cursor()
        log_id = fs.getvalue('trans_log_id')
        trans_id = fs.getvalue('trans_id')
        cursor.execute("""
            UPDATE trans_log SET flagged = NOT flagged
            WHERE trans_log_id = %s
            """, (log_id,))

        R.db.commit()
        self._res.redirect("/view_trans?trans_id=%s&m=fl", trans_id)
        
application = Program.app
