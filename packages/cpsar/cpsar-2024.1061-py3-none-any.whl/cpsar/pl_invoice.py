""" Module to provide objects that match the interface of cpsar.print_invoice
for mjoseph. The objects defined here are to be given to the invoice_pdf
module and other interface pages that list invoices
"""
from __future__ import division
from builtins import map
from builtins import zip
from past.utils import old_div
from builtins import object
import datetime
import math
import re
from itertools import groupby

from cpsar import config
from cpsar.runtime import db
from cpsar.txlib import BusinessError
from cpsar.util import imemoize, count_money

################################
## Update methods

def balance_overpayment(overpayment_id):
    cursor = db.cursor()
    cursor.execute("""
    select coalesce(sum(trans_payment.amount), 0)
        from trans_payment
        where overpayment_id = %s and
        void_date is null""", (overpayment_id,))

    amount, = cursor.fetchone()
    cursor.execute("""
        update overpayment set balance = total - %s
        where overpayment_id = %s
        returning balance
        """, (amount, overpayment_id))

    balance, = cursor.fetchone()
    if balance < 0:
        raise BusinessError('Not enough funds in overpayment. Makes balance %s' % balance)

def balance_reversal(reversal_id):
    cursor = db.cursor()
    cursor.execute("""
    select coalesce(sum(trans_payment.amount), 0)
        from trans_payment
        where reversal_id = %s and
        void_date is null""", (reversal_id,))

    amount, = cursor.fetchone()
    cursor.execute("""
        update reversal set balance = total - %s
        where reversal_id = %s
        returning balance
        """, (amount, reversal_id))

    balance, = cursor.fetchone()
    if balance < 0:
        t = 'Not enough funds in reversal %s. Makes balance %s'
        raise BusinessError(t % (reversal_id, balance))

def balance_trans(trans_id):
    cursor = db.cursor()
    cursor.execute("""
    select coalesce(sum(trans_payment.amount), 0)
        from trans_payment
        where trans_id=%s and
        void_date is null""", (trans_id,))

    amount, = cursor.fetchone()
    cursor.execute("""
        update trans set balance = total - %s
        where trans_id = %s
        returning balance
        """, (amount, trans_id))

    balance, = cursor.fetchone()
    if balance < 0:
        raise BusinessError('Too large of payment. Makes balance %s' % balance)

##########################

class DataError(Exception): pass

class InvoiceStore(object):
    def __init__(self, include_paid=True):
        self._client_factory = ClientFactory()
        self.invoice_base_path = config.inv_base()
        self.html2ps_config_path = "%s/invoice/print.html2ps"
        self.html2ps_config_path %= config.mako_template_dir()
        self.print_options = PrintOptions(show_past_due_stamp=False)
        self.include_paid = include_paid

    __invoice_factory = None

    @property
    def _invoice_factory(self):
        if not self.__invoice_factory:
            self.__invoice_factory = InvoiceFactory(self._client_factory, self.include_paid)
        return self.__invoice_factory

    def invoice_by_id(self, invoice_id):
        return self._invoice_factory.for_invoice_id(invoice_id)

    def invoice_by_trans_id(self, trans_id):
        return self._invoice_factory.for_trans_id(trans_id)

    def outstanding_for_group(self, group_number, invoice_date):
        return self._invoice_factory.outstanding_for_group(group_number, invoice_date)

    def all_outstanding_for_group(self, group_number):
        return self._invoice_factory.all_outstanding_for_group(group_number)

    def for_date(self, group_number, invoice_date):
        return self._invoice_factory.for_date(group_number, invoice_date)

    def patient_invoice_list(self, group_number, ssn, dob):
        return self._invoice_factory.patient_invoice_list(
            group_number, ssn, dob)

    def paginated_patient_invoices(self, group_number, ssn, dob, page, size):
        return self._invoice_factory.paginated_patient_invoices(group_number, ssn, dob, page, size)

class PrintOptions(object):
    def __init__(self, show_past_due_stamp=False):
        self.show_past_due_stamp = show_past_due_stamp

    def as_dict(self):
        return {'show_past_due_stamp': self.show_past_due_stamp}

