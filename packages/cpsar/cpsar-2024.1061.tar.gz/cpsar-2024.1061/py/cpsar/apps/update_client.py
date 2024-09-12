import cpsar.ws as W
import cpsar.runtime as R
from cpsar import pg
from cpsar import util

class Program(W.GProgram):
    def main(self):
        fs = self.fs 
        cursor = R.db.dict_cursor()

        if not fs.has_key('group_number'):
            self._res.redirect("/view_client")
            return
        fields = [
            'client_name',
            'savings_formula',
            'tin',
            'group_code',
            'address_1',
            'address_2',
            'city',
            'state',
            'zip_code',
            'contact_name',
            'contact_phone',
            'contact_email',
            'contact_fax',
            'billing_name',
            'invoice_processor_code',
            'force_under_state_fee',
            'invoice_multiplier',
            'memo',
            'collections_contact',
            'collections_phone',
            'collections_email',
            'collections_fax',
            'billing_contact',
            'billing_phone',
            'billing_email',
            'billing_fax',
            'print_multiplier_invoice',
            'print_nonmultiplier_invoice',
            'mo_ship_fee',
            'print_hcfa_1500',
            'print_ncpdp',
            'show_awp_on_invoice',
            'show_sfs_on_invoice',
            'show_uc_on_invoice',
            'show_copay_on_invoice',
            'show_pharmacy_tax_id_on_invoice',
            'show_pharmacy_cost_on_invoice',
            'show_savings_on_invoice',
            'ccmsi_savings_percent',
            'ccmsi_client_number',
            'send_ca_state_reporting',
            'send_fl_state_reporting',
            'send_mg_state_reporting',
            'send_or_state_reporting',
            'send_tx_state_reporting',
            'send_nc_state_reporting',
            'insurer',
            'insurer_tin',
            'insurer_zip',
            'show_all_ingredients_on_invoice',
            'email_adjusters_inv_notification',
            'email_billing_inv_notification',
            'trans_rebate_amount',
            'trans_rebate_percent',
            'auto_apply_trans_rebate',
            'show_cmpd_cost_on_invoice',
            'show_due_date_on_invoice',
            'claim_admin_fein',
            'claim_admin_name',
            'claim_admin_zip',
            'inactive',
            'wq_adjuster_required',
            'wq_adjuster_inital_required',
            'wq_claim_number_required',
            'wq_policy_number_required',
            'wq_phcy_tax_id_required',
            'due_date_days',
            'pricing_module'
            ]

        bool_fields = [
            'print_multiplier_invoice',
            'print_nonmultiplier_invoice',
            'print_hcfa_1500',
            'show_awp_on_invoice',
            'show_sfs_on_invoice',
            'show_copay_on_invoice',
            'show_pharmacy_tax_id_on_invoice',
            'show_pharmacy_cost_on_invoice',
            'show_savings_on_invoice',
            'send_ca_state_reporting',
            'send_fl_state_reporting',
            'send_mg_state_reporting',
            'send_or_state_reporting',
            'send_tx_state_reporting',
            'send_nc_state_reporting',
            'force_under_state_fee',
            'show_all_ingredients_on_invoice',
            'email_adjusters_inv_notification',
            'email_billing_inv_notification',
            'auto_apply_trans_rebate',
            'show_cmpd_cost_on_invoice',
            'show_due_date_on_invoice',
            'inactive',
            'wq_adjuster_required',
            'wq_adjuster_inital_required',
            'wq_claim_number_required',
            'wq_policy_number_required',
            'wq_phcy_tax_id_required'
        ]

        currency_fields = [
            'mo_ship_fee'
        ]

        record = dict((f, fs.getvalue(f)) for f in fields)

        for f in bool_fields:
            if not record[f]:
                record[f] = False
            else:
                record[f] = True
        for f in currency_fields:
            if not record[f]:
                record[f] = '0'
            else:
                record[f] = record[f].replace('$', '').replace(',', '')

        group_number = fs.getvalue('group_number')
        match = {'group_number': group_number}
        sql = util.update_sql('client', record, match)

        R.log.info("Updating client record with group #%s", group_number)
        cursor.execute(sql)
        update_carriers(fs)
        update_liberty_insurance_codes(fs)
        if R.has_errors():
            map(R.flash, R.get_errors())
            self._res.redirect("/view_client?group_number=%s", group_number)
            return

        R.db.commit()
        R.flash("Update successful")
        self._res.redirect("/view_client?group_number=%s", group_number)

def update_liberty_insurance_codes(fs):
    group_number = fs.getvalue('group_number', '').strip()
    codes = fs.getvalue('liberty_insurance_codes', '').split(',')
    codes = [c.strip().upper() for c in codes if c.strip()]
    cursor = R.db.cursor()
    cursor.execute("""
        delete from client_liberty_insurance_code
        where group_number = %s
        """, (group_number,))
    if not codes:
        return

    code_frag = "(%s)" % ",".join(map(pg.qstr, codes))
    cursor.execute("""
        select group_number, insurance_code
        from client_liberty_insurance_code
        where insurance_code in %s
        """ % code_frag)
    if cursor.rowcount:
        for gn, ic in cursor:
            R.error("code %s is already on group %s" % (ic, gn))
        return
    for code in codes:
        if len(code) > 5:
            R.error("Code %s is too long. max length 5" % code)
            return
        cursor.execute("""
            insert into client_liberty_insurance_code (group_number, insurance_code, username)
            values (%s, %s, %s)
            """, (group_number, code, R.username()))

def update_carriers(fs):
    cursor = R.db.dict_cursor()
    group_number = fs.getvalue('group_number')
    for state in [ 'ca', 'fl', 'nc', 'or', 'tx']:
        cursor.execute("""
            insert into sr_carrier (
                group_number, state, carrier_name, carrier_fein, carrier_zip, payor_id)
            values (%s, %s, %s, %s, %s, %s)
            on conflict (group_number, state) do update set
            carrier_name=EXCLUDED.carrier_name,
            carrier_fein=EXCLUDED.carrier_fein,
            carrier_zip=EXCLUDED.carrier_zip,
            payor_id=EXCLUDED.payor_id
            """, (
                group_number,
                state.upper(),
                fs.getvalue('%s_carrier_name' % state),
                fs.getvalue('%s_carrier_fein' % state),
                fs.getvalue('%s_carrier_zip' % state),
                fs.getvalue('%s_payor_id' % state)))

application = Program.app
