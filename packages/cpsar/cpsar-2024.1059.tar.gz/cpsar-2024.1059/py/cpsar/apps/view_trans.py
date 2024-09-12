import collections
import datetime
import os
import urllib.parse
from decimal import Decimal

import cpsar.rebate as RB
import cpsar.runtime as R
import cpsar.txlib
import cpsar.ws as W

from cpsar import pg
from cpsar.util import imemoize

class Program(W.MakoProgram):
    messages = {
        'rp' : 'Payment revoked',
        'rw' : 'Write Off revoked',
        'ra' : 'Adjudication revoked',
        'cr' : 'Reversal balance marked for settlement',
        'cgr': 'Reversal balance applied to group credits',
        'cm' : 'Reversal balance unmarked for settlement',
        'ud' : 'Overpayment revoked'
    }

    def payment_types(self):
        cursor = R.db.dict_cursor()
        cursor.execute("""
          SELECT ptype_id, type_name, default_ref_no,
             type_name
                || COALESCE(' *' || substring(default_ref_no from length(default_ref_no)-3), '')
                AS caption
          FROM payment_type
          WHERE group_number = %s OR group_number IS NULL
          ORDER BY COALESCE(group_number, '--'), ptype_id
          """, (self.trans.group_number,))
        return list(cursor)
          
    @property
    def trans_id(self):
        try:
            return int(self.fs.getvalue('trans_id', 0))
        except ValueError:
            return 0

    @property
    @imemoize
    def trans(self):
        return cpsar.txlib.Transaction(self.trans_id)

    @property
    @imemoize
    def rebate(self):
        return RB.for_trans_id(self.trans_id)

    @property
    @imemoize
    def batch_file(self):
        if self.trans.batch_file_id:
            return BatchFile.for_id(self.trans.batch_file_id)
        else:
            return None

    def main(self):
        if not self.trans_id:
            raise W.HTTPNotFound()
        if not self.trans:
            raise W.HTTPNotFound(str(self.trans_id))
        self.trans.history_distributions
        self.tmpl['trans'] = self.trans
        self.tmpl['rebate'] = self.rebate
        self.tmpl['activity'] = activity(self.trans_id)
        self.tmpl['pk_sup'] = pk_sup_data(self.trans_id)
        self.tmpl['has_rebate_funds_available'] = RB.has_rebate_funds_available(self.trans_id)
        self.tmpl['rebates_with_balances'] = RB.rebates_with_balances_for(self.trans_id)
        self.tmpl['rebate'] = self.rebate
        self.tmpl.update(self.trans.record)

ZERO = Decimal("0.00")

class BatchFile(object):
    @classmethod
    def for_id(cls, batch_file_id):
        cursor = R.db.dict_cursor()
        cursor.execute(
          "SELECT * FROM batch_file WHERE batch_file_id=%s",
          (batch_file_id,))
        if not cursor.rowcount:
            raise ValueError(batch_file_id)
        return cls(cursor.fetchone())

    def __init__(self, dbrec):
        for k, v in dbrec.items():
            setattr(self, k, v)

class ActivityRow:
    """ Abstract Base Class for objects which provide the data for a
    row on the view trans screen.
    """
    @classmethod
    def records(cls, trans_id):
        return []

    desc = 'entry'
    source = ''
    dest = ''

    balance = ZERO
    reversal = ZERO
    overpaid = ZERO
    rebill = ZERO
    paid = ZERO
    settled = ZERO
    distributed = ZERO
    transfered = ZERO

    links = []
    qs = ''

    def __init__(self, rec):
        self.rec = rec

    def __getattr__(self, attr):
        return self.rec.get(attr, '')

    def buttons(self):
        html = []
        for link, label in self.links:
            html.append('<a class="button" href="%s?%s">%s</a>' %
                        (link, self.qs, label))
        return "".join(html)

    @property
    def sort_priority(self):
        e = self.entry_date
        return (datetime.date(e.year, e.month, e.day), 0)

