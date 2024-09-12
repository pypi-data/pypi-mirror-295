from cpsar import runtime as R
from cpsar import txlib
from cpsar import ws

class Program(ws.GProgram):
    """ Relink the doctor ID on the trans and history records based off the DEA and NPI
    numbers on the history record. This was fixed implemented when we migrated from
    blue-doctor to doctor, in the even of some mix up of doctor id's.
    """

    ## Form Data
    @property
    def trans_id(self):
        try:
            return int(self.fs.getvalue('trans_id'))
        except (TypeError, ValueError):
            return None

    ## Action Handlers
    def main(self):
        if not self.trans_id:
            self._res.write("No transaction given")
            return 

        cursor = R.db.cursor()
        cursor.execute("""
            select history.doctor_dea_number,
                   history.doctor_npi_number,
                   history.history_id,
                   history.doctor_id,
                   trans.doctor_id
            from history
            join trans using(history_id)
            where trans_id = %s
            """, (self.trans_id,))
        if not cursor.rowcount:
            raise ws.HTTPNotFound("%s" % self.trans_id)

        dea, npi, history_id, history_doctor_id, trans_doctor_id = next(cursor)
        keys = set()
        for key in [dea, npi]:
            if not key:
                continue
            cursor.execute("""
                select doctor_id from doctor_key
                where doc_key = %s
                """, (key,))
            if not cursor.rowcount:
                continue
            keys.add(next(cursor)[0])

        if not keys:
            R.error("No doctors could be found with the DEA: %s or NPI: %s" % (dea, npi))
            self.redirect_to_trans()
            return

        if len(keys) > 1:
            R.error("Different doctor id are assigned to the DEA %s and NPI %s" % (dea,npi))
            self.redirect_to_trans()
            return

        doctor_id = keys.pop()
        if doctor_id == trans_doctor_id and doctor_id == history_doctor_id:
            R.flash("Doctor ID %s verified. No updated needed.", doctor_id)
            self.redirect_to_trans()
            return

        if doctor_id != trans_doctor_id:
            cursor.execute("""
                update trans set doctor_id=%s
                where trans_id=%s
                """, (doctor_id, self.trans_id))
            txlib.log(self.trans_id,"Updated trans doctor_id from %s to %s" % (trans_doctor_id, doctor_id))
        if doctor_id != history_doctor_id:
            cursor.execute("""
                update history set doctor_id=%s
                where history_id=%s
                """, (doctor_id, history_id))
            txlib.log(self.trans_id,"Updated history doctor_id from %s to %s" % (history_doctor_id, doctor_id))

        R.flash("Doctor successfully relinked to ID %s" % doctor_id)
        R.db.commit()
        self.redirect_to_trans()

    def redirect_to_trans(self):
        self.redirect("/view_trans?trans_id=%s" % self.trans_id)

application =  Program.app