class InvoiceFactory(object):
    def __init__(self, client_factory, include_paid=True):
        self._client_factory = client_factory
        self._include_paid = include_paid

    @imemoize
    def for_invoice_id(self, invoice_id):
        client = self._client_factory.for_invoice_id(invoice_id)
        line_items = []
        dbrecs = self._dbrecs_for_invoice_id(invoice_id)
        for record in dbrecs:
            ingredients = self._ingredients_for_history_id(record['history_id'])
            line_item = LineItem(record, client, ingredients)
            if not self._include_paid and line_item.balance == 0:
                continue
            # The line_item and ingredients have a circular dependency so we go
            # back and assign it here
            for ingredient in ingredients:
                ingredient.line_item = line_item
            line_items.append(line_item)
        return self._invoice_for(client, line_items)

    @imemoize
    def for_trans_id(self, trans_id):
        cursor = db.cursor()
        cursor.execute("select invoice_id from trans where trans_id=%s", (trans_id,))
        if not cursor.rowcount:
            return None
        return self.for_invoice_id(cursor.fetchone()[0])

    def patient_invoice_list(self, group_number, ssn, dob):
        cursor = self._trans_cursor("""
            SELECT trans.trans_id
            FROM trans
            JOIN patient USING(patient_id)
            WHERE patient.group_number=%s
              AND patient.ssn=%s
              AND patient.dob=%s
            """, (group_number, ssn, dob))
        return list(self._invoices_for_cursor(cursor))

    def paginated_patient_invoices(self, group_number, ssn, dob, page, size):
        """ sorts by most recent first """
        cursor = self._trans_cursor("""
            SELECT trans.trans_id
            FROM trans
            JOIN patient USING(patient_id)
            WHERE patient.group_number=%s
              AND patient.ssn=%s
              AND patient.dob=%s
            """, (group_number, ssn, dob))

        #for invoice_id, trans_records in groupby(cursor, lambda s: s['invoice_id']):
        invoices = [(invoice_id, list(i)) for invoice_id, i in groupby(cursor, lambda s: s['invoice_id'])]
        invoices = list(reversed(invoices))
        number_pages = int(math.ceil(len(invoices)/float(size)))
        if page > number_pages:
            page = number_pages

        slice = invoices[(page-1)*size: page*size]
        info = {
            'number_invoices': len(invoices),
            'number_pages': number_pages,
            'invoices': []
        }

        for invoice_id, trans_records in slice:
            line_items = []
            for record in trans_records:
                group_number = record['group_number']
                client = self._client_factory.for_group_number(group_number)
                ingredients = self._ingredients_for_history_id(record['history_id'])
                line_item = LineItem(record, client, ingredients)
                if not self._include_paid and line_item.balance == 0:
                    continue
                # The line_item and ingredients have a circular dependency so we go
                # back and assign it here
                for ingredient in ingredients:
                    ingredient.line_item = line_item
                line_items.append(line_item)
            info['invoices'].append(self._invoice_for(client, line_items))
        return info

    def all_outstanding_for_group(self, group_number):
        cursor = self._trans_cursor("""
         with s as (
            SELECT trans.trans_id, sum(balance) over (partition by invoice_id) as invoice_balance
            FROM trans
            WHERE trans.group_number=%s
        )
         select trans_id from s
         where invoice_balance > 0
            """, (group_number,))
        return list(self._invoices_for_cursor(cursor))

    def outstanding_for_group(self, group_number, invoice_date):
        cursor = self._trans_cursor("""
         with s as (
            SELECT trans.trans_id, sum(balance) over (partition by invoice_id) as invoice_balance
            FROM trans
            WHERE trans.group_number=%s
              AND trans.invoice_date = %s
        )
         select trans_id from s
         where invoice_balance > 0
            """, (group_number, invoice_date))
        return list(self._invoices_for_cursor(cursor))

    def for_date(self, group_number, invoice_date):
        cursor = self._trans_cursor("""
            SELECT trans.trans_id
            FROM trans
            WHERE trans.group_number=%s AND trans.invoice_date=%s
            """, (group_number, invoice_date))
        return list(self._invoices_for_cursor(cursor))

    def _invoices_for_cursor(self, cursor):
        """ provide an iterable of invoices for the given cursor which has
        executed a query that includes all the fields from the trans, patient
        and other tables.
        """
        for invoice_id, trans_records in groupby(cursor, lambda s: s['invoice_id']):
            line_items = []
            for record in trans_records:
                group_number = record['group_number']
                client = self._client_factory.for_group_number(group_number)
                ingredients = self._ingredients_for_history_id(record['history_id'])
                line_item = LineItem(record, client, ingredients)
                if not self._include_paid and line_item.balance == 0:
                    continue
                # The line_item and ingredients have a circular dependency so we go
                # back and assign it here
                for ingredient in ingredients:
                    ingredient.line_item = line_item
                line_items.append(line_item)
            yield self._invoice_for(client, line_items)

    def _invoice_for(self, client, line_items):
        invoice_class_map = {
            'bd': Invoice,
            'mjoseph': MJosephInvoice,
            'msq': Invoice,
            'sunrise': SunriseInvoice,
            's1': Invoice
        }
        cls = invoice_class_map.get(config.invoice_class(), Invoice)
        return cls(client, line_items)

    def _trans_cursor(self, strans_query, args=()):
        cursor = db.dict_cursor()
        if args:
            strans_query = cursor.mogrify(strans_query, args).decode()

        sql = """
         WITH strans AS (%s)
         , payment AS (
            SELECT strans.trans_id,
                   array_accum(trans_payment.ref_no) AS ref_nos,
                   array_accum(trans_payment.amount) AS payment_amounts,
                   array_accum(reversed_trans.invoice_id) AS reversed_invoice_ids
            FROM strans
            JOIN trans_payment USING(trans_id)
            LEFT JOIN reversal USING(reversal_id)
            LEFT JOIN trans AS reversed_trans ON
                reversal.trans_id = reversed_trans.trans_id
            WHERE trans_payment.void_date IS NULL
            GROUP BY strans.trans_id
        )
            SELECT trans.trans_id,
                   trans.group_number,
                   trans.line_no,
                   trans.invoice_id,
                   trans.invoice_date,
                   trans.rx_date,
                   COALESCE(claim.claim_number, trans.claim_number) AS claim_number,
                   trans.quantity,
                   trans.days_supply,
                   history.doctor_dea_number,
                   history.doctor_npi_number,
                   history.compound_code,
                   history.date_processed,
                   trans.state_fee,
                   trans.awp,
                   trans.sales_tax, 
                   trans.total,
                   trans.balance,
                   trans.usual_customary,
                   trans.patient_id,
                   history.doctor_id,
                   trans.adjuster1_email,
                   COALESCE(u1.first_name || ' ' || u1.last_name,
                            trans.adjuster1_email) AS adjuster1_name,
                   trans.adjuster2_email,
                   COALESCE(u2.first_name || ' ' || u2.last_name,
                            trans.adjuster2_email) AS adjuster2_name,
                   drug.ndc_number AS drug_ndc_number,
                   brand_drug.name AS brand_drug_name,
                   drug.ndc_number,
                   drug.brand AS brand_or_generic,
                   drug.name AS drug_name,
                   drug.gpi_code AS drug_gpi_code,
                   pharmacy.name AS pharmacy_name,
                   pharmacy.nabp AS pharmacy_nabp,
                   pharmacy.address_1 AS pharmacy_address_1,
                   pharmacy.address_2 AS pharmacy_address_2,
                   pharmacy.city AS pharmacy_city,
                   pharmacy.state AS pharmacy_state,
                   pharmacy.zip_code AS pharmacy_zip,
                   pharmacy.npi AS pharmacy_npi,
                   COALESCE(pharmacy.tax_id, '') AS pharmacy_tax_id,
                   pharmacy.zip_code AS pharmacy_zip_code,
                   doctor.name AS doctor_name,
                   doctor.address_1 as doctor_address_1,
                   doctor.address_2 as doctor_address_2,
                   doctor.city as doctor_city,
                   doctor.state as doctor_state,
                   doctor.zip_code as doctor_zip_code,
                   history.history_id,
                   pharmacist.lic_number AS pharmacist_license_number,
                   pharmacist.first_name AS pharmacist_first_name,
                   pharmacist.last_name AS pharmacist_last_name,
                   pharmacist.middle_init AS pharmacist_middle_initial,
                   history.refill_number,
                   history.rx_number,
                   history.daw,
                   history.inv_class,
                   history.reverse_date,
                   claim.doi,
                   claim.ref_nbr_1,
                   claim.ref_nbr_2,
                   payment.ref_nos,
                   payment.payment_amounts,
                   payment.reversed_invoice_ids,
                   patient.first_name as patient_first_name,
                   patient.last_name as patient_last_name,
                   patient.sex as patient_sex,
                   patient.ssn as patient_ssn,
                   patient.dob as patient_dob,
                   patient.division_code,
                   patient.jurisdiction,

                   group_info.company_name || ' #' || group_info.group_number 
                    AS billing_name,
                   COALESCE(group_info.address_1, '') AS billing_address_1,
                   COALESCE(group_info.address_2, '') AS billing_address_2,
                   COALESCE(group_info.city, '') AS billing_city,
                   COALESCE(group_info.state, '') AS billing_state,
                   COALESCE(group_info.zip_code, '') AS billing_zip_code,

                   soj.abbr as jurisdiction_state,
                   patient.address_1 as patient_address_1,
                   patient.address_2 as patient_address_2,
                   patient.city as patient_city,
                   patient.state as patient_state,
                   patient.zip_code as patient_zip_code,
                   patient.telephone_nbr1 as patient_phone
            FROM trans
            JOIN strans USING(trans_id)
            JOIN group_info on trans.group_number = group_info.group_number
            JOIN drug ON
                 drug.drug_id = trans.drug_id
            JOIN history ON
                 trans.history_id = history.history_id
            LEFT JOIN payment ON strans.trans_id = payment.trans_id
            LEFT JOIN drug AS brand_drug ON
                 drug.brand_ndc = brand_drug.ndc_number
            LEFT JOIN patient ON
                 trans.patient_id = patient.patient_id
            LEFT JOIN soj ON patient.jurisdiction = soj.jurisdiction
            LEFT JOIN pharmacy ON
                 trans.pharmacy_id = pharmacy.pharmacy_id
            left join user_info as u1 on trans.adjuster1_email = u1.email
            left join user_info as u2 on trans.adjuster2_email = u2.email
            LEFT JOIN doctor ON
                 history.doctor_id = doctor.doctor_id
            LEFT JOIN claim ON
                 history.claim_id = claim.claim_id
            LEFT JOIN pharmacist ON
                 history.pharmacist_id = pharmacist.pharmacist_id
            ORDER BY trans.invoice_id, trans.line_no
            """
        sql %= (strans_query,)
        cursor.execute(sql)
        return cursor

    def _dbrecs_for_invoice_id(self, invoice_id):
        sql = """SELECT trans_id
                 FROM trans
                 WHERE invoice_id=%s"""
        return self._trans_cursor(sql, (invoice_id,))

    def _ingredients_for_history_id(self, history_id):
        cursor = db.dict_cursor()
        cursor.execute("""
            SELECT I.ingredient_id,
                   I.ingredient_nbr,
                   I.qty,
                   I.cost_submitted,
                   I.cost_allowed,
                   I.drug_id,
                   I.awp,
                   drug.name AS drug_name,
                   drug.ndc_number,
                   drug.gpi_code,
                   history.patient_id
            FROM history_ingredient as I
            JOIN drug USING(drug_id)
            JOIN history USING(history_id)
            WHERE I.history_id=%s
            ORDER BY ingredient_nbr ASC
            """, (history_id,))
        return list(map(Ingredient, cursor))

