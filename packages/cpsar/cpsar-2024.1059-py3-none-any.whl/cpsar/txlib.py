from builtins import next
from future.utils import raise_
from builtins import object
from decimal import Decimal
import datetime
import logging; logg=logging.getLogger('')
import pprint
import re

import cpsar.invoice 
import cpsar.runtime as R
from cpsar.util import insert_sql, count_money, imemoize

ZERO = Decimal("0.00")

###############################################################################
## Business Procedures

_drug_brand_cache = None
def get_brand(record):
    global _drug_brand_cache
    if _drug_brand_cache is None:
        cursor = R.db.cursor()
        cursor.execute("SELECT ndc_number, brand FROM drug")
        _drug_brand_cache = dict(list(cursor))

    return _drug_brand_cache[record['drug_ndc_number']]

def change_tx_type(trans_id, tx_type):
    """ Change the tx type for the given transaction. Right now this is only
    allowed for CPS compounds.
    """
    cursor = R.db.cursor()
    cursor.execute("""
      SELECT compound_code, pharmacy_nabp
      FROM trans
      WHERE trans_id=%s""", (trans_id,))
    if not cursor.rowcount:
        raise DataError("Trans not found %s" % trans_id)
    cc, nabp = cursor.fetchone()
    if cc != '2':
        raise BusinessError("Cannot change tx_type of non compound tx %s" % trans_id)
    if nabp != R.CPS_NABP_NBR:
        raise BusinessError("Cannot change tx_type of non CPS tx %s" % trans_id)

    if tx_type not in ('PC', 'MC'):
        raise BusinessError("Can only change tx_type to PC or MC, not %s for %s"
            % (tx_type, trans_id))

    cursor.execute("UPDATE trans SET tx_type=%s WHERE trans_id=%s",
        (tx_type, trans_id))

def update_cost_allowed(tx, new_cost_allowed):
    """ Change the cost allowed for the transaction to the new given cost allowed
    """
    if tx.cost_allowed == new_cost_allowed:
        raise BusinessError("The cost allowed has not changed")

    if not tx.cost_allowed_editable:
        raise BusinessError("The cost allowed cannot be edited on this transaction")

    #if new_cost_allowed > tx.cost_allowed:
        # No big deal, just update and do a transaction check
    _update_dbase_cost_allowed(tx, new_cost_allowed)
    check(tx.trans_id)

    tx = Transaction(tx.trans_id)
    adjust_payment_to_trans_total(tx)

def _update_dbase_cost_allowed(tx, cost_allowed):
    cursor = R.db.cursor()
    cursor.execute("""
        UPDATE trans SET cost_allowed=%s
        WHERE trans_id=%s
        """, (cost_allowed, tx.trans_id))
    log(tx.trans_id, "Cost allowed changed from %s to %s" % 
            (tx.cost_allowed, cost_allowed))
    cursor.execute("""
        UPDATE trans
         SET total=cost_allowed + dispense_fee + processing_fee + sales_tax - eho_network_copay
        WHERE trans_id=%s
        RETURNING total
        """, (tx.trans_id,))
    total = cursor.fetchone()[0]
    log(tx.trans_id, "Updated total to %s" % total)

def adjust_payment_to_trans_total(tx):
    """ If the payment on the given transaction is more than the total of the
    transaction, then change the payment to pay up to the total and
    create an overpayment entry for the difference.
    """
    if tx.paid_amount < tx.total:
        return

    if len(tx.payments) != 1:
        raise BusinessError("The system does not support automatically adjusting "
            "more than one payment at a time. Please manually revoke the extra "
            "payments.")
    payment = tx.payments[0]

    log_msg = ("Adjusting Payment %s amount from %s to %s because the payment "
               "amount is more than the transaction total.")
    log(tx.trans_id, log_msg % (payment['payment_id'], payment['amount'], tx.total))

    cursor = R.db.cursor()
    cursor.execute("""
        UPDATE trans_payment SET amount=%s
        WHERE payment_id=%s
        """, (tx.total, payment['payment_id']))

    difference = payment['amount'] - tx.total

    log_msg = "Creating overpayment of %s for the difference of payment %s"
    log(tx.trans_id, log_msg % (difference, payment['payment_id']))
    add_overpayment(tx.trans_id,
        ptype_id=payment['ptype_id'],
        ref_no=payment['ref_no'],
        amount=difference,
        entry_date=payment['entry_date'],
        note="Automatically created overpayment")

class BusinessError(Exception):
    pass

class DataError(Exception):
    pass

def add_distribution(trans_id, account, amount):
    """ Add distribution record to a transaction. This does not reconcile
    the distribution.
    """
    cursor = R.db.cursor()
    cursor.execute("""
        INSERT INTO distribution
            (trans_id, distribution_account, amount)
        VALUES (%s, %s, %s)""",
        (trans_id, account, amount))
    amount = "%.02f" % Decimal(amount)
    log(trans_id, "Added distribution of %s to %s" % (amount, account))
    return True

def remove_distribution(did):
    """ Remove a distribution record from the system. If the distribution
    has been reconciled, an error is given.
    """
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT amount, distribution_account, distribution_date, trans_id
        FROM distribution
        WHERE distribution_id=%s
        """, (did,))
    if not cursor.rowcount:
        R.error('Invalid Distribution # %s' % did)
        return False

    amount, account, date, trans_id = cursor.fetchone()

    if date:
        R.error('Cannot remove reconciled distribution %s', date)
        return False

    log(trans_id, 'Removed distribution %s from %s' % (amount, account))
    cursor.execute("""
        DELETE FROM distribution
        WHERE distribution_id=%s
        """, (did,))
    return trans_id

def revoke_overpayment(puc_id):
    """ Remove an overpayment record from the system. Overpayment
    records can only be removed if they have not been used.
    """

    cursor = R.db.cursor()
    cursor.execute("""
        SELECT trans_id, balance, amount, type_name, ref_no
        FROM overpayment
        JOIN payment_type USING(ptype_id)
        WHERE puc_id=%s
        """, (puc_id,))
    if not cursor.rowcount:
        raise ValueError("Unknown puc_id %s" % puc_id)
    trans_id, balance, amount, type_name, ref_no = cursor.fetchone()
    if balance != amount:
        raise ValueError("Cannot remove overpayment with applied portion")

    cursor.execute("DELETE FROM overpayment WHERE puc_id=%s", (puc_id,))
    if trans_id:
        msg = "Revoked %s: %s overpayment for %s" % (type_name, ref_no, amount)
        log(trans_id, msg)

def revoke_distributed_payment(trans_id):
    """ Cancels a payment on a transaction that has already been distributed.

    We will remove the payment record and create negative distribution records
    for each distribution record for the given transaction and sets their
    distribution date to now.

    This procedure only supports transactions that have a single payment
    that is for the total amount of the transaction. In the future, we can
    update the logic to revoke more than one payment as long as they all
    equal the transaction total.
    """

    def err(msg, *a):
        if a: msg %= a
        R.error("Trans %08d: Cannot revoke distributed payment, %s",
                trans_id, msg)
        return False

    trans = R.db.dict_cursor()
    trans.execute("""
        SELECT paid_amount, distributed_amount, paid_amount
        FROM trans
        WHERE trans_id=%s
        """, (trans_id,))
    trans = trans.fetchone()

    if trans['distributed_amount'] != trans['paid_amount']:
        return err("Paid amount %s != distributed amount %s", 
                trans['paid_amount'], trans['distributed_amount'])

    payment = R.db.dict_cursor()
    payment.execute("""
        SELECT payment_id, amount
        FROM trans_payment
        WHERE trans_id=%s
        """, (trans_id,))

    if payment.rowcount != 1:
        return err("More than one payment. Only one payment supported.")
    payment = payment.fetchone()

    distributions = R.db.dict_cursor()
    distributions.execute("""
        SELECT distribution_account, amount
        FROM distribution
        WHERE trans_id=%s AND amount > 0 AND distribution_date IS NOT NULL
        """, (trans_id,))
    distributions = list(distributions)
    distributed_total = sum(d['amount'] for d in distributions)

    if payment['amount'] != distributed_total:
        return err('Payment amount %s != distributed total %s', 
                   payment['amount'], distributed_total)

    remove_payment(payment['payment_id'])

    for distribution in distributions:
        amount = -distribution['amount']
        account = distribution['distribution_account']
        ndist = R.db.cursor()
        ndist.execute(insert_sql('distribution', {
            'trans_id': trans_id,
            'distribution_account': account,
            'amount': amount,
            'distribution_date': datetime.datetime.now()
        }))

        amount = "%.02f" % Decimal(amount)
        log(trans_id, "Added distribution of %s to %s" % (amount, account))

        check_distributed_amount(trans_id)
    return True

def remove_payment(pid):
    """ Remove the given payment_id (pid) from the system. This procedure is
    responsible for:

     - Ensuring the given pid exists in the trans_payment table
     - Delete the entry from trans_payment table
     - Recording the action in the transaction log
     - Updating the transaction and invoice fields to maintain db invariants
    """
    cursor = R.db.dict_cursor()
    cursor.execute("""
        SELECT trans_payment.ptype_id,
               trans_payment.trans_id, 
               trans_payment.amount, 
               payment_type.type_name,
               trans_payment.ref_no,
               trans.invoice_id,
               trans_payment.puc_id
        FROM trans_payment
        JOIN trans USING(trans_id)
        LEFT JOIN payment_type USING(ptype_id)
        WHERE payment_id=%s
        """, (pid,))
    if not cursor.rowcount:
        return False
    payment = cursor.fetchone()
    trans_id = payment['trans_id']
    invoice_id = payment['invoice_id']

    cursor.execute("""
        DELETE FROM trans_payment
        WHERE payment_id=%s
        """, (pid,))
    if payment['puc_id']:
        c = R.db.cursor()
        cursor.execute("""
            SELECT payment_type.type_name, overpayment.ref_no
            FROM overpayment
            JOIN payment_type USING(ptype_id)
            WHERE puc_id=%s
            """, (payment['puc_id'],))
        type_name, ref_no = cursor.fetchone()
        msg = "Revoked payment from overpayment %s: %s for %s" % (
                    type_name, ref_no, payment['amount'])
        cursor.execute("""
            UPDATE overpayment SET balance = balance + %s
            WHERE puc_id=%s
            """, (payment['amount'], payment['puc_id']))
    else:
        msg = "Revoked %(type_name)s: %(ref_no)s payment of %(amount)s" % payment
    log(trans_id, msg)
    check_paid_amount(trans_id)
    check_transfered_amount(trans_id)
    check_balance(trans_id)
    check_paid_date(trans_id)

    refresh_group_credit_views()

    if invoice_id:
        cpsar.invoice.check(invoice_id)

    cancel_state_report_entries(trans_id)
    return trans_id

def refresh_group_credit_views():
    cursor = R.db.cursor()
    cursor.execute("""
        refresh materialized view group_ledger;
        refresh materialized view group_ledger_balance;
        """)
    cursor.close()

def add_reversal(trans_id, reversal_date):
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT reversal_id FROM reversal WHERE trans_id=%s
        """, (trans_id,))
    if cursor.rowcount:
        rid = cursor.fetchone()
        R.error("trans #%s already reversed with reversal %s", trans_id, rid)
        return

    cursor.execute("""
        SELECT group_number, group_auth, total
        FROM trans
        WHERE trans_id=%s
        """, (trans_id,))
    group_number, group_auth, total = cursor.fetchone()
    if group_number not in('GROUPH', 'GROUPMJO', 'GROUPSPL', 'GROUPSUN') :
        R.error('Only GROUPH transactions can be reversed from AR at this time')
        return

    sql = insert_sql("reversal", dict(
        group_number=group_number,
        group_auth=group_auth,
        reversal_date=reversal_date,
        trans_id=trans_id,
        total=total,
        balance=total))
    cursor.execute(sql)
    log(trans_id, "Reversed trans %s from interface" % trans_id)

