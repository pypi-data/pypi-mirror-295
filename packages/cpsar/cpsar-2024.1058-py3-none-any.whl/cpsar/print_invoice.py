""" Invoice Printing Object System

Primary collaborators:
 - PDFWriter
 - InvoiceFactory
 - Invoice
 - LineItem
 - Client
"""
from __future__ import print_function
from __future__ import division
from future import standard_library
standard_library.install_aliases()
from builtins import map
from past.utils import old_div
from builtins import object
import cmd
import os
import sys
import six

from decimal import Decimal
from subprocess import getstatusoutput

import cpsar.runtime as R
import cpsar.invoice_pdf as P

from cpsar import config
from cpsar import formulary
from cpsar.util import Mako, count_money, imemoize

class Factory(object):
    """ Object assembler. Use an instance of me for an easy API to creating
    objects. This is the primary module interface.
    """
    def __init__(self):
        self.client_factory = ClientFactory()
        self.invoice_base_path = config.inv_base()
        self.html2ps_config_path = "%s/invoice/print.html2ps"
        self.html2ps_config_path %= config.mako_template_dir()
        self.print_options = PrintOptions(show_past_due_stamp=False)

    def invoice_factory(self, include_paid_items=True):
        item_factory = LineItemFactory(self.client_factory, include_paid_items)
        invoice_factory = InvoiceFactory(self.client_factory, item_factory)
        return invoice_factory

    def multiplied_invoice_factory(self, include_paid_items=True):
        item_factory = MultipliedLineItemFactory(self.client_factory, include_paid_items)
        invoice_factory = InvoiceFactory(self.client_factory, item_factory)
        return invoice_factory

    def writer(self):
        return P.PDFWriter(self.print_options.show_past_due_stamp)

    def disk_file_factory(self):
        writer_factory = PDFWriterFactory(self.print_options)
        return InvoiceDiskFileFactory(writer_factory)

class InvoiceDiskFileFactory(object):
    """ Invoice file on disk """
    def __init__(self, writer_factory):
        self._writer_factory = writer_factory

    def for_invoice(self, invoice):
        """ Provide the invoice disk file for the given invoice """
        return InvoiceDiskFile(invoice, self._writer_factory)

class InvoiceDiskFile(object):
    """ A physical disk on file storing a printout of an invoice. """
    def __init__(self, invoice, writer_factory):
        self._invoice = invoice
        self._writer_factory = writer_factory

    def write(self, fpath):
        writer = self._writer_factory.get()
        fd = open(fpath, 'wb')
        writer.add_invoice(self._invoice)
        writer.write(fd)
        fd.close()

class PDFWriterFactory(object):
    def __init__(self, print_options):
        self._print_options = print_options

    def get(self):
        return P.PDFWriter(self._print_options.show_past_due_stamp)

class PrintOptions(object):
    def __init__(self, show_past_due_stamp=False):
        self.show_past_due_stamp = show_past_due_stamp

    def as_dict(self):
        return {
            'show_past_due_stamp': self.show_past_due_stamp}