class LineItem(object):
    """ A particular line item on the invoice.  Construction controlled by
    InvoiceFactory.
    """
    rebate_credit_total = 0
    def __init__(self, record, client, ingredients):
        self._client = client
        self._ingredients = ingredients
        self._record = record
        for key, value in list(record.items()):
            if key == 'doctor_dea_number':
                self._doctor_dea_number = value
            elif key == 'claim_number':
                self._claim_number = value
            elif key == 'state_fee':
                self._state_fee = value
            elif key == 'ref_nos':
                if not value:
                    self.ref_nos = []
                else:
                    self.ref_nos = value
            else:
                setattr(self, key, value)

    _claim_number = None

    @property
    def claim_number(self):
        if not self._claim_number:
            return ''
        split = self._claim_number.split(',')
        split = [s.strip() for s in split]
        split = [_f for _f in split if _f]
        if len(split) != 2:
            return self._claim_number

        l = {}
        good = ['MCA', 'MSA']
        for cn in split:
            prefix = cn.upper()[:3]
            if prefix in good:
                if prefix not in l:
                    l[prefix] = cn
            else:
                return self._claim_number

        if self.inv_class == 'C':
            try:
                return l['MCA']
            except KeyError:
                return self._claim_number
        else:
            try:
                return l['MSA']
            except KeyError:
                return self._claim_number


    doctor_license_number = None

    @property
    def savings(self):
        if self._client.savings_formula == 'AWP':
            return self.awp - self.total
        else:
            return self.state_fee - self.total

    @property
    def payment_label(self):
        return " ".join(map(self._pmt_item_label, self._payments))

    def _pmt_item_label(self, item):
        ref_no = item['ref_no'] or ''
        if item['reversed_invoice_id']:
            return 'CR:%s' % item['reversed_invoice_id']
        elif re.match('^\d+$', ref_no):
            return 'CK:%s' % ref_no
        else:
            return ref_no

    @property
    def _payments(self):
        squash = list(zip(self.ref_nos, self.payment_amounts or [], self.reversed_invoice_ids or []))
        keys = ['ref_no', 'amount', 'reversed_invoice_id']
        return [dict(list(zip(keys, v))) for v in squash]

    @property
    @imemoize
    def payments(self):
        cursor = db.dict_cursor()
        cursor.execute("""
            SELECT trans_payment.payment_id,
                   trans_payment.amount,
                   trans_payment.void_date,
                   trans_payment.entry_date,
                   COALESCE(trans_payment.ref_no, '') as ref_no,
                   trans_payment.username,
                   COALESCE('reversal ' || reversal.group_number || '-' || reversal.group_auth
                    || ' ' || reversal.reversal_date,
                            'overpayment ' || overpayment.ref_no) AS source
            FROM trans_payment
            LEFT JOIN reversal USING(reversal_id)
            LEFT JOIN overpayment USING(overpayment_id)
            WHERE trans_payment.trans_id=%s
            """, (self.trans_id,))
        return [Payment(self, d) for d in cursor]

    @property
    @imemoize
    def doctor_dea_number(self):
        if self._doctor_dea_number:
            return self._doctor_dea_number
        if not self.doctor_id:
            return ''
        cursor = db.cursor()
        cursor.execute("""
            SELECT doc_key
            FROM doctor_key
            WHERE doctor_id=%s
             AND LENGTH(doc_key) = 9
            """, (self.doctor_id,))
        if cursor.rowcount:
            return cursor.fetchone()[0]

    @property
    def ingredients(self):
        return self._ingredients

    @property
    def state_fee(self):
        """ Kentucky compounds dont really have a state fee so we
        fall back to the total for zero savings.
        """
        if self.jurisdiction == '16' and self.compound_code == '2' \
           and self._state_fee < self.total:
            return self.total

        return self._state_fee

    @property
    def ingredients_to_show_on_invoice(self):
        unknown_drug_id = 15281
        ingredients = [i for i in self._ingredients if i.drug_id != unknown_drug_id]
        if self._client.show_all_ingredients_on_invoice:
            return ingredients
        else:
            keyf = lambda i: (not i.on_formulary, i.ingredient_nbr)
            ingredients = sorted(ingredients, key=keyf)
            return ingredients[:3]

    @property
    def amount(self):
        return self._record['total']

    @property
    def paid(self):
        return self._record['balance'] == 0

    @property
    def paid_amount(self):
        return self._record['total'] - self._record['balance']

    @property
    def adj_total(self):
        return self._record['total']

    # Friend methods for ingredient used to do AWP calculations
    @property
    def _ingredient_awp_sum(self):
        return sum(i.awp for i in self.ingredients)

    @property
    def _ingredient_cost_sum_except_first(self):
        """ The first ingredient uses this to calculate the fudge factor
        to apply to its own cost. """
        return sum(i.cost for i in self.ingredients if i.ingredient_nbr != 1)