def revoke_reversal(trans_id):
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT reversal_id, balance, total FROM reversal WHERE trans_id=%s
        """, (trans_id,))
    if not cursor.rowcount:
        R.error("No reversal on trans %s", trans_id)
        return
    reversal_id, balance, total = cursor.fetchone()
    if total != balance:
        R.error("Reversal %s has applied credits. Cannot remove.", reversal_id)
        return

    cursor.execute("SELECT group_number FROM trans WHERE trans_id=%s", (trans_id,))
    if not cursor.rowcount:
        R.error("trans %s not found", (trans_id,))
    group_number, = cursor.fetchone()
    if group_number != 'GROUPH':
        R.error("Cannot remove reversal in AR of non GROUPH trans")
        return

    cursor.execute("DELETE FROM reversal WHERE reversal_id=%s", (reversal_id,))
    log(trans_id, "Revoked reversal %s from trans %s" % (reversal_id, trans_id))

def add_payment(trans_id, ptype_id, ref_no, amount, entry_date, note=None):
    """ Add payment amount to a transaction, reducing the balance and possibly
    marking it as paid. """
    cursor = R.db.cursor()
    entry_date = _fix_date(entry_date)

    cursor.execute("""
        SELECT group_number, balance, invoice_id
        FROM trans
        WHERE trans_id=%s
        """, (trans_id,))
    if not cursor.rowcount:
        return R.error("Unknown transaction # %s" % trans_id)
    group_number, balance, invoice_id = cursor.fetchone()

    cursor.execute("""
        SELECT type_name
        FROM payment_type
        WHERE ptype_id=%s
        """, (ptype_id,))
    if not cursor.rowcount:
        return R.error("Unknown Payment Type ID %s" % ptype_id)
    type_name, = cursor.fetchone()

    if balance < amount:
        return R.error("Transaction %08d: Cannot apply %s. Transaction balance is "
                "only %s", trans_id, amount, balance)

    cursor.execute(insert_sql("trans_payment", dict(
        trans_id=trans_id,
        ptype_id=ptype_id,
        ref_no=ref_no,
        amount=amount,
        username=R.username(),
        entry_date=entry_date,
        note=note)
    ))

    log(trans_id,"Added %s: %s payment for %s" % (type_name, ref_no, amount)) 

    check_paid_amount(trans_id)
    check_balance(trans_id)
    check_paid_date(trans_id)

    if invoice_id:
        cpsar.invoice.check(invoice_id)

    mark_for_state_reporting(trans_id)

def add_overpayment(trans_id, ptype_id, ref_no, amount, entry_date, note=None):
    """ Add overpayment to transaction. This does not use the overpayment,
    simply registers the overpayment with the transaction signifying that the
    particular transaction has been overpaid.
    """
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT type_name FROM payment_type WHERE ptype_id=%s
        """, (ptype_id,))
    if not cursor.rowcount:
        raise ValueError("Invalid ptype_id %s" % ptype_id)
    type_name = cursor.fetchone()[0]
    cursor.execute(insert_sql('overpayment', dict(
        amount=amount,
        balance=amount,
        trans_id=trans_id,
        ptype_id=ptype_id,
        ref_no=ref_no,
        username=R.username(),
        entry_date=entry_date,
        note=note
    )))

    check_paid_amount(trans_id)
    check_balance(trans_id)
    log_msg = "Added %s: %s overpayment for %s" % (type_name, ref_no, amount)
    log(trans_id, log_msg)

def add_overpayment_payment(trans_id, puc_id, amount, entry_date, note=None):
    """ Pay on a transaction with an outstanding transaction overpayment record.
    """
    entry_date = _fix_date(entry_date)
    cursor = R.db.cursor()

    cursor.execute("""
        SELECT group_number, balance, invoice_id
        FROM trans
        WHERE trans_id=%s
        """, (trans_id,))
    if not cursor.rowcount:
        raise_(ValueError, "Unknown transaction # %s" % trans_id)
    group_number, balance, invoice_id = cursor.fetchone()

    if balance < amount:
        R.error("Transaction %08d: Cannot apply %s. Transaction balance is "
                "only %s", trans_id, amount, balance)
        return False

    cursor.execute("""
      SELECT balance, ptype_id, ref_no 
      FROM overpayment
      WHERE puc_id=%s
      """, (puc_id,))

    if not cursor.rowcount:
        R.error('Unknown puc_id %s' % puc_id)
        return False

    puc_balance, ptype_id, ref_no = cursor.fetchone()
    if puc_balance < amount:
        R.error("PUC Balance %s on %s less than amount trying to apply %s",
                puc_balance, puc_id, amount)
        return False

    cursor.execute(insert_sql("trans_payment", dict(
        trans_id=trans_id,
        puc_id=puc_id,
        ptype_id=ptype_id,
        ref_no=ref_no,
        amount=amount,
        username=R.username(),
        entry_date=entry_date,
        note=note
        )))
    log(trans_id, "Applied %s unapplied cash from PUC %s" % (amount, puc_id))

    cursor.execute("""
        UPDATE overpayment SET balance = balance - %s
        WHERE puc_id=%s
        """, (amount, puc_id))

    check_paid_amount(trans_id)
    check_balance(trans_id)
    check_paid_date(trans_id)

    if invoice_id:
        cpsar.invoice.check(invoice_id)

    mark_for_state_reporting(trans_id)
    return True

def add_group_credit_payment(trans_id, amount, group_number, username):
    cursor = R.db.cursor()
    cursor.execute("""
        insert into trans_payment 
               (trans_id, amount, username, credit_group_number, ref_no, ptype_id)
        values (%s, %s, %s, %s, %s, 255)
        """, (trans_id, amount, username, group_number, f'GROUP:{group_number}'))
    log(trans_id, f"Added payment from group credit for {amount} from group {group_number}")
    check_paid_amount(trans_id)
    check_balance(trans_id)
    check_paid_date(trans_id)
    refresh_group_credit_views()

def revoke_debit(debit_id):
    cursor = R.db.cursor()
    cursor.execute("""
      SELECT trans_id, amount
      FROM trans_debit
      WHERE debit_id=%s
      """, (debit_id,))

    if not cursor.rowcount:
        raise ValueError("debit %s not found" % debit_id)

    trans_id, amount = cursor.fetchone()
    cursor.execute("DELETE FROM trans_debit WHERE debit_id=%s", (debit_id,))
    cursor.execute("""
      UPDATE trans SET
            debit_total = debit_total - %s,
            adjustments = adjustments - %s,
            balance = balance - %s
      WHERE trans_id=%s
      RETURNING balance 
        """, (amount, amount, amount, trans_id))
    balance, = cursor.fetchone()
    log(trans_id, "Revoked debit %s for %s" % (debit_id, amount))

    if balance == 0:
        cursor.execute("""
         UPDATE trans SET paid_date=NOW()
         WHERE trans_id=%s
         """, (trans_id,))
        log(trans_id, "Set paid date due to revoking of debit note")


def add_debit(trans_id, amount, entry_date, note):
    cursor = R.db.cursor()
    cursor.execute("SELECT paid_date FROM trans WHERE trans_id=%s", (trans_id,))
    if not cursor.rowcount:
        raise ValueError("trans %s not found" % trans_id)
    paid_date, = cursor.fetchone()

    cursor.execute(insert_sql("trans_debit", {
        "trans_id": trans_id,
        "amount": amount,
        "entry_date": entry_date,
        "username": R.username(),
        "note": note}))

    cursor.execute("""
        UPDATE trans SET
            debit_total = debit_total + %s,
            adjustments = adjustments + %s,
            balance = balance + %s
        WHERE trans_id=%s
        """, (amount, amount, amount, trans_id))

    log(trans_id, "Added debit for %s" % amount)

    if paid_date:
        cursor.execute("""
          UPDATE trans SET paid_date = NULL
          WHERE trans_id=%s
          """, (trans_id,))
        log(trans_id, "Clearing out paid date")

