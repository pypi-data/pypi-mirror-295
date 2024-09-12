import cpsar.runtime as R
import cpsar.ws as W
import cpsar.txlib

class Program(W.GProgram):
    def main(self):
        try:
            aid = int(self.fs.getvalue('adjudication_id'))
        except (TypeError, ValueError):
            self._res.write("Adjudication %s not found" %
                self.fs.getvalue('adjudication_id'))
        cpsar.txlib.remove_adjudication(aid)
        R.db.commit()
        R.flash("Adjudication revoked")
        self._res.redirect(self._req.referer)

application = Program.app