class InvoiceFactory(object):
    """ Creates invoice objects """
    def __init__(self, client_factory, item_factory):
        self._client_factory = client_factory
        self._item_factory = item_factory

    def for_invoice_id(self, invoice_id):
        cursor = R.db.dict_cursor()
        cursor.execute(self._sql("invoice_id=%s"), (invoice_id,))
        if cursor.rowcount != 1:
            raise DataError("Invoice records with invoice_id %s = %s"
                            % (invoice_id, cursor.rowcount))
        return self._for_dbrec(cursor.fetchone())

    def unpaid(self):
        """ All unpaid invoices """
        cursor = R.db.dict_cursor()
        cursor.execute(self._sql("invoice.balance != 0"))
        return list(map(self._for_dbrec, cursor))

    def unpaid_internet_invoices(self):
        """ All unpaid invoices that are to be published to the website.
        """
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT
               invoice.invoice_id,
               invoice.create_date::date,
               invoice.batch_date,
               invoice.due_date,
               invoice.memo,
               invoice.group_number,
               invoice.balance,
               patient.first_name as patient_first_name,
               patient.last_name as patient_last_name,
               patient.ssn as patient_ssn,
               patient.dob as patient_dob,
               patient.jurisdiction,
               patient.zip_code as patient_zip_code,
               ar_payer.billing_name,
               ar_payer.billing_address_1,
               ar_payer.billing_address_2,
               ar_payer.billing_city,
               ar_payer.billing_state,
               ar_payer.billing_zip_code
            FROM invoice
            JOIN client ON invoice.group_number = client.group_number
            JOIN patient ON invoice.patient_id = patient.patient_id
            JOIN ar_payer ON patient.patient_id = ar_payer.patient_id
            WHERE invoice.balance != 0 AND
            client.invoice_processor_code = 'INTERNET'
            ORDER BY invoice.invoice_id DESC
            """)
        return list(map(self._for_dbrec, cursor))

    def unpaid_for_client_on(self, client, batch_date):
        """ All unpaid invoices for the given client on the given batch date
        """
        cursor = R.db.dict_cursor()
        sql =  """
            with t as (
                select distinct invoice_id
                from trans
                where group_number=%s
                  and batch_date >= %s
                  and balance != 0
            )
            SELECT
               invoice.invoice_id,
               invoice.create_date::date,
               invoice.batch_date,
               invoice.due_date,
               invoice.memo,
               invoice.group_number,
               patient.first_name as patient_first_name,
               patient.last_name as patient_last_name,
               patient.ssn as patient_ssn,
               patient.dob as patient_dob,
               patient.jurisdiction,
               patient.zip_code as patient_zip_code,
               ar_payer.billing_name,
               ar_payer.billing_address_1,
               ar_payer.billing_address_2,
               ar_payer.billing_city,
               ar_payer.billing_state,
               ar_payer.billing_zip_code
            FROM invoice
            JOIN t using(invoice_id)
            JOIN client ON invoice.group_number = client.group_number
            JOIN patient ON invoice.patient_id = patient.patient_id
            JOIN ar_payer ON patient.patient_id = ar_payer.patient_id
            WHERE invoice.batch_date = %s
            ORDER BY patient.last_name, patient.first_name
        """
        cursor.execute(sql, (client.group_number, batch_date, batch_date))
        return list(map(self._for_dbrec, cursor))

    def unpaid_for_report_code_on(self, report_code, batch_date):
        cursor = R.db.dict_cursor()
        sql = self._sql("""
            invoice.batch_date=%s AND
            client.group_number IN (
                SELECT group_number
                FROM client_report_code
                WHERE report_code=%s)
            """)
        cursor.execute(sql, (batch_date, report_code))
        return list(map(self._for_dbrec, cursor))

    def unpaid_for_client(self, client):
        """ All unpaid invoices for the given client"""
        cursor = R.db.dict_cursor()
        sql = self._sql("invoice.group_number=%s AND invoice.balance != 0")
        cursor.execute(sql, (client.group_number,))
        return list(map(self._for_dbrec, cursor))

    def _for_dbrec(self, dbrec):
        invoice_id = dbrec['invoice_id']
        items = self._item_factory.for_invoice_id(invoice_id)
        client = self._client_factory.for_invoice_id(invoice_id)
        return self._invoice_class(dbrec)(dbrec, client, items)

    def _invoice_class(self, dbrec):
        if dbrec['group_number'] == '70076':
            return LAIGAInvoice
        else:
            return Invoice

    def _sql(self, where_frag, order_by='invoice.invoice_id'):
        return """
            SELECT
               invoice.invoice_id,
               invoice.create_date::date,
               invoice.batch_date,
               invoice.due_date,
               invoice.memo,
               invoice.group_number,
               patient.first_name as patient_first_name,
               patient.last_name as patient_last_name,
               patient.ssn as patient_ssn,
               patient.dob as patient_dob,
               patient.jurisdiction,
               patient.zip_code as patient_zip_code,
               ar_payer.billing_name,
               ar_payer.billing_address_1,
               ar_payer.billing_address_2,
               ar_payer.billing_city,
               ar_payer.billing_state,
               ar_payer.billing_zip_code
            FROM invoice
            JOIN client ON invoice.group_number = client.group_number
            JOIN patient ON invoice.patient_id = patient.patient_id
            JOIN ar_payer ON patient.patient_id = ar_payer.patient_id
            WHERE %s
            ORDER BY %s
        """ % (where_frag, order_by)

class LineItemFactory(object):
    def __init__(self, client_factory, include_paid_transactions=True):
        self._client_factory = client_factory
        self.include_paid_transactions = include_paid_transactions

    def for_invoice_id(self, invoice_id):
        dbrecs = self._dbrecs_for_invoice_id(invoice_id)
        client = self._client_factory.for_invoice_id(invoice_id)
        for record in dbrecs:
            ingredients = self._ingredients_for_history_id(record['history_id'])
            item_class = self._item_class(client.group_number)
            if item_class == MSQLineItem:
                line_item = item_class(record, client, ingredients)
            else:
                line_item = item_class(record, client, ingredients)
            # The line_item and ingredients have a circular dependency so we go
            # back and assign it here
            for ingredient in ingredients:
                ingredient.line_item = line_item
            if line_item.paid:
                if self.include_paid_transactions:
                    yield line_item
            else:
                yield line_item

    def _dbrecs_for_invoice_id(self, invoice_id):
        cursor = R.db.dict_cursor()
        sql = """
         WITH payment_count AS (
            SELECT trans.trans_id, COUNT(*) as val
            FROM trans_payment
            JOIN trans USING(trans_id)
            WHERE trans.invoice_id=%s
            GROUP BY trans.trans_id
        )
            SELECT trans.trans_id,
                   trans.line_no,
                   trans.rx_date,
                   trans.claim_number,
                   trans.quantity,
                   trans.days_supply,
                   trans.savings,
                   history.doctor_dea_number,
                   history.doctor_npi_number,
                   trans.state_fee,
                   trans.adjustments,
                   trans.awp,
                   trans.sales_tax,
                   trans.compound_code,
                   trans.eho_network_copay,
                   trans.cost_allowed,
                   trans.dispense_fee,
                   trans.processing_fee,
                   trans.usual_customary,
                   trans.tx_type,
                   trans.paid_amount,
                   trans.patient_id,
                   trans.doctor_id,
                   trans.adjuster1_email,
                   trans.rebate_credit_total,
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
                   pharmacy.tax_id as pharmacy_tax_id,
                   pharmacy.city AS pharmacy_city,
                   pharmacy.state AS pharmacy_state,
                   pharmacy.zip_code AS pharmacy_zip,
                   pharmacy.npi AS pharmacy_npi,
                   COALESCE(pharmacy.tax_id, '') AS pharmacy_tax_id,
                   pharmacy.zip_code AS pharmacy_zip_code,
                   doctor.name AS doctor_name,
                   history.history_id,
                   pharmacist.lic_number AS pharmacist_license_number,
                   pharmacist.first_name AS pharmacist_first_name,
                   pharmacist.last_name AS pharmacist_last_name,
                   pharmacist.middle_init AS pharmacist_middle_initial,
                   history.cost_submitted as pharmacy_cost_submitted,
                   history.refill_number,
                   history.rx_number,
                   history.daw,
                   history.inv_class,
                   claim.doi,
                   claim.ref_nbr_1,
                   claim.ref_nbr_2,
                   COALESCE(payment_count.val, 0) AS payment_count,
                   COALESCE(trans.doctor_state_lic_number, doctor_state.license_number) as doctor_license_number
            FROM trans
            JOIN drug ON
                 drug.drug_id = trans.drug_id
            JOIN history ON
                 trans.history_id = history.history_id
            LEFT JOIN payment_count USING(trans_id)
            LEFT JOIN drug AS brand_drug ON
                 drug.brand_ndc = brand_drug.ndc_number
            LEFT JOIN patient ON
                 trans.patient_id = patient.patient_id
            LEFT JOIN pharmacy ON
                 trans.pharmacy_id = pharmacy.pharmacy_id
            LEFT JOIN user_info AS u1 ON
                 trans.adjuster1_email = u1.email
            LEFT JOIN user_info AS u2 ON
                 trans.adjuster2_email = u2.email
            LEFT JOIN doctor ON
                 trans.doctor_id = doctor.doctor_id
            LEFT JOIN claim ON
                 history.claim_id = claim.claim_id
            LEFT JOIN pharmacist ON
                 history.pharmacist_id = pharmacist.pharmacist_id
            LEFT JOIN doctor_state ON
                 history.doctor_id = doctor_state.doctor_id
             AND patient.state = doctor_state.state

            WHERE trans.invoice_id=%s
            ORDER BY trans.line_no
            """
        cursor.execute(sql, (invoice_id, invoice_id))
        return cursor

    def _item_class(self, group_number):
        tmpl_classes = {
            '70234': BridgewellLineItem,
            '77701': MSQLineItem,
            '70036': BridgePointLineItem,
            '70852': BridgePointLineItem,
        }
        return tmpl_classes.get(group_number, LineItem)

    def _ingredients_for_history_id(self, history_id):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT I.ingredient_id,
                   I.ingredient_nbr,
                   I.qty,
                   I.cost_submitted,
                   I.cost_allowed,
                   I.drug_id,
                   I.awp,
                   I.cost,
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

class MultipliedLineItemFactory(LineItemFactory):
    """ Responsible for creating line items which are multiplied """
    def _item_class(self, group_number):
        return MultipliedLineItem

class ClientFactory(object):
    def __init__(self):
        self._obj_cache = {}

    def for_invoice_id(self, invoice_id):
        cursor = R.db.cursor()
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

    def with_print_for_batch(self, batch_file_id):
        """ All of the clients with transactions in the
        given batch that have an invoice processor of
        PRINT """
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT 
               client.group_number,
               client.billing_name,
               client.print_multiplier_invoice,
               client.print_nonmultiplier_invoice,
               client.invoice_multiplier,
               client.address_1,
               client.address_2,
               client.city,
               client.state,
               client.zip_code,
               client.savings_formula,
               client.invoice_processor_code,
               client.show_awp_on_invoice,
               client.show_sfs_on_invoice,
               client.show_copay_on_invoice,
               client.show_pharmacy_tax_id_on_invoice,
               FALSE as show_gpi_code_on_invoice,
               client.show_pharmacy_cost_on_invoice,
               client.show_uc_on_invoice AS show_uc_on_invoice,
               client.show_savings_on_invoice,
               client.force_under_state_fee,
               client.show_all_ingredients_on_invoice,
               client.show_cmpd_cost_on_invoice,
               client.show_due_date_on_invoice,
               group_info.card_id_number
            FROM client
            JOIN group_info USING(group_number)
            WHERE client.group_number IN (
                SELECT group_number
                FROM trans
                WHERE batch_file_id=%s)
               AND client.invoice_processor_code = 'PRINT'
            ORDER BY client.group_number
            """, (batch_file_id,))
        return list(map(Client, cursor))

    def all_with_invoices_on(self, batch_date):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT 
               client.group_number,
               client.billing_name,
               client.print_multiplier_invoice,
               client.print_nonmultiplier_invoice,
               client.invoice_multiplier,
               client.address_1,
               client.address_2,
               client.city,
               client.state,
               client.zip_code,
               client.savings_formula,
               client.invoice_processor_code,
               client.show_awp_on_invoice,
               client.show_sfs_on_invoice,
               client.show_copay_on_invoice,
               client.show_pharmacy_tax_id_on_invoice,
               FALSE as show_gpi_code_on_invoice,
               client.show_pharmacy_cost_on_invoice,
               client.show_uc_on_invoice AS show_uc_on_invoice,
               client.show_savings_on_invoice,
               client.force_under_state_fee,
               client.show_all_ingredients_on_invoice,
               client.show_cmpd_cost_on_invoice,
               client.show_due_date_on_invoice,
               group_info.card_id_number
            FROM client
            JOIN group_info USING(group_number)
            WHERE client.group_number IN (
                SELECT group_number
                FROM trans
                WHERE batch_date=%s)
            ORDER BY client.group_number
            """, (batch_date,))
        return list(map(Client, cursor))

    def _fetch_from_db(self, group_number):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT
               client.group_number,
               client.billing_name,
               client.print_multiplier_invoice,
               client.print_nonmultiplier_invoice,
               client.invoice_multiplier,
               client.address_1,
               client.address_2,
               client.city,
               client.state,
               client.zip_code,
               client.savings_formula,
               client.invoice_processor_code,
               client.show_awp_on_invoice,
               client.show_sfs_on_invoice,
               client.show_copay_on_invoice,
               client.show_pharmacy_tax_id_on_invoice,
               FALSE as show_gpi_code_on_invoice,
               client.show_pharmacy_cost_on_invoice,
               client.show_uc_on_invoice AS show_uc_on_invoice,
               client.show_savings_on_invoice,
               client.force_under_state_fee,
               client.show_all_ingredients_on_invoice,
               client.show_cmpd_cost_on_invoice,
               client.show_due_date_on_invoice,
               group_info.card_id_number
            FROM client
            JOIN group_info USING(group_number)
            WHERE client.group_number=%s
        """, (group_number,))
        if cursor.rowcount != 1:
            raise DataError("Database has %s clients with group number %s" %
                (cursor.rowcount, group_number))

        dbrec = cursor.fetchone()
        self._obj_cache[group_number] = Client(dbrec)

