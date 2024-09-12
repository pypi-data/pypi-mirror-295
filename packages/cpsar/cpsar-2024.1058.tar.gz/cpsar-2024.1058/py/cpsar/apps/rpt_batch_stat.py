import os

import cpsar.runtime as R
from cpsar import pg
from cpsar import util
from cpsar import ws

class Program(ws.MakoProgram):
    def main(self):
        if self.fs.getvalue('reset_invoice_print_time'):
            self.reset_invoice_print_time()

    @property
    def batch_file_id(self):
        return self.fs.getvalue('batch_file_id')

    @property
    @util.imemoize
    def batch(self):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            select * from batch_file where batch_file_id=%s
            """, (self.batch_file_id,))
        return pg.one(cursor)

    def trans_totals(self):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT
                COUNT(trans.trans_id) AS "TX Count",
                COUNT(t1.trans_id) AS "Paid Count",
                SUM(trans.cost_allowed) as "Cost Allowed",
                SUM(trans.adjustments) as "Adjustments",
                SUM(trans.total) AS "Billed",
                SUM(trans.balance) AS "Balance",
                MIN(trans.rx_date) AS "Oldest RX Date",
                MAX(trans.rx_date) AS "Newest RX Date",
                COUNT(patnull.trans_id) AS "Unlinked Patient Count",
                COUNT(pharmnull.trans_id) AS "Unlinked Pharmacy Count",
                COUNT(docnull.trans_id) AS "Unlinked Doctor Count"
            FROM trans
            LEFT JOIN trans AS t1 ON
                trans.trans_id = t1.trans_id AND
                t1.balance = 0
            LEFT JOIN trans AS patnull ON
                trans.trans_id = patnull.trans_id AND
                patnull.patient_id IS NULL
            LEFT JOIN trans AS pharmnull ON
                trans.trans_id = pharmnull.trans_id AND
                pharmnull.pharmacy_id IS NULL
            LEFT JOIN trans AS docnull ON
                trans.trans_id = docnull.trans_id AND
                docnull.doctor_id IS NULL
            WHERE trans.batch_file_id = %s
            """, (self.batch_file_id,))

        return pg.one(cursor)

    def reset_invoice_print_time(self):
        cursor = R.db.cursor()
        cursor.execute("""
            update batch_file set invoice_print_time = NULL
            where batch_file_id = %s
            """, (self.batch_file_id,))
        os.system("bd-run ar-inv-print")
        R.flash("Print file recreated")

application = Program.app
