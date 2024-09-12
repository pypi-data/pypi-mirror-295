import decimal
from cpsar import ajson as json
from cpsar.runtime import db
import cpsar.runtime as R
from cpsar import txlib
from cpsar import ws

class Program(ws.GProgram):
    def main(self):
        fs = self.fs
        trans_id = fs.getvalue('trans_id')
        if not trans_id:
            R.error("No trans id given")
            return self.reply()

        batch_file_id = fs.getvalue('batch_file_id') or None
        if batch_file_id:
            try:
                batch_file_id = int(batch_file_id)
            except ValueError:
                R.error("Invalid batch file id %s" % batch_File_id)
                return self.reply()

        cursor = db.cursor()

        cursor.execute("select reversal_id from reversal where trans_id=%s",
            (trans_id,))
        if not cursor.rowcount:
            R.error("No reversal found for trans %s" % trans_id)
            return
        reversal_id, = next(cursor)

        cursor.execute("""
            update reversal set batch_file_id = %s
            where reversal_id = %s
            """, (batch_file_id, reversal_id))
        db.commit()
        self.reply()

    def reply(self):
        lb = self.fs.getvalue('linkback')
        if lb:
            for er in R.get_errors():
                R.flash(err)
            self.redirect(lb)
        else:
            self._res.content_type = 'application/json'
            self._res.write(json.write({'errors': list(R.get_errors())}))

application = Program.app