class Payment(object):
    def __init__(self, trans, dbrec):
        self._trans = trans
        self.amount = dbrec['amount']
        self.void_date = dbrec['void_date']
        self.entry_date = dbrec['entry_date']
        self.username = dbrec['username']
        self.ref_no = dbrec['ref_no']
        self.payment_id = dbrec['payment_id']
        self.source = dbrec['source']


class Invoice(object):
    """ Represents an invoice to be printed. Contains all of the
    calculations for the invoice and depends on line items.
    """
    def __init__(self, client, items):
        self._items = tuple(items)
        self._client = client

    invoice_date = property(lambda s: s._first_item_attr('invoice_date'))
    batch_date = property(lambda s: s._first_item_attr('invoice_date'))
    create_date = property(lambda s: s._first_item_attr('invoice_date'))
    group_number = property(lambda s: s._first_item_attr('group_number'))
    invoice_id = property(lambda s: s._first_item_attr('invoice_id'))
    division_code = property(lambda s: s._first_item_attr('division_code'))

    @property
    def memo(self):
        return ""

    @property
    def trailer(self):
        return ""

    @property
    def patient_ssn(self):
        if self._client.card_id_number:
            return self._client.card_id_number
        else:
            return self._first_item_attr("patient_ssn")

    patient_dob =  property(lambda s: s._first_item_attr("patient_dob"))
    patient_first_name =  property(lambda s: s._first_item_attr("patient_first_name"))
    patient_last_name =  property(lambda s: s._first_item_attr("patient_last_name"))
    patient_sex = property(lambda s: s._first_item_attr('patient_sex'))
    patient_zip_code = property(lambda s: s._first_item_attr("patient_zip_code"))
    jurisdiction =  property(lambda s: s._first_item_attr("jurisdiction"))

    billing_name = property(lambda s: s._first_item_attr("billing_name"))
    billing_address_1 = property(lambda s: s._first_item_attr("billing_address_1"))
    billing_address_2 = property(lambda s: s._first_item_attr("billing_address_2"))
    billing_city = property(lambda s: s._first_item_attr("billing_city"))
    billing_state = property(lambda s: s._first_item_attr("billing_state"))
    billing_zip_code = property(lambda s: s._first_item_attr("billing_zip_code"))

    claim_number =  property(lambda s: s._first_item_attr("claim_number"))
    doi =  property(lambda s: s._first_item_attr("doi"))

    pharmacy_name =  property(lambda s: s._first_item_attr("pharmacy_name"))
    pharmacy_nabp =  property(lambda s: s._first_item_attr("pharmacy_nabp"))
    pharmacy_tax_id =  property(lambda s: s._first_item_attr("pharmacy_tax_id"))
    pharmacy_address_1 =  property(lambda s: s._first_item_attr("pharmacy_address_1"))
    pharmacy_address_2 =  property(lambda s: s._first_item_attr("pharmacy_address_2"))
    pharmacy_city =  property(lambda s: s._first_item_attr("pharmacy_city"))
    pharmacy_state =  property(lambda s: s._first_item_attr("pharmacy_state"))
    pharmacy_zip_code =  property(lambda s: s._first_item_attr("pharmacy_zip_code"))

    client = property(lambda s: s._client)

    @property
    def show_cmpd_cost_on_invoice(self):
        return self.client.show_cmpd_cost_on_invoice

    @property
    def show_due_date_on_invoice(self):
        """ This is in the database for non private label groups. Added from BD Issue 28238. """
        return True

    pharmacy_street_1 = property(lambda s: s._phcy_address()[0])
    pharmacy_street_2 = property(lambda s: s._phcy_address()[1])
    def _phcy_address(self):
        """ COBOL stores this in a very strange way. Line 1 might be an attention
        line, pushing everything else down."""
        addr1, addr2 = self.pharmacy_address_1 or None, self.pharmacy_address_2 or None
        if addr1 and addr2:
            return addr2, addr1
        elif addr1:
            return addr1, ''
        elif addr2:
            return addr2, ''
        else:
            return '', ''

    @property
    def due_date(self):
        id = self._first_item_attr('invoice_date')
        return id + datetime.timedelta(days=14) 

    internal_control_number = ""

    @property
    def doi_row(self):
        d = set([i.doi.strftime("%m/%d/%y") for i in self._items if i.doi])
        return ["PATIENT DOI:", " ".join(d)]

    @property
    def trans_id_list(self):
        return sorted(i.trans_id for i in self._items)

    @property
    def items(self):
        return self._items

    @property
    def total(self):
        return sum(item.total for item in self._items)

    @property
    def sfs_total(self):
        return sum(item.state_fee for item in self._items)

    @property
    def savings(self):
        return self.sfs_total - self.total

    @property
    def paid(self):
        return self.paid_amount == self.total

    @property
    def balance(self):
        return sum(item.balance for item in self._items)

    @property
    def paid_amount(self):
        return self.total - self.balance

    @property
    def item_count(self):
        return len(self.items)

    @property
    def processing_fee_total(self):
        return 0

    @property
    def state_fee_total(self):
        return sum(item.state_fee for item in self._items)

    @property
    def awp_total(self):
        return sum(item.awp for item in self._items)

    @property
    def adj_total(self):
        return self.total

    def _first_item_attr(self, attr):
        if not self.items:
            return ''
        return getattr(self.items[0], attr)

