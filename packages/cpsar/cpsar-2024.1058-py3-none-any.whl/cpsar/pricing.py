""" The master pricing library. This has been extracted from ar-sync-trans and
its dependencies to create a stand alone pricing module that can be used 
outside of the context of doing actual billing.

Object Dependency Tree
Transaction---------+
 |   |              |
 |   +              |
 | Prescription     |
 |  |       |       |
 +  +       +       +
Client Pharmacy  PBMHistory


Usage
====

The easiest usage is to compose a Transaction object using a dictionary of
values. The needed keys are given below:

group_number -> str
brand -> {'B', 'G'}
compound_code -> {1, 2}
awp -> Decimal
state_fee -> Decimal
nabp -> str
cost_allowed
dispense_fee
processing_fee
sales_tax
eho_network_copay


"""
import itertools
import json
import os
import sys
import warnings

from decimal import Decimal, ROUND_HALF_UP

import cpsar.runtime as R
from cpsar.util import imemoize, memoize

LOSE_MONEY_GROUPS = ['70765', '70768']

def transaction_for_trans_id(trans_id, trans=None):
    cursor = R.db.dict_cursor()
    cursor.execute("""
        select dispense_fee, processing_fee, cost_allowed, total, group_number,
            pharmacy_nabp, drug.brand, drug.ndc_number, history_id, state_fee,
            compound_code, awp
        from trans
        join drug using(drug_id)
        where trans_id=%s
        """, (trans_id,))
    assert cursor.rowcount, "Trans %s not found" % trans_id
    if trans is None:
        trans = cursor.fetchone()
    else:
        trans.update(cursor.fetchone())
    history_id = trans['history_id']

    pbm = _pbm_for_history_id(history_id)
    client = Client()
    client.group_number = trans['group_number']
    rx = Prescription(client)
    rx.brand = trans['brand']
    rx.compound_code = trans['compound_code']
    rx.awp = trans['awp']
    rx.state_fee = trans['state_fee']
    rx.ndc = trans['ndc_number']
    rx.nabp = trans['pharmacy_nabp']

    return Transaction(rx, pbm, client)

#//////////////////////////////////////////////////////////////////////////////
def _pbm_for_history_id(history_id):
    pbm = PBMHistory()
    cursor = R.db.cursor()
    cursor.execute("""
        select cost_allowed, dispense_fee, processing_fee, sales_tax,
               eho_network_copay
        from history
        where history_id=%s
        """, (history_id,))
    pbm.cost_allowed, \
    pbm.dispense_fee, \
    pbm.processing_fee, \
    pbm.sales_tax, \
    pbm.copay = cursor.fetchone()
    return pbm

#//////////////////////////////////////////////////////////////////////////////

_use_db = False
def use_db():
    global _use_db
    _use_db = True

def dont_use_db():
    global _use_db
    _use_db = False

class History(object):
    """ The EHO history record """
    @classmethod
    def for_record(cls, rec):
        """ history """
        return cls(Transaction.for_record(rec))

    def __init__(self, tx):
        self.tx = tx

    @property
    def cost_allowed(self):
        t = self.tx
        return t.cost_allowed + t.processing_fee - t.eho_processing_fee

    @property
    def dispense_fee(self):
        """ Failsafe incase there is a huge negative processing fee or
        something weird """
        return max(self.tx.dispense_fee, Decimal("0"))

    def write_text_record(self, fd):
        fd.write("%08d" % (self.cost_allowed*100))
        fd.write("%08d" % (self.dispense_fee*100))
        fd.write("\n")

