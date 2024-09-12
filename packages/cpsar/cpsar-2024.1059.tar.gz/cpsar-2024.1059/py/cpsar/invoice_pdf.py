#!/usr/bin/env python
from __future__ import division
from builtins import map
from builtins import range
from past.utils import old_div
from builtins import object
import collections
import copy
import datetime
import io
import itertools
import os
import re
import sys
import tempfile

from decimal import Decimal

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter, inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, \
    PageBreak, Paragraph, Spacer, KeepTogether, Image, Indenter

# Used to register a custom font
from reportlab.pdfbase.ttfonts import TTFont

import cpsar.runtime as R
import cpsar.sr.fl as F

from cpsar import config
from cpsar.pg import format_date, format_currency

## monkey patch reportlab because of errors on None in sum call
## Issue: 994
def __patch_reportlab():
    mod = sys.modules['reportlab.platypus.tables']
    orig = mod.spanFixDim
    from reportlab import rl_config
    def spanFixDim(V0,V,spanCons,lim=None,FUZZ=rl_config._FUZZ):
        while True:
            try: 
                V[V.index(None)] = 0
            except ValueError:
                break
        return orig(V0, V, spanCons, lim, FUZZ)
    mod.spanFixDim = spanFixDim
__patch_reportlab()

###############################################################################
## Public interface

class PDFWriter(object):
    """ Adapted to interface of the old PDFWriter in cpsar.print_invoice """
    use_group_separator = False
    canvas_maker = None

    def __init__(self, show_past_due=False):
        self._invoices = []
        self._pages = []
        self._last_group_number = None
        self._show_past_due = show_past_due
        self._setup_fixed_font()

    def add_invoice(self, invoice):
        self._maybe_add_group_separator(invoice)
        self._invoices.append(invoice)
        istory = invoice_page_elements(invoice)
        if self._show_past_due:
            istory.extend([
                Spacer(8*inch, inch),
                Paragraph("PAST DUE", GroupSepStyle)])
        self._pages.append(istory)

    def write(self, fd):
        tf = tempfile.NamedTemporaryFile(mode='wb')
        doc = _invoice_doc_template(tf.name)
        doc.build(self._story(), canvasmaker=self._canvas_for_invoices())
        tf.flush()
        t2 = open(tf.name, mode='rb')
        fd.write(t2.read(-1))
        t2.close()
        tf.close()

    def tobytes(self):
        buf = io.BytesIO()
        self.write(buf)
        return buf.getvalue()

    def _canvas_for_invoices(self):
        if self.canvas_maker is not None:
            return self.canvas_maker
        else:
            return _canvas_for_invoices(self._invoices)

    def _setup_fixed_font(self):
        """ We have our own custom Fixed font in the data dir """
        pdfmetrics.registerFont(TTFont('Fixed', config.font_path('Courier Prime Sans.ttf')))
        pdfmetrics.registerFont(TTFont('FixedBd', config.font_path('Courier Prime Sans Bold.ttf')))
        pdfmetrics.registerFont(TTFont('FixedIt', config.font_path('Courier Prime Sans Italic.ttf')))
        pdfmetrics.registerFont(TTFont('FixedBI', config.font_path('Courier Prime Sans Bold Italic.ttf')))
        pdfmetrics.registerFontFamily('Fixed', normal='Fixed', bold='FixedBd', italic='FixedIt', boldItalic='FixedBI')

    def _story(self):
        # http://stackoverflow.com/questions/952914
        pages = self._pages_with_pagebreaks()
        #return [item for sublist in pages for item in sublist]
        return list(itertools.chain(*pages))

    def _pages_with_pagebreaks(self):
        # http://stackoverflow.com/questions/5920643
        result = [[PageBreak()]] * (len(self._pages) * 2 - 1)
        result[0::2] = self._pages
        return result

    def _maybe_add_group_separator(self, invoice):
        if not self.use_group_separator:
            return
        if invoice.group_number == self._last_group_number:
            return
        self._pages.append(_group_separator(invoice.group_number))
        self._last_group_number = invoice.group_number

###############################################################################
## Implementation

def _canvas_for_invoices(invoices):
    if not invoices:
        return canvas.Canvas
    pl = invoices[0].client.invoice_class
    pl_lookup = {
        'mjoseph': MJosephCanvas,
        'sunrise': SunriseCanvas,
        's1': S1Canvas,
        'msq': MSQCanvas
    }
    return pl_lookup.get(pl, canvas.Canvas)

class MSQCanvas(canvas.Canvas):
    def showPage(self):
        self.drawInlineImage(config.inv_base('images/msq.tif'),
                181, letter[1] - 1.2*inch ,
               300, 62)
        canvas.Canvas.showPage(self)

class S1Canvas(canvas.Canvas):
    def showPage(self):
        self.drawInlineImage(config.inv_base('images/s1.tif'),
                0.5*inch, letter[1] - 1.2*inch, 164, 60)
        canvas.Canvas.showPage(self)