class MJosephInvoice(Invoice):
    @property
    def trailer(self):
        return "* DEFINITION AND DISCLAIMER REGARDING AWP\nhttp://www.wolterskluwercdi.com/pricing-policy-update/"

    @property
    @imemoize
    def internal_control_number(self):
        cursor = db.cursor()
        cursor.execute("""
            SELECT sum(mjoseph_total) *100
            FROM trans WHERE invoice_id=%s
            """, (self.invoice_id,))
        v = int(cursor.fetchone()[0])
        import random, string
        c  = random.sample(string.ascii_uppercase, 3)
        c = ''.join(c)
        return "Internal Control Code: %06d%s" % (v, c)

class SunriseInvoice(Invoice):
    @property
    def internal_control_number(self):
        return ''

class ClientFactory(object):
    def __init__(self):
        self._obj_cache = {}

    def for_invoice_id(self, invoice_id):
        cursor = db.cursor()
        cursor.execute("""
            SELECT DISTINCT group_number
            FROM trans
            WHERE invoice_id=%s
            """, (invoice_id,))
        if cursor.rowcount != 1:
            raise DataError("Invoice %s has %s group numbers" %
                (invoice_id, cursor.rowcount))
        group_number = cursor.fetchone()[0]
        return self.for_group_number(group_number)

    def for_group_number(self, group_number):
        if group_number not in self._obj_cache:
            self._fetch_from_db(group_number)
        return self._obj_cache[group_number]

    def _fetch_from_db(self, group_number):
        cursor = db.dict_cursor()
        cursor.execute("""
            SELECT
               group_info.group_number,
               group_info.company_name AS billing_name,
               False as print_multiplier_invoice,
               True as print_nonmultiplier_invoice,
               NULL AS invoice_multiplier,
               group_info.address_1,
               group_info.address_2,
               group_info.city,
               group_info.state,
               group_info.zip_code,
               group_info.savings_formula,
               group_info.card_id_number,
               'PRINT' AS invoice_processor_code,
               CASE WHEN savings_formula = 'AWP' THEN True ELSE False END as show_awp_on_invoice,
               CASE WHEN savings_formula = 'SFS' THEN True ELSE False END as show_sfs_on_invoice,
               False as show_copay_on_invoice,
               False AS show_uc_on_invoice,
               True as show_savings_on_invoice,
               False as force_under_state_fee,
               False as show_all_ingredients_on_invoice,
               CASE WHEN group_info.group_number = '81116' THEN True
                   ELSE False
                   END as show_cmpd_cost_on_invoice
            FROM group_info
            WHERE group_number=%s
        """, (group_number,))
        if cursor.rowcount != 1:
            raise DataError("Database has %s clients with group number %s" %
                (cursor.rowcount, group_number))

        dbrec = cursor.fetchone()
        self._obj_cache[group_number] = self._client_for(dbrec)

    def _client_for(self, rec):
        client_map = {
            'bd': Client,
            'mjoseph': MJosephClient,
            'msq': MSQClient,
            'sunrise': SunriseClient,
            's1': S1Client
        }
        cls = client_map.get(config.invoice_class(), Client)
        return cls(rec)

