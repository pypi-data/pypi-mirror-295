import cpsar.runtime as R
import cpsar.txlib
import cpsar.ws as W

class Program(W.GProgram):
    def main(self):
        try:
            wid = int(self.fs.getvalue('writeoff_id'))
        except (TypeError, ValueError):
            self._res.write("writeoff %s not found" % wid)
            return

        cpsar.txlib.revoke_writeoff(wid)
        R.db.commit()
        R.flash("Writeoff revoked")
        self._res.redirect(self._req.referer)

application = Program.app