class MJosephCanvas(canvas.Canvas):
    def showPage(self):
        t = self.beginText()
        t.setFont("Helvetica", 9)
        drawCenteredText(t, "* Definition and disclaimer regarding AWP: http://www.wolterskluwercdi.com/pricing-policy-update/",
            4.25*inch, .8*inch)
        self.drawText(t)

        t = self.beginText()
        t.setFont("Helvetica", 10)

        drawCenteredText(t, 'P.O. Box 436559 Louisville, KY 40253', 1.9*inch, .4*inch)
        drawCenteredText(t, '(844) 363-2637', 4.25*inch, .4*inch)
        drawCenteredText(t, 'www.mjosephmedical.com', 6.3*inch, .4*inch)
        t.setFont("ZapfDingbats", 11)

        t.setFillColorRGB(36/255.0, 97/255.0, 48/255.0)
        drawCenteredText(t, "\x6F", 3.45*inch, .4*inch)
        drawCenteredText(t, "\x6F", 5.1*inch, .4*inch)
        self.drawText(t)
        self.drawInlineImage(config.inv_base('images/mjoseph_logo.png'),
                181, letter[1] - 1.2*inch ,
                3.458*inch, 0.819*inch)

        canvas.Canvas.showPage(self)

class SunriseCanvas(canvas.Canvas):
    def showPage(self):
        self.drawInlineImage(config.inv_base('images/sunrise_logo_white.png'),
                10, letter[1] - 1.5*inch, 3*1.193*inch, 3*0.4*inch)

        canvas.Canvas.showPage(self)

def drawCenteredText(textobj, text, x, y):
    width = pdfmetrics.stringWidth(text, textobj._fontname, textobj._fontsize)
    textobj.setTextOrigin(x-old_div(width,2), y)
    textobj.textLine(text)

def _invoice_doc_template(fpath):
    return SimpleDocTemplate(fpath,
        pagesize=letter,
        leftMargin=.25*inch,
        rightMargin=.25*inch,
        topMargin=0*inch,
        bottomMargin=inch)

def group_invoice_items_on_pages(items):
    """ Given a list of items, produce a list of lists of the items. This used to be
    a fixed 6, but since compounds can be so big we count them as their own page.

    The old implementation was:
        items = [items[i:i+num_pp] for i in range(0, len(items), num_pp)]
    MJ Issue 387
    """
    sized_items = [(i, 3 if i.compound_code == '2' else 1) for i in items]
    ilist = []
    current, current_size = [], 0
    for item, size in sized_items:
        new_size = current_size + size
        if new_size > 6:
            ilist.append(current)
            current, current_size = [item], size
        else:
            current.append(item)
            current_size = new_size
    if current:
        ilist.append(current)
    return ilist

def invoice_page_elements(invoice):
    """ All the flowables for the given invoice used to build the document
    """
    items = invoice.items
    # number of invoice items to show on each page of the invoice
    num_pp = 6
    items = group_invoice_items_on_pages(items)

    flows = []
    for pitems in items[:-1]:
        pinvoice = copy.deepcopy(invoice)
        pinvoice._items = pitems
        flows.extend([
            _logo_block(pinvoice),
            _header(pinvoice),
            HorizontalRule(),
            _info_table(pinvoice),
            _item_table(pinvoice),
            Spacer(1, .33*inch)
            ])
        flows.extend(_invoice_memo_flowable(pinvoice))
        flows.extend([
            _footer(pinvoice),
            Spacer(1, .33*inch)
            ])
        if len(items) > 1:
            flows.append(PageBreak())

    pinvoice = copy.deepcopy(invoice)
    if items:
        pinvoice._items = items[-1]
        flows.extend([
            _logo_block(pinvoice),
            _header(pinvoice),
            HorizontalRule(),
            _info_table(pinvoice),
            _item_table(pinvoice),
            _total_table(invoice),
            Spacer(1, .33*inch)
            ])
        flows.extend(_invoice_memo_flowable(pinvoice))
        flows.extend([
            _footer(pinvoice),
            Spacer(1, .33*inch)
            ])

    return flows

###############################################################################
## Configuration 

def _invoice_memo_flowable(invoice):
    flows = []
    settings = [
       ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
       ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
       ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
       ('BOX', (0, 0), (-1, -1), 0.5, colors.black)]

    if invoice.memo:
        flows.append(Table([[invoice.memo]], None, None, settings))

    reversal_text = "The above marked claim has been reversed. This invoice " \
                    "is to serve as notice only for reporting purposes that " \
                    "the marked claim has been reversed. Do not process for payment."

    reversal_para = Paragraph(reversal_text, HeaderStyle)

    if has_reversal(invoice):
        flows.append(reversal_para)
        # Table([[reversal_para]], None, None, settings))
    return flows