class Client(object):
    """ A client who pays CPS for the prescription """

    _cache = {}

    @classmethod
    def for_record(cls, rec):
        """ client """
        gn = rec['group_number']
        if gn in cls._cache:
            return cls._cache[gn]
        if _use_db or not os.path.exists(PROCESSOR_FILE):
            client = DBClient()
        else:
            client = cls()
        client.group_number = gn
        cls._cache[gn] = client
        return client

    group_number = None
    """ The group number of the client """

    @property
    def never_lose_money(self):
        # This is currently the only group we are allowed to lose money on
        # due to a clause not going into the contract. Salt Lake County
        if self.group_number in LOSE_MONEY_GROUPS:
            return False
        else:
            return True

    @property
    def force_under_state_fee(self):
        x = _json_processing_data()['force_state_fee']
        return _json_processing_data()['force_state_fee'].get(self.group_number)

    def eho_processing_fee(self, tx_type):
        fees = [amount 
                for account, amount in self.fixed_processing_fees(tx_type)
                if account == 'eho']
        return sum(fees)

    def fixed_processing_fees(self, tx_type, subtotal=0):
        key = "%s:%s" % (self.group_number, tx_type)
        v = _json_processing_data()['fixed_distribution_rule'].get(key, [])
        for account, amount, min_cost, max_cost in v:
            amount, min_cost, max_cost = map(Decimal, [amount, min_cost, max_cost])
            if max_cost or min_cost:
                continue
            yield account, amount

    def percent_processing_fees(self, tx_type, subtotal=0):
        key = "%s:%s" % (self.group_number, tx_type)
        v = _json_processing_data()['percent_distribution_rule'].get(key, [])
        for account, amount, min_cost, max_cost in v:
            amount, min_cost, max_cost = map(Decimal, [amount, min_cost, max_cost])
            if max_cost and subtotal > max_cost:
                continue
            if min_cost and subtotal and subtotal < min_cost:
                continue
            yield account, amount

    def ranged_processing_fees(self, tx_type, subtotal):
        key = "%s:%s" % (self.group_number, tx_type)
        v = _json_processing_data()['fixed_distribution_rule'].get(key, [])
        for account, amount, min_cost, max_cost in v:
            amount, min_cost, max_cost = map(Decimal, [amount, min_cost, max_cost])
            if not max_cost and not min_cost:
                continue
            if max_cost and subtotal > max_cost:
                continue
            if min_cost and subtotal and subtotal < min_cost:
                continue
            yield account, amount

    def overriden_cost_allowed_for(self, tx_type, awp):
        key = "%s:%s" % (self.group_number, tx_type)
        factor = Decimal(_json_processing_data()['awp_cost_override'].get(key, 0))
        if factor:
            return count_money(awp * factor)
        else:
            return 0

    def cps_dispense_fee_for(self, tx_type):
        """ Give a dispense fee for the given transaction type for
        a tx in this group. """
        key = "%s:%s" % (self.group_number, tx_type)
        lu = _json_processing_data()['dispense_fee_override']
        if key not in lu:
            return None
        return Decimal(lu[key])


def tx_type_for(group_number, rx, cache={}, nabp_tt_cache={}):
    """ Determine the tx_type for the given fields. Use the nabp_tt_prefix
    table
    """

    def db_result():
        cursor = R.db.cursor()
        if not cache:
            cursor.execute("""
                select group_number, nabp, prefix
                from nabp_tt_prefix
                """)
            v = dict(((gn, nabp), prefix) for gn, nabp, prefix in cursor)
            cache.update(v)

        if (group_number, rx.nabp) in cache:
            prefix = cache[(group_number, rx.nabp)]
        elif ('', rx.nabp) in cache:
            prefix = cache[('', rx.nabp)]
        else:
            prefix = 'R'
        return '%s%s' % (prefix, suffix())

    def suffix():
        # these are ndc numbers that we put no markup on at all
        _passthru_ndcs = ['00001000100', '00001002500']
        if rx.ndc in _passthru_ndcs:
            return 'P'
        elif rx.compound_code == '2':
            return 'C'
        else:
            return rx.brand

    if _use_db or not os.path.exists(PROCESSOR_FILE):
        return db_result()
    else:
        try:
            prefixes = _json_processing_data()['nabp_prefix']
        except KeyError:
            return db_result()

    keys = ["%s:%s" % (group_number, rx.nabp), ':%s' % rx.nabp]
    for k in keys:
        if k in prefixes:
            return '%s%s' % (prefixes[k], suffix())
    return 'R%s' % suffix()