class InvoiceRow(ActivityRow):
    @classmethod
    def records(cls, trans_id):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT trans.create_date,
                   trans.total,
                   trans.invoice_id,
                   trans.line_no,
                   trans.trans_id,
                   trans.rebilled_trans_id
            FROM trans
            WHERE trans_id = %s
            """, (trans_id,))
        return map(cls, cursor)

    @property
    def entry_date(self):
        return self.create_date

    desc = 'invoice'

    @property
    def ref(self):
        return "IN: %s-%s" % (self.invoice_id, self.line_no)

    @property
    def dest(self):
        return "TX: %s" % self.trans_id

    @property
    def source(self):
        if self.rebilled_trans_id:
            return txl(self.rebilled_trans_id, "TX: %s" % self.rebilled_trans_id)
        else:
            return ''

    @property
    def balance(self):
        return self.total

class VoidRebateRow(ActivityRow):
    @classmethod
    def records(cls, trans_id):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT rebate_credit.void_date AS entry_date,
                   rebate_credit.username,
                   rebate_credit.amount,
                   rebate_credit.rebate_id,
                   rebate_credit.rebate_credit_id,
                   rebate.trans_id AS source_trans_id,
                   NULL AS note
            FROM rebate_credit
            JOIN rebate USING(rebate_id)
            WHERE rebate_credit.trans_id=%s
              AND rebate_credit.void_date IS NOT NULL
        """, (trans_id,))
        return map(cls, cursor)

    desc = 'void'

    @property
    def source(self):
        return 'RB: %s' % self.rebate_credit_id

    @property
    def balance(self):
        return self.amount

    @property
    def paid(self):
        return -self.amount

    def buttons(self):
        t = "<a class='button' href='/rebate/unvoid_credit?rebate_credit_id=%s'>Unvoid</a>"
        return t % self.rebate_credit_id

    @property
    def sort_priority(self):
        e = self.entry_date
        return (datetime.date(e.year, e.month, e.day), 1)

class RebateRow(ActivityRow):
    @classmethod
    def records(cls, trans_id):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT rebate_credit.entry_date,
                   rebate_credit.username,
                   rebate_credit.amount,
                   rebate_credit.rebate_id,
                   rebate_credit.rebate_credit_id,
                   rebate_credit.trans_id,
                   rebate.trans_id AS source_trans_id,
                   rebate_credit.void_date
            FROM rebate_credit
            JOIN rebate USING(rebate_id)
            WHERE rebate_credit.trans_id=%s
        """, (trans_id,))
        return map(cls, cursor)

    desc = 'rebate'

    @property
    def qs(self):
        t = "rebate_credit_id=%s&trans_id=%s"
        return t % (self.rebate_credit_id, self.trans_id)

    def buttons(self):
        if self.void_date:
            return ""
        return super(RebateRow, self).buttons()

    links = [("/rebate/revoke_credit", "Revoke"),
             ("/rebate/void_credit", "Void")]

    @property
    def source(self):
        return '<a href="/view_trans?trans_id=%s">RB: %s</a>' % (
            self.source_trans_id, self.rebate_credit_id)

    @property
    def dest(self):
        return 'TX: %s' % self.trans_id

    @property
    def balance(self):
        return -self.amount

    @property
    def paid(self):
        return self.amount

class DebitRow(ActivityRow):
    @classmethod
    def records(cls, trans_id):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT trans_debit.entry_date,
                   trans_debit.username,
                   trans_debit.amount,
                   trans_debit.debit_id,
                   trans_debit.note
            FROM trans_debit
            WHERE trans_id=%s
        """, (trans_id,))
        return map(cls, cursor)

    desc = 'debit'

    @property
    def qs(self):
        return "debit_id=%s&trans_id=%s" % (self.debit_id, self.trans_id)

    links = [("/revoke_trans_debit", "Revoke")]

    @property
    def source(self):
        return 'DB: %s' % self.debit_id

    @property
    def balance(self):
        return self.amount

