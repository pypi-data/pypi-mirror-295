import cpsar.runtime as R
import cpsar.txlib
import cpsar.ws as W

class Program(W.GProgram):
    def main(self):
        did = self.fs.getvalue('distribution_id')
        assert did

        trans_id = cpsar.txlib.remove_distribution(did)
        if not trans_id:
            return

        if R.has_errors():
            self._res.error(", ".join(R.get_errors()))
        else:
            self._res.error("Distribution Deleted")
            R.db.commit()

        self.redirect("/view_trans?trans_id=%s", trans_id)

application = Program.app