class DBClient(object):
    """ Object which provides the same interface as Client but uses the database,
    not a file on disk """
    """ A client who pays CPS for the prescription """

    @classmethod
    def for_record(cls, rec):
        """ client """
        client = cls()
        client.group_number = rec['group_number']
        return client

    group_number = None
    """ The group number of the client """

    @property
    def never_lose_money(self):
        # This is currently the only group we are allowed to lose money on
        # due to a clause not going into the contract.
        if self.group_number in LOSE_MONEY_GROUPS:
            return False
        else:
            return True

    @property
    @imemoize
    def force_under_state_fee(self):
        cursor = R.db.cursor()
        cursor.execute("""
            select force_under_state_fee
            from client where group_number=%s
            """, (self.group_number,))
        if not cursor.rowcount:
            return False
        else:
            return cursor.fetchone()[0]

    def eho_processing_fee(self, tx_type):
        fees = [amount 
                for account, amount in self.fixed_processing_fees(tx_type)
                if account == 'eho']
        return sum(fees)

    def fixed_processing_fees(self, tx_type, subtotal=0):
        for account, amount, min_cost, max_cost in self._fixed_processing_fee_list(tx_type):
            if max_cost or min_cost:
                continue
            yield (account, amount)

    def ranged_processing_fees(self, tx_type, subtotal=0):
        for account, amount, min_cost, max_cost in self._fixed_processing_fee_list(tx_type):
            if not max_cost and not min_cost:
                continue
            if max_cost and subtotal > max_cost:
                continue
            if min_cost and subtotal and subtotal < min_cost:
                continue
            yield (account, amount)

    @imemoize
    def _fixed_processing_fee_list(self, tx_type):
        cursor = R.db.cursor()
        cursor.execute("""
            select distribution_account, amount, min_cost, max_cost
            from distribution_rule
            where group_number=%s and tx_type=%s
              and amount is not null
        """, (self.group_number, tx_type))
        return [c for c in cursor]

    def percent_processing_fees(self, tx_type, subtotal=0):
        for account, amount, min_cost, max_cost in self._percent_processing_fee_list(tx_type):
            if max_cost and subtotal > max_cost:
                continue
            if min_cost and subtotal and subtotal < min_cost:
                continue
            yield (account, amount)

    @imemoize
    def _percent_processing_fee_list(self, tx_type):
        cursor = R.db.cursor()
        cursor.execute("""
            select distribution_account, percent, min_cost, max_cost
            from distribution_rule
            where group_number=%s and tx_type=%s
              and percent is not null
        """, (self.group_number, tx_type))
        return [c for c in cursor]

    def overriden_cost_allowed_for(self, tx_type, awp):
        factor = self._client_bill_rule(tx_type)
        if factor:
            return count_money(awp * factor)
        else:
            return 0

    @imemoize
    def cps_dispense_fee_for(self, tx_type):
        """ Give a dispense fee for the given transaction type for
        a tx in this group. """
        cursor = R.db.cursor()
        cursor.execute("""
            select amount
            from client_dispense_fee_rule
            where group_number=%s and tx_type=%s and amount is not null
            """, (self.group_number, tx_type))
        if cursor.rowcount:
            return cursor.fetchone()[0]
        else:
            return None


    @imemoize
    def _client_bill_rule(self, tx_type):
        cursor = R.db.cursor()
        cursor.execute("""
            select amount
            from client_bill_rule
            where group_number=%s and tx_type=%s
            """, (self.group_number, tx_type))
        if not cursor.rowcount:
            return None
        else:
            return cursor.fetchone()[0]

