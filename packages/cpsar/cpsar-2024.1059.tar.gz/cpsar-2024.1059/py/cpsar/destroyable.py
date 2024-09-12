""" Destroyable Transaction Trait

This is almost an experiment in OO Design. All of these methods could have
easily been defined on the transaction class in txlib but in an attempt to
divide and conquer, I have put all of the functionality here. You should mix
in the Destroyable class with your own transaction class. Your class must also
inherit from cpsar.txlib.Transaction
"""
import cpsar.runtime as R
import cpsar.txlib as T

class Destroyable:
    """ I am a transaction that can be destroyed! GRRR!! I am not nice!
    Mix Me into your transaction.
    """

    def invoice_has_other_batches(self):
        """ We probably don't want to blow away the invoice record if the
        invoice id has transactions for other batches. This method returns
        True if the transaction's invoice has transactions with different
        batch dates than this transaction. False if not.
        """
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT COUNT(*)
            FROM trans
            WHERE invoice_id=%s AND batch_date <> %s
            """, (self.invoice_id, self.batch_date))
        return cursor.fetchone()[0]

    def destroy_invoice(self):
        """ the invoice associated with the transaction must die!
        """
        cursor = R.db.cursor()
        cursor.execute("""
            DELETE FROM invoice WHERE invoice_id=%s
            """, (self.invoice_id,))

    def _error(self, msg, *args):
        """ Report an error on this transaction. """
        if args: msg %= args
        R.log.error(msg)
        self.errors.append(msg)

    def destroy(self):
        """ I am the harbinger of death to the transaction. Call me at your
        own peril. Call this method to completely eradicate the transaction
        from the entire system. No trace will be left!
        """
        cursor = R.db.cursor()
        cursor.execute("""
            DELETE FROM distribution
            WHERE trans_id=%s
            """, (self.trans_id,))

        cursor.execute("""
            DELETE FROM trans_log
            WHERE trans_id=%s
            """, (self.trans_id,))

        cursor.execute("""
            DELETE FROM trans
            WHERE trans_id=%s
            """, (self.trans_id,))

        cursor.execute("""
            UPDATE reversal SET trans_id=NULL
            WHERE trans_id=%s
            """, (self.trans_id,))

        cursor.execute("""
            DELETE FROM pk_trans_sup
            WHERE trans_id=%s
            """, (self.trans_id,))

    def approve_destruction(self):
        """ Approve the destruction of the transaction. Returns a list of
        problems with destruction. If the empty list is returned, then the
        transaction is safe to destroy.
        """
        tref_cache.reset(self.trans_id)

        # Be sure no payments have been made on this transaction. 
        tref_cache.check(
            'trans_payment', 
            'Transaction %s has %s payments. Cannot update')
        tref_cache.check(
            'trans_adjudication',
            'Transaction %s has %s adjudications. Cannot update')
        tref_cache.check(
            'trans_writeoff',
            'Transaction %s has %s writeoffs. Cannot update')

        # Be sure the transaction has never been reconciled
        tref_cache.check(
            'distribution',
            'Transaction %s has %s distributed distributions')

        # Be sure no reversal settlements have been made
        tref_cache.check(
            'reversal_settlement',
            'Transaction %s has %s reversal settlement')

        # Be sure nothing has been reported to the state
        tref_cache.check(
            'state_report_entry',
            'Transaction %s has %s state report entries')

        return tref_cache.problems

class TransReferenceCache:
    """ I am a cache that stores the number of foreign references of trans_id's
    on other tables. We don't delete transactions if they have FK's in other
    places.
    """
    trans_id = None
    problems = []
    def __init__(self):
        self._cache = {}


    def reset(self, trans_id):
        self.trans_id = trans_id
        self.problems = []

    def check(self, table, err_tmpl):
        if table not in self._cache:
            self._populate_cache(table)
        hits = self._cache[table].get(self.trans_id, 0)
        if hits:
            self.problems.append(err_tmpl % (self.trans_id, hits))
        return hits

    def _populate_cache(self, table):
        cursor = R.db.cursor()
        if table == 'distribution':
            sql = """
                SELECT trans_id, COUNT(*)
                FROM distribution
                WHERE distribution_date IS NOT NULL
                GROUP BY trans_id"""
        elif table == 'reversal_settlement':
            sql = """
                SELECT reversal.trans_id,
                       COUNT(*)
                FROM reversal
                JOIN reversal_settlement USING(reversal_id)
                GROUP BY reversal.trans_id
            """
        else:
            sql = """
                SELECT trans_id, COUNT(*)
                FROM %s
                GROUP BY trans_id
                """ % table
        cursor.execute(sql)
        self._cache[table] = dict(cursor)


tref_cache = TransReferenceCache()