def add_adjudication(trans_id, reversal_id, amount, entry_date, note):
    """ Apply a credit to the transaction with the given reversal as the
    source of the credit funds.
    """
    cursor = R.db.cursor()

    # Get the invoice the adjudication is for
    cursor.execute("""
        SELECT invoice_id
        FROM trans
        WHERE trans_id=%s""",
        (trans_id,))
    invoice_id, = cursor.fetchone()

    # Get which tx the reversal is coming from
    cursor.execute("""
        SELECT trans_id, balance
        FROM reversal
        WHERE reversal_id=%s""",
        (reversal_id,))
    adj_trans_id, reversal_balance = cursor.fetchone()

    # Ensure the reversal has the funds
    if reversal_balance < amount:
        raise BusinessError("Reversal %s does not have enough funds to apply "
            "%s. Only has a balance of %s" %
            (reversal_id, amount, reversal_balance))

    reversal_balance
    cursor.execute("""
        INSERT INTO trans_adjudication
            (trans_id, reversal_id, note, amount, username, entry_date)
        VALUES
            (%s, %s, %s, %s, %s, %s)
        """,
        (trans_id, reversal_id, note, amount, R.username(), entry_date))

    log(trans_id, "Adjudicated %s with reversal # %s" % (amount, reversal_id))
    log(adj_trans_id, "Adjudicated tx %s for $%s with reversal # %s" % 
            (trans_id, amount, reversal_id))

    check(trans_id)
    check_reversal(reversal_id)
    if invoice_id:
        cpsar.invoice.check(invoice_id)
    mark_for_state_reporting(trans_id)

def remove_adjudication(aid):
    """ Cancel an adjudication with the adjudication ID. """
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT trans_id, amount, reversal_id
        FROM trans_adjudication
        WHERE adjudication_id=%s""", (aid,))
    if not cursor.rowcount:
        return
    trans_id, amount, reversal_id = cursor.fetchone()

    # Get the invoice the adjudication is for
    cursor.execute("""
        SELECT invoice_id
        FROM trans
        WHERE trans_id=%s""",
        (trans_id,))
    invoice_id, = cursor.fetchone()

    cursor.execute("""
        DELETE from trans_adjudication
        WHERE adjudication_id=%s""", (aid,))
    log(trans_id, "Revoked adjudication of %s with reversal # %s" %
        (amount, reversal_id))
    check(trans_id)
    check_reversal(reversal_id)
    cancel_state_report_entries(trans_id)

    if invoice_id:
        cpsar.invoice.check(invoice_id)
    return trans_id

def void_adjudication(adjudication_id, void_date):  
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT void_date, trans_id, reversal_id
        from trans_adjudication
        WHERE adjudication_id=%s
        """, (adjudication_id,))
    if not cursor.rowcount:
        raise DataError("adjudication %s not found" % adjudication_id)
    current_void_date, trans_id, reversal_id = cursor.fetchone()
    if current_void_date:
        raise BusinessError("adjudication %s is already voided for %s" %
            (adjudication_id, current_void_date))
    cursor.execute("""
        UPDATE trans_adjudication SET void_date=%s
        WHERE adjudication_id=%s
        """, (void_date, adjudication_id))
    check(trans_id)
    check_reversal(reversal_id)
    cancel_state_report_entries(trans_id)

def unvoid_adjudication(adjudication_id):
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT void_date, trans_id, reversal_id
        from trans_adjudication
        WHERE adjudication_id=%s
        """, (adjudication_id,))
    if not cursor.rowcount:
        raise DataError("adjudication %s not found" % adjudication_id)
    current_void_date, trans_id, reversal_id = cursor.fetchone()
    if not current_void_date:
        raise BusinessError("adjudication %s is not currently voided" %
            adjudication_id)
    cursor.execute("""
        UPDATE trans_adjudication SET void_date=NULL
        WHERE adjudication_id = %s
        """, (adjudication_id,))
    check(trans_id)
    check_reversal(reversal_id)
    cancel_state_report_entries(trans_id)

def revoke_writeoff(writeoff_id):
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT trans.trans_id, trans.invoice_id, trans_writeoff.amount
        FROM trans_writeoff
        JOIN trans USING(trans_id)
        WHERE writeoff_id=%s""", (writeoff_id,))
    if not cursor.rowcount:
        return ValueError('Writeoff %s not found' % writeoff_id)
    trans_id, invoice_id, amount = cursor.fetchone()
    cursor.execute("""
        DELETE FROM trans_writeoff
        WHERE writeoff_id=%s""", (writeoff_id,))
    log(trans_id, "Revoked writeoff for %s" % amount)

    cursor.execute("""
        UPDATE trans SET
            balance=balance + %s,
            writeoff_total=writeoff_total - %s,
            adjustments=adjustments + %s
        WHERE trans_id=%s""",
        (amount, amount, amount, trans_id))
    check(trans_id)
    if invoice_id:
        cpsar.invoice.check(invoice_id)
    mark_for_state_reporting(trans_id)

def add_writeoff(trans_id, amount, entry_date, note):
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT invoice_id, balance
        FROM trans
        WHERE trans_id=%s""",
        (trans_id,))
    if not cursor.rowcount:
        raise ValueError("trans %s not found" % trans_id)
    invoice_id, balance = cursor.fetchone()
    if balance < amount:
        raise BusinessError("Cannot write off %s on trans %s. Balance only %s"
            % (amount, trans_id, balance))
    cursor.execute(insert_sql("trans_writeoff", {
        "trans_id": trans_id,
        "note": note,
        "amount": amount,
        "entry_date": entry_date,
        "username": R.username()}))
    log(trans_id, "Wrote off %s" % amount)
    check(trans_id)
    if invoice_id:
        cpsar.invoice.check(invoice_id)
    mark_for_state_reporting(trans_id)

def void_writeoff(writeoff_id, void_date):
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT trans_id, void_date
        FROM trans_writeoff
        WHERE writeoff_id=%s
        """, (writeoff_id,))
    if not cursor.rowcount:
        raise DataError("writeoff %s not found" % writeoff_id)
    trans_id, current_void_date = cursor.fetchone()
    if current_void_date:
        raise BusinessError("writeoff %s already voided on %s" %
            (writeoff_id, current_void_date))
    cursor.execute("""
        UPDATE trans_writeoff SET void_date=%s
        WHERE writeoff_id=%s
        """, (void_date, writeoff_id))
    check(trans_id)
    mark_for_state_reporting(trans_id)

def unvoid_writeoff(writeoff_id):
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT trans_id, void_date
        FROM trans_writeoff
        WHERE writeoff_id=%s
        """, (writeoff_id,))
    if not cursor.rowcount:
        raise DataError("writeoff %s not found" % writeoff_id)
    trans_id, current_void_date = cursor.fetchone()
    if not current_void_date:
        raise BusinessError("writeoff %s is not voided")
    cursor.execute("""
        UPDATE trans_writeoff SET void_date=NULL
        WHERE writeoff_id=%s
        """, (writeoff_id,))
    check(trans_id)
    cancel_state_report_entries(trans_id)

def mark_for_state_reporting(trans_id):
    """ Mark the given tranasction to be reported to the state if
    applicable.
    """
    return
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT balance, paid_amount, patient_id, group_number, freeze_sr_entry
        FROM trans
        WHERE trans_id=%s
        """, (trans_id,))

    balance, paid_amount, patient_id, group_number, freeze_sr_entry = cursor.fetchone()
    # ignore mark for state reporting if the rec is frozen
    if freeze_sr_entry == True:
        return

    # Only transactions who are paid and have actually had monies applied to
    # them are candidates for state reporting
    if balance != 0 or paid_amount == 0:
        return

    cursor.execute("""
        SELECT jurisdiction
        FROM patient
        WHERE patient_id=%s
        """, (patient_id,))
    soj, = cursor.fetchone()

    cursor.execute("""
        SELECT send_ca_state_reporting,
               send_fl_state_reporting,
               send_or_state_reporting,
               send_tx_state_reporting,
               send_nc_state_reporting
        FROM client
        WHERE group_number=%s
        """, (group_number,))
    report_ca, report_fl, report_or, report_tx, report_nc = cursor.fetchone()

    if soj == '07' and report_ca:
        reportzone = 'CA'
    elif soj == '09' and report_fl:
        reportzone = 'FL'
    elif soj == '36' and report_or:
        reportzone = 'OR'
    elif soj == '42' and report_tx:
        reportzone = 'TX'
    elif soj == '32' and report_tx:
        reportzone = 'NC'
    else:
        return

    # Do we already have any existing state report entries? 
    # if so cancel or reject them
    cursor.execute("""
        SELECT entry_id, file_id, cancel_file_id, ack_code
        FROM state_report_entry
        WHERE trans_id=%s AND reportzone=%s
        """, (trans_id, reportzone))

    for entry_id, file_id, cancel_file_id, ack_code in list(cursor):
        if cancel_file_id:
            # This entry has already been canceled with the agency. Ignore it.
            continue
        if file_id is None:
            # There is already a pending entry to be sent to the agency
            # We will just let that take care of the current update
            return

        if ack_code == 'R':
            # Make sure we don't cancel rejections
            return

        # Setup the record for being canceled
        cursor.execute("""
            UPDATE state_report_entry SET pending_cancel=TRUE
            WHERE entry_id=%s
            """, (entry_id,))

    # Adding a new record (new 00 or a new 01 for 00)
    dbrec = {'trans_id': trans_id, 'reportzone': reportzone}
    sql = insert_sql('state_report_entry', dbrec)
    cursor.execute(sql)

