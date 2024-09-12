from cpsar import ajson as json
from cpsar.runtime import db
from cpsar.txlib import BusinessError, Transaction
from cpsar import ws

class Program(ws.GProgram):
    def main(self):
        fs = self.fs

        trans_id = fs.getvalue('trans_id')
        t = Transaction(trans_id)
        if not t.record:
            self._reply("trans not found")
            return

        lic_number = fs.getvalue("lic_number", "")

        cursor = db.cursor()
        cursor.execute("""
            update trans set doctor_state_lic_number = %s
            where trans_id = %s
            """, (lic_number, trans_id))
        db.commit()
        self._reply()

    def _reply(self, *errs):
        self._res.content_type = 'application/json'
        self._res.write(json.write({'errors': list(errs)}))


application = Program.app
