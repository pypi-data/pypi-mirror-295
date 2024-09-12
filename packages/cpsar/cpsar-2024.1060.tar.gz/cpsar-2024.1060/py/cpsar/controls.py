import html
from lxml import etree

import cpsar.runtime as R
import cpsar.txtype as TT
import kcontrol

ListBox = kcontrol.ListBox
TextBox = kcontrol.TextBox
DatePicker = kcontrol.DatePicker
Hidden = kcontrol.Hidden
CheckBox = kcontrol.CheckBox
StateListBox = kcontrol.StateListBox
Currency = kcontrol.Currency

store = kcontrol.store

def update_store(vals):
    """ Update the form storage with the given values """
    kcontrol.store.update(vals)

def middleware(proc):
    """ middleware to use when controls are used. We have to
    clear out the thread local store state.
    """
    def wsgi_app(environ, start_response):
        try:
            return proc(environ, start_response)
        finally:
            kcontrol.store.clear()
    return wsgi_app


class ValueCheckBox(object):
    def __init__(self, name, field_value, caption=None):
        self._name = name
        self._html_id = "%s_%s" % (name, field_value)
        self._field_value = field_value
        self._caption = caption
        self._checked = None

    def _get_checked(self):
        if self._checked is None:
            self._assign_checked_by_store()
        return self._checked

    def _set_checked(self, value):
        self._checked = bool(value)

    checked = property(_get_checked, _set_checked)

    def _assign_checked_by_store(self):
        try:
            value = kcontrol.store[self._name]
        except KeyError:
            self._checked = False
            return

        if isinstance(value, list):
            self._checked = self._field_value in value
        else:
            self._checked = self._field_value == value

    def __str__(self):
        span = etree.Element('span')
        e = etree.Element('input',
            type='checkbox',
            name=self._name,
            value=self._field_value,
            id=self._html_id)
        if self.checked:
            e.attrib['checked'] = 'checked'
        span.append(e)
        if self._caption:
            label = etree.Element('label')
            label.attrib['for'] = self._html_id
            label.text = self._caption
            span.append(label)

        return etree.tostring(span).decode()


class ClientBillRuleTypeListBox(ListBox):
    values = [
        ('AP', 'AP - Factor of AWP'),
        ('CF', 'CF - Factor of EHO Cost Allowed'),
        ('GB', 'GB - AWP-16% + 20%'),
        ('GG', 'GG - AWP-65% + 20%')
        ]
    def __init__(self, name='rule_type', blankOption=False, *a, **k):
        super(ClientBillRuleTypeListBox, self).__init__(name, 
            blankOption=blankOption, *a, **k)
        self.values = ClientBillRuleTypeListBox.values
cbr_lookup = dict(ClientBillRuleTypeListBox.values)

def client_bill_rule_label(value):
    try:
        return cbr_lookup[value]
    except:
        return ''

class PharmacyFilterListBox(kcontrol.ListBox):
    def __init__(self, name='pharmacy_filter', blankOption=True, *a, **k):
        super(PharmacyFilterListBox, self).__init__(name, 
            blankOption=blankOption, *a, **k)
        self.values = [('M', 'Mail Order'), ('R', 'Retail'),
                       ('C', 'Mail Order Compound')]

class TxTypeSelectListBox(kcontrol.ListBox):
    """ A list box to select an available transaction type for a specific
    group.
    """
    def __init__(self, group_number, name='tx_type', *a, **k):
        super(TxTypeSelectListBox, self).__init__(name, *a, **k)
        for tt in TT.tx_types_for_group(group_number):
            self.values.append((tt, tt))

class SOJListBox(kcontrol.ListBox):
    def __init__(self, name, *a, **k):
        super(SOJListBox, self).__init__(name, *a, **k)
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT jurisdiction, state
            FROM soj
            ORDER BY jurisdiction
            """)
        for soj, state in cursor:
            self.values.append((soj, '%s-%s' % (soj, state)))

class RecentBatchesListbox(kcontrol.ListBox):
    def __init__(self, name, *a, **k):
        super(RecentBatchesListbox, self).__init__(name, *a, **k)
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT batch_file_id, batch_file_id || ' ' || file_name
            FROM batch_file
            order by batch_file_id DESC
            LIMIT 100
            """)
        for id, cap in cursor:
            self.values.append((str(id), cap))

class SavingsFormulaListBox(kcontrol.ListBox):
    """ The system supports these savings formulas to calculate the savings
    for a transaction.
    """
    def __init__(self, name='savings_formula', *a, **k):
        super(SavingsFormulaListBox, self).__init__(name, *a, **k)
        self.values = [('SFS', 'SFS'), ('AWP', 'AWP'), ('UC', 'U/C')]

class GroupNumberListBox(kcontrol.ListBox):
    """ A list box that contains all of the groups in the system. Additionally,
    the title attribute of each option is set to the client name to be used
    by javascript.
    """
    def __init__(self, name='group_number', *a, **k):
        super(GroupNumberListBox, self).__init__(name, *a, **k)
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT group_number, client_name,
                   group_number || ' ' || client_name
            FROM client
            ORDER BY group_number ASC
            """)
        self.values = list(cursor)

    def drawOptions(self):
        opts = []
        if self.blankOption:
            opts.append("<option value=''></option>")
        if not isinstance(self.value, list):
            values = [str(self.value)]
        else:
            values = [str(s) for s in self.value]

        for value, title, caption in self.values:
            opts.append('<option title="%s" value="%s" %s>%s</option>' % (
                html.escape(str(title), True),
                html.escape(str(value), True),
                value in values and "selected='selected'" or '',
                html.escape(str(caption))
            ))
        return '\n'.join(opts)

class DistributionAccountListBox(kcontrol.ListBox):
    def __init__(self, name, *a, **k):
        super(DistributionAccountListBox, self).__init__(name, *a, **k)
        self.values = [(c, c) for c in self._accounts()]

    def _accounts(self):
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT name
            FROM distribution_account
            ORDER BY name
            """)
        return [c for c, in cursor]

class GroupCodeListBox(kcontrol.ListBox):
    def buildValues(self):
        self.values = [
            ('COM', 'COM - COMMERCIAL'),
            ('CSH', 'CSH - CASH PATIENTS'),
            ('DCG', 'DCG - DISCOUNT/COUPON GROUP'),
            ('GF', 'GF - GUARANTY FUNDS'),
            ('GH', 'GH - GROUP HEALTH'),
            ('HOP', 'HOP - HOSPICE GROUP'),
            ('MLC', 'MLC - MEDICAL LIEN COMPANIES'),
            ('MSA', 'MSA - MEDICARE SET ASIDE'),
            ('SF', 'SF - SETTLEMENT FUNDS'),
            ('STATE', 'STATE - STATE AGENCIES'),
            ('TPA', 'TPA - THIRD PARTY ADMINISTRATORS')]

class ReportZoneListBox(kcontrol.ListBox):
    def buildValues(self):
        self.values = [
            ('',''), 
            ('CA', 'CA'), 
            ('MG', 'MG'), 
            ('TX', 'TX')]