def resend_state_report_rejection(trans_id):
    cursor = R.db.cursor()

    # ignore marking for state reporting if the rec is frozen
    cursor.execute("""
        SELECT freeze_sr_entry
            FROM trans
        WHERE trans_id=%s
        """, (trans_id,))
    assert cursor.rowcount == 1
    if cursor.fetchone()[0]:
        return

    # set the file_id = Null so 837 picks it up again
    cursor.execute("""
        UPDATE state_report_entry SET file_id = Null 
        WHERE trans_id=%s
        """, (trans_id,))

def cancel_state_report_entries(trans_id):
    return
    cursor = R.db.cursor()

    # ignore marking for state reporting if the rec is frozen
    cursor.execute("""
        SELECT freeze_sr_entry
            FROM trans
        WHERE trans_id=%s
        """, (trans_id,))
    assert cursor.rowcount == 1
    if cursor.fetchone()[0]:
        return

    # Make sure we don't cancel a rejection
    cursor.execute("""
        SELECT ack_code from state_report_entry
        WHERE trans_id=%s 
        AND ack_code = 'R' OR cancel_ack_code= 'R'
        """, (trans_id,))
    if cursor.rowcount:
        return

    # if the file hasn't been sent delete it
    cursor.execute("""
        DELETE FROM state_report_entry
        WHERE trans_id=%s AND file_id IS NULL
        """, (trans_id,))

    # if the file has been sent update it to be canceled
    cursor.execute("""
        UPDATE state_report_entry SET pending_cancel=TRUE
        WHERE trans_id=%s AND cancel_file_id IS NULL
        """, (trans_id,))

def add_reversal_settlement(reversal_id, check_no, amount, trans_id=None,
                            entry_date=None):
    """ Add a reversal settlement to the system. This interface does not
    deal with pending reversal settlements. If the source of the
    settlement is a pending record, that must be handled outside of this
    procedure.
    """
    cursor = R.db.cursor()

    if trans_id is None:
        cursor.execute("""
            SELECT trans_id
            FROM reversal
            WHERE reversal_id=%s
            """, (reversal_id,))
        if not cursor.rowcount:
            raise ValueError("No reversal_id %s" % reversal_id)
        trans_id, = cursor.fetchone()

    if entry_date is None:
        entry_date = datetime.datetime.now()
    cursor.execute("""
        INSERT INTO reversal_settlement 
         (check_no, reversal_id, amount, username, entry_date)
        VALUES (%s, %s, %s, %s, %s)
        """, (check_no, reversal_id, amount, R.username(), entry_date))
    cursor.execute("""
        SELECT currval('reversal_settlement_settlement_id_seq')
        """)
    settlement_id, = cursor.fetchone()

    cursor.execute("""
        UPDATE reversal SET balance = balance - %s
        WHERE reversal_id=%s
        """, (amount, reversal_id))

    cursor.execute("""
        UPDATE trans SET settled_amount = settled_amount + %s
        WHERE trans_id = %s
        """, (amount, trans_id))

    log(trans_id, "Added reversal settlement %s for %s CK %s" % (
                    settlement_id, amount, check_no))

def revoke_overpayment_settlement(puc_settle_id):
    """ Revoke a settlement on an overpayment
    """
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT puc_id, amount
        FROM overpayment_settlement
        WHERE puc_settle_id=%s
        """, (puc_settle_id,))

    if not cursor.rowcount:
        raise DataError("overpayment settlement %s not found" % puc_settle_id)

    puc_id, settlement_amount = cursor.fetchone()

    cursor.execute("""
        SELECT trans_id
        FROM overpayment
        WHERE puc_id=%s
        """, (puc_id,))
    trans_id, = cursor.fetchone()

    # Delete the settlement
    cursor.execute("""
        DELETE FROM overpayment_settlement
        WHERE puc_settle_id=%s
        """, (puc_settle_id,))

    # Increase the balance on the overpayment by the amount of the
    # settlement we just revoked
    cursor.execute("""
        UPDATE overpayment SET balance = balance + %s
        WHERE puc_id=%s
        """, (settlement_amount, puc_id))

    log(trans_id, "Revoked Overpayment Settlement on PUC ID %s for %s" % (
        puc_id, settlement_amount))

def void_overpayment_settlement(puc_settle_id, void_date=None):
    """ Effectively cancel an overpayment settlement. 
    """
    cursor = R.db.cursor()

    if void_date is None:
        void_date = datetime.datetime.now()

    # Fetch the foreign keys to update their records and
    # the amount to know how much we're revoking
    cursor.execute("""
        SELECT trans_id, puc_id, amount
        FROM overpayment
        WHERE puc_id=(
            SELECT puc_id
            FROM overpayment_settlement
            WHERE puc_settle_id=%s)
        """, (puc_settle_id,))
    
    if cursor.rowcount != 1:
        raise DataError("overpayment settlement %s not found" % puc_settle_id)
    trans_id, puc_id, amount = cursor.fetchone()

    # Set the void date Delete the settlement
    cursor.execute("""
        UPDATE overpayment_settlement
        SET void_date=%s
        WHERE puc_settle_id=%s
        """, (void_date, puc_settle_id))

    # Update the overpayment to reflect that it has not been
    # settled anymore.
    cursor.execute("""
        UPDATE overpayment SET balance = balance + %s
        WHERE puc_id=%s
        """, (amount, puc_id))

    log(trans_id, "Voided Overpayment Settlement on PUC ID %s for %s" % (
                  puc_id, amount))

def add_overpayment_settlement(puc_id, check_no, entry_date=None):
    """ Settle the balance on the overpayment with a check going back to the
    sponsor.
    """
    if entry_date is None:
        entry_date = datetime.datetime.now()
    cursor = R.db.cursor()
    # Fetch the current balance so we know how much to settle and the trans
    # to update the settled amount
    cursor.execute("""
        SELECT trans_id, balance
        FROM overpayment
        WHERE puc_id = %s
        """, (puc_id, ))
    trans_id, balance = cursor.fetchone()

    # Create the overpayment settlement record for the current balance
    cursor.execute("""
        INSERT INTO overpayment_settlement
         (check_no, puc_id, username, amount, entry_date)
         VALUES (%s, %s, %s, %s, %s)
         """, (check_no, puc_id, R.username(), balance, entry_date))

    # The overpayment is now balanced, so set it to 0.
    cursor.execute("""
        UPDATE overpayment SET balance = 0
        WHERE puc_id = %s
        """, (puc_id,))

def revoke_reversal_settlement(settlement_id):
    """ Undo a reversal settlement. If distributions have been processed
    for this settlement, then of course those will have to be backed out.
    """
    cursor = R.db.dict_cursor()
    cursor.execute("""
        SELECT reversal_settlement.*, reversal.trans_id
        FROM reversal_settlement
        JOIN reversal USING(reversal_id)
        WHERE settlement_id=%s
        """, (settlement_id,))
    if not cursor.rowcount:
        raise ValueError("Reversal settlement %s not found." % settlement_id)

    settlement = cursor.fetchone()
    trans_id = settlement['trans_id']
    reversal_id = settlement['reversal_id']
    amount = settlement['amount']
    log(trans_id, "Revoked reversal settlement %(settlement_id)s "
                  "for %(amount)s CK %(check_no)s" % settlement)

    cursor.execute("""
        DELETE FROM reversal_settlement
        WHERE settlement_id=%s
        """, (settlement_id,))
    
    # Maintain IV
    cursor.execute("""
        UPDATE reversal SET balance = balance + %s
        WHERE reversal_id=%s
        """, (amount, reversal_id))

    cursor.execute("""
        UPDATE trans SET settled_amount = settled_amount + %s
        WHERE trans_id = %s
        """, (amount, trans_id))

def void_reversal_settlement(settlement_id, void_date=None):
    """ Effectively cancel a reversal settlement. The settlement will not
    affect the balance of the transaction anymore, but will show up in
    transaction history.
    """
    if void_date is None:
        void_date = datetime.datetime.now()

    cursor = R.db.dict_cursor()
    cursor.execute("""
        SELECT reversal_settlement.*, reversal.trans_id
        FROM reversal_settlement
        JOIN reversal USING(reversal_id)
        WHERE settlement_id=%s
        """, (settlement_id,))
    if not cursor.rowcount:
        raise ValueError("Reversal settlement %s not found." % settlement_id)

    settlement = cursor.fetchone()
    trans_id = settlement['trans_id']
    reversal_id = settlement['reversal_id']
    amount = settlement['amount']
    log(trans_id, "Revoked reversal settlement %(settlement_id)s "
                  "for %(amount)s CK %(check_no)s" % settlement)

    cursor.execute("""
        UPDATE reversal_settlement
        SET void_date=%s
        WHERE settlement_id=%s
        """, (void_date, settlement_id))
    
    # Maintain IV
    cursor.execute("""
        UPDATE reversal SET balance = balance + %s
        WHERE reversal_id=%s
        """, (amount, reversal_id))

    cursor.execute("""
        UPDATE trans SET settled_amount = settled_amount - %s
        WHERE trans_id = %s
        """, (amount, trans_id))

def unvoid_reversal_settlement(settlement_id):
    """ If an reversal settlement was voided in error, this procedure
    will cancel the voiding.
    """
    cursor = R.db.cursor()

    # Pull out the reversal reference and the amount we are about to
    # reapply.
    cursor.execute("""
        SELECT reversal_settlement.amount,
               reversal.reversal_id,
               reversal.trans_id
        FROM reversal_settlement
        JOIN reversal USING(reversal_id)
        WHERE settlement_id=%s
        """, (settlement_id,))

    if not cursor.rowcount:
        raise ValueError("Invalid settlement_id %s" % settlement_id)
    amount, reversal_id, trans_id = cursor.fetchone()

    # Do the unvoiding
    cursor.execute("""
        UPDATE reversal_settlement 
        SET void_date = NULL
        WHERE settlement_id=%s
        """, (settlement_id,))

    ## MAINTAIN IV
    # Reapply the settlement amount to the reversal balance
    cursor.execute("""
        UPDATE reversal SET balance = balance - %s
        WHERE reversal_id=%s
        """, (amount, reversal_id))

    # Reapply the amount to the total settled amount on the trans
    cursor.execute("""
        UPDATE trans SET settled_amount = settled_amount + %s
        WHERE trans_id = %s
        """, (amount, trans_id))

    log(trans_id, "Unvoided reversal settlement %s for %s" % (
                    settlement_id, amount))


def unvoid_overpayment_settlement(puc_settle_id):
    """ If an overpayment settlement was voided in error, this procedure
    will cancel the voiding.
    """
    cursor = R.db.cursor()

    # Fetch the settlement record to grab references to the overpayment
    # Fetch the current balance so we know how much to settle and the trans
    # to update the settled amount
    cursor.execute("""
        SELECT overpayment.puc_id,
               overpayment.trans_id,
               overpayment_settlement.amount
        FROM overpayment_settlement
        JOIN overpayment USING(puc_id)
        WHERE puc_settle_id=%s
        """, (puc_settle_id,))

    if not cursor.rowcount:
        raise ValueError("Invalid puc_settle_id %s" % puc_settle_id)

    puc_id, trans_id, amount = cursor.fetchone()

    # Do the unvoiding
    cursor.execute("""
        UPDATE overpayment_settlement
        SET void_date = NULL
        WHERE puc_settle_id=%s
        """, (puc_settle_id,))

    # Reapply the settlement amount to the overpayment balance
    cursor.execute("""
        UPDATE overpayment SET balance = balance - %s
        WHERE puc_id = %s
        """, (amount, puc_id))

class PFCalculator(object):
    """ Provides processing fee calculations for transactions
    """
    def __init__(self):
        # Build Lookup that is keyed on the group number and the transaction
        # type.
        self._lookup = {}
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT group_number, tx_type, distribution_account, amount, percent
            FROM distribution_rule
            WHERE tx_type IS NOT NULL
            """)

        for gn, tx_type, account, amount, percent in cursor:
            key = (gn, tx_type)
            if key not in self._lookup:
                self._lookup[key] = _PFTypeCalc(gn, tx_type)
            calc = self._lookup[key]
            if amount:
                calc.add_fixed_amount(account, amount)
            if percent:
                calc.add_percent_amount(account, percent)

    def get_processing_fees(self, trans):
        """ Provide a list of pairs of the processing fees for the given
        transaction.

        group_number: the group number of the transaction
        tx_type: the 2 character transaction type code of the transaction
        total: the total amount of the transction
        """
        pharm_amount = self.trans_pharm_amount(trans)
        calc = self._lookup[(trans['group_number'], trans['tx_type'])]
        return calc.fees(pharm_amount)

    def set_processing_fee(self, trans):
        """ Set the processing fee for the given transaction record. """
        pharm_amount = self.trans_pharm_amount(trans)
        calc = self._lookup[(trans['group_number'], trans['tx_type'])]
        trans['processing_fee'] = sum(count_money(c[1]) for c in calc.fees(pharm_amount))

    def trans_pharm_amount(self, trans):
        """ The pharm amount is the total amount we use to calculate processing
        fees that are multipliers
        """
        return  (trans['cost_allowed'] +
                 trans['dispense_fee'] +
                 trans['sales_tax'] -
                 trans['eho_network_copay'])

