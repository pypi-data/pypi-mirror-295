#!/usr/bin/env python
""" Process EHO's patient feed file in real time, loading it into the cpsar
database stage.patient_feed and processing it.
"""
import io
import logging; log=logging.getLogger('')

from six import StringIO
from itertools import groupby

import cpsar.runtime as R
from cpsar.fwimport import create_fw_table
from cpsar.util import benchmark
from .lib import run, Parser

def main():
    R.db.setup()
    run(process_lines)

def process_lines(lines):
    for action, records in groupby(lines, lambda rec: rec.action):
        if action == 'S':
            for rec in store_records(records):
                yield rec

def store_records(lines):
    processed = []
    buf = io.BytesIO()
    for line in lines:
        if line.version == '003':
            buf.write(line.payload.encode("ascii"))
        else:
            log.error("Ignoring line with unknown version %s", line.version)
        processed.append(line)

    buf.seek(0)
    cursor = R.db.cursor()
    create_fw_table('history_feed', file_layout(), buf)
    cursor.execute_file("ar/process_history_feed.sql")
    _log_activity(cursor)

    cursor.execute("""select error_msg from history_feed where error_msg is not null""")
    for c, in cursor:
        log.info("ERROR: %s" % c)

    cursor.execute("DROP TABLE history_feed")
    R.db.commit()
    return processed

def _log_activity(cursor):
    log.info("INSERT: %d, UPDATE: %d, ERROR: %d", _inserted(cursor),
        _updated(cursor), _errored(cursor))

def _inserted(cursor):
    cursor.execute("""
        select count(*) from history_feed
        where history_id is null and error_msg is null""")
    return cursor.fetchone()[0]

def _updated(cursor):
    cursor.execute("""
        select count(*) from history_feed
        where history_id is not null and error_msg is null""")
    return cursor.fetchone()[0]

def _errored(cursor):
    cursor.execute("""
        select count(*) from history_feed where error_msg is not null
        """)
    return cursor.fetchone()[0]

def file_layout():
    return [
#        ('_action', 1),
#        ('_version', 3),
        ('modify_datetime', 16),    
        ('pharmacy', 7),
        ('rx_nbr', 7),
        ('refill_nbr', 2),
        ('group_nbr', 8),
        ('auth_nbr', 7),
        ('datef', 6),
        ('cardholder_nbr', 11),
        ('birth_date', 8),
        ('doctor_dea', 10),
        ('ndc_nbr', 11),
        ('qty', 8),
        ('days_supply', 4),
        ('compound_code', 1),
        ('cost_allowed', 8),
        ('fee', 8),
        ('sales_tax', 8),
        ('copay', 8),
        ('settle_date', 6),
        ('process_fee', 4),
        ('settle_ref', 14),
        ('reversal_flag', 1),
        ('reversal_date', 6),
        ('prior_auth_nbr', 8),
        ('cost_submitted', 8),
        ('deductible', 6),
        ('date_written', 6),
        ('disp_as_written', 1),
        ('payment_date', 6),
        ('payment_ck_nbr', 6),
        ('interaction_flag', 1),
        ('protocol_originator', 1),
        ('total_submitted', 8),
        ('last_claim_ref', 7),
        ('date_processed', 6),
        ('wc_claim_nbr', 9),
        ('fm_audit_date', 6),
        ('fm_audit_time', 8),
        ('wc_date_of_injury', 8),
        ('time_processed', 6),
        ('phcy_cost_allowed', 8),
        ('phcy_fee', 8),
        ('sponsor_check_nbr', 10),
        ('tcp_txid', 10),
        ('tcp_region', 2),
        ('sponsor_check_amt', 6),
        ('time_reversed', 6),
        ('other_payer_amt', 8),
        ('rds_flag', 1),
        ('rebate_amt', 6),
        ('navitus_tier', 1),
        ('special_id', 5),
        ('refills_authorized', 2),
        ('wc_invoice_class', 1),
        ('cost_basis', 2),
        ('authorized_by', 1),
        ('level_of_effort', 2),
    ]

if __name__ == '__main__':
    main()