def _show_processing_fee(group_number):
    # Only protocols MSQ group shows the processing fee
    if group_number == '77701':
        return True
    else:
        return False

def _show_state_reporting_item_detail(group_number):
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM client_report_code
        WHERE group_number=%s AND report_code = 'CRS'
        """, (group_number,))
    return cursor.fetchone()[0] > 0 or group_number in (
        '54010', '70846')

def _group_separator(group_number):
    return [
        Paragraph("GROUP: %s" % group_number, GroupSepStyle),
        HorizontalRule(), 
        HorizontalRule()
    ]

###############################################################################
## Header
def _logo_block(invoice):
    """ Most groups are printed on CPS letter head with a preprinted invoice but
    a few have rendered logos like MSQ """
    if invoice.group_number == '77701':
        # I could not figure out how to align the image. Instead of dropping down to
        # frames and canvas, I just use a table.
        img = Image(config.inv_base('images/msq_logo_small.jpg'), 4.29984252*inch, 0.88881888*inch)
        # Make table 1.5 inch tall and since element is bottom aligned, the difference is
        # the top margin.  there will be .25 below
        t = Table([[img]], None, [1.25*inch], [
            ('BOTTOMPADDING', (0, 0), (0, 0), .25*inch)
        ])
        t.hAlign = 'LEFT'
        return t
    elif invoice.group_number == '70084':
        left = Image(config.inv_base('images/cps_lh_top_left.gif'))
        right = Image(config.inv_base('images/cps_lh_top_right.gif'))
        return Table([[left, right]], [4*inch, 4*inch], [1.3*inch], [
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), .2*inch)
        ])
    else:
        return Spacer(8.5*inch, 1.5*inch)

def _header(invoice):
    if invoice.client.use_invoice_color:
        s = "<b><font textColor='red'>Invoice #%s</font></b> - Date: %s (Please include invoice # in remittance)"
    else:
        s = "<b>Invoice #%s</b> - Date: %s (Please include invoice # in remittance)"

    s = s % (invoice.invoice_id, format_date(invoice.batch_date))
    h1 = Paragraph(s, HeaderStyle)

    if invoice.group_number != '70076':
        return h1

    # LAIGA shows the short codes and the total off to the right for some reason

    t2 = Table([
      ['CLAIM:', invoice.short_codes],
      ['TOTAL:', format_currency(invoice.total)]
    ], [0.5*inch, 0.5*inch])
    t2.setStyle(TableStyle([
        ('FONT',         (0, 0), (0, 1), 'Helvetica-Bold'),
        ('LEFTPADDING', (0, 0), (0, 1), -5)
    ]))
    o = Table([[h1, t2]])
    o.setStyle(TableStyle([
        ('ALIGN', (1, 0), (1, 0), 'RIGHT')
    ]))
    return o

    s = "<b>CLAIM: </b>%s<br/> <b>TOTAL: </b>%s" % (
        invoice.short_codes,
        format_currency(invoice.total))
    h2 = Paragraph(s, RightHeaderStyle)
    return Table([[h1, h2]])


###############################################################################
## Info Table
def _info_table(invoice):
    client = invoice.client

    def client_mailing_address():
        if invoice.billing_city and invoice.billing_state:
            bcl = "%s, %s %s" % (
                invoice.billing_city,
                invoice.billing_state,
                invoice.billing_zip_code)
        else:
            bcl = ""

        frags = [
            invoice.billing_name,
            invoice.billing_address_1,
            invoice.billing_address_2,
            bcl]

        return Paragraph("<br/>".join(frags), NormalStyle)

    def patient_name():
         n = "%s %s" % (invoice.patient_first_name, invoice.patient_last_name)
         return Paragraph(n, NormalStyle)
    
    if client.use_invoice_color:
        class phone_style(NormalStyle):
            textColor = 'green'
    else:
        phone_style = NormalStyle

    data = [
        "CLIENT:", client_mailing_address(), 
        "REMIT TO:", client.biller_mailing_address,
        "PATIENT:", patient_name(),
         "BILLER PHONE:", Paragraph(client.biller_phone, phone_style),
        "PATIENT ID:", invoice.patient_ssn]
    if client.biller_phone_2:
        data.extend(["", Paragraph(client.biller_phone_2, phone_style)])
    data.extend(client.biller_tax_id_row)
    if invoice.doi_row:
        data.extend(invoice.doi_row)
    # http://stackoverflow.com/questions/9671224/split-a-python-list-into-other-sublists-i-e-smaller-lists
    data = [data[x:x+4] for x in range(0, len(data), 4)]

    widths = [0.5*inch, 2.5*inch, 1.0*inch, 2.5*inch]
    t = Table(data, widths)
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 6),
        ('FONT', (0, 0), (-1, -1), 'Helvetica'),
        ('SIZE', (0, 0), (-1, -1), 10),
        ('FONT', (0, 0), (0, 0), 'Helvetica-Bold'),
        ('FONT', (2, 0), (2, 0), 'Helvetica-Bold'),
    ]))
    return t

###############################################################################
## Invoice Item (trans) table
def _item_table(invoice):
    t = Table(_item_table_data(invoice),
              _item_table_col_widths(invoice),
              style=_item_table_style(invoice))
    t.hAlign = 'RIGHT'
    #t.keepWithNext = True
    return t

def _item_table_col_widths(invoice):
    return [c.width for c in _item_cols(invoice)]

def _item_table_data(invoice):
    """ Return A list of lists of Flowables which are the tabular data for each
    line item of an invoice.  """
    client = invoice.client
    rows = []
    cols = _item_cols(invoice)
    rows.append([c.header for c in cols])
    for item in invoice.items:
        rows.append([c.row_func(item) for c in cols])
        # We have to append blank cells that the SPAN will cover
        # as per doc. not like HTML.
        dtl_row = [_item_detail_data(invoice, item)]
        if item.paid_amount:
            empty_rows = len(cols) - 3
        else:
            empty_rows = len(cols) - 1
        dtl_row.extend(['']*empty_rows)
        if item.paid_amount:
            dtl_row.extend(_item_paid_data(item))
        rows.append(dtl_row)
    return rows

def _item_paid_data(item):
    fc = format_currency
    cell2 = "-%s" % fc(item.paid_amount)
    return [
        Paragraph(item.payment_label, RightCellStyle),
        Paragraph(cell2, RightCellStyle)]

def _item_detail_data(invoice, item):
    """ Return a list of Flowables which are the cell contents of the 2nd row
    of each item detail.
    """
    client = invoice.client
    def ingredients():
        fc = format_currency
        tdata = [[
            "",
            "Ingredient",
            "NDC",
            "QTY",
            "AWP",
            "PRICE"
        ]]
        for i in item.ingredients_to_show_on_invoice:
            if i.on_formulary:
              row = ["*"]
            else:
              row = [" "]
            row.extend([
              i.drug_name,
              i.ndc_number,
              i.qty])
            if invoice.show_cmpd_cost_on_invoice:
                row.extend([fc(i.awp), fc(i.cost)])
            else:
                row.extend([""] * 4)
            tdata.append(row)
        widths = [10, 2*inch, inch, _cur_width, _cur_width, _cur_width]
        t = Table(tdata, widths, style=[
            ('FONT', (0, 1), (-1, -1), 'Fixed'),
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            #('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('ALIGN', (-1, 0), (-1, -1), 'RIGHT'),
            ('ALIGN', (-3, 0), (-3, -1), 'RIGHT'),
            ('ALIGN', (4, 0), (4, -1), 'RIGHT'),
            ('LINEABOVE', (0, 1), (-1, -1), 0.5, colors.black),
            ('LEFTPADDING', (0, 0), (-1, -1), 2),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('SIZE', (0, 0), (-1, -1), 8)])
        return t

    def info():
        dtls = []
        a = lambda s, *v: dtls.append(s % v)

        a("<b>TX:</b>")
        a(str(item.trans_id))
        if item.brand_or_generic == 'B':
            a("<b>BRAND</b>")
        else:
            a("<b>GENERIC</b>")
            if item.brand_drug_name:
                a("(BRAND EQ: %s)", item.brand_drug_name)

        a("<b>RX:</b>%s-%s", item.rx_number, item.refill_number)
        a("<b>DAW:</b>%s", item.daw)

        adjs = [item.adjuster1_name, item.adjuster2_name]
        adjs = [_f for _f in adjs if _f]
        if adjs:
            a("<b>ADJUSTERS:</b> %s", " ".join(adjs))

        a("<p><b>PHARMACY:</b>%s <b>NABP:</b> %s <b>NPI:</b> %s",
                item.pharmacy_name,
                item.pharmacy_nabp,
                item.pharmacy_npi)
        if client.show_pharmacy_tax_id_on_invoice:
            a("<b>Tax ID:</b> %s", item.pharmacy_tax_id)
        if client.show_pharmacy_cost_on_invoice:
            a("<b>Cost:</b> %s", item.pharmacy_cost_submitted)
        if client.show_gpi_code_on_invoice:
            a("<b>GPI:</b> %s", item.drug_gpi_code)

        if _show_state_reporting_item_detail(invoice.group_number):
            paddr = [
                "A:", 
                item.pharmacy_address_1,
                item.pharmacy_address_2,
                item.pharmacy_city,
                item.pharmacy_state,
                item.pharmacy_zip]
            paddr = [_f for _f in paddr if _f]
            a(" ".join(paddr))

            if item.pharmacist_license_number:
                pharmacist_fields = [
                    item.pharmacist_license_number,
                    item.pharmacist_first_name,
                    item.pharmacist_middle_initial,
                    item.pharmacist_last_name
                ]
                pharmacist_fields = [_f for _f in pharmacist_fields if _f]
                pharmacist_str = " ".join(pharmacist_fields)
                a("<b>PHARMACIST:</b>%s", pharmacist_str)

        a("<b>DOCTOR:</b> %s", item.doctor_name)
        if item.doctor_dea_number:
            a("<b>DEA:</b> %s", item.doctor_dea_number)
        if item.doctor_npi_number:
            a("<b>NPI:</b> %s", item.doctor_npi_number)
        if item.doctor_license_number:
            a("<b>LIC:</b> %s" % item.doctor_license_number)

        return Paragraph(" ".join(dtls), CellStyle)

    paras = []
    paras.append(info())
    if item.ingredients:
        paras.append(ingredients())
    return paras

def _item_table_style(invoice):
    settings = [
       ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
       ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
       ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
       ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
       ('LINEABOVE', (0, 1), (-1, 1), 0.5, colors.black),
       ('LEFTPADDING', (0, 0), (-1, -1), 2),
       ('RIGHTPADDING', (0, 0), (-1, -1), 2),
    ]

    # Add span's for detail rows. We have to go to the end or third from
    # last depending on if there is payment data to show
    for i, item in enumerate(invoice.items):
        row_idx = 2 + (i*2)
        if item.paid_amount:
            end_y = -3
        else:
            end_y = -1
        settings.append(('SPAN', (0, row_idx), (end_y, row_idx)))
        settings.append(('LEFTPADDING', (0, row_idx), (0, row_idx), .25*inch))
    return TableStyle(settings)

# All the currency fields have the same size
_cur_width = 0.72 * inch

def _item_cols(invoice):
    """ Returns back a list of Column namedtuples with header, width and
    data source values. The header is the value to be displayed in the table
    header row. width is the size to make the column in the table and
    row_func is a function that will provide the value to put in the table
    when given a single invoice item. The number of columns varies depending
    on which client the invoice is for and other factors. 
    
    This is implemented this way so we can have a centralized place in the code
    where all the logic of which columns to display is located.
    """
    Column = collections.namedtuple("Column", ["header", "width", "row_func"])

    # Column Header Functions
    def left(caption):
        return Paragraph(caption, DataLabelStyle)

    def right(caption):
        return Paragraph(caption, RightDataLabelStyle)

    # Column Row Value Function factories
    def number(attr_name, fmt="%d"):
        def getter(item):
            ptext = fmt % getattr(item, attr_name)
            return Paragraph(ptext, RightCellStyle)
        return getter

    def text(attr_name):
        def getter(item):
            ptext = getattr(item, attr_name)
            if not ptext:
                return ''
            ptext = re.sub('\s+', ' ', ptext)
            return Paragraph(ptext, CellStyle)
        return getter

    def date(attr_name):
        return lambda i: Paragraph(format_date(getattr(i, attr_name)), CellStyle)

    def currency(attr_name):
        def getter(item):
            ptext = format_currency(getattr(item, attr_name))
            return Paragraph(ptext, RightCellStyle)
        return getter

    def drug(item):
        ptext = "%s: %s" % (p, item.drug_name)
        ptext = re.sub('\s+', ' ', ptext)
        return Paragraph(ptext, CellStyle)

    client = invoice.client

    def reversal(item):
        if getattr(item, 'reversed', False):
            return Paragraph("Y", CellStyle)
        else:
            return Paragraph("", CellStyle)

    # Column definitions
    if has_reversal(invoice):
        cols = [ Column(left("Reversed"), 1.00*inch, reversal) ]
    else:
        cols = []
    cols.extend([
        Column(left("#"), 0.15*inch, number("line_no")),
        Column(left("NDC #"), 0.80*inch, text("drug_ndc_number")),
        Column(left("DRUG"), None , text("drug_name")),
        Column(left("RX DATE"), 0.75*inch, date("rx_date"))])
    if client.show_claim_number_column:
        cols.append(Column(left("CLAIM #"), None, text("claim_number")))
    cols.extend([
        Column(right("QTY"), 0.5*inch, number("quantity", "%.03f")),
        Column(right("DAYS"), 0.4*inch, number("days_supply")),
        Column(right("AMOUNT"), _cur_width, currency("amount"))])

    # Optional columns depending on client configuration
    if _show_processing_fee(client.group_number):
        cols.append(Column(right("P/F"), _cur_width, currency("processing_fee")))
    if client.show_sfs_on_invoice:
        if invoice.client.invoice_class == 'mjoseph':
            cols.append(Column(right("*FEE SCH"), _cur_width, currency("state_fee")))
        else:
            cols.append(Column(right("FEE SCH"), _cur_width, currency("state_fee")))

    if client.show_awp_on_invoice:
        cols.append(Column(right("AWP"), _cur_width, currency("awp")))
    if client.show_uc_on_invoice:
        cols.append(Column(right("U/C"), _cur_width, currency("usual_customary")))
    if client.show_savings_on_invoice:
        cols.append(Column(right("SAVINGS"), _cur_width, currency("savings")))
    
    cols.append(Column(right("ADJ"), _cur_width, currency("adj_total")))
    return cols

###############################################################################
## Total Table
def _total_table(invoice):
    if not invoice.internal_control_number:
        return _item_total_table(invoice)

    #widths = [2.25*inch, .65*2*inch, _cur_width]
    style = TableStyle([
        ('VALIGN', (1, 0), (1, 0), 'TOP'),
        ('VALIGN', (0, 0), (0, 0), 'BOTTOM'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('SIZE', (0, 0), (-1, -1), 9)
    ])
    icn = Paragraph(invoice.internal_control_number, ICNStyle)
    t = Table([[icn, _item_total_table(invoice)]], style=style)
    #t.hAlign = 'RIGHT'
    return t

def _item_total_table(invoice):
    client = invoice.client

    def lval(v): return Paragraph(v, RightDataLabelStyle)
    def cval(v): return Paragraph(format_currency(v), TotalCellStyle)

    def data():
        rows = [
         [lval("PRESCRIPTIONS PROCESSED: %s" % invoice.item_count),
          lval("INVOICE TOTAL"),
          cval(invoice.total)]]

        if _show_processing_fee(invoice.group_number):
            rows.append(["",
                lval("PROCESSING FEE TOTAL"), 
                cval(invoice.processing_fee_total)])

        if client.show_awp_on_invoice:
            rows.append(["", lval("AWP TOTAL"), cval(invoice.awp_total)])
        if client.show_sfs_on_invoice:
            rows.append(["", lval("FEE SCH TOTAL"), cval(invoice.state_fee_total)])

        if client.use_invoice_color:
            AmountDueLabelStyle.textColor = 'red'
            AmountDueValueStyle.textColor = 'red'
        else:
            AmountDueLabelStyle.textColor = 'black'
            AmountDueValueStyle.textColor = 'black'

        ad = Paragraph(format_currency(invoice.balance), AmountDueValueStyle)

        if client.show_adjusted_total:
            rows.append(["", lval("ADJUSTED TOTAL"), cval(invoice.adj_total)])

        rows.extend([
            ["", lval("PAYMENT"), cval(invoice.paid_amount)],
            ["", Paragraph("AMOUNT DUE", AmountDueLabelStyle), ad]])
        return rows

    style = TableStyle([
        ('SPAN', (0, 0), (0, -1)),
        ('VALIGN', (0, 0), (0, 0), 'TOP'),
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
        ('SIZE', (0, 0), (-1, -1), 9),
        ('FONT', (0, -1), (-1, -1), 'Helvetica-Bold'),
    ])

    widths = [2.25*inch, .65*2*inch, _cur_width*2]
    t = Table(data(), widths, style=style)
    t.hAlign = 'RIGHT'
    return t


###############################################################################
## Footer 
def _footer(invoice):
    flows = []
    msg = "<b>*Pre-negotiated*</b> DO NOT SEND FOR RE-PRICING"
    if invoice.client.use_invoice_color:
        para = Paragraph(msg, RePriceStyle)
    else:
        para = Paragraph(msg, NormalStyle)
    flows.append(para)

    if invoice.show_due_date_on_invoice:
        idate = format_date(invoice.due_date)
        msg = "<b>**** Please remit payment on or before %s ****</b>" % idate
        para = Paragraph(msg, NormalStyle)
        para.hAlign = 'RIGHT'
        flows.append(para)

    widths = [4.25*inch, 3.75*inch]
    return Table([flows], widths)

def _compound_disclaimer():
    para = Paragraph("Compounds may have more ingredients than listed<br/>"
        "Ingredients marked with an * are on the formulary", 
                     CompoundDisclaimerStyle)
    para.hAlign = "CENTER"
    return para

###############################################################################
### Styling

class HeaderStyle(ParagraphStyle):
    alignment = 0
    allowOrphans = 0
    allowWidows = 1
    backColor = None
    borderColor = None
    borderPadding = 0
    borderRadius = None
    borderWidth = 0
    endDots=None
    firstLineIndent = 0
    fontName = 'Helvetica'
    fontSize = 10
    justifyBreaks = 0
    justifyLastLine = 0
    leading = 10
    leftIndent = 0
    rightIndent = 0
    spaceAfter = 6
    spaceBefore = 0
    spaceShrinkage = 0.05
    splitLongWords=1
    textTransform = None
    textColor = colors.black
    underlineProportion = 0
    wordWrap = None

class InvoiceHeaderStyle(HeaderStyle):
    textColor = "green"

class GroupSepStyle(HeaderStyle):
    fontSize = 20
    leading = 27
    alignment = TA_CENTER

class RightHeaderStyle(HeaderStyle):
    alignment = TA_RIGHT


class DataLabelStyle(ParagraphStyle):
    alignment = 0
    allowOrphans = 0
    allowWidows = 1
    backColor = None
    borderColor = None
    borderPadding = 0
    borderRadius = None
    borderWidth = 0
    endDots=None
    firstLineIndent = 0
    fontName = 'Helvetica-Bold'
    fontSize = 8
    leading = 9
    justifyBreaks = 0
    justifyLastLine = 0
    leftIndent = 0
    rightIndent = 0
    spaceAfter = 0
    spaceBefore = 0
    spaceShrinkage = 0.05
    splitLongWords=1
    textTransform = None
    textColor = colors.black
    underlineProportion = 0
    wordWrap = None

class RightDataLabelStyle(DataLabelStyle):
    alignment = TA_RIGHT

class ICNStyle(DataLabelStyle):
    fontSize = 9
    fontName = 'Helvetica'

class CellStyle(ParagraphStyle):
    alignment = 0
    allowOrphans = 0
    allowWidows = 1
    backColor = None
    borderColor = None
    borderPadding = 0
    borderRadius = None
    borderWidth = 0
    firstLineIndent = 0
    #fontName = 'Fixed'
    fontName = "Fixed"
    defaults = {
        'fontName': "Times-Roman"
    }
    endDots=None
    fontSize = 7
    justifyBreaks = 0
    justifyLastLine = 0
    leading = 9
    leftIndent = 0
    rightIndent = 0
    spaceAfter = 0
    spaceBefore = 0
    spaceShrinkage = 0.05
    splitLongWords=1
    textTransform = None
    textColor = colors.black
    underlineProportion = 0
    wordWrap = None

class RightCellStyle(CellStyle):
    alignment = TA_RIGHT

class TotalCellStyle(CellStyle):
    alignment = TA_RIGHT
    fontSize = 9

class NormalStyle(ParagraphStyle):
    alignment = 0
    allowOrphans = 0
    allowWidows = 1
    backColor = None
    borderColor = None
    borderPadding = 0
    borderRadius = None
    borderWidth = 0
    bulletFontName = 'Helvetica'
    bulletFontSize = 10
    bulletIndent = 0
    endDots=None
    firstLineIndent = 0
    fontName = 'Helvetica'
    fontSize = 10
    justifyBreaks = 0
    justifyLastLine = 0
    leading = 12
    leftIndent = 0
    rightIndent = 0
    spaceAfter = 0
    spaceBefore = 0
    spaceShrinkage = 0.05
    splitLongWords=1
    textColor = colors.black
    textTransform = None
    underlineProportion = 0
    wordWrap = None

class RePriceStyle(NormalStyle):
    fontSize = 12
    textColor = "red"

class CompoundDisclaimerStyle(NormalStyle):
    alignment = TA_CENTER
    borderColor= colors.black
    borderWidth = 0.5
    borderPadding = 0.1*inch

class AmountDueLabelStyle(DataLabelStyle):
    textColor = 'red'
    alignment = TA_RIGHT

class AmountDueValueStyle(CellStyle):
    textColor = 'red'
    alignment = TA_RIGHT
    fontSize = 9

class HorizontalRule(Spacer):
    """ No idea why reportlab doesnt have a HR flowable """
    def __init__(self, height=.25*inch, strokewidth=1):
        Spacer.__init__(self, 8*inch, height)
        self.strokewidth = strokewidth

    def draw(self):
        canvas = self.canv
        canvas.setLineWidth(self.strokewidth)
        canvas.setStrokeColor(colors.black)
        canvas.line(0, self._line_y, self.width, self._line_y)

    @property
    def _line_y(self):
        return self.height - self.strokewidth

def has_reversal(invoice):
    for i in invoice.items:
        if getattr(i, 'reversed', False):
            return True
    return False

###############################################################################
## Testing
def write_invoice_pdf(invoice, fpath):
    doc = _invoice_doc_template(fpath)
    doc.build(invoice_page_elements(invoice))

def write_print_batch(batch_date, fpath=None):
    """ Write out the batch file for the given batch date. If no fpath is given, then
    it is automatically calculated in the dpath
    """
    import cpsar.print_invoice as I
    if fpath is None:
        path_frag = 'invoice/print/invoice-batch-%s.pdf' % batch_date.strftime('%Y%m%d')
        fpath = R.dpath(path_frag)

    # Go ahead and open it to be sure we can before wasting our time
    fd = open(fpath, 'wb')

    clients = I.ClientFactory()
    templates = I.TemplateFactory()

    items = I.LineItemFactory(clients, include_paid_transactions=False)
    invoices = I.InvoiceFactory(clients, items)

    mitems = I.MultipliedLineItemFactory(clients, include_paid_transactions=False)
    minvoices = I.InvoiceFactory(clients, mitems)

    writer = PDFWriter(show_past_due=True)
    writer.use_group_separator = True

    for client in clients.all_with_invoices_on(batch_date):
        if client.invoice_processor_code != 'PRINT':
            continue
        for invoice in invoices.unpaid_for_client_on(client, batch_date):
            if invoice.balance == 0:
                continue
            if client.print_nonmultiplier_invoice:
                writer.add_invoice(invoice)
            if client.print_multiplier_invoice:
                mul_invoice = minvoices.for_invoice_id(invoice.invoice_id)
                writer.add_invoice(mul_invoice)
    
    writer.write(fd)
    fd.close()

def test_write_invoice_file():
    import cpsar.print_invoice as I
    factory = I.Factory()

    invoice_ids = [
        480083,             # Has previous payments
        430699,             # Long client name
        483037, 483036,     # Shows AWP on Invoice and has big values
        483559,             # MSQ protocols invoice that shows processing fees - msq.tmpl
        483517,             # LAIGA
        480744,             # BREC uses cps-lh shows letter head on invoice
        483032,             # Companion with state reporting detail. but can't
                            # find real tx with pharm provider
        481351              # has compound ingredients
    ]

    invoice_ids = [698807]
    invoicef = factory.invoice_factory()
    invoices = list(map(invoicef.for_invoice_id, invoice_ids))
    #invoices = invoicef.unpaid_internet_invoices()

    for invoice in invoices:
        writer = PDFWriter()
        writer.add_invoice(invoice)
        fpath = "/home/jeremy/data/invoice/%s.pdf" % invoice.invoice_id
        with open(fpath, 'wb') as fd:
            writer.write(fd)

def test_write_batch():
    # Large batch
    write_print_batch('2013-02-28', '/home/jeremy/data/invoice/2013-02-28.pdf')

def test_layout():
    """ Create an invoice with maxed out lengths of all the fields to test the
    layout """
    writer = PDFWriter()
    writer.add_invoice(MockInvoice())
    fpath = "/home/jeremy/data/invoice/test.pdf"
    with open(fpath, 'wb') as fd:
        writer.write(fd)

class MockInvoice(object):
    class MockClient(object):
        use_invoice_color = False
        billing_name = 'Z'*30
        group_number = 'XXXXX'
        address_1 = 'D'*30
        address_2 = 'D'*30
        city = 'C'*20
        state = 'XX'
        zip_code = 'X'*10
        biller_mailing_address = ("CORPORATE PHARMACY SERVICES, INC.\n"
                                "P.O. BOX 1950\n"
                                "GADSDEN, AL 35902")

        biller_tax_id_row = ["TAX ID:", "63-1040950"]
        biller_phone = "(256) 543-9000"
        biller_phone_2 = ""
        show_adjusted_total = True
        invoice_class = None
        show_sfs_on_invoice = True
        show_awp_on_invoice = True
        show_uc_on_invoice = False
        show_savings_on_invoice = True

    invoice_id = 99999999
    batch_date = datetime.date(2015, 12, 31)
    group_number = 'XXXXX'
    client = MockClient()
    patient_first_name = 'PATIEN FNAME'
    patient_last_name = 'PATIENT LA NAME'
    patient_ssn = 'X'*11
    claim_numbers = 'D'*30

    internal_control_number = None
    doi_row = None

    class MockItem(object):
        line_no = 99
        drug_ndc_number = '8'*11
        drug_name = 'D'*30
        rx_date = datetime.date(2015, 12, 31)
        claim_number = 'Z'*30
        quantity = Decimal("9999.999")
        days_supply = 999
        amount = Decimal("99999.99")
        state_fee = Decimal("99999.99")
        awp = Decimal("99999.99")
        savings = Decimal("9999.99")
        total = Decimal('99999.99')
        adj_total = Decimal('99999.99')
        ingredients = []
        brand_or_generic = 'B'
        rx_number = '9'*7
        refill_number = '99'
        daw = '9'
        adjuster1_name = 'XXXXXXXX XXXXXXXXXX'
        adjuster2_name = 'XXXXXXXX XXXXXXXXXX'
        pharmacy_name = 'X'*40
        pharmacy_nabp = '9'*7
        doctor_name = 'X'*60
        paid_amount = Decimal("99999.99")
        doctor_dea_number = '9'*10
        payment_label = "PAYMENT"

    
    item_count = 1
    total = Decimal("99999.99")
    awp_total = Decimal("99999.99")
    state_fee_total = Decimal("99999.99")
    balance = Decimal("99999.99")
    adj_total = Decimal("99999.99")
    paid_amount = Decimal("99999.99")
    due_date = datetime.date(2015, 12, 31)

    items = [MockItem()]
    memo = 'X'*60



def main():
    R.db.setup()
#    test_write_invoice_file()
    test_layout()
#    test_write_batch()

if __name__ == '__main__':
    main()
