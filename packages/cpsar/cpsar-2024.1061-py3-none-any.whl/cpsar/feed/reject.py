#!/usr/bin/env python
""" Process EHO's reject file in real time, saving records in the reject table
"""
import io
import logging; log=logging.getLogger('')

from cpsar.fwimport import create_fw_table
from .lib import run

import cpsar.runtime as R

def main():
    R.db.setup()
    run(process_lines)

def process_lines(records):
    cursor = R.db.cursor()
    buf = copy_table_buffer(records)
    create_fw_table('reject_feed', reject_file_fields(), buf)
    try:
        copy_to_reject_table(cursor)
        R.db.commit()
    finally:
        try:
            cursor.execute("DROP TABLE reject_feed")
        except:
            pass
    return iter(records)

def copy_table_buffer(records):
    lines = [r.line for r in records]
    buf = io.BytesIO()
    buf.write((b"".join(lines)))
    if not buf.getvalue():
        return iter(records)
    buf.seek(0)
    return buf

def copy_to_reject_table(cursor):
    cursor.execute_file("ar/feed_reject.sql")

def reject_file_fields():
    return [
      ('undeed_prefix', 4),
      ('reject_timestamp', 16),
      ('nabp', 7 ),
      ('date_filled_timestamp', 14),
      ('rx_nbr', 7),
      ('version', 2),
      ('group_nbr', 8),
      ('cardholder_id', 11),
      ('birth_date',  8),
      ('sex', 1),
      ('new_refill', 2),
      ('qty', 8),
      ('days_supply', 3),
      ('compound_code', 1),
      ('ndc_nbr', 11),
      ('disp_as_written', 1),
      ('cost', 8),
      ('doctor_dea_nbr', 10),
      ('date_written', 6),
      ('authorized', 2),
      ('denial_override', 2),
      ('usual_customary', 8),
      ('fee', 8),
      ('sales_tax', 8),
      ('prior_auth_nbr', 8),
      ('metric_quantity', 8),
      ('doctor_name', 30),
      ('doctor_street', 30),
      ('doctor_city', 20),
      ('doctor_state', 2),
      ('doctor_zip_code', 5),
      ('carrier_id', 10),
      ('wc_claim_nbr', 14),
      ('reject_nbr', 2),
      ('reject_code1', 2), 
      ('reject_code2', 2), 
      ('rts_sequence', 38),
      ('reject_message',  42),
      ('reject_additional1', 43),
      ('reject_additional2', 43),
      ('reject_additional3', 43),
      ('reject_additional4', 35),
      ('reject_hits_number', 12)
  ]

if __name__ == '__main__': main()
