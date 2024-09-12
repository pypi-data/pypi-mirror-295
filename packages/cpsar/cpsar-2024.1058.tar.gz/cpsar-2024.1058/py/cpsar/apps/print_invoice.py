import os
import cpsar.pg as P
import cpsar.runtime as R
import cpsar.ws as W

from cpsar import print_invoice

class Program(W.MakoProgram):
    pdf_data = None

    @property
    def include_paid_transactions(self):
        return self.fs.getvalue('show_paid')

    @property
    def show_balance(self):
        return self.fs.getvalue('show_balance')

    @property
    def show_past_due_stamp(self):
        return self.fs.getvalue('show_past_due_stamp')

    def all_requested_invoice_ids(self):
        return self._invoice_ids + self._invoice_ids_for_transactions()

    def main(self):
        if not self.fs.getvalue('generate'):
            return
        print_factory = print_invoice.Factory()
        print_factory.print_options.show_balance = self.show_balance
        print_factory.print_options.show_past_due_stamp = self.show_past_due_stamp
        invoice_factory = print_factory.invoice_factory(self.include_paid_transactions)
        minvoice_factory = print_factory.multiplied_invoice_factory(
            self.include_paid_transactions)
        client_factory = print_factory.client_factory
        writer = print_factory.writer()

        invoice_ids = self.all_requested_invoice_ids()
        if not invoice_ids:
            R.error('nothing to do.')
            return

        for invoice_id in invoice_ids:
            invoice = invoice_factory.for_invoice_id(invoice_id)
            client = client_factory.for_group_number(invoice.group_number)
            if client.print_nonmultiplier_invoice:
                writer.add_invoice(invoice)
            if client.print_multiplier_invoice:
                minvoice = minvoice_factory.for_invoice_id(invoice_id)
                writer.add_invoice(minvoice)

        self.mako_auto_publish = False 
        self._res.content_type = 'application/pdf'
        self._res.headers.add("Content-Disposition", "attachment;filename=%s.pdf"
            % invoice_ids[0])
        writer.write(self._res)

    @property
    def _invoice_ids(self):
        return self.fs.getlist('invoice_id')

    def _invoice_ids_for_transactions(self):
        """ Generate a PDF file for invoices with the given set of
        transactions. This procedure was written to provide invoice
        generation from the trans search page.
        """
        trans_ids = self.fs.getlist('trans_id')
        if not trans_ids:
            return []
        frag = ", ".join(map(P.qstr, trans_ids))
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT DISTINCT invoice_id FROM trans
            WHERE trans_id IN (%s)
            ORDER BY invoice_id
            """ % frag)
        return [invoice_id for invoice_id, in cursor]

application = Program.app