class Client(object):
    def __init__(self, dbrec):
        self.group_number = dbrec['group_number']
        self.address_1 = dbrec['address_1'] or ''
        self.address_2 = dbrec['address_2'] or ''
        self.billing_name = dbrec['billing_name'] or ''
        self.card_id_number = dbrec['card_id_number']
        self.city = dbrec['city'] or ''
        self.state = dbrec['state'] or ''
        self.zip_code = dbrec['zip_code'] or ''
        self.savings_formula = dbrec['savings_formula']
        self.invoice_processor_code = dbrec['invoice_processor_code']
        self.invoice_multiplier = dbrec['invoice_multiplier']
        self.show_awp_on_invoice = dbrec['show_awp_on_invoice']
        self.show_sfs_on_invoice = dbrec['show_sfs_on_invoice']
        self.show_copay_on_invoice = dbrec['show_copay_on_invoice']
        self.show_uc_on_invoice = dbrec['show_uc_on_invoice']
        self.show_savings_on_invoice = dbrec['show_savings_on_invoice']
        self.print_multiplier_invoice = dbrec['print_multiplier_invoice']
        self.print_nonmultiplier_invoice = dbrec['print_nonmultiplier_invoice']
        self.force_under_state_fee = dbrec['force_under_state_fee']
        self.show_all_ingredients_on_invoice = dbrec['show_all_ingredients_on_invoice']
        self.show_cmpd_cost_on_invoice = dbrec['show_cmpd_cost_on_invoice']

    show_claim_number_column = True
    use_invoice_color = False
    show_adjusted_total = False
    show_pharmacy_tax_id_on_invoice = False
    show_gpi_code_on_invoice = False
    show_pharmacy_cost_on_invoice = False

    @property
    def invoice_class(self):
        return config.invoice_class()

    biller_mailing_address = ""
    biller_tax_id_row = ["", ""]
    biller_phone = ""
    biller_phone_2 = ""