class _PFTypeCalc(object):
    """ Calculates the processing fees for a single type of transaction. """
    def __init__(self, group_number, type):
        self.group_number = group_number
        self.type = type
        self.fixed_fees = []
        self.percent_fees = []

    def add_fixed_amount(self, account, amount):
        self.fixed_fees.append((account, amount))

    def add_percent_amount(self, account, percent):
        self.percent_fees.append((account, percent))

    def fees(self, amount):
        """ Calculate all the processing fees for the given amount. """
        fees = []
        fixed_total = amount
        for account, fee_amt in self.fixed_fees:
            fees.append((account, fee_amt))
            fixed_total += fee_amt

        for account, fee_percent in self.percent_fees:
            fees.append((account, fixed_total * fee_percent))
        return fees

###############################################################################
#{ Date Integritry Checking Procedures. Fixes calculated columns
def check(trans_id):
    """ After having a lot of smaller procedures that delt with
    updating transaction totals or balances, applying the formulas, etc.
    I've decided that having a more coarsly-grained procedure whose job
    it was to assure that the transaction record was consistent would
    be a good idea.

    Some of these procedures depend on the calculated values produced by
    other procedures so they must be called in the correct order. Had
    a bug where the paid date was calculated before the balance.

    """
    check_adjudications(trans_id)
    check_writeoffs(trans_id)
    check_rebill_credit_total(trans_id)
    check_rebate_credit_total(trans_id)
    check_adjustments(trans_id)
    check_paid_amount(trans_id)
    check_transfered_amount(trans_id)
    check_settled_amount(trans_id)
    check_distributed_amount(trans_id)

    check_balance(trans_id)
    check_paid_date(trans_id)
    check_savings(trans_id)

    cursor = R.db.cursor()
    cursor.execute("""
        SELECT invoice_id
        FROM trans
        WHERE trans_id=%s
        """, (trans_id,))
    invoice_id, = cursor.fetchone()
    if invoice_id:
        cpsar.invoice.check(invoice_id)

    check_overpayments(trans_id)

def check_adjudications(trans_id):
    """ 
    @invariant: trans.adjudication_total =
        SUM(trans_adjudication.amount WHERE void_date IS NULL)
    """
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM trans_adjudication
        WHERE trans_id=%s AND void_date IS NULL
        """, (trans_id,))
    calc, = cursor.fetchone()
    cursor.execute("""
        SELECT adjudication_total
        FROM trans
        WHERE trans_id=%s
        """, (trans_id,))
    given, = cursor.fetchone()

    if calc == given:
        return False

    log(trans_id, "Updated adjudication total from %s to %s" %
        (given, calc))

    cursor.execute("""
        UPDATE trans SET adjudication_total=%s
        WHERE trans_id=%s""", (calc, trans_id))
    return True

def check_writeoffs(trans_id):
    """ @invariant: trans.writeoff_total
        = SUM(trans_writeoff.amount WHERE void_date IS NULL) """
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM trans_writeoff
        WHERE trans_id=%s AND void_date IS NULL
        """, (trans_id,))
    calc, = cursor.fetchone()
    cursor.execute("""
        SELECT writeoff_total
        FROM trans
        WHERE trans_id=%s
        """, (trans_id,))
    given, = cursor.fetchone()

    if calc == given:
        return False

    log(trans_id, "Updated writeoff total from %s to %s" %
        (given, calc))

    cursor.execute("""
        UPDATE trans SET writeoff_total=%s
        WHERE trans_id=%s""", (calc, trans_id))

    return True

def check_rebill_credit_total(trans_id):
    """ @invariant: trans.rebill_credit_total = SUM(rebill_credit.amount)
    """
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM rebill_credit
        WHERE trans_id=%s
        """, (trans_id,))
    calc, = cursor.fetchone()
    cursor.execute("""
        SELECT rebill_credit_total
        FROM trans
        WHERE trans_id=%s
        """, (trans_id,))
    given, = cursor.fetchone()

    if calc == given:
        return False

    log(trans_id, "Updated rebill credit total from %s to %s" %
        (given, calc))
    cursor.execute("""
        UPDATE trans SET rebill_credit_total=%s
        WHERE trans_id=%s""", (calc, trans_id))

    return True

def check_rebate_credit_total(trans_id):
    """ @invariant: trans.rebate_credit_total = SUM(rebate_credit.amount)
    """
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM rebate_credit
        WHERE trans_id=%s
        """, (trans_id,))
    calc, = cursor.fetchone()
    cursor.execute("""
        SELECT rebate_credit_total
        FROM trans
        WHERE trans_id=%s
        """, (trans_id,))
    given, = cursor.fetchone()

    if calc == given:
        return False

    log(trans_id, "Updated rebate credit total from %s to %s" %
        (given, calc))
    cursor.execute("""
        UPDATE trans SET rebate_credit_total=%s
        WHERE trans_id=%s""", (calc, trans_id))
    return True

def check_adjustments(trans_id):
    """ @invariant: trans.adjustments = trans.debit_total
            - trans.adjudication_total - trans.writeoff_total
            - trans.rebill_credit_total
    """
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT adjustments,
               debit_total - adjudication_total - writeoff_total
               - rebill_credit_total
        FROM trans
        WHERE trans_id=%s
        """, (trans_id,))
    given, calc = cursor.fetchone()

    if calc == given:
        return False

    log(trans_id, "Updated adjustments from %s to %s" % (given, calc))
    cursor.execute("""
        UPDATE trans SET adjustments=%s
        WHERE trans_id=%s""", (calc, trans_id))
    return True

def check_settled_amount(trans_id):
    """ @invariant: trans.settled_amount =
                    SUM(reversal_settlement.amount WITH void_date IS NULL) 
    """
    cursor = R.db.cursor()

    # Fetch the total amount of reversal settlements
    cursor.execute("""
        SELECT COALESCE(SUM(reversal_settlement.amount), 0.00)
        FROM trans
        JOIN reversal USING(trans_id)
        JOIN reversal_settlement USING(reversal_id)
        WHERE trans.trans_id=%s AND
              reversal_settlement.void_date IS NULL
        """, (trans_id,))
    calc, = cursor.fetchone()

    # Fetch the computed settled amount stored on the trans
    cursor.execute("""
        SELECT settled_amount
        FROM trans
        WHERE trans_id=%s
        """, (trans_id,))
    given, = cursor.fetchone()

    # Ensure values are the same or fix
    if calc == given:
        return False

    cursor.execute("""
        UPDATE trans SET settled_amount=%s WHERE trans_id=%s
        """, (calc, trans_id))
    return True

def check_transfered_amount(trans_id):
    """ @invariant: SUM(group_credit.amount WHERE source_reversal_id = reversal.reversal_id)
    """
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT COALESCE(SUM(group_credit.amount), 0.00)
        FROM group_credit
        JOIN reversal on group_credit.source_reversal_id = reversal.reversal_id
        WHERE reversal.trans_id=%s
        """, (trans_id,))
    calc, = next(cursor)

    cursor .execute("""
        select transfered_amount from trans where trans_id=%s
        """, (trans_id,))

    given, = next(cursor)
    if calc == given:
        return False

    cursor.execute("""
        update trans set transfered_amount = %s where trans_id=%s
        """, (calc, trans_id))
    return True

