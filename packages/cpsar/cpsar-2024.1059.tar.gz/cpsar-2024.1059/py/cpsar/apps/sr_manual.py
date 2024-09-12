"""

"""
import datetime
import itertools
import decimal
import os
import sys
import tempfile

import cpsar.runtime as R
import cpsar.wsgirun as W

from cpsar import config
from cpsar import txlib
from cpsar import util
from cpsar.pg import qstr
from cpsar.sr import bishop
from cpsar.util import sftp
from cpsar.wsgirun import json, mako

reg = W.PathDispatch()

required_bill_fields = [
    'bill_number',
    'juris',
    'claim_freq',
]

text_bill_fields = [
    'bill_number',
    'bill_type',
    'claim_number',
    'juris',
    'claim_freq',
    'control_number',
    'insurer_code_number',
    'insurer_fein',
    'subscriber_member_number',
    'payor_name',
    'payor_id',
    'icd_code',
    'payor_fein',
    'payor_address_1',
    'payor_address_2',
    'payor_city',
    'payor_state',
    'payor_zip_code',
    'patient_last_name',
    'patient_first_name',
    'patient_ssn',
    'patient_sex',
    'patient_address_1',
    'patient_address_2',
    'patient_city',
    'patient_state',
    'patient_zip_code',
    'principal_diagnosis_code',
    'diagnosis_code_2',
    'diagnosis_code_3',
    'diagnosis_code_4',
    'diagnosis_code_5',
    'insured_name',
    'doctor_last_name',
    'doctor_first_name',
    'doctor_npi',
    'doctor_state_lic_number',
    'pharmacist_last_name',
    'pharmacist_first_name',
    'pharmacist_lic_number',
    'pharmacist_taxonomy_code',
    'pharmacy_name',
    'pharmacy_npi',
    'pharmacy_nabp',
    'pharmacy_address_1',
    'pharmacy_address_2',
    'pharmacy_city',
    'pharmacy_state',
    'pharmacy_zip_code',
    'pharmacy_state_license_number'
]

numeric_bill_fields = [
]

date_bill_fields = [
    'bill_date',
    'payor_receive_date',
    'patient_dob',
    'payment_date',
    'doi',
    'date_of_admission',
    'date_of_discharge'
]

text_entry_fields = [
    'entry_doctor_last_name',
    'entry_doctor_first_name',
    'entry_doctor_npi',
    'entry_doctor_state_lic_number',
    'hcpcs',
    'hcpcs_paid',
    'ndc',
    'drug_name',
    'days_supply',
    'rx_number',
    'refill_number',
    'quantity',
    'eob_review_code',
    'daw',
    'repackaged_ndc'
]

numeric_entry_fields = [
    'total',
    'sales_tax',
    'state_fee',
    'insurer_paid'
]

date_entry_fields = [
    'date_of_service'
]

@reg
@mako('state_report_files.tmpl')
def files(req, res):
    page_size = 40
    try:
        page = int(req.params.get('page'))
    except (ValueError, TypeError):
        page = 1
    if page < 1:
        page = 1
    offset = (page-1)*page_size

    try:
        trans_id = int(req.params.get('trans_id'))
    except (ValueError, TypeError):
        trans_id = None
    try:
        reversal_id = int(req.params.get('reversal_id'))
    except (ValueError, TypeError):
        reversal_id = None

    cursor = R.db.mako_dict_cursor('ar/state_reporting.sql')
    if trans_id:
        cursor.files_by_trans_id(offset, page_size, trans_id)
    elif reversal_id:
        cursor.files_by_reversal_id(offset, page_size, reversal_id)
    else:
        cursor.files(offset, page_size)

    res.update({
        'files': list(cursor),
        'trans_id': trans_id,
        'reversal_id': reversal_id,
        'page': page
    })

@reg
def index(req, res):
    res.redirect("/sr_manual/add")

