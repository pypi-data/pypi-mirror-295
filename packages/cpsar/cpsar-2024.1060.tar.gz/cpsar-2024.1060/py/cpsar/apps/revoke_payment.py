import cpsar.runtime as R
import cpsar.txlib 
import cpsar.ws as W

class Program(W.GProgram):
    def main(self):
        pid = self.fs.getvalue('payment_id')
        trans_id = cpsar.txlib.remove_payment(pid)

        if not trans_id:
            return self._res.redirect("/")

        R.db.commit()
        self._res.redirect("/view_trans?trans_id=%s&m=rp", trans_id)

application = Program.app
