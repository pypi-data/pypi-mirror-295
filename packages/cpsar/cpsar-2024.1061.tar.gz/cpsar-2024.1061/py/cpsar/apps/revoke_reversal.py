import cpsar.runtime as R
import cpsar.txlib 
import cpsar.ws as W

class Program(W.GProgram):
    def main(self):
        trans_id = self.fs.getvalue('trans_id')
        cpsar.txlib.revoke_reversal(trans_id)
        if R.has_errors():
            for error in R.get_errors():
                self._res.write("<div>%s</div>" % error)
            return
        R.db.commit()
        R.flash("Reversal revoked")
        self._res.redirect("/view_trans?trans_id=%s", trans_id)

application = Program.app