class Transaction(object):
    """ A calculated EHO history record values to be stored in EHO's history
    file. We have to expose everything in the cost_allowed and dispense_fee
    fields since we do not have a processing fee field
    """
    @classmethod
    def for_record(cls, rec):
        """ rec = dictionary with keys:
            group_number, cost_allowed, dispense_fee, processing_fee, 
            sales_tax, eho_netowrk_copay, brand, compound_code, awp, state_fee,
            nabp, ndc
        """
        return cls(Prescription.for_record(rec),
                   PBMHistory.for_record(rec),
                   Client.for_record(rec))

    def __init__(self, rx, pbm, client):
        self.pbm = pbm
        self.client = client
        self.rx = rx

    def __eq__(self, other):
        attrs = ['total', 'cost_allowed', 'dispense_fee', 'processing_fee', 'sales_tax', 'copay']
        for a in attrs:
            if getattr(self, a) != getattr(other, a):
                return False
        return True

    def __repr__(self):
        attrs = ['total', 'cost_allowed', 'dispense_fee', 'processing_fee', 'sales_tax', 'copay']
        vals = [getattr(self, a) for a in attrs]
        s = ["%s=%s" % x for x in zip(attrs, vals)]
        return "<Transaction %s>" % ", ".join(s)

    sales_tax = property(lambda s: s.pbm.sales_tax)
    copay = property(lambda s: s.pbm.copay)

    @property
    def eho_processing_fee(self):
        return self.client.eho_processing_fee(self.rx.tx_type)

    @property
    def total(self):
        return (self.cost_allowed + self.dispense_fee + self.processing_fee
                + self.sales_tax - self.copay)

    @property
    def cost_allowed(self):
        """ The cost used to calculate the bill amount to the client.  """
        calc = self._raw_cost_allowed - self._adjudication_amount
        return max(calc, self._lowest_allowed_cost_allowed)

    @property
    def dispense_fee(self):
        """ A marked up dispense fee. We may have to adjudicate this if we
        can't adjudicate the cost allowed enough. """
        diff = self._adjudication_amount - self._cost_adjudicated_amount
        return self._raw_dispense_fee - diff

    @property
    def processing_fee(self):
        """ The CPS marked up processing fee """
        return self._processing_fee_list.total

    @property
    def distributions(self):
        """ Distributions to insert into CPS's distribution table. The
        distributions will add up to the total of the transaction. """
        pbm = self.pbm
        d = self._processing_fee_list
        if self.rx.nabp == R.CPS_NABP_NBR:
            phcy_account = 'cps'
        else:
            phcy_account = 'pharmacy'
        d.append((phcy_account, pbm.cost_allowed + pbm.dispense_fee + pbm.sales_tax - pbm.copay))

        if self.total < d.total:
            # If we are over then we have to adjudicate them in the correct order
            self._adjudicate_distributions(d)
        elif self.total > d.total:
            # If we are under, we have to add the profits to CPS
            d.append(('cps', self.total - d.total))
        return d

    @property
    def _cost_adjudicated_amount(self):
        """ How much have we adjudicated the cost allowed ? """
        return self._raw_cost_allowed - self.cost_allowed

    @property
    def _adjudication_amount(self):
        """ How much do we need to cut the total down by? """
        if not self.client.force_under_state_fee:
            return 0
        test_total = (self._raw_cost_allowed + self._raw_dispense_fee
            + self.processing_fee + self.sales_tax - self.copay)
        if test_total <= self.rx.state_fee:
            return 0
        else:
            return test_total - self.rx.state_fee

    @property
    def _raw_cost_allowed(self):
        client = self.client
        cost = client.overriden_cost_allowed_for(self.rx.tx_type, self.rx.awp)
        if not cost:
            return self.pbm.cost_allowed
        if client.never_lose_money:
            return max(self.pbm.cost_allowed, cost)
        else:
            return cost

    @property
    def _lowest_allowed_cost_allowed(self):
        """ How low can the cost allowed go before we give a negative number to
        COBOL ? """
        return Decimal(".01") - self.processing_fee + self.eho_processing_fee

    @property
    def _raw_dispense_fee(self):
        override = self.client.cps_dispense_fee_for(self.rx.tx_type)
        if override is None:
            return self.pbm.dispense_fee
        else:
            return override

    @property
    def _processing_fee_list(self):
        return FeeList(
            self._fixed_processing_fee_list +
            self._percent_processing_fee_list +
            self._ranged_processing_fee_list)

    def _adjudicate_distributions(self, d):
        """ adjudicate the distributions down the total """
        difference = d.total - self.total

        for account, amount in list(d):
            if account in ('eho', 'cps', 'pharmacy'):
                continue
            hit = min(difference, amount)
            d.append((account, -hit))
            difference -= hit
            if not difference:          # out of money
                break

        if difference:
            # smoebody has to eat it
            d.append(('cps', -difference))

    @property
    def _fixed_processing_fee_list(self):
        fees = FeeList()
        sub_total = self._raw_cost_allowed + self._raw_dispense_fee + self.sales_tax - self.copay
        for account, fee_amt in self.client.fixed_processing_fees(self.rx.tx_type, sub_total):
            fees.append((account, fee_amt))
        return fees

    @property
    def _percent_processing_fee_list(self):
        fees = FeeList()
        pbm = self.pbm

        assert isinstance(self._raw_cost_allowed, Decimal), type(self._raw_cost_allowed)
        assert isinstance(pbm.sales_tax, Decimal)
        assert isinstance(self._raw_dispense_fee, Decimal)
        assert isinstance(self.copay, Decimal)
        rt = self._raw_cost_allowed + pbm.sales_tax + self._raw_dispense_fee - self.copay
        assert isinstance(rt, Decimal)
        rt += self._fixed_processing_fee_list.total
        for account, percent in self.client.percent_processing_fees(self.rx.tx_type, rt):
            fees.append((account, count_money(rt * percent)))
        return fees

    @property
    def _ranged_processing_fee_list(self):
        fees = FeeList()
        sub_total = self._raw_cost_allowed + self._raw_dispense_fee \
                  + self.sales_tax - self.copay + self._fixed_processing_fee_list.total \
                  + self._percent_processing_fee_list.total
        """
        raise ValueError(
            self._raw_cost_allowed, self._raw_dispense_fee,
                  self.sales_tax, self.copay, self._fixed_processing_fee_list,
                  self._percent_processing_fee_list
        )"""

        for account, fee_amt in self.client.ranged_processing_fees(self.rx.tx_type, sub_total):
            fees.append((account, fee_amt))
        return fees