@reg
def delete(req, res):
    sr_file_id = req.params.get("sr_file_id")
    if not sr_file_id:
        res.redirect("/sr_manual/files")
        return
    cursor = R.db.cursor()
    cursor.execute("""
        select send_time
        from state_report_file
        where sr_file_id = %s
        """, (sr_file_id,))
    if not cursor.rowcount:
        res.redirect("/state_reporting")
        return
    send_time, = next(cursor)
    if send_time:
        R.flash("Could not delete file that has already ben sent")
        res.redirect("/sr_manual/files")
        return
    if req.params.get("remark"):
        cursor.execute("""
            update trans set sr_mark = 'Y'
            from state_report_entry
            where state_report_entry.trans_id = trans.trans_id
              and state_report_entry.sr_file_id = %s
        """, (sr_file_id,))

    cursor.execute("delete from state_report_entry where sr_file_id=%s", (sr_file_id,))
    cursor.execute("delete from state_report_bill where sr_file_id=%s", (sr_file_id,))
    cursor.execute("delete from state_report_file where sr_file_id=%s", (sr_file_id,))
    R.db.commit()
    res.redirect("/sr_manual/files")

@reg
@json
def update_srfile_note(req, res):
    sr_file_id = req.params.get('sr_file_id')
    note = ((req.params.get('note') or '').strip()) or None
    if not sr_file_id:
        res.error("no sr_file_id given")
        return
    cursor = R.db.cursor()
    cursor.execute("""
        update state_report_file set note=%s
        where sr_file_id=%s
        returning *
        """, (note, sr_file_id))
    if not cursor.rowcount:
        res.error("sr_file_id %s not found" % sr_file_id)
        return
    R.db.commit()
    res['msg'] = 'Note updated successfully'

@reg
def delete_bill(req, res):
    bill_id = req.params.get('bill_id')
    if not bill_id:
        res.redirect("/")
        return
    cursor = R.db.cursor()
    cursor.execute("""
        delete from state_report_bill where bill_id=%s
        returning sr_file_id
        """, (bill_id,))
    file_id, = next(cursor)
    R.flash("Bill %s deleted" % bill_id)
    R.db.commit()
    res.redirect("/sr_manual/report_file?sr_file_id=%s" % file_id)

@reg
@mako('sr_manual.tmpl')
def add(req, res):
    res['file_name'] = default_file_name()
    res['status_flag'] = 'P'
    res['lines'] = None

    resub_bill_id = req.params.get('resub')
    if resub_bill_id:
        bill = state_report_bill(resub_bill_id)
        if not bill:
            R.error("Invalid resubmission bill_id")
        else:
            for key in ('bill_id', 'sr_file_id', 'intermediary_id'):
                bill[key] = ''
            bill['claim_freq'] = '7'
    else:
        bill = {'bill_number': '', 'intermediary_id': ''}
        bill['lines'] = [{} for _ in range(6)]
    for k in req.params:
        bill[k] = req.params.get(k)

    res['bill'] = bill

    # show form
    if req.method != 'POST':
        return

    # do add
    frecord = _file_record(req)
    if R.has_errors():
        return

    cursor = R.db.real_dict_cursor()
    sql = util.insert_sql('state_report_file', frecord, ['*'])
    cursor.execute(sql)
    sr_file = next(cursor)
    brecord = _bill_record(req, sr_file['sr_file_id'])
    if R.has_errors():
        R.db.rollback()
        return

    sql = util.insert_sql('state_report_bill', brecord, ['*'])
    cursor.execute(sql)
    bill = next(cursor)

    # Manually entered claims have the same intermediary id as the bill id
    bill['intermediary_id'] = bill['bill_id']
    cursor.execute("""
        update state_report_bill set intermediary_id=bill_id
        where bill_id=%s
        """, (bill['bill_id'],))

    # Make lines
    bill['lines'] = []
    for i in range(1, 7):
        entry_rec = _line_record(req, i, bill['bill_id'], sr_file['sr_file_id'])
        if not entry_rec['ndc']:
            continue
        if R.has_errors():
            R.db.rollback()
            return

        entry_rec['position'] = i
        sql = util.insert_sql('state_report_entry', entry_rec, ['*'])
        cursor.execute(sql)
        line = next(cursor)
        bill['lines'].append(line)


    if not bill['lines']:
        R.error("The given bill has no lines. Provide NDC #s")
        return

    R.db.commit()
    res.redirect("/sr_manual/report_file?sr_file_id=%s", sr_file['sr_file_id'])

