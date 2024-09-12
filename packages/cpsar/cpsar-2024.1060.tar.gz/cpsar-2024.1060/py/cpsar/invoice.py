import glob
import os

import cpsar.runtime as R

def check(invoice_id):
    check_total(invoice_id)
    check_adjustments(invoice_id)
    check_balance(invoice_id)

def check_total(invoice_id):
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT invoice.total,
               SUM(trans.total)
        FROM invoice
        JOIN trans ON
            invoice.invoice_id = %s AND
            invoice.invoice_id = trans.invoice_id
        GROUP BY invoice.total
        """, (invoice_id,))
    if not cursor.rowcount:
        return
    given, calc = cursor.fetchone()
    if given != calc:
        cursor.execute("""
            UPDATE invoice SET total=%s
            WHERE invoice_id=%s
            """, (calc, invoice_id))
        return True

def check_adjustments(invoice_id):
    """ invoice.adjusments = SUM(trans.adjustments) """
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT invoice.adjustments,
               COALESCE(SUM(trans.adjustments), 0)
        FROM invoice
        JOIN trans ON invoice.invoice_id = trans.invoice_id AND
            invoice.invoice_id = %s
        GROUP BY invoice.invoice_id, invoice.adjustments
        """,
        (invoice_id,))

    if not cursor.rowcount:
        return
    given, calc = cursor.fetchone()
    if given != calc:
        cursor.execute("""
            UPDATE invoice SET adjustments=%s
            WHERE invoice_id=%s
            """, (calc, invoice_id))
        return True

def check_balance(invoice_id):
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT invoice.balance,
               SUM(trans.balance)
        FROM invoice
        JOIN trans ON
            invoice.invoice_id = %s AND
            invoice.invoice_id = trans.invoice_id
        GROUP BY invoice.balance
        """, (invoice_id,))
    if not cursor.rowcount:
        return
    given, calc = cursor.fetchone()
    if given != calc:
        cursor.execute("""
            UPDATE invoice SET balance=%s
            WHERE invoice_id=%s
            """, (calc, invoice_id))
        return True


