""" Generate a SCSAF Data file based on a rebill. """
import cpsar.ws as W
import cpsar.runtime as R

class Program(W.GProgram):
    def main(self):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT trans_id, patient.patient_id, patient.first_name,
                   patient.last_name, history.rx_number, history.refill_number,
                   drug.name AS drug_name
            FROM trans
            JOIN history ON trans.history_id = history.history_id
            JOIN patient ON history.patient_id = patient.patient_id
            JOIN drug ON history.drug_id = drug.drug_id
            WHERE trans.rebill=TRUE AND
                  trans.group_number IN ('56600', '70300', '70303', '70483', '70081', '70888', '70891')
            """)

        if not cursor.rowcount:
            self._res.write("""There are currently no transactions for group 56600
                     marked for rebill. Please mark some transactions
                     from the transactions screen.""")
            return
        self._res.write("""<p>The following %s transactions are marked for rebill. Click
                 <a href="edi_scsaf_send">Here</a> to generate a new SCASF EDI
                 file and send it to SCSAF's server.</p>
              """ % cursor.rowcount)

        self._res.write("""<table class='grid'>
        <tr>
            <th>Trans #</th>
            <th>Patient</th>
            <th>Rx #</th>
            <th>Drug</th>
        </tr>
        
        """)
        for rec in cursor:
            self._res.write("""<tr>
                <td>%(trans_id)s</td>
                <td><a href='/patient?patient_id=%(patient_id)s'>
                    %(first_name)s %(last_name)s</a></td>
                <td><a href='/view_trans?trans_id=%(trans_id)s'>
                        %(rx_number)s-%(refill_number)s</a></td>
                <td>%(drug_name)s</td>
                </tr>""" % rec)
        self._res.write("</table>")
 
application = Program.app