class Client(object):
    biller_mailing_address = ("CORPORATE PHARMACY SERVICES, INC.\n"
                            "P.O. BOX 1950\n"
                            "GADSDEN, AL 35902")

    biller_tax_id_row = ["TAX ID:", "63-1040950"]
    biller_phone = "(256) 543-9000"
    biller_phone_2 = ""
    use_invoice_color = False
    show_adjusted_total = True
    private_label = None
    invoice_class = None
    show_claim_number_column = False

    def __init__(self, dbrec):
        self.group_number = dbrec['group_number']
        self.address_1 = dbrec['address_1'] or ''
        self.address_2 = dbrec['address_2'] or ''
        self.billing_name = dbrec['billing_name']
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
        self.show_pharmacy_tax_id_on_invoice = dbrec['show_pharmacy_tax_id_on_invoice']
        self.show_pharmacy_cost_on_invoice = dbrec['show_pharmacy_cost_on_invoice']
        self.show_gpi_code_on_invoice = dbrec['show_gpi_code_on_invoice']
        self.show_uc_on_invoice = dbrec['show_uc_on_invoice']
        self.show_savings_on_invoice = dbrec['show_savings_on_invoice']
        self.print_multiplier_invoice = dbrec['print_multiplier_invoice']
        self.print_nonmultiplier_invoice = dbrec['print_nonmultiplier_invoice']
        self.force_under_state_fee = dbrec['force_under_state_fee']
        self.show_all_ingredients_on_invoice = dbrec['show_all_ingredients_on_invoice']
        self.show_cmpd_cost_on_invoice = dbrec['show_cmpd_cost_on_invoice']
        self.show_due_date_on_invoice = dbrec['show_due_date_on_invoice']

