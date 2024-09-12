import cpsar.ws as W
import cpsar.txlib
import cpsar.runtime as R

class Program(W.GProgram):
    def main(self):
        trans_id = int(self.fs.getvalue('trans_id'))

        cpsar.txlib.check(trans_id)
        R.db.commit()
        
        R.flash('Transaction Values Checked')
        self._res.redirect('/view_trans?trans_id=%s', trans_id)

application = Program.app