class OverpaymentRow(ActivityRow):
    @classmethod
    def records(cls, trans_id):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT overpayment.entry_date,
                   overpayment.username,
                   overpayment.amount,
                   overpayment.ptype_id,
                   payment_type.type_name,
                   COALESCE(overpayment.ref_no, '') AS ref_no,
                   overpayment.balance,
                   overpayment.note,
                   overpayment.puc_id
            FROM overpayment
            LEFT JOIN payment_type USING(ptype_id)
            WHERE trans_id = %s
            """, (trans_id,))
        return map(cls, cursor)

    desc = 'overpay'

    @property
    def sort_priority(self):
        e = self.entry_date
        return (datetime.date(e.year, e.month, e.day), 1)

    @property
    def ref(self):
        return "%(type_name)s: %(ref_no)s" % self.rec

    @property
    def overpaid(self):
        return self.amount

    @property
    def dest(self):
        return "PUC: %s" % self.puc_id

    @property
    def qs(self):
        return "puc_id=%s" % self.puc_id

    def buttons(self):
        if self.rec['balance'] == self.rec['amount']:
            self.links = [("/revoke_overpayment", "Revoke")]
        else:
            self.links = []
        if self.rec['balance']:
            self.links.append(("/settle_overpayment", "Settle"))
        return ActivityRow.buttons(self)

class PaymentRow(ActivityRow):
    @classmethod
    def records(cls, trans_id):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT trans_payment.entry_date,
                   trans_payment.username,
                   trans_payment.amount,
                   trans_payment.note,
                   trans_payment.payment_id,
                   COALESCE(trans_payment.ref_no, '') AS ref_no,
                   payment_type.type_name,
                   trans_payment.credit_group_number
            FROM trans_payment
            LEFT JOIN payment_type USING(ptype_id)
            WHERE trans_payment.trans_id = %s AND puc_id IS NULL
            """, (trans_id,))
        return map(cls, cursor)

    desc = 'payment'
    links = [("/revoke_payment", "Revoke")]

    @property
    def ref(self):
        return "%(type_name)s: %(ref_no)s" % self.rec

    @property
    def balance(self):
        return -self.amount

    @property
    def source(self):
        if self.rec['credit_group_number']:
            return '<span title="Group Credit">GC: %s</span>' % self.rec['credit_group_number']
        return ''

    @property
    def dest(self):
        return "PY: %s" % self.payment_id

    @property
    def paid(self):
        return self.amount

    @property
    def qs(self):
        return "payment_id=%s" % self.payment_id


class RebillRow(ActivityRow):
    @classmethod
    def records(cls, trans_id):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT rebill.rebill_id,
                   rebill.entry_date,
                   rebill.username,
                   rebill.total,
                   trans.trans_id AS rebill_trans_id
            FROM rebill
            LEFT JOIN trans ON trans.rebilled_trans_id = %s
            WHERE rebill.trans_id = %s
            """, (trans_id, trans_id))
        return map(cls, cursor)

    desc = 'rebill'

    @property
    def dest(self):
        return "RB: %s" % self.rebill_id

    @property
    def rebill(self):
        return self.total

    @property
    def ref(self):
        return txl(self.rebill_trans_id, "TX: %s" % self.rebill_trans_id)

class RebillCreditRow(ActivityRow):
    @classmethod
    def records(cls, trans_id):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT rebill_credit.rebill_credit_id,
                   rebill_credit.rebill_id,
                   rebill_credit.entry_date,
                   rebill_credit.username,
                   rebill_credit.amount,
                   rebill_credit.trans_id,
                   rebill.trans_id AS source_trans_id
            FROM rebill_credit
            JOIN rebill USING(rebill_id)
            WHERE rebill_credit.trans_id = %s
            """, (trans_id,))
        return map(cls, cursor)

    desc = 'credit'

    @property
    def source(self):
        return 'RB: %s' % self.rebill_id

    @property
    def dest(self):
        return "RC: %s" % self.rebill_credit_id

    @property
    def balance(self):
        return -self.amount

    @property
    def rebill(self):
        return -self.amount

    @property
    def ref(self):
        if self.trans_id != self.source_trans_id:
            return "<a href='/view_trans?trans_id=%s'>TX: %s</a>" % (
                self.source_trans_id, self.source_trans_id)
        else:
            return ""