class Invoice(object):
    """ Represents an invoice to be printed. Contains all of the
    calculations for the invoice and depends on line items.
    """
    def __init__(self, dbrec, client, items):
        self.batch_date = dbrec['batch_date']
        self.create_date = dbrec['create_date']
        self.due_date = dbrec['due_date']
        self.group_number = dbrec['group_number']
        self.invoice_id = dbrec['invoice_id']
        self.memo = dbrec['memo']
        self.patient_dob = dbrec['patient_dob']
        self.patient_first_name = dbrec['patient_first_name']
        self.patient_last_name = dbrec['patient_last_name']
        self.patient_zip_code = dbrec['patient_zip_code']
        self._patient_ssn = dbrec['patient_ssn']
        self.jurisdiction = dbrec['jurisdiction']
        self.billing_name = dbrec['billing_name']
        self.billing_address_1 = dbrec['billing_address_1']
        self.billing_address_2 = dbrec['billing_address_2']
        self.billing_city = dbrec['billing_city']
        self.billing_state = dbrec['billing_state']
        self.billing_zip_code = dbrec['billing_zip_code']

        self._items = tuple(items)
        self._client = client

    @property
    def patient_ssn(self):
        if self._client.card_id_number:
            return self._client.card_id_number
        else:
            return self._patient_ssn

    # Used for mjo
    internal_control_number = None
    @property
    def doi_row(self):
        d = set([i.claim_number for i in self._items if i.claim_number])
        if len(d):
            return ["Claim #:", " ".join(d)]
        else:
            return None

    @property
    def client(self):
        return self._client

    @property
    def show_cmpd_cost_on_invoice(self):
        return self._client.show_cmpd_cost_on_invoice

    @property
    def show_due_date_on_invoice(self):
        return self._client.show_due_date_on_invoice

    @property
    def items(self):
        return self._items

    @property
    def total(self):
        return sum(item.amount for item in self._items)

    @property
    def paid(self):
        return self.paid_amount == self.total

    @property
    def paid_amount(self):
        return sum(item.paid_amount for item in self._items)

    @property
    def balance(self):
        return self.adj_total - self.paid_amount

    @property
    def item_count(self):
        return len(self.items)

    @property
    def processing_fee_total(self):
        return sum(item.processing_fee for item in self._items)

    @property
    def state_fee_total(self):
        return sum(item.state_fee for item in self._items)

    @property
    def awp_total(self):
        return sum(item.awp for item in self._items)

    @property
    def adj_total(self):
        return sum(item.adj_total for item in self._items)