def check_paid_amount(trans_id):
    """ @invariant: trans.paid_amount = SUM(trans_payment.amount) +
                    SUM(rebate_credit.amount WHERE void_date IS NULL) 
                    - SUM(group_credit.amount WHERE source_reversal_id=reversal_id)
    """
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0.00)
        FROM trans_payment
        WHERE trans_id=%s
        """, (trans_id,))
    payment_sum, = cursor.fetchone()

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0.00)
        FROM rebate_credit
        WHERE trans_id=%s AND void_date IS NULL
        """, (trans_id,))
    rebate_sum, = cursor.fetchone()

    calc = payment_sum + rebate_sum

    cursor.execute("""
        SELECT paid_amount
        FROM trans
        WHERE trans_id=%s
        """, (trans_id,))
    given, = cursor.fetchone()

    if calc == given:
        return False

    cursor.execute("""
        UPDATE trans SET paid_amount=%s WHERE trans_id=%s
        """, (calc, trans_id))

    return True

def check_balance(trans_id):
    """ Responsible for fixing a transaction balance if needed. This a one
    transaction version of the functionality in ar-trans-balance.

    @invariant: trans.balance = trans.total + trans.adjustments -
                trans.paid_amount
    """
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT total, adjustments, balance, paid_amount
        FROM trans
        WHERE trans_id = %s
        """, (trans_id,))

    if not cursor.rowcount:
        raise_(ValueError, 'Invalid trans #' % trans_id)
    total, adjustments, given, paid_amount = cursor.fetchone()

    calculated = total + adjustments - paid_amount
    if given == calculated:
        return False

    log(trans_id, 'Updating balance from %s to %s' % (given, calculated))
    cursor.execute("""
        UPDATE trans SET balance=%s WHERE trans_id=%s
        """, (calculated, trans_id))

    return True

def check_paid_date(trans_id):
    """ Responsible for setting the paid date to 0 when the transaction is
    fully paid.

    @invariant: trans.paid_date = MAX(
        trans_payment.entry_date, 
        trans_adjudication.entry_date WHERE void_date IS NULL, 
        trans_writeoff.entry_date WHERE void_date IS NULL
        ) IF trans.balance = 0
    """
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT balance, paid_date
        FROM trans
        WHERE trans_id=%s""",
        (trans_id,))
    balance, given = cursor.fetchone()
    if balance != 0:
        return

    cursor.execute("""
        SELECT MAX(entry_date::date)
        FROM (
            SELECT MAX(entry_date) AS entry_date
            FROM trans_payment
            WHERE trans_id=%s
            UNION ALL
            SELECT MAX(entry_date) AS entry_date
            FROM trans_adjudication
            WHERE trans_id=%s AND void_date IS NULL
            UNION ALL
            SELECT MAX(entry_date) AS entry_date
            FROM trans_writeoff
            WHERE trans_id=%s AND void_date IS NULL) AS e
        """, (trans_id, trans_id, trans_id))
    calc, = cursor.fetchone()
    if calc and calc != given:
        cursor.execute("""
            UPDATE trans
            SET paid_date = %s
            WHERE trans_id=%s""",
            (calc, trans_id))
        log(trans_id, "Updating paid date to %s" % calc)
        return True
    elif not given:
        calc = datetime.datetime.today()
        cursor.execute("""
            UPDATE trans
            SET paid_date = %s
            WHERE trans_id=%s""",
        (calc, trans_id))
        log(trans_id, "Updating paid date to %s" % calc)
        return True
    return False

def check_savings(trans_id):
    """ Savings in calculated from the state fee schedule or awp depending
    on the client record. Even if the client is set to AWP, we fall back
    on the state fee schedule when the transaction does not have an AWP
    value.  This is because we historically do not have the AWP's for all 
    transactions.

    @invariant: ::
         if client.savings_formula = 'SFS':
            trans.savings = trans.state_fee - trans.total
         elif client.savings_formula = 'UC':
            trans.savings = trans.usual_customary - trans.total
         else:
            trans.savings = trans.awp - trans.total
    """
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT savings, 
            CASE WHEN savings_formula = 'SFS'
                      THEN state_fee - total
                 WHEN savings_formula = 'AWP' AND awp IS NOT NULL
                      THEN awp - total
                 WHEN savings_formula = 'UC' AND usual_customary IS NOT NULL
                    THEN usual_customary - total
                 ELSE state_fee - total
            END
        FROM trans
        JOIN client ON
            trans.group_number = client.group_number
        WHERE trans_id=%s
        """, (trans_id,))
    given, calc = cursor.fetchone()
    if given != calc:
        log(trans_id, "Updating savings from %s to %s" % (given, calc))
        cursor.execute("""
            UPDATE trans SET savings=%s WHERE trans_id=%s""",
            (calc, trans_id))

def check_distributed_amount(trans_id):
    """ @invariant: trans.distributed_amount = SUM(distribution.amount WITH
                    valid distribution_date)
    """
    cursor = R.db.cursor()
    cursor.execute(
        "SELECT distributed_amount FROM trans WHERE trans_id=%s",
        (trans_id,))

    given, = cursor.fetchone()
    cursor.execute("""
        SELECT SUM(amount)
        FROM distribution
        WHERE distribution_date IS NOT NULL AND trans_id=%s
        """, (trans_id,))
    calc, = cursor.fetchone()
    if calc is None:
        calc = ZERO
    if given != calc:
        log(trans_id, "Updating distributed_amount from %s to %s" %
                        (given, calc))
        cursor.execute("""
            UPDATE trans SET distributed_amount=%s WHERE trans_id=%s""",
            (calc, trans_id))

def check_distributed_amount_all():
    """
    @invariant: trans.distributed_amount = SUM(distribution.amount WITH
                                   VALID distribution_date)
    @change: This logic has historically been placed in ar-audit-trans but I'm
             trying to modularize the system better.
    """
    cursor = R.db.cursor()
    cursor.execute(
        """
        SELECT COALESCE(trans.trans_id, dist.trans_id) AS trans_id,
               COALESCE(trans.distributed_amount, 0),
               COALESCE(dist.amount, 0)
        FROM trans
        FULL OUTER JOIN
            (SELECT trans_id, SUM(amount) AS amount
             FROM distribution
             WHERE distribution_date IS NOT NULL
             GROUP BY trans_id) AS dist
        ON trans.trans_id = dist.trans_id
        WHERE COALESCE(trans.distributed_amount, 0) <> COALESCE(dist.amount, 0)
        """)
    for trans_id, given, calc in list(cursor):
        log(trans_id, "Updating distributed_amount from %s to %s" %
                        (given, calc))
        cursor.execute("""
            UPDATE trans SET distributed_amount=%s WHERE trans_id=%s""",
            (calc, trans_id))

def check_overpayments_all():
    """ @invariant: overpayment.balance = SUM(trans_payment.amount WITH puc_id)
    """
    cursor = R.db.cursor()
    cursor.execute("""
      SELECT X.puc_id, overpayment.amount - X.calc 
      FROM (
        SELECT puc_id, SUM(amount) AS calc
        FROM trans_payment
        WHERE puc_id IS NOT NULL
        GROUP BY puc_id
        ) AS X

        JOIN overpayment ON 
        X.puc_id = overpayment.puc_id
        WHERE overpayment.amount - X.calc != overpayment.balance
        """)
    for puc_id, calc in list(cursor):
        cursor.execute("""UPDATE overpayment
            SET balance=%s
            WHERE puc_id=%s
            """, (calc, puc_id))

def check_overpayments(trans_id):
    """ @invariant: overpayment.balance = overpayment.total -
                    SUM(trans_payment.amount WITH puc_id) -
                    SUM(overpayment_settlement.amount WITH puc_id
                        AND void_date IS NULL)
    An overpayment's balance is what is left of the overpayment's amount
    after you take into consideration the payments that have been created
    from the overpayment and the settlements that have been created for
    the overpayment.
    """
    cursor = R.db.cursor()

    # There may be more than one overpayment for the given trans so check
    # them all.
    cursor.execute("""
        SELECT overpayment.puc_id,
               overpayment.balance,
               overpayment.amount
        FROM overpayment
        WHERE overpayment.trans_id=%s
        """, (trans_id,))
    for puc_id, given, amount in list(cursor):
        # What payments are created from the the overpayment
        cursor.execute("""
            SELECT COALESCE(SUM(trans_payment.amount), 0)
            FROM trans_payment
            WHERE puc_id=%s
            """, (puc_id,))
        applied, = cursor.fetchone()

        # What settleemnts are created from the overpayment?
        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM overpayment_settlement
            WHERE puc_id=%s AND void_date IS NULL
            """, (puc_id,))
        settled, = cursor.fetchone()

        # Check IV
        calculated = amount - applied - settled
        if calculated != given:
            cursor.execute("""
                UPDATE overpayment
                SET balance = %s
                WHERE puc_id=%s
                """, (calculated, puc_id))

