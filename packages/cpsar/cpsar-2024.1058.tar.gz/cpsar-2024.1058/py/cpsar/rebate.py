import cpsar.runtime as R

from cpsar.txlib import BusinessError, log
from cpsar.util import insert_sql, imemoize

def for_trans_id(trans_id):
    cursor = R.db.dict_cursor()
    cursor.execute("""
        SELECT *
        FROM rebate
        WHERE trans_id=%s
        """, (trans_id,))
    if not cursor.rowcount:
        return None
    return Rebate(cursor.fetchone())

def by_id(rebate_id):
    cursor = R.db.dict_cursor()
    cursor.execute("""
        SELECT *
        FROM rebate
        WHERE rebate_id=%s
        """, (rebate_id,))
    if not cursor.rowcount:
        return None
    return Rebate(cursor.fetchone())

def credit_by_id(credit_id):
    cursor = R.db.dict_cursor()
    cursor.execute("""
        SELECT * FROM rebate_credit
        WHERE rebate_credit_id = %s
        """, (credit_id,))
    if not cursor.rowcount:
        return None
    return RebateCredit(cursor.fetchone())

class RebateCredit(object):
    def __init__(self, rec):
        self.trans_id = rec['trans_id']
        self.rebate_credit_id = rec['rebate_credit_id']
        self.void_date = rec['void_date']
        self.amount = rec['amount']
        self.rebate_id = rec['rebate_id']

    def unvoid(self):
        if not self.void_date:
            a = self.rebate_credit_id
            raise BusinessError("Credit %s is not voided" % a)
        cursor = R.db.dict_cursor()
        cursor.execute("""
            UPDATE rebate_credit SET void_date=NULL
            WHERE rebate_credit_id=%s
            """, (self.rebate_credit_id,))
        log(self.trans_id, "Unvoided rebate credit %s" % self.rebate_credit_id)
        self._inc_dep_tables()

    def void(self, void_date):
        if self.void_date:
            a = (self.rebate_credit_id, self.void_date)
            raise BusinessError("Credit %s already voided on %s" % a)
        cursor = R.db.dict_cursor()
        cursor.execute("""
            UPDATE rebate_credit SET void_date=%s
            WHERE rebate_credit_id=%s
            """, (void_date, self.rebate_credit_id))
        log(self.trans_id, "Voided rebate credit for %s" % self.amount)
        self._adj_dep_tables()

    def revoke(self):
        cursor = R.db.cursor()
        cursor.execute("""
            DELETE FROM rebate_credit
            WHERE rebate_credit_id = %s
            """, (self.rebate_credit_id,))
        log(self.trans_id, "Revoked rebate credit for %s" % self.amount)
        self._adj_dep_tables()

    def _adj_dep_tables(self):
        cursor = R.db.cursor()
        a = self.amount
        cursor.execute("""
         UPDATE trans SET rebate_credit_total = rebate_credit_total - %s,
                          adjustments = adjustments + %s,
                          balance = balance + %s
         WHERE trans_id=%s
         """, (a, a, a, self.trans_id))
        cursor.execute("""
         UPDATE invoice SET balance = invoice.balance + %s
         FROM trans
         WHERE trans.trans_id = %s
           AND invoice.invoice_id = trans.invoice_id
         """, (a, self.trans_id))
        cursor.execute("""
         UPDATE rebate SET client_balance = client_balance + %s
         WHERE rebate_id = %s
         """, (a, self.rebate_id))

    def _inc_dep_tables(self):
        cursor = R.db.cursor()
        a = self.amount
        cursor.execute("""
         UPDATE trans SET rebate_credit_total = rebate_credit_total + %s,
                          adjustments = adjustments - %s,
                          balance = balance - %s
         WHERE trans_id=%s
         """, (a, a, a, self.trans_id))
        cursor.execute("""
         UPDATE invoice SET balance = invoice.balance - %s
         FROM trans
         WHERE trans.trans_id = %s
           AND invoice.invoice_id = trans.invoice_id
         """, (a, self.trans_id))
        cursor.execute("""
         UPDATE rebate SET client_balance = client_balance - %s
         WHERE rebate_id = %s
         """, (a, self.rebate_id))

def rebates_with_balances_for(trans_id):
    """ All of the rebates that have balances that can be used on the
    given trans_id
    """
    cursor = R.db.dict_cursor()
    cursor.execute("""
     WITH p AS (SELECT patient_id FROM trans WHERE trans_id=%s)
     SELECT rebate.*
     FROM rebate
     JOIN trans USING(trans_id)
     JOIN p USING(patient_id)
     ORDER BY rebate.trans_id
        """, (trans_id,))
    return map(Rebate, cursor)

class Rebate(object):
    def __init__(self, dbrec):
        self.rebate_id = dbrec['rebate_id']
        self.trans_id = dbrec['trans_id']
        self.entry_date = dbrec['entry_date']
        self.total_amount = dbrec['total_amount']
        self.client_amount = dbrec['client_amount']
        self.client_balance = dbrec['client_balance']

    def credit_trans(self, trans_id, amount, username):
        if amount > self.client_balance:
            e = "Insufficient balance of %s on rebate"
            raise BusinessError(e % self.client_balance)
        cursor = R.db.cursor()
        # Ensure that the trans is for the same patient
        cursor.execute("""
         SELECT patient_id, balance FROM trans WHERE trans_id=%s
         """, (trans_id,))
        if not cursor.rowcount:
            raise BusinessError("trans %s not found" % trans_id)
        patient_id,trans_balance = cursor.fetchone()
        if patient_id != self.patient_id:
            m = "cannot apply rebate credit on different patient"
            raise BusinessError(m)
        if amount > trans_balance:
            m = "trans balance not large enough for %s credit" % amount
            raise BusinessError(m)

        sql = insert_sql("rebate_credit", dict(
            rebate_id=self.rebate_id,
            trans_id=trans_id,
            amount=amount,
            username=username
        ))
        cursor.execute(sql)

        # Decrease the rebate balance
        cursor.execute("""
          UPDATE rebate SET client_balance = client_balance - %s
          WHERE rebate_id=%s
          """, (amount, self.rebate_id))
        self.client_balance -= amount

        # Decrease the trans balance
        cursor.execute("""
          UPDATE trans SET balance = balance - %s
          WHERE trans_id=%s
          """, (amount, trans_id))

    @property
    @imemoize
    def patient_id(self):
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT patient_id
            FROM trans
            WHERE trans_id=%s
            """, (self.trans_id,))
        if not cursor.rowcount:
            return None
        return cursor.fetchone()[0]

def has_rebate_funds_available(trans_id):
    """ Are there any rebate monies that are available to credit
    the given transaction?
    """
    cursor = R.db.cursor()
    cursor.execute("""
     WITH p AS (SELECT patient_id FROM trans WHERE trans_id=%s)
     SELECT COALESCE(SUM(client_balance), 0)
     FROM rebate
     JOIN trans USING(trans_id)
     JOIN p USING(patient_id)
        """, (trans_id,))
    amt = cursor.fetchone()[0]
    return amt > 0
