
#!/usr/bin/env python
import cpsar.ws as W
import cpsar.runtime as R
import cpsar.txlib

class Program(W.GProgram):

    def main(self):
        fs = self.fs
        cursor = R.db.cursor()

        trans_id = fs.getvalue('trans_id')
        cursor.execute("SELECT history_id FROM trans WHERE trans_id=%s",
                       (trans_id,))
        if not cursor.rowcount:
            raise ValueError('blah')
            return self._res.redirect("/")
        history_id = cursor.fetchone()[0]

        cursor.execute("SELECT temp_sr_ndc_override FROM history WHERE history_id=%s",
                       (history_id,))
        if not cursor.rowcount:
            raise ValueError('blah2')
            return self._res.redirect("/")
        old_ndc = cursor.fetchone()[0]
        new_ndc = fs.getvalue('temp_sr_ndc_override', '')
        
        new_ndc = new_ndc.replace("$", "").strip() or None

        cursor.execute("""
            UPDATE history SET temp_sr_ndc_override=%s
            WHERE history_id =%s
            """, (new_ndc, history_id))

        cpsar.txlib.log(
            trans_id, "Updated Temporary NDC Override from %s to %s" % (
                        old_ndc, new_ndc))
                           
        cpsar.txlib.check(trans_id)
        R.db.commit()
        self._res.redirect("/view_trans?trans_id=%s", trans_id)

application = Program.app