def check_reversal(reversal_id):
    check_reversal_total(reversal_id)
    check_reversal_balance(reversal_id)

def check_reversal_total(reversal_id):
    """ @invariant: reversal.total = trans.cost_allowed + trans.dispense_fee +
                    trans.sales_tax + trans.processing_fee -
                    trans.eho_network_copay
    """
    cursor = R.db.cursor()

    # Do we have a reversal that needs updating as well?
    cursor.execute("""
        SELECT total, trans_id
        FROM reversal
        WHERE reversal_id=%s
        """, (reversal_id,))
    given, trans_id = cursor.fetchone()

    if not trans_id:
        return

    cursor.execute("""
        SELECT cost_allowed + dispense_fee + sales_tax +
               processing_fee - eho_network_copay
        FROM trans
        WHERE trans_id=%s""", (trans_id,))
    calc, = cursor.fetchone()

    if given != calc:
        log(trans_id, 'Updating reversal %s total from %s to %s' %
                (reversal_id, given, calc))
        cursor.execute("""
            UPDATE reversal SET total=%s WHERE reversal_id=%s
            """, (calc, reversal_id))

def check_reversal_balance(reversal_id):
    """ @invariant: reversal.balance = reversal.total -
                    SUM(trans_adjudication.amount WHERE void_date IS NULL) -
                    SUM(reversal_settlement.amount) -
                    SUM(group_credit.amount WHERE source_reversal_id = reverse_id)
    """
    cursor = R.db.cursor()
    # Fetch the balance we are ensuring is correct and the total
    # of the reversal that is subtracted from
    cursor.execute("""
        SELECT reversal.balance, reversal.total
        FROM reversal
        WHERE reversal.reversal_id=%s
        """, (reversal_id,))
    given, total = cursor.fetchone()

    # Fetch the adjudications for the reversal that are applied
    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)::numeric
        FROM trans_adjudication
        WHERE reversal_id=%s AND void_date IS NULL
        """, (reversal_id,))
    adjduciated_calc, = cursor.fetchone()

    # Fetch the settlements for the reversal
    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)::numeric
        FROM reversal_settlement
        WHERE reversal_id=%s AND void_date IS NULL
        """, (reversal_id,))
    settled, = cursor.fetchone()

    # Ensure the calculated field is correct, If not, fix it.

    # Fetch the group credits
    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)::numeric
        FROM group_credit
        WHERE source_reversal_id = %s
        """, (reversal_id,))
    group_credit, = next(cursor)

    calc = total - adjduciated_calc - settled - group_credit

    if given != calc:
        cursor.execute("""
            UPDATE reversal SET balance = %s
            WHERE reversal_id=%s
        """, (calc, reversal_id))
        return False
    else:
        return True

#}

###############################################################################
## Object-based data access

class Transaction(object):
    """ A data-access object for the trans relation in the database,
    along with properties for foreign references.
    """
    @classmethod
    def from_record(cls, record):
        """ construct a transaction object from a transaction record in the
        backend.
        """
        tx = cls(record['trans_id'])
        tx.record = record
        return tx

    @classmethod
    def from_group_auth(cls, gn, ga):
        """ Create a transaction record from the group number and the claim
        reference number.
        """
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT *
            FROM trans
            WHERE group_number=%s AND group_auth=%s
            """, (gn, ga))
        if not cursor.rowcount:
            raise ValueError("%s:%s not found" % (gn, ga))
        rec = cursor.fetchone()
        tx = cls(rec['trans_id'])
        tx.record = rec
        return tx

    def __init__(self, trans_id):
        self.trans_id = trans_id
        self._record = None

    def _get_record(self):
        if self._record is None:
            cursor = R.db.dict_cursor()
            cursor.execute("""
                SELECT *,
                       paid_amount - settled_amount - distributed_amount - transfered_amount
                       AS left_to_distribute
                FROM trans WHERE trans_id=%s""",
                           (self.trans_id,))
            self._record = cpsar.pg.one(cursor)
        return self._record
    def _set_record(self, r):
        self._record = r
        self._patient = None
        self._drug = None
    record = property(_get_record, _set_record)

    def __getattr__(self, attr):
        if attr in self.record:
            return self.record[attr]
        raise AttributeError(attr)

    @property
    def left_to_distribute(self):
        return self.paid_amount - settled_amount - distributed_amount - self.reversal_group_credit_amount

    @property
    def reversal_group_credit_amount(self):
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT COALESCE(SUM(group_credit.amount), 0.00)
            FROM group_credit
            JOIN reversal ON group_credit.source_reversal_id = reversal.reversal_id
            WHERE reversal.trans_id = %s
            """, (self.trans_id,))
        if cursor.rowcount:
            return next(cursor)
        else:
            reversal_group_credit = 0

    @property
    def cost_allowed_editable(self):
        """ Can the cost allowed be changed on this transaction? """
        if self.reversal or self._has_adjudication or self._has_writeoff:
            return False
        else:
            return True

    @property
    @imemoize
    def patient(self):
        cursor = R.db.dict_cursor()
        cursor.execute("SELECT * FROM patient WHERE patient_id=%s",
                       (self.patient_id,))
        return cpsar.pg.one(cursor)

    @property
    def age(self):
        return (datetime.datetime.now() - self.create_date).days

    @property
    @imemoize
    def invoice(self):
        cursor = R.db.dict_cursor()
        cursor.execute("SELECT * FROM invoice WHERE invoice_id=%s",
                       (self.invoice_id,))
        return cpsar.pg.one(cursor)

    @property
    @imemoize
    def pharmacist(self):
        if not self.history['pharmacist_id']:
            return None
        cursor = R.db.dict_cursor()
        cursor.execute("SELECT * FROM pharmacist WHERE pharmacist_id=%s",
                       (self.history['pharmacist_id'],))
        return cpsar.pg.one(cursor)

    @property
    @imemoize
    def place_of_service(self):
        if not self.history['place_of_service_id']:
            return None
        cursor = R.db.dict_cursor()
        cursor.execute("SELECT * FROM pharmacy WHERE pharmacy_id=%s",
                       (self.history['place_of_service_id'],))
        return cpsar.pg.one(cursor)

    @property
    @imemoize
    def drug(self):
        cursor = R.db.dict_cursor()
        cursor.execute("SELECT * FROM drug WHERE drug_id=%s",
                       (self.drug_id,))
        return cpsar.pg.one(cursor)

    @property
    @imemoize
    def report_entries(self):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT state_report_entry.srid,
                   null::int as reversal_id,
                   state_report_entry.create_time::date AS create_date,
                   state_report_entry.claim_freq_type_code,
                   state_report_entry.control_number,
                   state_report_file.file_name
            FROM state_report_entry
            LEFT JOIN state_report_file USING(sr_file_id)
            WHERE trans_id = %s
            UNION
            SELECT state_report_entry.srid,
                   state_report_entry.reversal_id,
                   state_report_entry.create_time::date AS create_date,
                   state_report_entry.claim_freq_type_code,
                   state_report_entry.control_number,
                   state_report_file.file_name
            FROM reversal
            JOIN state_report_entry USING(reversal_id)
            LEFT JOIN state_report_file USING(sr_file_id)
            WHERE reversal.trans_id = %s
            """, (self.trans_id, self.trans_id))
        return cpsar.pg.all(cursor)

    @property
    @imemoize
    def has_sr_ndc_override(self):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT
                temp_sr_ndc_flag
            FROM history
            JOIN trans USING(history_id)
            WHERE trans_id = %s
            """, (self.trans_id,))
        flag, = cursor.fetchone()

        if flag:
            return True 
        else:
            return False

    def has_reversal_settlement(self):
        cursor = R.db.cursor()
        cursor.execute("""
            select count(*)
            from reversal_settlement
            join reversal using(reversal_id)
            join trans using(trans_id)
            where trans_id = %s and reversal_settlement.void_date is null
            """, (self.trans_id,))
        return next(cursor)[0] > 0

    @property
    @imemoize
    def ndc_override(self):
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT
                temp_sr_ndc_override
            FROM history
            JOIN trans USING(history_id)
            WHERE trans_id = %s
            """, (self.trans_id,))
        ndc, = cursor.fetchone()

    _client = None
    @property
    def client(self):
        if self._client is None:
            cursor = R.db.dict_cursor()
            cursor.execute("SELECT * FROM client WHERE group_number=%s",
                           (self.group_number,))
            self._client = cpsar.pg.one(cursor)
        return self._client

    _pharmacy = None
    @property
    def pharmacy(self):
        if self._pharmacy is None:
            cursor = R.db.dict_cursor()
            cursor.execute("SELECT * FROM pharmacy WHERE pharmacy_id=%s",
                           (self.pharmacy_id,))
            self._pharmacy = cpsar.pg.one(cursor)
        return self._pharmacy

    _doctor = None
    @property
    def doctor(self):
        if self._doctor is None:
            cursor = R.db.dict_cursor()
            cursor.execute("SELECT * FROM doctor WHERE doctor_id=%s",
                           (self.doctor_id,))
            self._doctor = cpsar.pg.one(cursor)
            if not self._doctor:
                return None
            self._doctor['npi_number'] = None
            self._doctor['dea_number'] = None
            if self._doctor:
                cursor.execute("SELECT doc_key FROM doctor_key WHERE doctor_id=%s",
                    (self._doctor['doctor_id'],))
                for rec in cursor:
                    doc_key = rec['doc_key']
                    if len(doc_key) == 9:
                        self._doctor['dea_number'] = doc_key
                    else:
                        self._doctor['npi_number'] = doc_key

        return self._doctor

    _employer = None
    @property
    def employer(self):
        if self.claim and self.claim['employer_tin']:
            cursor = R.db.dict_cursor()
            cursor.execute("""
                SELECT *
                FROM employer
                WHERE group_number=%s AND tin=%s
                """, (self.group_number, self.claim['employer_tin']))
            if cursor.rowcount:
                self._employer = cpsar.pg.one(cursor)
        return self._employer

    _logs = None
    @property
    def logs(self):
        if self._logs is None:
            cursor = R.db.dict_cursor()
            cursor.execute("""
                SELECT *
                FROM trans_log
                WHERE trans_id=%s
                ORDER BY entry_date DESC
                """, (self.trans_id,))
            self._logs = cpsar.pg.all(cursor)
        return self._logs

    _adjuster1 = None
    @property
    def adjuster1(self):
        if self._adjuster1 is None and self.adjuster1_email is not None:
            cursor = R.db.dict_cursor()
            cursor.execute("SELECT * FROM user_info WHERE email=%s",
                           (self.adjuster1_email,))
            self._adjuster1 = cpsar.pg.one(cursor)
        return self._adjuster1

    _adjuster2 = None
    @property
    def adjuster2(self):
        if self._adjuster2 is None and self.adjuster2_email is not None:
            cursor = R.db.dict_cursor()
            cursor.execute("SELECT * FROM user_info WHERE email=%s",
                           (self.adjuster2_email,))
            self._adjuster2 = cpsar.pg.one(cursor)
        return self._adjuster2

    _overpayments = None
    @property
    def overpayments(self):
        if self._overpayments is None:
            cursor = R.db.dict_cursor()
            cursor.execute("""
                SELECT *
                FROM overpayment
                WHERE trans_id=%s
                """, (self.trans_id,))
            self._overpayments = cpsar.pg.all(cursor)

            for u in self._overpayments:
                cursor.execute("""
                    SELECT 'TX' AS type, trans_id AS ref_id
                    FROM trans_payment AS puc
                    WHERE puc_id = %s
                    UNION ALL
                    SELECT 'SET', pucs.puc_settle_id
                    FROM overpayment_settlement AS pucs
                    WHERE puc_id = %s
                """, (u['puc_id'], u['puc_id']))

                u['applications'] = list(cursor)
        return self._overpayments

    @property
    @imemoize
    def ingredients(self):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT history_ingredient.*, drug.name AS drug_name,
                   drug.ndc_number
            FROM history_ingredient
            LEFT JOIN drug USING(drug_id)
            WHERE history_id = %s
            ORDER BY ingredient_nbr
            """, (self.history_id,))
        return list(cursor)

    _payments = None
    @property
    def payments(self):
        if self._payments is None:
            cursor = R.db.dict_cursor()
            cursor.execute("""
                SELECT *
                FROM trans_payment
                WHERE trans_id=%s
                ORDER BY payment_id
                """, (self.trans_id,))
            self._payments = cpsar.pg.all(cursor)
        return self._payments

    @property
    def _has_writeoff(self):
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT COUNT(*)
            FROM trans_writeoff
            WHERE trans_id=%s
            """, (self.trans_id,))
        return cursor.fetchone()[0] > 0

    @property
    def _has_adjudication(self):
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT COUNT(*)
            FROM trans_adjudication
            WHERE trans_id=%s
            """, (self.trans_id,))
        return cursor.fetchone()[0] > 0

    _reversal = None
    @property
    def reversal(self):
        if self._reversal is None:
            cursor = R.db.dict_cursor()
            cursor.execute("SELECT * FROM reversal WHERE trans_id=%s",
                           (self.trans_id,))
            self._reversal = cpsar.pg.one(cursor)
        return self._reversal

    _reversal_settlement = None
    @property
    def reversal_settlement(self):
        if self._reversal_settlement:
            return self._reversal_settlement
        if self.reversal:
            cursor = R.db.dict_cursor()
            cursor.execute("""
                SELECT *
                FROM reversal_settlement
                WHERE reversal_id=%s""",
               (self.reversal['reversal_id'],))
            if cursor.rowcount:
                self._reversal_settlement = cpsar.pg.one(cursor)
            else:
                self._reversal_settlement = None
        return self._reversal_settlement


    _pending_reversal_settlement = None
    @property
    def pending_reversal_settlement(self):
        if self._pending_reversal_settlement:
            return self._pending_reversal_settlement
        if self.reversal:
            cursor = R.db.dict_cursor()
            cursor.execute("""
                SELECT *
                FROM pending_reversal_settlement
                WHERE reversal_id=%s""",
               (self.reversal['reversal_id'],))
            if cursor.rowcount:
                self._pending_reversal_settlement = cpsar.pg.one(cursor)
            else:
                self._pending_reversal_settlement = None
        return self._pending_reversal_settlement

    _adj_candidates = None
    @property
    def adj_candidates(self):
        if self._adj_candidates is None:
            cursor = R.db.dict_cursor()
            cursor.execute("""
                SELECT reversal.*,
                       trans.invoice_id,
                       trans.line_no
                FROM reversal
                JOIN trans ON
                    trans.patient_id = %s AND
                    reversal.trans_id = trans.trans_id AND
                    reversal.balance <> 0
                """, (self.patient_id,))

            self._adj_candidates = cpsar.pg.all(cursor)
        return self._adj_candidates

    _adj_txs = None
    @property
    def adj_txs(self):
        if self._adj_txs is None:
            cursor = R.db.dict_cursor()
            cursor.execute("""
                SELECT trans.*, drug.name as drug_name
                FROM trans
                JOIN drug ON
                    trans.drug_id = drug.drug_id
                WHERE patient_id=%s AND
                      balance <> 0
                ORDER BY batch_date DESC
                """, (self.patient_id,))
            self._adj_txs = cpsar.pg.all(cursor)
        return self._adj_txs

    _distributions = None
    @property
    def distributions(self):
        if self._distributions is None:
            cursor = R.db.dict_cursor()
            cursor.execute("""
                SELECT *
                FROM distribution
                WHERE trans_id=%s
                """, (self.trans_id,))
            self._distributions = cpsar.pg.all(cursor)
        return self._distributions

    _distribution_rules = None
    @property
    def distribution_rules(self):
        if self._distribution_rules is None:
            cursor = R.db.dict_cursor()
            cursor.execute("""
                SELECT distribution_account, amount
                FROM distribution_rule
                WHERE group_number=%s AND tx_type=%s
                UNION ALL
                SELECT 'pharmacy' AS distribution_account,
                       cost_allowed + dispense_fee + sales_tax - eho_network_copay
                       AS amount
                FROM trans WHERE trans_id = %s
                ORDER BY distribution_account
                """, (self.group_number,
                      self.tx_type,
                      self.trans_id))
            self._distribution_rules = cpsar.pg.all(cursor)
        return self._distribution_rules

    @property
    @imemoize
    def history(self):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT *
            FROM history
            WHERE history_id=%s
            """, (self.history_id,))
        return cpsar.pg.one(cursor)

    @property
    @imemoize
    def history_distributions(self):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            select *
            from history_distribution
            where history_id=%s
            order by line_no
            """, (self.history_id,))
        return cpsar.pg.all(cursor)

    @property
    @imemoize
    def history_distribution_total(self):
        cursor = R.db.cursor()
        cursor.execute("""
            select sum(amount)
            from history_distribution
            where history_id=%s
            """, (self.history_id,))
        return next(cursor)[0]

    _history_addons = None
    @property
    def history_addons(self):
        if self._history_addons is None:
            cursor = R.db.dict_cursor()
            cursor.execute("""
                SELECT *
                FROM history_addon
                WHERE history_id=%s
                """, (self.history_id,))
            self._history_addons = cpsar.pg.all(cursor)
        return self._history_addons

    @property
    def history_addon_summed(self):
        return sum(s['amount'] for s in self.history_addons)

    _claim = None
    @property
    def claim(self):
        if self._claim:
            return self._claim
        if self.history:
            cursor = R.db.dict_cursor()
            cursor.execute("""
                SELECT *
                FROM claim
                WHERE claim_id=%s
                """, (self.history['claim_id'],))
            if cursor.rowcount:
                self._claim = cpsar.pg.one(cursor)
        return self._claim

    _edited_pharmacy = None
    @property
    def edited_pharmacy(self):
        if self._edited_pharmacy:
            return self._edited_pharmacy

        if self.history:
            cursor = R.db.dict_cursor()
            cursor.execute("""
                SELECT pharmacy.*
                FROM history_edits
                JOIN pharmacy ON
                    history_edits.pharmacy_id = pharmacy.pharmacy_id
                WHERE history_edits.history_id = %s
                """, (self.history['history_id'],))
            if cursor.rowcount:
                self._edited_pharmacy = cpsar.pg.one(cursor)
        return self._edited_pharmacy



###############################################################################
#{ Utility
suppress_log = False

def log(trans_id, msg):
    """ Log activity for a transaction. Adds an entry to the global AR
    log and also adds an entry to the transaction log table to show the
    message on the transaction screen.
    """
    global suppress_log
    if not isinstance(trans_id, int):
        trans_id = int(trans_id)
    logg.info("Transaction %08d: %s" % (trans_id, msg))
    if suppress_log:
        return

    cursor = R.db.cursor()
    cursor.execute(insert_sql("trans_log", {
      "trans_id": trans_id,
      "message": msg,
      "username": R.username()}))

def _fix_date(inDate):
    """run a process to a timestamp to a date field (entry_date) in 
    this case."""

    if not inDate:
        outDate = datetime.datetime.now()
    else:
        outDate = ('%s %s' % (inDate, datetime.datetime.now().strftime("%T")))
 
    return outDate

#}
