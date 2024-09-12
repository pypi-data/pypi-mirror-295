""" Creates new transaction records rebilled from old transactions
"""

import pprint as PP 
import datetime as DT
import decimal as D
import copy as C

import cpsar.runtime as R
import cpsar.ws as W
import cpsar.util as U

from cpsar import edi
from cpsar import txlib
from cpsar.invoice_id import RebillInvoiceKeyMaker

class Program(W.HTTPMethodMixIn, W.MakoProgram):
    mako_auto_publish = False
    dp = PP.PrettyPrinter(indent=4)

    def do_get(self):
        # load the template with
        self.tmpl['transactions'] = transactions_marked_for_rebill()
        self.mako()

    def do_post(self):
        trans_ids = self.fs.getlist('trans_id')
        trans_ids = good_transaction_ids(trans_ids)
        if not trans_ids:
            R.error("No transactions checked")
            return self.do_get()

        batch_file = new_batch_file()

        # trans values
        data = self.tmpl
        data['old_trans'] = get_old_trans_records(trans_ids)
        data['new_trans'] = create_new_trans_records(data['old_trans'], batch_file)
        insert_new_transactions(data['new_trans'])

        # invoice values
        data['old_invoices'] = get_old_invoices(
            data['old_trans'])
        data['new_invoices'] = new_invoice_records( 
            data['new_trans'])
        insert_new_invoices(data['new_invoices'])

        # distribution values 
        data['old_distributions'] = get_old_distributions(
            data['old_trans']) 
        data['new_distributions'] = create_new_distributions(
            data['old_distributions'],
            data['new_trans'])
        insert_new_distributions(data['new_distributions'])

        # create new note for the new trans
        data['new_trans_notes'] = create_trans_note(
            data['new_trans'])
        insert_new_notes(data['new_trans_notes'])

        # create rebill records = {}
        data['rebill_records'] = create_new_rebills(
            data['new_trans'])
        insert_rebills(data['rebill_records'])

        # create rebill credits
        data['rebill_credits'] = create_new_rebill_credits(
            data['old_trans'],
            data['new_trans'],
            data['rebill_records'])
        insert_rebill_credits(data['rebill_credits'])

        # execute balancing proceedure for old_trans and rebill records
        resolve_balances(
            data['rebill_credits'],
            data['rebill_records'], 
            data['old_trans'],
            data['new_trans'],
            data['old_invoices'],
            data['new_invoices'])

        # Create EDI Files
        edi.insert_rebill(batch_file['batch_file_id'])

        # turn rebill option off
        rebill_option_switch(data['old_trans'])

        self.tmpl.template_name = "create_rebill_trans_report.tmpl" 

        self.tmpl.update(data)
        self.mako()

        if R.has_errors():
             self.do_get()
             return

        # commit changes
        R.db.commit()
        
def get_old_trans_records(trans_ids):
    recs = {}
    cursor = R.db.dict_cursor()
    for key in trans_ids:
        cursor.execute("""
            SELECT * 
            FROM trans
            WHERE trans_id = %s
        """ % key)
        rec = dict(cursor.fetchone())
        recs[key] = rec
    return recs

def create_new_trans_records(old_recs, batch_file):
    recs = C.deepcopy(old_recs)
    remove_rebilled_rebills(recs) #rebilled more than once
    set_invoice_values(recs)
    assign_new_trans_record_values(recs, batch_file)
    return recs

def remove_rebilled_rebills(recs):
    tlist = []
    cursor = R.db.dict_cursor()
    for key in recs:
        cursor.execute("""
            SELECT trans_id 
            FROM rebill
            WHERE trans_id = %s
        """ % key)
        ids = cursor.fetchone()
        if ids is not None:
            tlist.append(key)

    for key in tlist:
        del recs[key]

def set_invoice_values(recs):
    maker = RebillInvoiceKeyMaker()

    invoice_id_tracker = {}
    last_invoice_id = 0
    line_no = 0
    invoice_id = 0

    for key in recs:
        rec = recs[key]
        maker.assign(rec)

