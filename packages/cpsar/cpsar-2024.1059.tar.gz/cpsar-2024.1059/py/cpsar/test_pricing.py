from __future__ import print_function
from decimal import Decimal

from nose.tools import assert_equals

from cpsar.pricing import *

def test_db():
    R.db.setup()
    use_db()

def test_json_file():
    global PROCESSOR_FILE
    PROCESSOR_FILE = '/usr/local/srv/bd/res/ar/test_pricing.json'
    dont_use_db()

def test_csv_file():
    pass

def test_tx_type():
    client = Client.for_record({"group_number": '56600'})
    rx = Prescription(client)
    rx.brand = 'G'
    rx.compound_code = '1'
    rx.awp = Decimal('12.12')
    rx.state_fee = Decimal('44.00')
    rx.nabp = '12345334'
    assert tx_type_for('56600', rx) == 'RG'

def mkptest(t):
    def est_pricing():
        pbm = PBMHistory()
        pbm.cost_allowed = t['pbm_cost_allowed']
        pbm.dispense_fee = t['pbm_dispense_fee']
        pbm.processing_fee = t['processing_fee']
        pbm.sales_tax = Decimal("0.00")
        pbm.copay = Decimal("0.00")
        client = Client.for_record({"group_number": t['group_number']})
        rx = Prescription(client)
        rx.brand = t['brand']
        rx.compound_code = '1'
        rx.awp = t['awp']
        rx.state_fee = t['state_fee']
        rx.nabp = t['nabp']
        tx = Transaction(rx, pbm, client)
        hy = History(tx)
        assert_equals(hy.cost_allowed, t['history_cost_allowed'])
        assert_equals(hy.dispense_fee, t['history_dispense_fee'])
        assert_equals(tx.total, t['tx_total'])
    return est_pricing


# No dispense fee override/No AWP override
test_no_override_1 = mkptest({'pbm_cost_allowed': Decimal("3.74"),
         'pbm_dispense_fee': Decimal("2.00"),
         'processing_fee': Decimal("1.00"),
         'group_number': '70017',
         'brand': 'G',
         'awp': Decimal('31.92'),
         'state_fee': Decimal('45.23'),
         'nabp': '1111111',
         # Calculated fields
         'history_cost_allowed': Decimal("9.74"),
         'history_dispense_fee': Decimal("2.00"),
         'tx_total': Decimal("12.74")})

# Has RB dispense fee overrides/Has only RB AWP override
test_rb_dispense_fee_override = mkptest({
         'pbm_cost_allowed': Decimal("567.53"),
         'pbm_dispense_fee': Decimal("2.00"),
         'processing_fee': Decimal("1.25"),
         'group_number': '56500',
         'brand': 'B',
         'awp': Decimal('679.68'),
         'state_fee': Decimal('722.68'),
         'nabp': '1111111',
         'history_cost_allowed': Decimal("625.31"),
         'history_dispense_fee': Decimal("2.95"),
         'tx_total': Decimal("629.51")})

test_mo_neg_distributions = mkptest(
        # Mail Order negative distributions
        {'pbm_cost_allowed': Decimal("8.10"),
         'pbm_dispense_fee': Decimal("16.50"),
         'processing_fee': Decimal("1.25"),
         'group_number': '56600',
         'brand': 'G',
         'awp': Decimal('763.11'),
         'state_fee': Decimal('812.97'),
         'nabp': R.CPS_NABP_NBR,
         'history_cost_allowed': Decimal("0.01"),
         'history_dispense_fee': Decimal("12.84"),
         'tx_total': Decimal("14.10")})

test_rb_dispense_fee_override_2 = mkptest(
         # Has RB dispense fee overrides/only RB AWP override
        {'pbm_cost_allowed': Decimal("375.80"),
         'pbm_dispense_fee': Decimal("2.00"),
         'processing_fee': Decimal("1.00"),
         'group_number': '56700',
         'brand': 'B',
         'awp': Decimal('450.06'),
         'state_fee': Decimal('481.58'),
         'nabp': '1111111',
         'history_cost_allowed': Decimal("417.54"),
         'history_dispense_fee': Decimal("2.50"),
         'tx_total': Decimal("421.04")})

test_no_neg_mo = mkptest(
        # No negative distributions/No overrides mailorder
        {'pbm_cost_allowed': Decimal("69.58"),
         'pbm_dispense_fee': Decimal("16.50"),
         'processing_fee': Decimal("1.00"),
         'group_number': '59000',
         'brand': 'G',
         'awp': Decimal('125.50'),
         'state_fee': Decimal('143.48'),
         'nabp': R.CPS_NABP_NBR,
         'history_cost_allowed': Decimal("74.95"),
         'history_dispense_fee': Decimal("16.50"),
         'tx_total': Decimal("92.45")})

test_percent_addon = mkptest(
        # Has perentage add on/RB dispense fee overide/RB AWP override
        {'pbm_cost_allowed': Decimal("554.21"),
         'pbm_dispense_fee': Decimal("2.00"),
         'processing_fee': Decimal("1.00"),
         'group_number': '59100',
         'brand': 'B',
         'awp': Decimal('663.72'),
         'state_fee': Decimal('705.93'),
         'nabp': '1111111',
         'history_cost_allowed': Decimal("626.08"),
         'history_dispense_fee': Decimal("2.50"),
         'tx_total': Decimal("629.58")})