class ApplyOverpaymentToOtherRow(ActivityRow):
    @classmethod
    def records(cls, trans_id):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT trans_payment.entry_date,
                   trans_payment.username,
                   trans_payment.amount,
                   trans_payment.note,
                   trans_payment.payment_id,
                   payment_type.type_name,
                   COALESCE(trans_payment.ref_no, '') AS ref_no,
                   overpayment.puc_id,
                   trans_payment.trans_id
            FROM trans_payment
            JOIN overpayment USING(puc_id)
            LEFT JOIN payment_type ON
              overpayment.ptype_id = payment_type.ptype_id
            WHERE overpayment.trans_id = %s AND
                  overpayment.trans_id != trans_payment.trans_id
            """, (trans_id,))
        return map(cls, cursor)

    desc = 'payment'
    links = [("/revoke_payment", "Revoke")]

    @property
    def ref(self):
        return "%(type_name)s: %(ref_no)s" % self.rec

    @property
    def overpaid(self):
        return self.amount

    @property
    def source(self):
        return "PUC: %s" % self.puc_id

    @property
    def dest(self):
        return "PY: %s" % txl(self.trans_id, self.payment_id)

    @property
    def overpaid(self):
        return -self.amount

    def buttons(self):
        if self.balance != self.amount:
            return ""
        else:
            return ActivityRow.buttons(self)

    @property
    def qs(self):
        return "payment_id=%s" % self.payment_id

class OtherOverpaymentAppliedtoSelfRow(ActivityRow):
    @classmethod
    def records(cls, trans_id):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT trans_payment.entry_date,
                   trans_payment.username,
                   trans_payment.amount,
                   trans_payment.note,
                   trans_payment.payment_id,
                   overpayment.puc_id,
                   overpayment.trans_id,
                   COALESCE(trans_payment.ref_no, '') AS ref_no,
                   payment_type.type_name
            FROM trans_payment
            JOIN overpayment USING(puc_id)
            LEFT JOIN payment_type ON
              overpayment.ptype_id = payment_type.ptype_id
            WHERE trans_payment.trans_id = %s AND
                  overpayment.trans_id != trans_payment.trans_id
            """, (trans_id,))
        return map(cls, cursor)

    desc = 'payment'
    links = [("/revoke_payment", "Revoke")]

    @property
    def ref(self):
        return "%(type_name)s: %(ref_no)s" % self.rec

    @property
    def source(self):
        return "PUC: %s" % txl(self.trans_id, self.puc_id)

    @property
    def dest(self):
        return "PY: %s" % self.payment_id

    @property
    def paid(self):
        return self.amount

    @property
    def balance(self):
        return -self.amount

    @property
    def qs(self):
        return "payment_id=%s" % self.payment_id


class OverpaymentAppliedtoSelfRow(ActivityRow):
    """ technically this should never happen but we'll put it in here in
    case it ever does so we can see it.
    """
    @classmethod
    def records(cls, trans_id):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT trans_payment.entry_date,
                   trans_payment.username,
                   trans_payment.amount,
                   trans_payment.note,
                   trans_payment.payment_id,
                   overpayment.puc_id,
                   overpayment.trans_id,
                   COALESCE(overpayment.ref_no, '') AS ref_no,
                   payment_type.type_name
            FROM trans_payment
            JOIN overpayment USING(puc_id)
            LEFT JOIN payment_type ON
              overpayment.ptype_id = payment_type.ptype_id
            WHERE trans_payment.trans_id = %s AND
                  overpayment.trans_id = trans_payment.trans_id
            """, (trans_id,))
        return map(cls, cursor)

    desc = 'payment'

    @property
    def ref(self):
        return "%(type_name)s: %(ref_no)s" % self.rec

    @property
    def source(self):
        return "PUC: %s" % self.puc_id

    @property
    def dest(self):
        return "PY: %s" % self.payment_id

    @property
    def overpaid(self):
        return -self.amount

    @property
    def balance(self):
        return -self.amount

    links = [("/revoke_payment", "Revoke")]

    @property
    def qs(self):
        return "payment_id=%s" % self.payment_id

class ReversalRow(ActivityRow):
    @classmethod
    def records(cls, trans_id):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT reversal.entry_date,
                   reversal.reversal_id,
                   reversal.batch_file_id,
                   reversal.total,
                   reversal.balance,
                   pending_reversal_settlement.prs_id,
                   trans.group_number,
                   trans.trans_id
            FROM reversal
            JOIN trans USING(trans_id)
            LEFT JOIN pending_reversal_settlement USING(reversal_id)
            WHERE trans_id = %s
            """, (trans_id,))

        return map(cls, cursor)

    desc = 'reversal'

    @property
    def dest(self):
        return "RV: %s" % self.reversal_id

    @property
    def reversal(self):
        return self.total

    def buttons(self):
        total = self.rec['total']
        balance = self.rec['balance']
        trans_id = self.rec['trans_id']
        btns = [
              """<a class='button reverse_batch' href='#'>Batch %s</a>""" % (self.rec['batch_file_id'] or '')
        ]
        if balance == 0:
            return " ".join(btns)
        if self.group_number == 'GROUPH' and total == balance:
            btns.append("""
              <a class='button' href='/revoke_reversal?trans_id=%s'>
              Revoke</a>""" % trans_id)

        if self.prs_id:
            btns.append("""
                <a class='button' href='/unmark_reversal_credit?reversal_id=%s'>
                Unmark Reversal for Settlement</a>
                """ % self.reversal_id)
        else:
            btns.append("""
                <a class='button' href="/mark_reversal_credit?reversal_id=%s">
                    Mark Reversal for Settlement</a>
                """ % self.reversal_id)
            btns.append("""
                <a class='button' href="/credit_reversal_to_group?reversal_id=%s">
                    Create Group Credit</a>
                """ % self.reversal_id)
        return " ".join(btns)