@reg
@mako('state_report_file.tmpl')
def report_file(req, tmpl):
    cursor = R.db.cursor()
    try:
        sr_file_id = int(req.params.get('sr_file_id'))
    except (ValueError, TypeError):
        sr_file_id = None

    try:
        bill_id = int(req.params.get('bill_id'))
    except (ValueError, TypeError):
        bill_id = None

    if bill_id and not sr_file_id:
        cursor.execute("""
            select sr_file_id from state_report_bill
            where bill_id=%s
            """, (bill_id,))
        if not cursor.rowcount:
            return
        sr_file_id, = next(cursor)


    tmpl['sr_file'] = state_report_file(sr_file_id)
    if not tmpl['sr_file']:
        raise W.HTTPNotFound("File not Found ID: %s" % sr_file_id)
    if bill_id:
        tmpl['bill'] = bill = state_report_bill(bill_id)
    else:
        tmpl['bill'] = bill = first_bill(sr_file_id)
        if bill:
            bill_id = bill['bill_id']
        else:
            bill_id = None

    cursor.execute("""
        select max(sr_file_id)
        from state_report_file
        where sr_file_id < %s
        """, (sr_file_id,))
    prev_sr_file_id, = next(cursor)
    if not prev_sr_file_id:
        prev_sr_file_id = sr_file_id
    cursor.execute("""
        select min(sr_file_id)
        from state_report_file
        where sr_file_id > %s
        """, (sr_file_id,))
    next_sr_file_id, = next(cursor)
    if not next_sr_file_id:
        next_sr_file_id = sr_file_id
    tmpl.update({
        'prev_sr_file_id': prev_sr_file_id,
        'next_sr_file_id': next_sr_file_id,
        'prev_bill_id': 0,
        'next_bill_id': 0,
        'bill_count': 0,
        'bill_index': 0
    })

    if not bill:
        return

    format_bill(bill)
    tmpl['bill_number'] = bill['bill_number']
    tmpl['original_bill_number'] = bill['original_bill_number']
    tmpl['lines'] = bill['lines']

    cursor.execute("""
        select bill_id
        from state_report_bill
        where sr_file_id = %s
        order by bill_id
        """, (sr_file_id,))
    bill_ids = [c for c, in cursor]
    if bill_id not in bill_ids:
        # mismatch of bill id and file id
        tmpl.redirect("/sr_manual/report_file?sr_file_id=%s", sr_file_id)
        return

    tmpl['bill_index'] = i = bill_ids.index(bill_id)
    tmpl['prev_bill_id'] = bill_ids[i-1]
    tmpl['next_bill_id'] = bill_ids[(i+1) % len(bill_ids)]
    tmpl['bill_count'] = len(bill_ids)

    tmpl['bill_totals'] = _bill_totals(bill['bill_id'])

@reg
def download_file(req, res):
    sr_file_id = req.params.get('sr_file_id')
    sr_file = state_report_file(sr_file_id)

    file_name = os.path.splitext(sr_file['file_name'])[0] + ".csv"
    res.headers.add("Content-Disposition", "attachment;filename=%s" % file_name)
    res.content_type = 'application/csv'

    if sr_file['contents']:
        res.write(bytes(sr_file['contents']))
    else:
        bills = state_report_bills(sr_file_id)
        for bill in bills:
            fix_submission_fields(bill)
        res.write(bishop.manual_bill_file(sr_file, bills))


def fix_submission_fields(bill):
    """ We have to fix up some fields on the bill before sending to bishop/csv file """
    bill['unique_originator_record_id'] = bill['bill_id']
    # Turn date fields into character
    for field in date_bill_fields:
        if bill[field]:
            bill[field] = bill[field].strftime("%Y%m%d")
        else:
            bill[field] = ''
    for line in bill['lines']:
        if line['date_of_service']:
            line['date_of_service'] = line['date_of_service'].strftime("%Y%m%d")
        if line['position']:
            line['line_no'] = str(line['position'])
        else:
            line['line_no'] = '1'

@reg
def delete_entry(req, res):
    srid = req.params.get('srid')
    cursor = R.db.cursor()
    cursor.execute("""
        delete from state_report_entry
        where srid=%s
        returning sr_file_id, bill_id
        """, (srid,))
    if cursor.rowcount == 0:
        res.redirect("/state_reporting")
        return
    sr_file_id, bill_id = next(cursor)
    R.db.commit()
    res.redirect("/sr_manual/report_file?sr_file_id=%s&bill_id=%s", sr_file_id, bill_id)