class SunriseClient(Client):
    biller_mailing_address = (
        "Sunrise Medical Solutions\n"
        "PO Box 425\n"
        "Grayson, GA 30017\n")
    biller_tax_id_row = ["TAX ID:", "45-3704253"]
    biller_phone = "844-683-6300"
    biller_phone_2 = ""

    use_invoice_color = False

class MJosephClient(Client):
    use_invoice_color = True
    biller_mailing_address = (
        "M. Joseph Medical\n"
        "PO Box 436559\n"
        "Louisville, KY 40253\n")
    biller_tax_id_row = ["TAX ID:", "42-1690410"]
    biller_phone = "844-DME-AND-Rx"
    biller_phone_2 = "(844-363-2637)"
    show_gpi_code_on_invoice = True

class MSQClient(Client):
    use_invoice_color = False
    @property
    def biller_mailing_address(self):
        if self.group_number == '87025':
            return  (
                "MedicalServiceQuotes.com\n"
                "695 Jerry St Ste 300\n"
                "Castle Rock, CO 80104\n"
            )
        else:
            # MSQ Issue 11210
            return (
                "MedicalServiceQuotes.com\n"
                "PO 31001-3272\n"
                "Pasadena, CA 91110-3272"
            )

    biller_tax_id_row = [
        "BILLER E-MAIL", "accounting@medicalservicequotes.com",
        "BILLER TAX ID:", "27-0335602"
    ]
    biller_phone = "(888) 894-3599"
    biller_phone_2 = ""

