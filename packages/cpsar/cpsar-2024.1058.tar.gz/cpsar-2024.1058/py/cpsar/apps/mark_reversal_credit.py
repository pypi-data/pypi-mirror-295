import cpsar.runtime as R
import cpsar.ws as W

class Program(W.GProgram):
    def main(self):
        reversal_id = self.fs.getvalue('reversal_id')
        cursor = R.db.dict_cursor()
        cursor.execute("SELECT * FROM reversal WHERE reversal_id=%s",
                       (reversal_id, ))
        reversal = cursor.fetchone()
        assert reversal

        cursor.execute("""
            INSERT INTO pending_reversal_settlement (
                reversal_id, amount, entry_date, username
            ) VALUES (
                %s, %s, NOW(), %s)
            """, (reversal_id, reversal['balance'], R.session['username']))
        R.db.commit()

        self._res.redirect("/view_trans?trans_id=%s&m=cgr", reversal['trans_id'])

application = Program.app