class ReversalGroupCreditRow(ActivityRow):
    @classmethod
    def records(cls, trans_id):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT group_credit.entry_date,
                   group_credit.source_reversal_id as reversal_id,
                   reversal.batch_file_id,
                   group_credit.amount as total,
                   NULL as balance,
                   group_credit.gcid as prs_id,
                   trans.group_number,
                   trans.trans_id
            FROM group_credit
            JOIN reversal ON reversal.reversal_id = group_credit.source_reversal_id
            JOIN trans USING(trans_id)
            WHERE reversal.trans_id = %s
            """, (trans_id,))

        return map(cls, cursor)

    desc = 'rev group credit'

    @property
    def dest(self):
        return "GN: %s" % self.group_number

    @property
    def reversal(self):
        return -self.total

    @property
    def transfered(self):
        return -self.total

    def buttons(self):
        return "<a class='button' href='/revoke_group_credit?gcid=%s&r=%s'>Revoke</a>" % (
            self.prs_id,
            urllib.parse.quote(f"/view_trans?trans_id={self.trans_id}"))


class AdjudicateThisRow(ActivityRow):
    @classmethod
    def records(cls, trans_id):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT trans_adjudication.entry_date,
                   trans_adjudication.amount,
                   trans_adjudication.note,
                   trans_adjudication.username,
                   trans_adjudication.adjudication_id,
                   reversal.reversal_id,
                   reversal.trans_id AS source_trans_id,
                   trans_adjudication.trans_id, void_date
            FROM trans_adjudication
            JOIN reversal USING(reversal_id)
            WHERE trans_adjudication.trans_id = %s AND
                  trans_adjudication.trans_id = reversal.trans_id
            """, (trans_id,))
        return map(cls, cursor)

    desc = 'credit'

    @property
    def dest(self):
        return "ADJ: %s" % self.adjudication_id

    @property
    def source(self):
        return "RV: %s" % self.reversal_id

    @property
    def balance(self):
        return -self.amount

    @property
    def reversal(self):
        return -self.amount

    def buttons(self):
        if self.void_date:
            return ""
        return ("""
          <a class='button' href='/revoke_adjudication?adjudication_id=%s'>Revoke</a>
          <a class='button voida' href='/void_adjudication' data-adjudication_id='%s'>Void</a>
           """ % (self.adjudication_id, self.adjudication_id))

class VoidAdjudicateThisRow(ActivityRow):
    @classmethod
    def records(cls, trans_id):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT trans_adjudication.void_date AS entry_date,
                   trans_adjudication.amount,
                   trans_adjudication.username,
                   trans_adjudication.adjudication_id,
                   reversal.reversal_id,
                   reversal.trans_id AS source_trans_id,
                   trans_adjudication.trans_id
            FROM trans_adjudication
            JOIN reversal USING(reversal_id)
            WHERE trans_adjudication.trans_id = %s AND
                  trans_adjudication.trans_id = reversal.trans_id AND
                  trans_adjudication.void_date IS NOT NULL
            """, (trans_id,))
        return map(cls, cursor)

    desc = 'void'

    @property
    def dest(self):
        return "ADJ: %s" % self.adjudication_id

    @property
    def source(self):
        return "RV: %s" % self.reversal_id

    @property
    def balance(self):
        return self.amount

    @property
    def reversal(self):
        return self.amount

    def buttons(self):
        return ("<a class='button' href='/unvoid_adjudication?adjudication_id=%s'>Unvoid</a>"
            % self.adjudication_id)

    @property
    def sort_priority(self):
        e = self.entry_date
        return (datetime.date(e.year, e.month, e.day), 1)

class OtherAdjudicatesMeRow(ActivityRow):
    @classmethod
    def records(cls, trans_id):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT trans_adjudication.entry_date,
                   trans_adjudication.amount,
                   trans_adjudication.note,
                   trans_adjudication.username,
                   trans_adjudication.adjudication_id,
                   reversal.reversal_id,
                   reversal.trans_id
            FROM trans_adjudication
            JOIN reversal USING(reversal_id)
            WHERE trans_adjudication.trans_id = %s AND
                  trans_adjudication.trans_id != reversal.trans_id
            """, (trans_id,))
        return map(cls, cursor)

    desc = 'credit'

    @property
    def source(self):
        return "RV: %s" % txl(self.trans_id, self.reversal_id)

    @property
    def dest(self):
        return "ADJ: %s" % self.adjudication_id

    @property
    def balance(self):
        return -self.amount

    def buttons(self):
        return ("""
          <a class='button' href='/revoke_adjudication?adjudication_id=%s'>Revoke</a>
          <a class='button voida' href='/void_adjudication' data-adjudication_id='%s'>Void</a>
           """ % (self.adjudication_id, self.adjudication_id))