class S1Client(Client):
    use_invoice_color = False
    # MSQ Issue 12973
    biller_mailing_address = (
        "S1 Medical\n"
        "P.O. Box 834\n"
        "Fort Washington, PA 19034-0834"
    )

    biller_tax_id_row = [
        "BILLER E-MAIL", "pharmacy@ancillary-s1-medical.com",
        "BILLER TAX ID:", "81-2854849"
    ]
    biller_phone = "(888) 894-3599"
    biller_phone_2 = ""


class Ingredient(object):
    # set by the factory during construction. Could not be passed to
    # constructor b/c of circular dependency

    line_item = None

    def __init__(self, dbrec):
        self.ingredient_id = dbrec['ingredient_id']
        self.ingredient_nbr = dbrec['ingredient_nbr']
        self.qty = dbrec['qty']
        self.drug_id = dbrec['drug_id']
        self.cost_submitted = dbrec['cost_submitted']
        self.cost_allowed = dbrec['cost_allowed']
        self.drug_name = dbrec['drug_name']
        self.ndc_number = dbrec['ndc_number']
        self.gpi_code = dbrec['gpi_code']
        self.awp = dbrec['awp']
        self._patient_id = dbrec['patient_id']

    @property
    def on_formulary(self):
        return False

    @property
    def cost(self):
        c = self.line_item.amount * self._percent_of_total_awp
        cost = count_money(c)
        if self.ingredient_nbr == 1:
            calc = self.line_item._ingredient_cost_sum_except_first + cost
            fudge = self.line_item.amount - calc
            #raise ValueError(calc, fudge, cost)
            cost = cost + fudge
        return cost

    @property
    def _percent_of_total_awp(self):
        return old_div(self.awp, self.line_item._ingredient_awp_sum)

    _on_formulary = None