@reg
def send_file(req, res):
    sr_file_id = req.params.get('sr_file_id')
    sr_file = state_report_file(sr_file_id)
    bills = state_report_bills(sr_file_id)
    for bill in bills:
        fix_submission_fields(bill)

    csv_contents = bishop.manual_bill_file(sr_file, bills)
    cursor = R.db.cursor()
    cursor.execute("""
        update state_report_file set contents=%s, send_time=NOW()
        where sr_file_id=%s
        """, (csv_contents, sr_file_id))

    target_map = {
        'bishop': dict(
            prod_path = 'Inbound/%s' % sr_file['file_name'],
            test_path = 'Inbound/Test/%s' % sr_file['file_name']),
        'test': dict(
            prod_path = 'data/%s' % sr_file['file_name'],
            test_path = 'data/%s' % sr_file['file_name']),
    }
    if config.dev_mode():
        target = target_map['test']
        sftp_conn = sftp.connect('jeremy_test')
    else:
        target = target_map['bishop']
        sftp_conn = sftp.connect('bishop_production')
    if sr_file['status_flag'] == 'T':
        target_path = target['test_path']
    else:
        target_path = target['prod_path']
    with tempfile.NamedTemporaryFile(mode="a+t") as f:
        try:
            f.write(csv_contents)
            f.flush()
            sftp_conn.put(f.name, target_path)
        finally:
            sftp_conn.close()
    R.db.commit()
    R.flash("File send successfully")
    res.redirect("/sr_manual/report_file?sr_file_id=%s", sr_file_id)

def first_bill(sr_file_id):
    cursor = R.db.real_dict_cursor()
    cursor.execute("""
        select *
        from state_report_bill
        where sr_file_id = %s
        order by bill_id
        """, (sr_file_id,))
    if not cursor.rowcount:
        return None
    bill = next(cursor)
    cursor.execute("""
        select * from state_report_entry
        where bill_id=%s
        order by srid
        """, (bill['bill_id'],))
    bill['lines'] = list(cursor)
    return bill

def format_bill(bill):
    claim_freq_lookup = dict([('1', '1 - original claim'),
                              ('7', '7 - replacement'),
                              ('8', '8 - voided/canceled')])

    bill['claim_freq_fmt'] = claim_freq_lookup.get(bill['claim_freq'], bill['claim_freq'])
    if bill['icd_code']:
        bill['icd_code'] = bill['icd_code'].strip()
    else:
        bill['icd_code'] = '0'

def state_report_file(sr_file_id):
    cursor = R.db.real_dict_cursor()
    cursor.execute("""
        select *
        from state_report_file
        where sr_file_id=%s
        """, (sr_file_id,))
    if cursor.rowcount:
        return next(cursor)
    else:
        return None

def state_report_bills(sr_file_id):
    cursor = R.db.real_dict_cursor()
    # Get fields on each table because we're going to get all the data in one query
    # and split it up without a field list
    cursor.execute("select * from state_report_bill where false")
    bill_fields = dict([(c[0], True) for c in cursor.description])
    cursor.execute("select * from state_report_bill_total where false")
    bill_total_fields = dict([(c[0], True) for c in cursor.description])
    cursor.execute("select * from state_report_entry where false")
    # We've got control_number columns in both tables. We want to use the one that is in state_report_bill
    # because it goes in the BBR.
    entry_fields = dict([(c[0], True) for c in cursor.description])
    del entry_fields['control_number']

    cursor.execute("""
        select state_report_bill.*,
            state_report_bill_total.*,
            state_report_entry.srid,
            state_report_entry.create_time,
            state_report_entry.position,
            state_report_entry.sr_file_id,
            state_report_entry.trans_id,
            state_report_entry.reversal_id,
            state_report_entry.claim_freq_type_code,
            state_report_entry.bill_id,
            state_report_entry.date_of_service,
            state_report_entry.hcpcs,
            state_report_entry.hcpcs_paid,
            state_report_entry.ndc,
            state_report_entry.repackaged_ndc,
            state_report_entry.drug_name,
            state_report_entry.days_supply,
            state_report_entry.total,
            state_report_entry.sales_tax,
            state_report_entry.state_fee,
            state_report_entry.insurer_paid,
            state_report_entry.rx_number,
            state_report_entry.refill_number,
            state_report_entry.quantity,
            state_report_entry.eob_review_code,
            state_report_entry.daw,
            state_report_entry.reconciled,
            state_report_entry.entry_doctor_last_name,
            state_report_entry.entry_doctor_first_name,
            state_report_entry.entry_doctor_state_lic_number,
            state_report_entry.entry_doctor_npi
        from state_report_bill
        join state_report_entry using(bill_id)
        join state_report_bill_total using(bill_id)
        where state_report_bill.sr_file_id = %s
          or state_report_entry.sr_file_id = %s
        order by state_report_bill.bill_id, state_report_entry.srid
        """, (sr_file_id, sr_file_id))

    bills = []
    for bill_id, entries in itertools.groupby(list(cursor), lambda s: s['bill_id']):
        entries = list(entries)
        bill = dict((k, entries[0][k]) for k in bill_fields)
        for k in bill_total_fields:
            bill[k] = entries[0][k]
        bill['lines'] = []
        for e in entries:
            entry = dict((k, e[k]) for k in entry_fields)
            bill['lines'].append(entry)
        bills.append(bill)
    return bills

