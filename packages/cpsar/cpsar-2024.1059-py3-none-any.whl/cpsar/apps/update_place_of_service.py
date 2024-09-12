
import cpsar.ws as W
import cpsar.runtime as R
from cpsar import util

class Program(W.GProgram):
    def main(self):
        fs = self.fs 
        cursor = R.db.cursor()
        trans_id = fs.getvalue("trans_id")
        if not trans_id:
            self._res.redirect("/")
            return

        cursor.execute("""
            select history_id
            from trans
            where trans_id=%s
            """, (trans_id,))
        if not cursor.rowcount:
            self._res.redirect("/")

        history_id, = next(cursor)

        pos = fs.getvalue("place_of_service", "").strip()
        if not pos:
            pos = None

        cursor.execute("""
            select pharmacy_id
            from pharmacy
            where npi = %s or nabp = %s
            """, (pos, pos))
        if cursor.rowcount:
            id, = next(cursor)
        else:
            id = None

        cursor.execute("""
            update history set place_of_service=%s, place_of_service_id=%s
            where history_id=%s
            """, (pos, id, history_id))

        R.db.commit()
        R.flash("Place of service update successful")
        self._res.redirect("/view_trans?trans_id=%s", trans_id)

application = Program.app
