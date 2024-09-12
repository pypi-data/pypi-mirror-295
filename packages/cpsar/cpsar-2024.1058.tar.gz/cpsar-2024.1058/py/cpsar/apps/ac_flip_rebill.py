import cpsar.ajson as J
import cpsar.runtime as R
import cpsar.ws as W

class Program(W.GProgram):
    def main(self):
        trans_id = self.fs.getlist('trans_id')
        self._errors = []
        self._change_rebill_flag(trans_id)
        self._res.content_type = 'application/json'
        self._res.write(J.write({'errors': self._errors}))
        R.db.commit()

    def _change_rebill_flag(self, trans_ids):
        if not trans_ids:
            self._errors.append("No transactions given")
            return 

        frag = ["%s"] * len(trans_ids)
        frag = ", ".join(frag)
        trans_ids = tuple(trans_ids)

        cursor = R.db.cursor()
        cursor.execute("""
            UPDATE trans SET rebill=NOT rebill
            WHERE trans_id IN (%s)
        """ % frag, trans_ids)

application = Program.app