def state_report_bill(bill_id):
    cursor = R.db.real_dict_cursor()
    cursor.execute("""
        select *
        from state_report_bill
        where bill_id = %s
        """, (bill_id,))
    if not cursor.rowcount:
        return
    bill = next(cursor)

    cursor.execute("""
        select * from state_report_entry
        where bill_id=%s
        order by srid
        """, (bill['bill_id'],))
    bill['lines'] = list(cursor)
    return bill

def default_file_name():
    ctime = datetime.datetime.now()
    return "CPS_%s%s_0001.bbr" % (ctime.strftime("%Y%m%d%H%M%S"), ctime.microsecond / 1000)

@reg
def add_bill_entry(req, res):
    bill_id = req.params.get('bill_id')
    cursor = R.db.cursor()
    cursor.execute(util.insert_sql('state_report_entry', {'bill_id': bill_id}))
    R.db.commit()
    R.flash("Entry added. Please fill out below")
    res.redirect("/sr_manual/report_file?bill_id=%s" % bill_id)

@reg
def copy_from_trans_id(req, res):
    try:
        srid = int(req.params.get('srid'))
    except (ValueError, TypeError):
        raise W.HTTPNotFound("SRID %s" % srid)

    bill_id, sr_file_id = _ids_from_srid(srid)
    if not bill_id:
        raise W.HTTPNotFound("SRID %s" % srid)
    try:
        trans_id = int(req.params.get('trans_id'))
    except (ValueError, TypeError):
        R.flash("Trans %s not found")
        res.redirect("/sr_manual/report_file?bill_id=%s" % bill_id)
    cursor = R.db.mako_dict_cursor('ar/state_reporting.sql')
    cursor.copy_trans_to_sre(srid, trans_id)
    R.flash("transaction %s copied to SRE %s", trans_id, srid)
    res.redirect("/sr_manual/report_file?bill_id=%s" % bill_id)
    R.db.commit()

@reg
def copy_from_srid(req, res):
    try:
        srid = int(req.params.get('srid'))
    except (ValueError, TypeError):
        raise W.HTTPNotFound("SRID %s" % srid)
    bill_id, sr_file_id = _ids_from_srid(srid)
    if not bill_id:
        raise W.HTTPNotFound("SRID %s" % srid)
    try:
        from_srid = int(req.params.get('from_srid'))
    except (ValueError, TypeError):
        R.flash("SRID %s not found")
        res.redirect("/sr_manual/report_file?bill_id=%s" % bill_id)
        return

    cursor = R.db.real_dict_cursor()
    cursor.execute("""
        SELECT * FROM state_report_entry
        WHERE srid=%s
        """, (from_srid,))
    if not cursor.rowcount:
        R.flash("SRID %s not found")
        res.redirect("/sr_manual/report_file?bill_id=%s" % bill_id)
        return

    rec = next(cursor)
    del rec['srid']
    rec['bill_id'] = bill_id
    rec['sr_file_id'] = sr_file_id

    sql = util.update_sql('state_report_entry', rec, {'srid': srid})
    cursor.execute(sql)
    R.db.commit()
    R.flash("Entry copied from %s to %s " % (from_srid, srid))
    if bill_id:
        res.redirect("/sr_manual/report_file?bill_id=%s" % bill_id)
    else:
        res.redirect("/sr_manual/report_file?sr_file_id=%s" % sr_file_id)

