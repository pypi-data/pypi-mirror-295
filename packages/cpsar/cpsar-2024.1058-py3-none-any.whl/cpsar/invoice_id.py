""" Provides objects which assign invoice ids and line numbers to transaction
records. L{InvoiceKeyMaker} should be used for new transactions while
L{RebillInvoiceKeyMaker} should be used for rebilled transactions, since these
two kinds of transactions have invoice_id's in different ranges.

Example usage:

    >>> maker = InvoiceKeyMaker()
    >>> tx = {
            'patient_id': 1,
            'doi': '2012-01-01',
            'group_number': '1111111',
            'pharmacy_nabp': '1111111'}
    >>> maker.assign(tx)
"""
from __future__ import print_function
import cpsar.runtime as R
from cpsar.util import memoize

STARTING_REBILL_INVOICE_ID = 8000000

class InvoiceKeyMaker(object):
    """ Creates new invoice id's and line numbers for transaction records.
    This object does not persist newly selected invoice id's to the database.
    It only selects the largest invoice id on first assignment and then
    increments by one for each new invoice id as transactions are assigned.
    """
    def __init__(self):
        self._table = {}
        self._cur_invoice_id = None

    def assign(self, trans):
        """ Assign the invoice_id and line_no of the given trans record.
        """
        key = _key(trans)
        tracker = self._existing_line_tracker(key)
        if not tracker:
            self._add_tracker_for(trans)
            tracker = self._existing_line_tracker(key)
        tracker.assign(trans)

    def _existing_line_tracker(self, key):
        """ Provide the existing line tracker for the given trans. Returns
        None if one isn't found or the existing one is full
        """
        if key not in self._table:
            return None
        tracker = self._table[key]
        if tracker.is_full():
            return None
        return tracker

    def _add_tracker_for(self, trans):
        """ Add a new invoice to the tracked table since the given trans key
        does not already have one. """
        if self._cur_invoice_id is None:
            self._cur_invoice_id = self._largest_unused_invoice_id()
        else:
            self._cur_invoice_id += 1

        maxi = _max_line_items_for(trans['group_number'])
        invoice = _InvoiceLineTracker(self._cur_invoice_id,  maxi)
        self._table[_key(trans)] = invoice

    def _largest_unused_invoice_id(self):
        """ The largest non-rebill invoice id not used in the database """
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT max(invoice_id) AS invoice_id
            FROM trans
            WHERE invoice_id < %s
            """, (STARTING_REBILL_INVOICE_ID,))
        invoice_id, = cursor.fetchone() or 0
        return invoice_id + 1

@memoize
def _max_line_items_for(group_number):
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT COUNT(*)
        FROM client_report_code
        WHERE  report_code = 'CCMSI' AND group_number=%s
        """, (group_number,))
    if cursor.fetchone()[0]:
        return 999
    else:
        return 6

class RebillInvoiceKeyMaker(InvoiceKeyMaker):
    """ An invoice key maker for rebilled transactions """
    def _largest_unused_invoice_id(self):
        """ The largest rebill invoice id not used in the database. """
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT max(invoice_id) AS invoice_id
            FROM trans
            WHERE invoice_id >= %s
            """, (STARTING_REBILL_INVOICE_ID,))
        invoice_id, = cursor.fetchone()
        if not invoice_id:
            return STARTING_REBILL_INVOICE_ID
        else:
            return invoice_id + 1

def _key(rec):
    """ Provide the key for a transaction record used to group together
    transactions on the same invoices. Transactions which evaluate to the
    same key will be placed on the same invoice.
    """
    # Meadowbrook
    if rec['group_number'] in ('70017', '70010', '70020', '70014'):
        return (rec['patient_id'], rec['doi'], rec['pharmacy_nabp'],
                rec['batch_file_id'], rec['rx_date'])
    # Bridge point has invoice classes which control MCA/MSA billing
    elif rec['group_number']  in ('70036', '70852'):
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT inv_class
            FROM history
            WHERE group_number=%(group_number)s AND group_auth=%(group_auth)s
            """, rec)
        inv_class, = cursor.fetchone()
        return (rec['patient_id'], rec['doi'], rec['pharmacy_nabp'],
                inv_class, rec['batch_file_id'], rec['rx_date'])
    else:
        return (rec['patient_id'], rec['doi'], rec['batch_file_id'], rec['pharmacy_nabp'])

class _InvoiceLineTracker(object):
    """ A single invoice id  in the `InvoiceKeyMaker`'s table which tracks a
    particular invoice_id and manages the line numbers.
    """
    def __init__(self, invoice_id, max_num_invoice_items=6):
        self._invoice_id = invoice_id
        self._line_no = 1
        self._max_num_invoice_item = max_num_invoice_items

    def is_full(self):
        """ Is this invoice maxed out on the number of items that can go on it?
        """
        return self._line_no > self._max_num_invoice_item

    def assign(self, trans):
        """ Assign the current invoice_id and line_number to the transaction
        """
        trans['invoice_id'] = self._invoice_id
        trans['line_no'] = self._line_no
        self._line_no += 1

def test():
    """ Execute basic test of module functionality """
    import pprint
    maker = InvoiceKeyMaker()
    txs = [{
        'patient_id': 1,
        'doi': '2012-01-01',
        'group_number': '1111111',
        'pharmacy_nabp': '1111111'},
    {   'patient_id': 1,
        'doi': '2012-01-01',
        'group_number': '1111111',
        'pharmacy_nabp': '1111111'},
    {   'patient_id': 2,
        'doi': '2012-01-01',
        'group_number': '1111111',
        'pharmacy_nabp': '1111111'},
    {   'patient_id': 3,
        'doi': '2012-01-01',
        'group_number': '70014',
        'pharmacy_nabp': '1111111',
        'rx_date': '2012-03-01'},
    ]
    for trans in txs:
        maker.assign(trans)
        pprint.pprint(trans)

    print()
    rebill_maker = RebillInvoiceKeyMaker()
    for trans in txs:
        rebill_maker.assign(trans)
        pprint.pprint(trans)


if __name__ == '__main__':
    test()
