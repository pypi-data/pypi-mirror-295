from __future__ import print_function
from decimal import Decimal
import cpsar.runtime as R
from cpsar import pricing2

def test_basic():
    R.db.setup()
    store = pricing2.PreloadPgStore()

    inq = pricing2.Inquiry()
    inq.cost_allowed =  Decimal("3.74")
    inq.dispense_fee = Decimal("2.00")
    inq.processing_fee = Decimal("1.00")
    inq.group_number = '70017'
    inq.brand_code = 'G'
    inq.awp = Decimal('31.92')
    inq.state_fee = Decimal('45.23')
    inq.state_fee = Decimal('8.23')
    inq.pharmacy_nabp = '4451111'

    price = pricing2.client_price(inq, store)
    print(price)

    distributions = pricing2.distributions(inq, price, store)
    for d in distributions:
        print(d)

    print()
    distributions = pricing2.distributions(inq, Decimal("23.00"), store)
    for d in distributions:
        print(d)


#         # Calculated fields
#         'history_cost_allowed': Decimal("9.74"),
#         'history_dispense_fee': Decimal("2.00"),
#         'tx_total': Decimal("12.74")})
#    tx = pricing2.trans_for(i, store)
#    tx.processing_fee = pricing2.ZERO
#    print pricing2.trans_processing_fee(i, store, tx.total)