def assign_new_trans_record_values(recs, batch_file):
    for key in recs:
        rec = recs[key]
        # Values that need computed/set for trans table
        #  
        rec['rebilled_trans_id'] = rec['trans_id']
        rec['trans_id'] = U.default
        rec['batch_date'] = batch_date()
        rec['create_date'] = batch_date()
        rec['batch_file_id'] = batch_file['batch_file_id']
        rec['adjustments'] = 0.00
        rec['balance'] = rec['total']
        rec['paid'] = False
        rec['paid_date'] = None 
        rec['rebill'] = False
        rec['distributed_amount'] = 0.00
        rec['paid_amount'] = 0.00
        rec['writeoff_total'] = 0.00
        rec['adjudication_total'] = 0.00
        rec['settled_amount'] = 0.00 
        assign_rebill_number(rec)

def assign_rebill_number(rec):
    key = (rec['group_number'], rec['group_auth'])
    rebill_number = rebill_lookup().get(key, 0)
    rec['rebill_number'] = rebill_number + 1

@U.memoize
def rebill_lookup():
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT group_number, group_auth, MAX(rebill_number)
        FROM trans
        WHERE rebill_number != 0
        GROUP BY group_number, group_auth
        """)
    return dict(((g, a), m) for g, a, m in cursor)

def batch_date():
    return DT.date.today()

def new_batch_file():
    cursor = R.db.dict_cursor()
    sql = U.insert_sql("batch_file", {
        "batch_date": batch_date(),
        "file_name": new_batch_file_name(),
        "username": R.username()
        }, "*")
    cursor.execute(sql)
    return cursor.fetchone()

def new_batch_file_name():
    return "%s-%s" % (batch_file_prefix(), existing_batch_file_count()+1)

def existing_batch_file_count():
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT COUNT(*)
        FROM batch_file
        WHERE file_name LIKE '%s%%'
        """ % batch_file_prefix())
    return cursor.fetchone()[0]

def batch_file_prefix():
    return "rebill-%s" % batch_date().strftime("%Y%m%d")

def insert_new_transactions(recs):
    cursor = R.db.cursor()
    for key in recs:
        rec = recs[key]
        sql = U.insert_sql("trans", rec,["trans_id"])
        cursor.execute(sql)
        rec['trans_id'] = cursor.fetchone()[0]

def get_old_invoices(old_recs):
    recs = {}
    cursor = R.db.dict_cursor()
    for key in old_recs:
        rec = old_recs[key] 
        sql = """
            SELECT * 
            FROM invoice 
            WHERE invoice_id = %s
        """ % rec['invoice_id']
        cursor.execute(sql)
        return_rec = dict(cursor.fetchone())
        recs[key] = return_rec
    return recs

def new_invoice_records(new_trans_recs):
    invoice_map = {}
    trans_rec = {}
    recs = {}

    for temp_rec in new_trans_recs.values():
        tlist = invoice_map.setdefault(temp_rec['invoice_id'], [])
        tlist.append(temp_rec)

    for key in invoice_map:
        recs[key] = new_invoice_record(invoice_map[key])
    return recs

def new_invoice_record(invoice_trans_recs):
    trans_rec = invoice_trans_recs[0]
    rec = {}
    rec['invoice_id'] = trans_rec['invoice_id']
    rec['patient_id'] = trans_rec['patient_id']
    rec['group_number'] = trans_rec['group_number']
    rec['batch_date'] = batch_date()
    rec['due_date'] = None 
    rec['total'] = get_invoice_sums(invoice_trans_recs, 'total')
    rec['adjustments'] = 0.00
    rec['balance'] = get_invoice_sums(invoice_trans_recs, 'balance')
    rec['item_count'] = get_invoice_max_line_no(invoice_trans_recs) 
    rec['memo'] = "Reissued invoice" #client table"Reissued invoice"
    rec['create_date'] = U.default
    return rec

def get_invoice_sums(recs, field_to_total):
    running_total = D.Decimal('0.00')
    counter = 0
    for key in recs:
        rec = recs[counter]
        running_total = running_total + rec[field_to_total]
        counter +=1
    return running_total

def get_invoice_max_line_no(invoice_trans_recs):
    tlist = []
    for rec in invoice_trans_recs:
        value = rec['line_no']
        tlist.append(value)

    return(max(tlist))

def insert_new_invoices(recs):
    cursor = R.db.cursor()
    for key in recs:
        rec = recs[key]
        sql = U.insert_sql("invoice", rec)
        cursor.execute(sql)

