from cpsar import db
from cpsar.wsgirun import mako, wsgi
from cpsar import pricing


@wsgi
@mako('reprice_trans.tmpl')
def application(req, res):
    try:
        trans_id = int(req.params.get('trans_id'))
    except (ValueError, TypeError):
        trans_id = None

    if not trans_id:
        res.write("No trans given")
        return


    cursor = db.dict_cursor()
    cursor.execute("""
        select history.cost_allowed as pbm_cost_allowed,
               history.dispense_fee as pbm_dispense_fee,
               history.group_number,
               pharmacy.nabp,
               history.sales_tax,
               history.eho_network_copay,
               history.processing_fee,
               history.state_fee,
               history.awp,
               drug.brand,
               history.compound_code,
               history.rx_date,
               history.date_processed,
               drug.ndc_number as ndc
        from history
        join pharmacy using(pharmacy_id)
        join drug using(drug_id)
        join trans using(history_id)
        where trans_id = %s""", (trans_id,))
    if not cursor.rowcount:
        res.write("trans %s not found" % trans_id)
        return

    rec = next(cursor)

    res['source'] = rec
    pbm = pricing.PBMHistory()
    pbm.cost_allowed = rec['pbm_cost_allowed']
    pbm.dispense_fee = rec['pbm_dispense_fee']
    pbm.processing_fee = rec['processing_fee']
    pbm.sales_tax = rec['sales_tax']
    pbm.copay = rec['eho_network_copay']

    client = pricing.Client.for_record({"group_number": rec['group_number']})

    rx = pricing.Prescription(client)
    rx.ndc = rec['ndc']
    rx.brand = rec['brand']
    rx.compound_code = rec['compound_code']
    rx.awp = rec['awp']
    rx.state_fee = rec['state_fee']
    rx.nabp = rec['nabp']

    tx = pricing.Transaction(rx, pbm, client)

    history = pricing.History(tx)

    res['history'] = {
        'cost_allowed': history.cost_allowed,
        'dispense_fee': history.dispense_fee
    }

    res['distributions'] = tx.distributions

