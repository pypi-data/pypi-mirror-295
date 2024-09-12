import csv

from cpsar import pg
import cpsar.runtime as R
import cpsar.ws as W
from cpsar import pricing


class Program(W.MakoProgram):

    def recent_batches(self):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT batch_file_id, file_name
            FROM batch_file
            order by batch_file_id DESC
            LIMIT 100
            """)
        return [(str(c['batch_file_id']),
            "%06d - %s" % (c['batch_file_id'], c['file_name']))
            for c in cursor]

    @property
    def batch_file_id(self):
        return self.fs.getvalue("batch_file_id")

    def clients(self):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT *
            FROM client
            ORDER BY group_number""")
        return list(cursor)

    results = None
    def main(self):
        fs = self.fs
        cursor = R.db.dict_cursor()
        batch_id = self.fs.getvalue("batch_file_id")
        if not batch_id:
            return
        cursor.execute("""
            select trans.trans_id,
            trans.dispense_fee,
            trans.processing_fee,
            trans.cost_allowed,
            trans.total,
            trans.group_number,
            trans.pharmacy_nabp,
            trans.state_fee,
            trans.compound_code,
            trans.awp,

            history.history_id,
            history.cost_allowed as hist_cost_allowed,
            history.dispense_fee as hist_dispense_fee,
            history.processing_fee as hist_processing_fee,
            history.sales_tax as hist_sales_tax,
            history.eho_network_copay as hist_copay,

            drug.brand, drug.ndc_number,
            pharmacy.name as pharmacy_name

        from trans
        join drug using(drug_id)
        join pharmacy using(pharmacy_id)
        join history using(history_id)
        where trans.batch_file_id = %s
--          and pharmacy.chain_code != '039'
        """, (batch_id,))

        pricing.use_db()
        self.results = []

        client_list = {}

        for trans in cursor:

            history_id = trans['history_id']

            pbm = pricing.PBMHistory()
            pbm.cost_allowed = trans['hist_cost_allowed']
            pbm.dispense_fee = trans['hist_dispense_fee']
            pbm.processing_fee = trans['hist_processing_fee']
            pbm.sales_tax = trans['hist_sales_tax']
            pbm.copay = trans['hist_copay']

            if trans['group_number'] in client_list:
                client = client_list[trans['group_number']]
            else:
                client = pricing.DBClient()
                client.group_number = trans['group_number']
                client_list[trans['group_number']] = client

            rx = pricing.Prescription(client)
            rx.brand = trans['brand']
            rx.compound_code = trans['compound_code']
            rx.awp = trans['awp']
            rx.state_fee = trans['state_fee']
            rx.ndc = trans['ndc_number']
            rx.nabp = trans['pharmacy_nabp']
            tx = pricing.Transaction(rx, pbm, client)

            eho_history = pricing.History(tx)

            result = {'bad': False}
            result['trans_id'] = trans['trans_id']
            result['existing_processing_fee'] = trans['processing_fee']
            result['existing_cost_allowed'] = trans['cost_allowed']
            result['existing_dispense_fee'] = trans['dispense_fee']
            result['existing_total'] = trans['total']
            result['calculated_processing_fee'] = tx.eho_processing_fee
            result['calculated_cost_allowed'] = eho_history.cost_allowed
            result['calculated_total'] = tx.total
            result['calculated_dispense_fee'] = eho_history.dispense_fee
            result['pharmacy_name'] = trans['pharmacy_name']
            result['group_number'] = trans['group_number']

            if eho_history.cost_allowed != trans['cost_allowed']:
                result['bad'] = True
            if tx.eho_processing_fee != trans['processing_fee']:
                result['bad'] = True
            if eho_history.dispense_fee != trans['dispense_fee']:
                result['bad'] = True
            if tx.total != trans['total']:
                result['bad'] = True
            if result['bad']:
                self.results.append(result)

        if self.fs.getvalue('csv'):
            self.mako_auto_publish = False
            self._res.content_type = 'application/csv'
            self._res.headers["Content-Disposition"] = "attachment; filename=trans.csv"
            writer = csv.writer(self._res)
            fields = sorted(result.keys())
            writer.writerow(fields)
            for r in self.results:
                writer.writerow([r[f] for f in fields])


application = Program.app