def good_transaction_ids(trans_ids):
    # If no transaction id's show error message
    # and show user setup form
    if not trans_ids:
        R.error('No transactions selected')
        return
    
    new_ids = []
    # validate the trans id's
    for trans_id in trans_ids:
        try:
            new_ids.append(int(trans_id))
        except ValueError:
            R.error("Ignoring invalid transaction ID %s", trans_id)
    return new_ids

def transactions_marked_for_rebill():
    # Get rebill transactions for display on the
    # Web form only getting enough info for do_get
    # Get the rest later
    cursor = R.db.dict_cursor()
    cursor.execute("""
        SELECT trans_id,
            total,
            balance
        FROM trans
        WHERE rebill = true
        ORDER BY trans_id""")

    return list(cursor)

def get_old_distributions(recs):
    old_recs = {}
    cursor = R.db.dict_cursor()
    for key in recs:
        cursor.execute("""
            SELECT *
            FROM distribution
            WHERE trans_id = %s
        """ % key)
        rec = list(map(dict, cursor))
        old_recs[key] = rec

    return old_recs

def create_new_distributions(recs, new_trans):
    new_recs = {}

    for old_trans_id in new_trans:
        tlist = recs[old_trans_id]
        for rec in tlist:
            old_distribution_id = rec['distribution_id']
            trans = new_trans[rec['trans_id']]
            trans_id = (trans['trans_id'])

            assign_distribution(rec, trans_id)
            new_recs[old_distribution_id] = rec

    return new_recs

def assign_distribution(rec, new_trans_id):    
    # Values that need computed/set for distributions
    rec['distribution_id'] = U.default      
    rec['trans_id'] = new_trans_id           
    rec['distribution_date'] = None     

def insert_new_distributions(recs):
    cursor = R.db.cursor()
    for key in recs:
        rec = recs[key]
        sql = U.insert_sql("distribution", rec, ['distribution_id'] )
        cursor.execute(sql)
        tlist = cursor.fetchone()
        for ids in tlist:
            rec['distribution_id'] = ids

def create_trans_note(trans_rec):
    new_notes = {}
    for old_trans_id in trans_rec:
        rec = assign_trans_note(old_trans_id, trans_rec[old_trans_id])
        new_notes[rec['trans_id']] = rec
    return new_notes
    
def assign_trans_note(old_trans_id, trans_rec):
    rec = {}
    # Values that need computed/set for distributions
    rec['note_id'] = U.default
    rec['trans_id'] = trans_rec['trans_id'] 
    rec['note'] = ("Reissued invoice from %s for trans %s" 
        % (trans_rec['create_date'],  old_trans_id))
    rec['username'] = R.username()
    return rec

def insert_new_notes(recs):
    cursor = R.db.cursor()
    for key in recs:
        rec = recs[key]
        sql = U.insert_sql("trans_note", rec, ['note_id'] )
        cursor.execute(sql)
        tlist = cursor.fetchone()
        for ids in tlist:
            rec['note_id'] = ids
    
def create_new_rebills(trans_rec):
    new_rebills = {}
    for old_trans_id in trans_rec:
        rec = assign_rebill(old_trans_id, trans_rec[old_trans_id])
        new_rebills[rec['trans_id']] = rec
    return new_rebills
    
def assign_rebill(old_trans_id, trans_rec):    
    rec = {}
    # Values that need computed/set for distributions
    rec['rebill_id'] = U.default 
    rec['trans_id'] = old_trans_id 
    rec['total'] = trans_rec['total']
    rec['balance'] = trans_rec['balance']
    rec['username'] = R.username() 
    return rec

def insert_rebills(recs):
    cursor = R.db.cursor()
    for key in recs:
        rec = recs[key]
        sql = U.insert_sql("rebill", rec, ['rebill_id'] )
        cursor.execute(sql)
        tlist, = cursor.fetchone()
        rec['rebill_id'] = tlist

