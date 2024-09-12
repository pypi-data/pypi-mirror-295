#!/usr/bin/env python
import cpsar.ws as W
import cpsar.runtime as R
import cpsar.txlib

class Program(W.GProgram):

    @property
    def trans_id(self):
        return int(self.fs.getvalue('trans_id'))

    @property
    def lic_number(self):
        return self.fs.getvalue('lic_number', '').strip()

    @property
    def lic_state(self):
        return self.fs.getvalue('lic_state')

    def main(self):
        cursor = R.db.cursor()
        if not self.lic_number:
            return self.unlink()
        cursor.execute("""
            select pharmacist_id
            from pharmacist
            where lic_state = %s and lic_number = %s
            """, (self.lic_state, self.lic_number))
        if cursor.rowcount:
            pharmacist_id, = next(cursor)
        else:
            cursor.execute("""
                insert into pharmacist (lic_state, lic_number)
                values (%s, %s)
                returning pharmacist_id
                """, (self.lic_state, self.lic_number))
            pharmacist_id, = next(cursor)

        cursor.execute("""
          UPDATE history SET
            pharmacist_id=%s,
            cps_lic_state=%s,
            cps_lic_number=%s
          FROM trans
          WHERE trans.trans_id=%s
            AND trans.history_id=history.history_id
            """, (pharmacist_id, self.lic_state, self.lic_number, self.trans_id))

        msg = "Pharmcist overriden to %s:%s" % (self.lic_state, self.lic_number)
        cpsar.txlib.check(self.trans_id)
        cpsar.txlib.log(self.trans_id, msg)
        R.db.commit()
        R.flash(msg)
        self._res.redirect("/view_trans?trans_id=%s", self.trans_id)

    def unlink(self):
        cursor = R.db.cursor()
        cursor.execute("""
            update history set pharmacist_id = NULL
            from trans
            where trans.history_id = history.history_id
              and trans.trans_id = %s
              """, (self.trans_id,))
        msg = "Pharmcist unlinked"
        cpsar.txlib.check(self.trans_id)
        cpsar.txlib.log(self.trans_id, msg)
        R.db.commit()
        R.flash(msg)
        self._res.redirect("/view_trans?trans_id=%s", self.trans_id)

application = Program.app
