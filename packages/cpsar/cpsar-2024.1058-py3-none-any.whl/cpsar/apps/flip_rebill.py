import cpsar.runtime as R
import cpsar.ws as W

class Program(W.GProgram):
    def main(self):
        trans_id = self.fs.getvalue('trans_id')
        assert trans_id

        cursor = R.db.cursor()
        cursor.execute("""
            UPDATE trans SET rebill=NOT rebill WHERE trans_id=%s
        """, (trans_id,))
        R.db.commit()

        self._res.redirect("/view_trans?trans_id=%s", trans_id)

application = Program.app
