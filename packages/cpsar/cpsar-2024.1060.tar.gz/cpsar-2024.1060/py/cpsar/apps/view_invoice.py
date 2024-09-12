import os

import cpsar.pg
import cpsar.runtime as R
import cpsar.ws as W

class Program(W.MakoProgram):
    def main(self):
        try:
            invoice_id = int(self.fs.getvalue('invoice_id', ''))
        except ValueError:
            R.flash('no invoice id')
            return self._res.redirect("/")

        cursor = R.db.dict_cursor()
        doc = {}

        invoice_id = int(self.fs.getvalue('invoice_id'))
        cursor.execute("""
            SELECT *
            FROM invoice
            WHERE invoice_id=%s
            """, (invoice_id,))
        
        invoice = cpsar.pg.one(cursor)
        assert invoice
        doc['invoice'] = invoice

        if invoice['patient_id']:
            cursor.execute("SELECT * FROM patient WHERE patient_id=%s",
                (invoice['patient_id'],))
            doc['patient'] = cpsar.pg.one(cursor)

        cursor.execute("""
            SELECT *
            FROM client
            WHERE group_number=%s""",
            (invoice['group_number'],))
        doc['client'] = cpsar.pg.one(cursor)
        cursor.execute("""
            SELECT trans.*,
                   patient.first_name,
                   patient.last_name,
                   drug.name as drug_name
            FROM trans
            LEFT JOIN drug ON
                 trans.drug_id = drug.drug_id
            LEFT JOIN patient ON
                 trans.patient_id = patient.patient_id
            WHERE
                 trans.invoice_id = %s
            ORDER BY line_no
        """, (invoice_id,))
        doc['transactions'] = cpsar.pg.all(cursor)
        self.tmpl.update(doc)

application = Program.app