class LAIGAInvoice(Invoice):
    @property
    def short_codes(self):
        codes = set(map(self._code_trunc, self.items))
        return " ".join(sorted(codes))

    def _code_trunc(self, item):
        if item.claim_number:
            return item.claim_number.split('-')[-1]
        else:
            return ''

class LineItem(object):
    """ A particular line item on the invoice. Different subclasses implement
    different business rules. Construction controlled by InvoiceFactory.
    """
    _doctor_npi_number = None
    _doctor_dea_number = None

    def __init__(self, record, client, ingredients):
        self._client = client
        self._ingredients = ingredients
        self._record = record
        for key, value in list(record.items()):
            if key == 'doctor_dea_number':
                self._doctor_dea_number = value
            elif key == 'doctor_npi_number':
                self._doctor_npi_number = value
            elif key == 'claim_number':
                self._claim_number = value
            else:
                setattr(self, key, value)

    _claim_number = None
    @property
    def claim_number(self):
        return self._claim_number

    @property
    def payment_label(self):
        if self.payment_count > 0 and self.rebate_credit_total > 0:
            return "PAY/REB"
        elif self.rebate_credit_total:
            return "REBATE"
        else:
            return "PAYMENT"

    @property
    @imemoize
    def doctor_dea_number(self):
        if self._doctor_dea_number and len(self._doctor_dea_number) == 9:
            return self._doctor_dea_number
        if not self.doctor_id:
            return ''
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT doc_key
            FROM doctor_key
            WHERE doctor_id=%s
             AND LENGTH(doc_key) = 9
            """, (self.doctor_id,))
        if cursor.rowcount:
            return cursor.fetchone()[0]

    @property
    @imemoize
    def doctor_npi_number(self):
        if self._doctor_npi_number and len(self._doctor_npi_number) == 10:
            return self._doctor_npi_number
        if not self.doctor_id:
            return ''
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT doc_key
            FROM doctor_key
            WHERE doctor_id=%s
             AND LENGTH(doc_key) = 10
            """, (self.doctor_id,))
        if cursor.rowcount:
            return cursor.fetchone()[0]

    @property
    def ingredients(self):
        return self._ingredients

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
        amt = (self.cost_allowed + self.dispense_fee + self.sales_tax +
                self.processing_fee - self.eho_network_copay)
        if self._client.force_under_state_fee and amt > self.state_fee:
            return self.state_fee
        return amt

    @property
    def paid(self):
        return self.balance == 0

    @property
    def adj_total(self):
        return self.amount + self.adjustments 

    @property
    def balance(self):
        return self.adj_total - self.paid_amount

