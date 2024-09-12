import cpsar.pg
import cpsar.runtime as R
import cpsar.ws as W

import kcontrol as K

class Program(W.MakoProgram):

    def clients(self):
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT *
            FROM client
            ORDER BY group_number""")
        return list(cursor)

    def main(self):
        fs = self.fs
        cursor = R.db.dict_cursor()

        if not fs.getvalue('group_number'):
            self._res.write('Please select a group to view')
            self.mako_auto_publish = False
            return

        R.session['current_group'] = fs.getvalue('group_number')
        R.session.save()
        group_number = fs.getvalue('group_number')

        doc = {}
        doc['form'] = fs

        K.store.update(carrier_values('CA', group_number))
        K.store.update(carrier_values('FL', group_number))
        K.store.update(carrier_values('OR', group_number))
        K.store.update(carrier_values('TX', group_number))
        K.store.update(carrier_values('NC', group_number))

        mmap = {'u' : 'Client Updated Successfully',
                'b' : 'Client Billing Updated Successfully',
                'dc' : 'Distribution Rule Deleted Successfully',
                'x' : 'Distribution Rule Added Successfully'}
        try:
            doc['msg'] = mmap[fs.getvalue('m')]
        except KeyError:
            pass

        cursor.execute("""
            SELECT *
            FROM client
            WHERE group_number = %s""",
            (group_number,))
        doc['client'] = cpsar.pg.one(cursor)
        if not doc['client']:
            self._res.status = 404
            return

        cursor.execute("""
            select insurance_code
            from client_liberty_insurance_code
            where group_number = %s
            order by insurance_code
            """, (group_number,))
        doc['liberty_insurance_codes'] = ",".join(c['insurance_code'] for c in cursor)

        cursor.execute("""
            SELECT 
                carrier_name as tx_carrier_name 
            FROM sr_carrier 
            WHERE group_number = %s
            AND state = 'TX' """,
            (group_number,))
        doc['tx_carrier'] = cpsar.pg.one(cursor)

        cursor.execute("""
            SELECT dr_id, distribution_account, amount,
                  tx_type, create_time, 
                  CASE WHEN percent IS NULL THEN NULL ELSE
                        percent * 100
                  END as percent,
                  show_on_invoice,
                  max_cost,
                  min_cost,
                  addon,
                  add_to_running_total,
                  priority
            FROM distribution_rule
            WHERE group_number=%s
            ORDER BY tx_type, priority, distribution_account, amount, percent""",
            (group_number,))
        doc['distribution_rules'] = cpsar.pg.all(cursor)

        cursor.execute("""
            SELECT tx_type, SUM(amount) AS processing_fee
            FROM distribution_rule
            WHERE group_number=%s AND tx_type IS NOT NULL
            GROUP BY tx_type
            ORDER BY tx_type
            """, (group_number,))
        doc['processing_fees'] = cpsar.pg.all(cursor)
        doc['processing_fees'] = dict((c['tx_type'], c) 
                                      for c in doc['processing_fees'])

        cursor.execute("SELECT name FROM distribution_account ORDER BY name")
        doc['distribution_accounts'] = [c[0] for c in cursor]

        cursor.execute("""
            SELECT *, EXISTS (
                SELECT ptype_id
                FROM trans_payment
                WHERE ptype_id=payment_type.ptype_id
                UNION
                SELECT ptype_id
                FROM overpayment
                WHERE ptype_id=payment_type.ptype_id
               ) AS has_payments
            FROM payment_type
            WHERE group_number=%s
            ORDER BY ptype_id
            """, (group_number,))
        doc['payment_types'] = list(cursor)

        cursor.execute("""
            SELECT *
            FROM client_dispense_fee_rule
            WHERE group_number=%s
            """, (group_number,))
        doc['dispense_fee_rules'] = list(cursor)

        cursor.execute("""
            SELECT *
            FROM client_bill_rule
            WHERE group_number=%s
            """, (group_number,))
        doc['bill_rules'] = list(cursor)

        cursor.execute("""
            SELECT report_code, internal FROM client_report_code
            WHERE group_number=%s
            order by report_code
            """, (group_number,))
        doc['report_codes'] = list(cursor)

        cursor.execute("""
            select comu_id, tx_type, account, percent*100 as percent
            from distribution_on_markup
            where group_number=%s
            order by tx_type, account
            """, (group_number,))
        doc['markup_commission_rules'] = list(cursor)

        cursor.execute("""
            SELECT tx_type, default_account
            FROM client_default_account_name
            WHERE group_number=%s
            order by tx_type
            """,(group_number,))
        doc['default_account_names'] = list(cursor)
        self.tmpl.update(doc)

def carrier_values(state, group_number):
    cursor = R.db.dict_cursor()
    cursor.execute("""
        SELECT 
            carrier_name,
            carrier_fein,
            carrier_zip,
            payor_id
        FROM sr_carrier
        WHERE group_number = %s
        AND state = %s """,
        (group_number, state))
    if cursor.rowcount == 0:
        return {}
    rec = cursor.fetchone()
    return dict(("%s_%s" % (state.lower(), k), v) for k, v in rec.items())

application = Program.app
