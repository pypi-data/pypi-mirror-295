import logging; log=logging.getLogger('')
from six import StringIO
from itertools import groupby

import cpsar.runtime as R
from cpsar.fwimport import create_fw_table

from .lib import Parser, run

def process_lines(lines):
    proc_map = {
        ('S', '001'): store_records,
        ('S', '002'): store_records_2,
        ('S', '003'): store_records_3,
        ('D', '001'): delete_records,
        ('D', '002'): delete_records,
        ('D', '003'): delete_records,
    }
    for k, records in groupby(lines, lambda rec: (rec.action, rec.version)):
        if k not in proc_map:
            continue
        proc = proc_map[k]
        for rec in proc(records):
            yield rec

def store_records(lines):
    lines = list(lines)
    parser = doctor_parser()
    copy_file = StringIO()
    copy_file.write("".join(x.payload for x in lines))
    copy_file.seek(0)
    create_fw_table('doctor_feed', parser.fields, copy_file,
                    pk_field='doctor_feed_id')
    cursor = R.db.cursor()
    log.info("Copying %s records to doctor_feed", len(lines))
    cursor.execute_file('ar/process_doctor_feed.sql')
    cursor.execute("DROP TABLE doctor_feed")
    R.db.commit()
    return lines

def store_records_2(lines):
    parser = Parser([
            ('modify_datetime', 16),
            ('doctor_id', 8),
            ('name',  60),
            ('status', 1 ),
            ('bac', 1),
            ('bac_description', 30),
            ('drug_schedule', 15),
            ('expiration_date', 8),
            ('address_1', 40),
            ('address_2', 40),
            ('address_3', 40),
            ('city', 30),
            ('state', 2),
            ('zip_code', 10),
            ('phone', 15),
            ('specialty', 50),
            ('med_school', 100),
            ('graduation_yr', 4),
            ('last_name', 30),
            ('first_name', 20)
        ], '002')

    lines = list(lines)
    copy_file = StringIO()
    copy_file.write("".join(x.payload for x in lines))
    copy_file.seek(0)
    create_fw_table('doctor_feed', parser.fields, copy_file,
                    pk_field='doctor_feed_id')
    cursor = R.db.cursor()
    log.info("Copying %s records to doctor_feed", len(lines))
    cursor.execute_file('ar/process_doctor_feed_2.sql')
    cursor.execute("DROP TABLE doctor_feed")
    R.db.commit()
    return lines

def store_records_3(lines):
    parser = Parser([
            ('modify_datetime', 16),
            ('doctor_id', 8),
            ('name',  60),
            ('status', 1 ),
            ('bac', 1),
            ('bac_description', 30),
            ('drug_schedule', 15),
            ('expiration_date', 8),
            ('address_1', 40),
            ('address_2', 40),
            ('address_3', 40),
            ('city', 30),
            ('state', 2),
            ('zip_code', 10),
            ('phone', 15),
            ('specialty', 50),
            ('med_school', 100),
            ('graduation_yr', 4),
            ('last_name', 30),
            ('first_name', 20),
            ('review_date', 8),
            ('fax', 15)
        ], '003')

    lines = list(lines)
    copy_file = StringIO()
    copy_file.write("".join(x.payload for x in lines))
    copy_file.seek(0)
    create_fw_table('doctor_feed', parser.fields, copy_file,
                    pk_field='doctor_feed_id')
    cursor = R.db.cursor()
    log.info("Copying %s records to doctor_feed", len(lines))
    cursor.execute_file('ar/process_doctor_feed_3.sql')
    cursor.execute("DROP TABLE doctor_feed")
    R.db.commit()
    return lines

def delete_records(lines):
    cursor = R.db.cursor()
    parser = doctor_parser()
    for line in lines:
        rec = parser.parse(line.payload)
        cursor.execute("DELETE FROM cobol.doctor WHERE doctor_id=%s",
                       (rec['doctor_id'],))
        log.debug("deleting %s", rec['doctor_id'])
        yield line
    R.db.commit()

def doctor_parser():
    return Parser([
            ('modify_datetime', 16),    
            ('doctor_id', 8),
            ('name',  60),
            ('status', 1 ),
            ('bac', 1),
            ('bac_description', 30),
            ('drug_schedule', 15),
            ('expiration_date', 8),
            ('address_1', 40),
            ('address_2', 40),
            ('address_3', 40),
            ('city', 30),
            ('state', 2),
            ('zip_code', 10),
            ('phone', 15),
            ('specialty', 50),
            ('med_school', 100),
            ('graduation_yr', 4)
        ], '001')

if __name__ == '__main__':
    R.db.setup()
    run(process_lines)