class VoidOtherAdjudicatesMeRow(ActivityRow):
    @classmethod
    def records(cls, trans_id):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT trans_adjudication.void_date AS entry_date,
                   trans_adjudication.amount,
                   trans_adjudication.note,
                   trans_adjudication.username,
                   trans_adjudication.adjudication_id,
                   reversal.reversal_id,
                   reversal.trans_id
            FROM trans_adjudication
            JOIN reversal USING(reversal_id)
            WHERE trans_adjudication.trans_id = %s AND
                  trans_adjudication.trans_id != reversal.trans_id AND
                  trans_adjudication.void_date IS NOT NULL
            """, (trans_id,))
        return map(cls, cursor)

    desc = 'void'

    @property
    def source(self):
        return "RV: %s" % txl(self.trans_id, self.reversal_id)

    @property
    def dest(self):
        return "ADJ: %s" % self.adjudication_id

    @property
    def balance(self):
        return self.amount

    def buttons(self):
        return ("<a class='button' href='/unvoid_adjudication?adjudication_id=%s'>Unvoid</a>"
            % self.adjudication_id)

    @property
    def sort_priority(self):
        e = self.entry_date
        return (datetime.date(e.year, e.month, e.day), 1)

class AdjudicateOtherRow(ActivityRow):
    @classmethod
    def records(cls, trans_id):
        cursor = R.db.dict_cursor()
        cursor.execute("""
        SELECT trans_adjudication.entry_date,
               trans_adjudication.username,
               trans_adjudication.note,
               trans_adjudication.amount,
               reversal.reversal_id,
               trans_adjudication.adjudication_id,
               trans_adjudication.trans_id AS other_trans_id
        FROM trans_adjudication
        JOIN reversal USING(reversal_id)
        WHERE reversal.trans_id = %s AND
              reversal.trans_id != trans_adjudication.trans_id
        """, (trans_id,))

        return map(cls, cursor)

    desc = 'credit'

    @property
    def reversal(self):
        return -self.amount

    @property
    def source(self):
        return "RV: %s" % self.reversal_id

    @property
    def dest(self):
        return "ADJ: %s" % txl(self.other_trans_id, self.adjudication_id)

    def buttons(self):
        return ("""
          <a class='button' href='/revoke_adjudication?adjudication_id=%s'>Revoke</a>
          <a class='button voida' href='/void_adjudication' data-adjudication_id='%s'>Void</a>
           """ % (self.adjudication_id, self.adjudication_id))

class VoidAdjudicateOtherRow(ActivityRow):
    @classmethod
    def records(cls, trans_id):
        cursor = R.db.dict_cursor()
        cursor.execute("""
        SELECT trans_adjudication.void_date AS entry_date,
               trans_adjudication.username,
               trans_adjudication.note,
               trans_adjudication.amount,
               reversal.reversal_id,
               trans_adjudication.adjudication_id,
               trans_adjudication.trans_id AS other_trans_id
        FROM trans_adjudication
        JOIN reversal USING(reversal_id)
        WHERE reversal.trans_id = %s AND
              reversal.trans_id != trans_adjudication.trans_id AND
              trans_adjudication.void_date IS NOT NULL
        """, (trans_id,))
        return map(cls, cursor)

    desc = 'void'

    @property
    def reversal(self):
        return self.amount

    @property
    def source(self):
        return "RV: %s" % self.reversal_id

    @property
    def dest(self):
        return "ADJ: %s" % txl(self.other_trans_id, self.adjudication_id)

    def buttons(self):
        return ("<a class='button' href='/unvoid_adjudication?adjudication_id=%s'>Unvoid</a>"
            % self.adjudication_id)

    @property
    def sort_priority(self):
        e = self.entry_date
        return (datetime.date(e.year, e.month, e.day), 1)

class ReversalSettlementRow(ActivityRow):
    @classmethod
    def records(cls, trans_id):
        cursor = R.db.dict_cursor()
        cursor.execute("""
        SELECT reversal_settlement.entry_date,
               reversal_settlement.username,
               reversal_settlement.amount,
               reversal_settlement.check_no,
               reversal_settlement.settlement_id,
               reversal.reversal_id,
               reversal_settlement.void_date
        FROM reversal
        JOIN reversal_settlement USING(reversal_id)
        WHERE reversal.trans_id = %s
        """, (trans_id,))
        return map(cls, cursor)

    desc = 'settlement'

    @property
    def settled(self):
        return self.amount

    @property
    def reversal(self):
        return -self.amount

    @property
    def source(self):
        return "RV: %s" % self.reversal_id

    @property
    def dest(self):
        return "SET: %s" % self.settlement_id

    @property
    def ref(self):
        return "CK: %s" % self.check_no

    links = [('/revoke_reversal_settlement', 'Revoke'),
             ('/void_reversal_settlement', 'Void')]

    def buttons(self):
        if self.void_date:
            return ''
        qs = 'settlement_id=%s' % self.settlement_id
        html = []
        for link, label in self.links:
            html.append('<a class="button" href="%s?%s">%s</a>' %
                        (link, qs, label))
        return "".join(html)

class ReversalSettlementVoidRow(ActivityRow):
    @classmethod
    def records(cls, trans_id):
        cursor = R.db.dict_cursor()
        cursor.execute("""
        SELECT reversal_settlement.void_date AS entry_date,
               reversal_settlement.username,
               reversal_settlement.amount,
               reversal_settlement.check_no,
               reversal_settlement.settlement_id,
               reversal.reversal_id,
               reversal_settlement.void_date
        FROM reversal
        JOIN reversal_settlement USING(reversal_id)
        WHERE reversal.trans_id = %s
              AND reversal_settlement.void_date IS NOT NULL
        """, (trans_id,))
        return map(cls, cursor)

    desc = 'void'

    @property
    def settled(self):
        return -self.amount

    @property
    def reversal(self):
        return self.amount

    @property
    def source(self):
        return "SET: %s" % self.settlement_id

    @property
    def dest(self):
        return "SET: %s" % self.settlement_id

    @property
    def ref(self):
        return "CK: %s" % self.check_no

    def buttons(self):
        uri = '/unvoid_reversal_settlement'
        qs = 'settlement_id=%s' % self.settlement_id
        return '<a class="button" href="%s?%s">Unvoid</a>' % (uri, qs)

class OverpaymentSettlementRow(ActivityRow):
    @classmethod
    def records(cls, trans_id):
        cursor = R.db.dict_cursor()
        cursor.execute("""
        SELECT overpayment_settlement.entry_date,
               overpayment_settlement.amount,
               overpayment_settlement.check_no,
               overpayment_settlement.puc_settle_id,
               overpayment_settlement.puc_id,
               overpayment_settlement.username,
               overpayment_settlement.void_date
        FROM overpayment_settlement
        JOIN overpayment USING(puc_id)
        WHERE overpayment.trans_id = %s
        """, (trans_id,))
        return map(cls, cursor)

    desc = 'settlement'

    @property
    def overpaid(self):
        return -self.amount

    @property
    def source(self):
        return "PUC: %s" % self.puc_id

    @property
    def dest(self):
        return "SET: %s" % self.puc_settle_id

    @property
    def ref(self):
        return "CK: %s" % self.check_no

    links = [
        ('/revoke_overpayment_settlement', 'Revoke'),
        ('/void_overpayment_settlement', 'Void')]
             
    def buttons(self):
        if self.void_date:
            return ''
        qs = 'puc_settle_id=%s' % self.puc_settle_id
        html = []
        for link, label in self.links:
            html.append('<a class="button" href="%s?%s">%s</a>' %
                        (link, qs, label))
        return "".join(html)

class OverpaymentSettlementVoidRow(ActivityRow):
    @classmethod
    def records(cls, trans_id):
        cursor = R.db.dict_cursor()
        cursor.execute("""
        SELECT overpayment_settlement.void_date AS entry_date,
               overpayment_settlement.amount,
               overpayment_settlement.check_no,
               overpayment_settlement.puc_settle_id,
               overpayment_settlement.puc_id,
               overpayment_settlement.username,
               overpayment_settlement.void_date
        FROM overpayment_settlement
        JOIN overpayment USING(puc_id)
        WHERE overpayment.trans_id = %s
              AND overpayment_settlement.void_date IS NOT NULL
        """, (trans_id,))
        return map(cls, cursor)

    desc = 'void'

    @property
    def overpaid(self):
        return self.amount

    @property
    def source(self):
        return "SET: %s" % self.puc_settle_id

    @property
    def dest(self):
        return "SET: %s" % self.puc_settle_id

    @property
    def ref(self):
        return "CK: %s" % self.check_no

    def buttons(self):
        qs = 'puc_settle_id=%s' % self.puc_settle_id
        uri = "/unvoid_overpayment_settlement"
        return '<a class="button" href="%s?%s">Unvoid</a>' % (uri, qs)

class WriteoffRow(ActivityRow):
    @classmethod
    def records(cls, trans_id):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT trans_writeoff.entry_date,
                   trans_writeoff.username,
                   trans_writeoff.amount,
                   trans_writeoff.writeoff_id,
                   trans_writeoff.note,
                   trans_writeoff.void_date
            FROM trans_writeoff
            WHERE trans_id = %s
            """, (trans_id,))
        return map(cls, cursor)

    desc = 'writeoff'

    @property
    def dest(self):
        return "WO: %s" % self.writeoff_id

    @property
    def balance(self):
        return -self.amount

    def buttons(self):
        if self.void_date:
            return ''
        return """
         <a class='button' href='/revoke_writeoff?writeoff_id=%s'>Revoke</a>
         <a class='button voidw' href='#' data-writeoff_id='%s'>Void</a>
         """  % (self.writeoff_id, self.writeoff_id)

