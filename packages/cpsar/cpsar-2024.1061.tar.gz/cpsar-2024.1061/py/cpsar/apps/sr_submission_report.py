import time

from cpsar import controls
import cpsar.runtime as R
import cpsar.wsgirun as W

from cpsar import db
from cpsar import util
from cpsar.pg import qstr
from cpsar.sr import bishop
from cpsar.wsgirun import json, mako, wsgi

@wsgi
@mako('sr_submission_report.tmpl')
def application(req, res):
    search_terms = [
        'trans_id', 'bishop_number', 'source_ref', 'ctime', 'begin_send_date',
        'end_send_date', 'patient_first_name', 'patient_last_name',
        'incoming_file_count',
        'claim_number']
    params = res['params'] = {}
    for t in search_terms:
        v = req.params.get(t)
        if v:
            params[t] = v
        else:
            params[t] = None

    for d in ['begin_send_date', 'end_send_date']:
        if not params[d]:
            params[d] = time.strftime("%Y-%m-%d")

    if not params:
        return
    if req.method != 'POST':
        return

    cursor = R.db.dict_cursor()
    cursor.execute("""
    with agg as (
        select state_report_bill.sr_file_id,
            count(distinct load_file.file_id) as incoming_file_count,
            array_accum(distinct bishop_bsr.bsr_message) as bsr_messages
        from state_report_bill
        left join state_report_entry using(bill_id)
        left join bishop_bsr on bishop_bsr.bill_id = state_report_bill.bill_id
        left join load_file on bishop_bsr.file_id = load_file.file_id
        group by state_report_bill.sr_file_id
    ),
    load_agg as (
        select load_file.file_id,
            array_accum(distinct bishop_bsr.bsr_message) as bsr_messages
        from load_file
        left join bishop_bsr using(file_id)
        group by load_file.file_id
    )

    select
       state_report_file.sr_file_id,
       state_report_file.file_name as outbound_file_name,
       state_report_file.create_time as outbound_create_time,
       state_report_bill.bill_id as outbound_bill_id,
       state_report_bill.control_number as outbound_control_number,
       to_char(state_report_file.send_time, 'YYYY-MM-DD') as outbound_send_date,
       load_file.name as incoming_file_name,
       load_file.file_id as incoming_file_id,
       to_char(load_file.scan_time, 'YYYY-MM-DD') as incoming_scan_time,
       to_char(load_file.load_time, 'YYYY-MM-DD') as incoming_load_time,
       agg.incoming_file_count,
       load_agg.bsr_messages

    from state_report_bill
    join state_report_file on state_report_bill.sr_file_id = state_report_file.sr_file_id
    join agg on state_report_bill.sr_file_id = agg.sr_file_id
    left join bishop_bsr on bishop_bsr.bill_id = state_report_bill.bill_id
    left join load_file on bishop_bsr.file_id = load_file.file_id
    left join load_agg on load_file.file_id = load_agg.file_id
    where state_report_file.send_time::date between %(begin_send_date)s::date and %(end_send_date)s::date
    order by state_report_file.sr_file_id
    """, params)

    res['fields'] = [c[0] for c in cursor.description]
    res['results'] = results = []

    for c in cursor:
        if params['incoming_file_count'] == '0' and c['incoming_file_count'] != 0:
            continue
        if params['incoming_file_count'] == '1' and c['incoming_file_count'] != 1:
            continue
        if params['incoming_file_count'] == '2' and c['incoming_file_count'] != 2:
            continue
        if params['incoming_file_count'] == '2+' and c['incoming_file_count'] <= 2:
            continue
        results.append(c)

    if not results:
        R.error("No matching records found")