def create_new_rebill_credits(old_trans, new_trans, rebills):
    rebill_credits = {}
    for old_trans_id in rebills:
        rebill_rec = rebills[old_trans_id]
        old_trans_rec = old_trans[old_trans_id]
        new_trans_id = new_trans[old_trans_id]['trans_id']
        rebill_id = rebill_rec['rebill_id']
        
        rebill_balance = rebill_rec['balance']
        old_trans_balance = old_trans_rec['balance'] 

        if rebill_balance == old_trans_balance:
            credit = new_rebill_credit(
                rebill_id,
                old_trans_id,
                rebill_rec['balance'])
            rebill_credits[old_trans_id] = credit
        # The old transaction balance != rebill credit.  We zero out the
        # balance on the old transaction and apply what is rest to the new
        # transaction.

        # Why is this even rebilled? 
        elif old_trans_balance == 0:
            credit = new_rebill_credit(rebill_id, new_trans_id, rebill_rec['balance'])
            rebill_credits[old_trans_id] = credit
        # Split the credit 
        else:
            credit = new_rebill_credit(rebill_id, old_trans_id, old_trans_balance)
            rebill_credits[old_trans_id] = credit
            new_amount = rebill_rec['balance'] - old_trans_balance
            credit = new_rebill_credit(rebill_id, new_trans_id, new_amount)
            rebill_credits[new_trans_id] = credit

    return rebill_credits

def new_rebill_credit(rebill_id, trans_id, amount):
    rec = {}
    # Values that need computed/set for distributions
    rec['rebill_credit_id'] = U.default 
    rec['rebill_id'] = rebill_id
    rec['trans_id'] = trans_id
    rec['amount'] = amount
    rec['username'] = R.username() 
    return rec

def insert_rebill_credits(recs):
    cursor = R.db.cursor()
    for key in recs:
        rec = recs[key]
        sql = U.insert_sql("rebill_credit", rec, ['rebill_credit_id'] )
        cursor.execute(sql)
        tlist, = cursor.fetchone()
        rec['rebill_credit_id'] = tlist

def resolve_balances(rebill_credits, rebills, old_trans_recs, new_trans_recs,
                     old_invoices, new_invoices):
    cursor =  R.db.cursor()
    cursor2 = R.db.cursor()
    cursor3 = R.db.cursor()
    cursor4 = R.db.cursor()
    cursor5 = R.db.cursor()

    # We need a map of new trans ids the new transactions. new_trans_recs is actually
    # keyed off the old trans
    new_trans_keys = {}
    for t in new_trans_recs.values():
        new_trans_keys[t['trans_id']] = t

    for trans_id, credit in rebill_credits.items():
        if trans_id in old_trans_recs:
            trans_rec = old_trans_recs[trans_id]
            invoice_rec = old_invoices[trans_id]
            rebill_rec = rebills[trans_id]
        else:
            trans_rec = new_trans_keys[trans_id]
            invoice_rec = new_invoices[trans_rec['invoice_id']]
            rebill_rec = rebills[trans_rec['rebilled_trans_id']]

        cursor.execute("""
            SELECT balance
            FROM invoice
            WHERE invoice_id = %s"""
            % (trans_rec['invoice_id']))
        invoice_balance = cursor.fetchone()[0]

        trans_rec['balance'] -= credit['amount']
        cursor2.execute("""
            UPDATE trans
            SET balance = %s 
            WHERE trans_id = %s""" 
            % (trans_rec['balance'], trans_rec['trans_id']))

        rebill_rec['balance'] -= credit['amount']
        cursor3.execute("""
            UPDATE rebill 
            SET balance = %s 
            WHERE trans_id = %s"""
            % (rebill_rec['balance'], rebill_rec['trans_id']))

        invoice_balance -= credit['amount']

        cursor4.execute("""
            UPDATE invoice
            SET balance = %s
            WHERE invoice_id = %s"""
            % (invoice_balance, invoice_rec['invoice_id']))

        trans_rec['rebill_credit_total'] += credit['amount'] 
        cursor5.execute("""
            UPDATE trans
            SET rebill_credit_total = %s
            WHERE trans_id = %s"""
            % (trans_rec['rebill_credit_total'], trans_rec['trans_id']))

        # For setting trans.adjustments correctly
        txlib.check_adjustments(trans_id)

def rebill_option_switch(recs):
    cursor = R.db.cursor()
    for invoice_id in recs:
        cursor.execute("""
            UPDATE trans
            SET rebill = False
            WHERE trans_id = %s"""
            % invoice_id)

application = Program.app