class VoidWriteoffRow(ActivityRow):
    @classmethod
    def records(cls, trans_id):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT trans_writeoff.void_date AS entry_date,
                   trans_writeoff.username,
                   trans_writeoff.amount,
                   trans_writeoff.writeoff_id
            FROM trans_writeoff
            WHERE trans_id = %s AND void_date IS NOT NULL
            """, (trans_id,))
        return map(cls, cursor)

    desc = 'void'

    @property
    def dest(self):
        return "WO: %s" % self.writeoff_id

    @property
    def balance(self):
        return self.amount

    def buttons(self):
        return ("<a class='button' href='/unvoid_writeoff?writeoff_id=%s'>Unvoid</a>"
            % self.writeoff_id)

    @property
    def sort_priority(self):
        e = self.entry_date
        return (datetime.date(e.year, e.month, e.day), 1)

class DistributionRow(ActivityRow):
    @classmethod
    def records(cls, trans_id):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT distribution.distribution_date AS entry_date,
                   distribution.amount,
                   distribution.distribution_account
            FROM distribution
            WHERE trans_id = %s AND distribution_date IS NOT NULL AND
                 amount != 0
            """, (trans_id,))
        return map(cls, cursor)

    desc = 'distribution'

    @property
    def dest(self):
        return self.distribution_account

    @property
    def distributed(self):
        return self.amount