class MockLineItem(LineItem):
    savings = property(lambda s: Decimal("0.00"))
    savings = savings.setter(lambda s, v: None)
    state_fee = property(lambda s: Decimal("0.00"))
    state_fee = state_fee.setter(lambda s, v: None)
    amount = property(lambda s: Decimal("0.00"))
    adj_total = property(lambda s: Decimal("0.00"))
    balance = property(lambda s: Decimal("0.00"))
    payment_label = ''
    paid_amount = property(lambda s: Decimal("0.00"))
    paid_amount = paid_amount.setter(lambda s, v: None)

class MSQLineItem(LineItem):
    def __init__(self, record, client, ingredients):
        super(MSQLineItem, self).__init__(record, client, ingredients)
        self.processing_fee = self._msq_processing_fee()

    @property
    def amount(self):
        return (self.cost_allowed + self.dispense_fee + self.sales_tax +
                self._processing_fee_in_total - self.eho_network_copay)

    @property
    def adj_total(self):
        return self.amount + self._msq_processing_fee() + self.adjustments 

    def _msq_processing_fee(self):
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT SUM(amount)
            FROM distribution
            WHERE trans_id=%s AND distribution_account = 'msq'
            """, (self.trans_id,))
        amount, = cursor.fetchone()
        return amount or 0

    @property
    def _processing_fee_in_total(self):
        return self._record['processing_fee'] - self._msq_processing_fee()

    @property
    def claim_number(self):
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


class MultipliedLineItem(LineItem):
    @property
    def amount(self):
        return count_money(LineItem.amount.fget(self) * self._client.invoice_multiplier)

class BridgePointLineItem(LineItem):
    @property
    def claim_number(self):
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

class BridgewellLineItem(LineItem):
    @property
    def amount(self):
        cost = self.cost_allowed + self.dispense_fee
        cost = old_div(cost, Decimal("1.1205"))
        cost = (cost + self.processing_fee)
        return cost * Decimal("2.5")

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
        self.cost = dbrec['cost']
        self._patient_id = dbrec['patient_id']

    @property
    def on_formulary(self):
        if self._on_formulary is not None:
            return self._on_formulary

        patient = formulary._patient_by_id(self._patient_id)
        drug = formulary._drug_by_ndc(self.ndc_number)
        self._on_formulary = formulary.patient_has_drug(patient, drug)
        return self._on_formulary

    _on_formulary = None

class DataError(Exception):
    pass

class StateError(Exception):
    pass

class ConfigError(Exception):
    pass

class Test(cmd.Cmd):
    def setup(self):
        import cpsar.runtime as R
        R.db.setup()
        self.clients = ClientFactory()

        item_factory = LineItemFactory(self.clients)
        self.invoices = InvoiceFactory(self.clients, item_factory)

        multiplied_items = MultipliedLineItemFactory(self.clients)
        self.multiplied_invoices = InvoiceFactory(self.clients, multiplied_items)

    def run(self):
        self.setup()
        if len(sys.argv) == 1:
            self.cmdloop()
        else:
            self.onecmd(" ".join(sys.argv[1:]))

    def do_mult(self, not_used):
        client = self.clients.for_group_number('70234')
        for invoice in self.invoices.unpaid_for_client(client):
            minvoice = self.multiplied_invoices.for_invoice_id(invoice.invoice_id)
            print('%07d' % invoice.invoice_id, end=' ')
            print('Multiplier:', client.invoice_multiplier, end=' ')
            print('Real total:', invoice.total, end=' ')
            print('Inflated total:', minvoice.total)

    def do_writer(self, invoice_id):
        if not invoice_id:
            invoice_id = 379492
        writer = P.PDFWriter()
        invoice = self.invoices.for_invoice_id(invoice_id)
        writer.add_invoice(invoice)
        writer.write(sys.stdout)

    def do_full_batch(self, batch_date):
        if not batch_date:
            batch_date = "2013-02-28"

        writer = P.PDFWriter()
        for client in self.clients.all_with_invoices_on(batch_date):
            if client.invoice_processor_code != 'PRINT':
                continue
            for invoice in self.invoices.unpaid_for_client_on(client, batch_date):
                if invoice.balance == 0:
                    continue
                if client.print_nonmultiplier_invoice:
                    writer.add_invoice(invoice)
                if client.print_multiplier_invoice:
                    mul_invoice = self.multiplied_invoices.for_invoice_id(invoice.invoice_id)
                    writer.add_invoice(mul_invoice)
        fd = open("/dev/null", "w")
        writer.write(fd)

    def do_batch(self, batch_date):
        if not batch_date:
            batch_date = "2013-02-28"
        for client in self.clients.all_with_invoices_on(batch_date):
            if client.invoice_processor_code != 'PRINT':
                continue
            for invoice in self.invoices.unpaid_for_client_on(client, batch_date):
                if client.print_nonmultiplier_invoice:
                    print(invoice.invoice_id, invoice.total, end=' ')
                if client.print_multiplier_invoice:
                    mul_invoice = self.multiplied_invoices.for_invoice_id(invoice.invoice_id)
                    print('mult:', mul_invoice.total, end=' ')
                print()

    def do_time_batch(self, stat_file_path):
        import cProfile
        cProfile.runctx('self.do_full_batch(None)', globals(), locals(), stat_file_path)

    def do_EOF(self, line):
        print()
        return True

if __name__ == '__main__':
    Test().run()

