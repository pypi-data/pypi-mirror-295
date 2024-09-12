""" Process EHO's patient feed file in real time, loading it into the cpsar
database stage.patient_feed and processing it.
"""
import logging; log=logging.getLogger('')
import io
from six import StringIO
from itertools import groupby
import time

from .lib import run, Parser
import cpsar.runtime as R

def main():
    R.db.setup()
    run(process_lines)

def process_lines(lines):
    for action, records in groupby(lines, lambda rec: rec.action):
        if action == 'S':
            for rec in store_records(records):
                yield rec

def store_records(lines):
    parser = patient_feed_parser()
    copy_file = io.BytesIO()
    processed = []
    for line in lines:
        if line.version != '002':
            log.error("Ignoring line with unknown version %s", line.version)
            processed.append(line)
            continue

        record = parser.parse(line.payload.encode())
        log.debug("Reading text record %(group_nbr)s:%(dob)s:%(cardholder_nbr)s "
                 "%(first_name)s %(last_name)s" % record)
        values = [record[f] or b'' for f in feed_fields()]
        values = [v.replace(b"\\", b"\\\\") for v in values]
        outline = b"\t".join(values)
        copy_file.write(outline)
        copy_file.write(b"\n")
        processed.append(line)
    copy_file.seek(0)
    cursor = R.db.cursor()
    log.info("Copying %s records to stage.patient_feed", len(processed))
    cursor.copy_from(copy_file, 'stage.patient_feed',
                     columns=patient_feed_fields())
    # Forget the ones that don't have valid group numbers like EHO's patient records.
    cursor.execute("""
        DELETE FROM stage.patient_feed WHERE group_number NOT IN
            (SELECT group_number FROM client
             UNION
             SELECT group_number FROM mjoseph.group_info
             UNION
             SELECT group_number FROM sunrise.group_info
             UNION
             SELECT group_number FROM msq.group_info
             )
        """)
    log.info("Cleaned out %s stage.patient_feed records that are not CPS patients",
        cursor.rowcount)
    start = time.time()
    cursor.execute("SELECT process_patient_feed()")
    rt = time.time() - start
    log.info("Processed stage.patient_feed records in %.04f secs" % rt)
    R.db.commit()
    return processed

def feed_fields():
    return [ffield for ffield, tfield in table_feed_map()]

def patient_feed_fields():
    return [tfield for ffield, tfield in table_feed_map()]

def table_feed_map():
    return [
        # text field    table field
        ('first_name', 'first_name'),
        ('last_name', 'last_name'),
        ('cardholder_nbr', 'ssn'),
        ('dob', 'dob'),
        ('group_nbr', 'group_number'),
        ('special_id', 'division_code'),
        ('status', 'status'),
        ('sex', 'sex'),
        ('effective_date', 'effective_date'),
        ('expiration_date', 'expiration_date'),
        ('phcy_message_sw', 'phcy_message_sw'),
        ('print_card', 'print_card')]

def patient_feed_parser():
    return Parser([
        ('modify_datetime', 16),        # 0-15
        ('group_nbr', 8),               # 16-23
        ('cardholder_nbr', 11),         # 24-35
        ('dob', 8),                     # 36-44
        ('last_name', 15),              # 45-60
        ('first_name', 12),             # 61-73
        ('middle_init', 1),
        ('zip_code', 5),
        ('sex', 1),
        ('relationship', 1),
        ('status', 1),
        ('effective_date', 6),
        ('expiration_date', 6),
        ('_history', 1160),
        ('special_id', 15),
        ('ytd_deductible', 6),
        ('ytd_benefit', 8),
        ('medical_total', 10),
        ('outside_ytd_deductible', 6),
        ('outside_ytd_benefit', 8),
        ('special_copay', 5),
        ('dues', 6),
        ('referred_to_mail_order', 1),
        ('dur_leve_2_sw', 1),
        ('mtd_benefit_cap', 6),
        ('mtd_benefit_amt', 8),
        ('alternate_insurance', 1),
        ('smoke_count', 1),
        ('_include_data', 492),
        ('include_expire_date', 6),
        ('_exclude_data', 492),
        ('iod', 7),
        ('print_card', 1),
        ('last_claim_ref', 7),
        ('allow_1k_med', 1),
        ('prior_auth_form', 10),
        ('exclude_formulary_sw', 1),
        ('rds_start_date', 8),
        ('hicn', 11),
        ('language', 1),
        ('erx_packet_mailed', 1),
        ('benefit_code', 3),
        ('required_nabp', 7),
        ('required_dea', 10),
        ('script_count', 4),
        ('days_supply', 4),
        ('ssan', 10),
        ('catastrophic', 1),
        ('telephonic_code', 2),
        ('restricted_flag', 1),
        ('ignore_inactive_wc', 1),
        ('ignore_wc_ed', 1),
        ('new_source_code', 1),
        ('new_date', 6),
        ('phcy_message_sw', 1),
        ('last_dme_claim_ref', 6),
        ('rds_cms_approved', 1),
        ('deceased_flag', 1),
        ('invoice_class', 24),
        ('diagnosis', 30),
        ('allow_compound', 1),
        ('fm_audit_inits', 10)
    ], '002')

if __name__ == '__main__':
    main()