test_mo_neg_1 = mkptest(
        # has Mail Order negative distributions
        {'pbm_cost_allowed': Decimal("6.57"),
         'pbm_dispense_fee': Decimal("16.50"),
         'processing_fee': Decimal("1.00"),
         'group_number': '70005',
         'brand': 'G',
         'awp': Decimal('199.90'),
         'state_fee': Decimal('221.60'),
         'nabp': R.CPS_NABP_NBR,
         'history_cost_allowed': Decimal("3.07"),
         'history_dispense_fee': Decimal("16.50"),
         'tx_total': Decimal("20.57")})

test_mo_neg_2 = mkptest(
        # Has Mail Order Negative Distributions
        {'pbm_cost_allowed': Decimal("145.60"),
         'pbm_dispense_fee': Decimal("16.50"),
         'processing_fee': Decimal("1.00"),
         'group_number': '70005',
         'brand': 'B',
         'awp': Decimal('498.38'),
         'state_fee': Decimal('532.32'),
         'nabp': R.CPS_NABP_NBR,
         'history_cost_allowed': Decimal("142.10"),
         'history_dispense_fee': Decimal("16.50"),
         'tx_total': Decimal("159.60")})

test_no_override_2 = mkptest(
        # No dispense fee override/no awp override
        {'pbm_cost_allowed': Decimal("8.11"),
         'pbm_dispense_fee': Decimal("2.00"),
         'processing_fee': Decimal("1.00"),
         'group_number': '70024',
         'brand': 'G',
         'awp': Decimal('200.71'),
         'state_fee': Decimal('222.45'),
         'nabp': '1111111',
         'history_cost_allowed': Decimal("14.11"),
         'history_dispense_fee': Decimal("2.00"),
         'tx_total': Decimal("17.11")})

test_no_neg_mo_2 = mkptest(
        # No negative distributions
        {'pbm_cost_allowed': Decimal("34.56"),
         'pbm_dispense_fee': Decimal("16.50"),
         'processing_fee': Decimal("1.00"),
         'group_number': '70076',
         'brand': 'G',
         'awp': Decimal('1036.80'),
         'state_fee': Decimal('1100.35'),
         'nabp': R.CPS_NABP_NBR,
         'history_cost_allowed': Decimal("38.56"),
         'history_dispense_fee': Decimal("16.50"),
         'tx_total': Decimal("56.06")})

test_dispense_fee_override = mkptest(
        # Has dispense fee override
        {'pbm_cost_allowed': Decimal("20.02"),
         'pbm_dispense_fee': Decimal("2.00"),
         'processing_fee': Decimal("1.00"),
         'group_number': '70115',
         'brand': 'G',
         'awp': Decimal('148.26'),
         'state_fee': Decimal('167.38'),
         'nabp': '1111111',
         'history_cost_allowed': Decimal("35.02"),
         'history_dispense_fee': Decimal("2.75"),
         'tx_total': Decimal("38.77")})

test_sliding_scale_1 = mkptest(
        # Slding scale add ons
        {'pbm_cost_allowed': Decimal("89.44"),
         'pbm_dispense_fee': Decimal("2.00"),
         'processing_fee': Decimal("1.00"),
         'group_number': '70036',
         'brand': 'G',
         'awp': Decimal('183.40'),
         'state_fee': Decimal('204.28'),
         'nabp': '1111111',
         'history_cost_allowed': Decimal("124.94"),
         'history_dispense_fee': Decimal("2.00"),
         'tx_total': Decimal("127.94")})

test_sliding_scale_2 = mkptest(
        # Sliding Scale Add ons # 2
        {'pbm_cost_allowed': Decimal("8.20"),
         'pbm_dispense_fee': Decimal("2.00"),
         'processing_fee': Decimal("1.00"),
         'group_number': '70036',
         'brand': 'G',
         'awp': Decimal('120.76'),
         'state_fee': Decimal('138.51'),
         'nabp': '1111111',
         'history_cost_allowed': Decimal("23.70"),
         'history_dispense_fee': Decimal("2.00"),
         'tx_total': Decimal("26.70")})

def _test_existing_trans(trans_id):
    """ Regression testing function. Pass in an existing trans_id and it will
    recalculate the transaction and check it against what is currently stored 
    in the database. If it's equal it will pass. If not, it will raise an
    assertion error with a message describing what is wrong with it """
    trans = {}
    tx = transaction_for_trans_id(trans_id, trans)
    #from IPython.core.debugger import Pdb
    #Pdb().set_trace()
    if tx.cost_allowed != trans['cost_allowed']:
        print("%s: cost allowed %s != %s" % (trans_id, tx.cost_allowed,  trans['cost_allowed']))
    if tx.processing_fee != trans['processing_fee']:
        print("%s: processing_fee %s != %s" % (trans_id, tx.processing_fee, trans['processing_fee']))
    if tx.dispense_fee != trans['dispense_fee']:
        print("%s: dispense_fee %s != %s" % (trans_id, tx.dispense_fee, trans['dispense_fee']))
    if tx.total != trans['total']:
        print("%s: total %s != %s" % (trans_id, tx.total, trans['total']))

