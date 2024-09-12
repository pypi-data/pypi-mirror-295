import datetime
import decimal

import cpsar.runtime as R
import cpsar.util as U
import cpsar.ws as W

from cpsar import txlib

class Program(W.GProgram):
    def main(self):
        fs = self.fs
        try:
            trans_id = int(fs.getvalue('trans_id'))
            invoice_id = int(fs.getvalue("invoice_id"))
        except (ValueError, TypeError):
            return

        cursor = R.db.cursor()
        cursor.execute("select invoice_id, group_number, patient_id from trans where trans_id=%s", (trans_id,))
        old_invoice_id, group_number, patient_id = next(cursor)

        cursor.execute("select patient_id from invoice where invoice_id=%s", (invoice_id,))
        if cursor.rowcount:
            current_patient_id, = next(cursor)
            if current_patient_id != patient_id:
                R.flash("Cannot change invoice id because the new invoice is for another patient")
                return self._res.redirect(self._req.referer)
        cursor.execute("update trans set invoice_id=%s where trans_id=%s", (invoice_id, trans_id))
        cursor.execute("""
    with v as (
      SELECT
               trans.invoice_id,
               trans.group_number,
               MIN(trans.batch_date) as batch_date,
               trans.patient_id,
               client.memo,
               MIN(trans.create_date) + INTERVAL '1 day' * client.due_date_days as due_date,
               SUM(trans.total) as total,
               SUM(trans.balance) as balance,
               SUM(trans.adjustments) as adjustments,
               COUNT(trans.trans_id) as item_count
        FROM trans
        JOIN client ON
             client.group_number = trans.group_number
        LEFT JOIN invoice ON
             trans.invoice_id = invoice.invoice_id
        WHERE trans.invoice_id=%s
        GROUP BY trans.invoice_id, trans.group_number,
                 trans.patient_id, client.memo, client.due_date_days
    )
    UPDATE invoice set total=v.total,balance=v.balance,adjustments=v.adjustments,item_count=v.item_count
    from v where v.invoice_id = invoice.invoice_id
    """, (old_invoice_id,))

        cursor.execute("""
    with v as (
      SELECT
               trans.invoice_id,
               trans.group_number,
               MIN(trans.batch_date) as batch_date,
               trans.patient_id,
               client.memo,
               MIN(trans.create_date) + INTERVAL '1 day' * client.due_date_days as due_date,
               SUM(trans.total) as total,
               SUM(trans.balance) as balance,
               SUM(trans.adjustments) as adjustments,
               COUNT(trans.trans_id) as item_count
        FROM trans
        JOIN client ON
             client.group_number = trans.group_number
        LEFT JOIN invoice ON
             trans.invoice_id = invoice.invoice_id
        WHERE trans.invoice_id=%s
        GROUP BY trans.invoice_id, trans.group_number,
                 trans.patient_id, client.memo, client.due_date_days
    )

    INSERT INTO invoice (invoice_id, group_number, batch_date, patient_id, memo,
                     due_date, total, balance, adjustments, item_count)
    SELECT * FROM V
    ON CONFLICT (invoice_id) DO UPDATE SET
        total=EXCLUDED.total,
        balance=EXCLUDED.balance,
        adjustments=EXCLUDED.adjustments,
        item_count=EXCLUDED.item_count
        """, (invoice_id,))

        txlib.log(trans_id, f"Invoice id changed from {old_invoice_id} to {invoice_id}")
        R.db.commit()
        R.flash("Invoice number changed")
        self._res.redirect(self._req.referer)

application = Program.app




