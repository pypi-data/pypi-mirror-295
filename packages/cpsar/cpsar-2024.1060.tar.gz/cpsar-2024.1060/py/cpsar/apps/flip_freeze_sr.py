import cpsar.runtime as R
import cpsar.ws as W

class Program(W.GProgram):
    def main(self):
        trans_id = self.fs.getvalue('trans_id')
        assert trans_id

        cursor = R.db.cursor()
        cursor.execute("""
            UPDATE trans SET freeze_sr_entry=NOT freeze_sr_entry WHERE trans_id=%s
            RETURNING freeze_sr_entry
        """, (trans_id,))

        freeze, = cursor.fetchone()
        if freeze:
            R.flash("State report entry communication with agency frozen")
        else:
            R.flash("State report entry communication with agency unfrozen")
        R.db.commit()
        self._res.redirect("/view_trans?trans_id=%s", trans_id)

application = Program.app