def cps_timely_adjustments(tx, sponsor_cost_allowed, sponsor_dispense_fee, sponsor_processing_fee):
    """ Check that EHO's sponsor cost equals our currently calculated sponsor
    cost. We have to honor what is in blue diamond because distributions are
    calculated here (But there is a half done project to use those that are
    calculated processing time).

    Reasons for price change:

    - Billing rules change in the middle of the week.
    - Change in state fee schedule formulary during the week (still apply?)
    """
    pbm = tx.pbm
    eho_saved_total = sponsor_cost_allowed + sponsor_dispense_fee \
              + sponsor_processing_fee + pbm.sales_tax - pbm.copay

    diff = eho_saved_total - tx.total
    if not diff:
        return FeeList([])
    else:
        return FeeList([('cps', diff)])

class FeeList(list):
    """ A list of fees. Includes total calculation. Each fee is stores
    as a pair of account -> amount """
    @property
    def total(self):
        return sum(s[1] for s in self)

    @property
    def grouped_totals(self):
        g = itertools.groupby(sorted(self), lambda s: s[0])
        return [(account, sum(amount for _, amount in amounts))
                for account, amounts in g]

class Prescription(object):
    """ A prescription for a drug """

    @classmethod
    def for_record(cls, rec):
        """ prescription"""
        rx = Prescription(Client.for_record(rec))
        rx.brand = rec['brand']
        rx.compound_code = rec['compound_code']
        rx.awp = rec['awp']
        rx.state_fee = rec['state_fee']
        rx.nabp = rec['nabp']
        rx.ndc = rec['ndc']
        rx.chain_code = rec.get('chain_code', '')
        rx.dosage_form_code = rec.get('dosage_form_code', '')
        rx.doctor_id = rec.get('doctor_id', '')
        rx.jurisdiction = rec.get('jurisdiction', '')
        return rx

    brand = None
    " Is the prescription brand or generic? "

    compound_code = False
    " 2 = compound, otherwise single "

    awp = None
    " How much is the AWP for the drug? "

    ndc = None
    " NDC of the drug being filled"

    state_fee = None
    " How much is the state fee schedule for the drug? "

    nabp = None
    " NABP of the filling pharmacy "

    client = None
    " Group (client) the prescription is filled for "

    chain_code = None
    " Chain code of pharmacy filling prescription"

    dosage_form_code = None
    " Dosage form code of drug being dispensed. from medispan. "

    doctor_id = None
    " DEA or NPI# of prescribing doctor "

    jurisdiction = None
    " Workers Comp State of Jurisidction filled under "

    def __init__(self, client):
        self.client = client

    @property
    def tx_type(self):
        return tx_type_for(self.client.group_number, self)

class PBMHistory(object):
    """ Billing record from EHO to CPS. """

    @classmethod
    def for_record(cls, rec):
        """ pbm history """
        pbm = cls()
        pbm.cost_allowed = rec['cost_allowed']
        pbm.dispense_fee = rec['dispense_fee']
        pbm.processing_fee = rec['processing_fee']
        pbm.sales_tax = rec['sales_tax']
        pbm.copay = rec['eho_network_copay']
        return pbm

    cost_allowed = 0
    " How much EHO says it will pay the pharmacy for the drug "

    dispense_fee = 0
    " How much EHO says it will pay the pharmacy for dispensing the drug "

    processing_fee = 0
    " How much EHO says it will be paid for processing the drug "

    sales_tax = 0
    " How much EHO says it will pay the pharmacy for sales tax "

    copay = 0
    " How much EHO says the patient paid the pharmacy for copay "

    def __init__(self):
        pass
    
    @property
    def total(self):
        """ How much CPS pays EHO """
        return self.cost_allowed + self.dispense_fee + self.sales_tax - self.copay + self.processing_fee

def count_money(amt, quantifier=Decimal("0.01")):
    return amt.quantize(quantifier, rounding=ROUND_HALF_UP)

@memoize
def _json_processing_data():
    with open(PROCESSOR_FILE) as fd:
        return json.load(fd)

PROCESSOR_FILE = "/server/spc/files/corp-processing.json"

if __name__ == '__main__': test()
