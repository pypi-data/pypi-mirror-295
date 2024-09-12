#!/usr/bin/env python
import cpsar.ws as W
import cpsar.runtime as R
import cpsar.txlib

class Program(W.GProgram):

    def main(self):
        fs = self.fs
        cursor = R.db.cursor()

        trans_id = fs.getvalue('trans_id')
        cursor.execute("SELECT state_fee FROM trans WHERE trans_id=%s",
                       (trans_id,))
        if not cursor.rowcount:
            return self._res.redirect("/")
        osfs = cursor.fetchone()[0]
        sfs = fs.getvalue('state_fee', '').replace("$", "")
        if not sfs:
            return self._res.redirect("/view_trans?trans_id=%s", trans_id)
        cursor.execute("""
            UPDATE trans SET state_fee=%s
            WHERE trans_id=%s
            """, (sfs, trans_id))
        cpsar.txlib.log(
            trans_id, "Updated state fee schedule from %s to %s" % (
                        osfs, sfs))
                           
        cpsar.txlib.check(trans_id)
        R.db.commit()
        self._res.redirect("/view_trans?trans_id=%s", trans_id)

application = Program.app