@reg
def mark_file_sent(req, res):
    try:
        sr_file_id = int(req.params.get('sr_file_id'))
    except (ValueError, TypeError):
        return
    cursor = R.db.cursor()
    cursor.execute("""
        update state_report_file set send_time=NOW()
        where sr_file_id=%s
        """, (sr_file_id,))
    R.db.commit()
    R.flash("File %s marked as sent" % sr_file_id)
    res.redirect("/sr_manual/report_file?sr_file_id=%s" % sr_file_id)

@reg
def update_bill(req, res):
    bill_id = req.params.get('bill_id')
    sr_file_id = req.params.get('sr_file_id')

    brecord = _bill_record(req, sr_file_id)
    cursor = R.db.real_dict_cursor()
    sql = util.update_sql('state_report_bill', brecord, {'bill_id': bill_id})
    cursor.execute(sql)

    for i in range(1, 7):
        srid = req.params.get("%s-srid" % i)
        if not srid:
            continue
        entry_rec = _line_record(req, i, bill_id, sr_file_id)
        if R.has_errors():
            R.db.rollback()
            for r in R.get_errors():
                res.write("%s\n" % r)
            return
        # If an integer comes in for srid then we update that, otherwise it's a sentinel
        # string telling us to insert a new item.
        try:
            srid = int(srid)
            sql = util.update_sql('state_report_entry', entry_rec, {'srid': srid})
        except ValueError:
            sql = util.insert_sql('state_report_entry', entry_rec)
        cursor.execute(sql)

    R.db.commit()
    R.flash("Bill updated")
    res.redirect('/sr_manual/report_file?sr_file_id=%s&bill_id=%s', sr_file_id, bill_id)


def _file_record(req):
    file_name = req.params.get('file_name')
    if not file_name:
        R.error("Missing file name")
        return
    if not os.path.splitext(file_name)[1]:
        R.error("file %s has no extension." % file_name)
        return
    status_flag = req.params.get('status_flag')
    if not status_flag:
        status_flag = 'T'
    return {
        'username': R.username(),
        'file_name': file_name,
        'status_flag': status_flag,
    }


def _ids_from_srid(srid):
    cursor = R.db.cursor()
    cursor.execute("""
        select bill_id, sr_file_id
        from state_report_entry
        where srid=%s
        """, (srid,))
    if not cursor.rowcount:
        return None
    return tuple(next(cursor))

def _bill_record(req, sr_file_id):
    record = {'sr_file_id': sr_file_id}

    for field in text_bill_fields:
        record[field] = req.params.get(field) or ''
    for field in numeric_bill_fields:
        if not req.params.get(field):
            record[field] = None
        else:
            try:
                record[field] = decimal.Decimal(req.params.get(field) or '')
            except decimal.InvalidOperation:
                R.error('Invalid decimal value %r for %s', req.params.get(field), field)
    for field in date_bill_fields:
        record[field] = req.params.get(field) or None
    for field in required_bill_fields:
        if not record.get(field):
            R.error("Missing required filed %s" % field)
    return record


def _line_record(req, i, bill_id, sr_file_id):
    entry_rec = {'bill_id': bill_id, 'sr_file_id': sr_file_id}
    for field in text_entry_fields:
        entry_rec[field] = req.params.get('%d-%s' % (i, field)) or ''
    for field in date_entry_fields:
        entry_rec[field] = req.params.get('%d-%s' % (i, field)) or None
    for field in ['trans_id', 'reversal_id']:
        #XXX:TODO add reversal
        pass
    for field in numeric_entry_fields:
        v = req.params.get('%d-%s' % (i, field))
        if v:
            try:
                entry_rec[field] = decimal.Decimal(v)
            except decimal.InvalidOperation:
                R.error('Invalid decimal value %s for %s', v, field)
        else:
            entry_rec[field] = decimal.Decimal("0")
    return entry_rec


def _bill_totals(bill_id):
    c2 = R.db.real_dict_cursor()
    c2.execute("""
        select bill_total, insurer_paid_amount, item_count
        from state_report_bill_total
        where bill_id=%s
        """, (bill_id,))
    rec = c2.fetchone()
    return {
        'bill_total': rec['bill_total'],
        'insurer_paid_amount': rec['insurer_paid_amount'],
        'item_count': rec['item_count']
    }

application = reg.get_wsgi_app()
