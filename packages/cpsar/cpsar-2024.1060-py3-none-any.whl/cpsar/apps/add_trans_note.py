import cpsar.runtime as R
import cpsar.ws as W

from cpsar import txlib

class Program(W.GProgram):
    def main(self):
        note = self.fs.getvalue('note')
        if not note:
            self._res.write("No note given")
            return
        try:
            trans_id = int(self.fs.getvalue('trans_id'))
        except (ValueError, TypeError):
            self._res.write("trans not found" % self.fs.getvalue('trans_id'))
            return

        txlib.log(trans_id, note)
        R.db.commit()
        self._res.redirect('/view_trans?trans_id=%s', trans_id)

application = Program.app