activity_types = [
    InvoiceRow,
    PaymentRow,
    RebillRow,
    RebillCreditRow,
    OverpaymentRow,
    DebitRow,
    RebateRow,
    VoidRebateRow,
    ReversalRow,
    ReversalGroupCreditRow,
    AdjudicateThisRow,
    VoidAdjudicateThisRow,
    AdjudicateOtherRow,
    VoidAdjudicateOtherRow,
    OtherAdjudicatesMeRow,
    VoidOtherAdjudicatesMeRow,
    OtherOverpaymentAppliedtoSelfRow, 
    ApplyOverpaymentToOtherRow,
    OverpaymentAppliedtoSelfRow, 
    WriteoffRow, 
    VoidWriteoffRow,
    DistributionRow,
    ReversalSettlementRow,
    ReversalSettlementVoidRow,
    OverpaymentSettlementRow,
    OverpaymentSettlementVoidRow
]

def activity(trans_id):
    items = []
    for cls in activity_types:
        items.extend(cls.records(trans_id))

    items.sort(key=lambda x: x.sort_priority)
    return ActivitySet(items)

class ActivitySet(list):
    """ The activity set provides a list of activity records for the transaction
    along with total amounts for each of the columns.
    """
    total_attrs = [
        'balance', 'reversal', 'overpaid', 'paid', 'settled', 'distributed',
        'transfered', 'rebill']

    def __init__(self, o):
        list.__init__(self, o)
        for attr in self.total_attrs:
            value = sum(getattr(t, attr) for t in self)
            setattr(self, attr, value)

def txl(trans_id, c=None):
    """ Return a HTML link to the given trans_id """
    if c is None:
        c = trans_id
    return "<a href='/view_trans?trans_id=%s'>%s</a>" % (trans_id, c)

def pk_sup_data(trans_id):
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT * FROM pk_trans_sup WHERE trans_id=%s
        """, (trans_id,))

    if not cursor.rowcount:
        return None

    fields = [c[0] for c in cursor.description]
    t = collections.namedtuple('pk_sup_data', fields)
    return t(*cursor.fetchone())

application = Program.app
