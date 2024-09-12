import logging; log=logging.getLogger('')
from six import StringIO
from itertools import groupby

import cpsar.runtime as R
from cpsar.fwimport import create_fw_table
from .lib import Parser, run

def process_lines(lines):
    proc_map = {'S': store_records, 'D': delete_records}
    for action, records in groupby(lines, lambda rec: rec.action):
        if action not in proc_map:
            continue
        proc = proc_map[action]
        for rec in proc(records):
            yield rec

def store_records(lines):
    lines = list(lines)
    parser = key_parser()
    copy_file = StringIO()
    copy_file.write("".join(x.payload for x in lines))
    copy_file.seek(0)
    create_fw_table('doctor_key_feed', parser.fields, copy_file,
                    pk_field='doctor_key_feed_id')
    cursor = R.db.cursor()
    for rec in lines:
        log.debug('doctor_key STORE %r' % rec.payload[16:26])

    cursor.execute_file('ar/process_doctor_key_feed.sql')
    cursor.execute("DROP TABLE doctor_key_feed")
    R.db.commit()
    return lines

def delete_records(lines):
    cursor = R.db.cursor()
    parser = key_parser()
    for line in lines:
        rec = parser.parse(line.payload)
        log.debug("doctor_key DELETE %r", rec['doc_key'])
        
        # Remove references to the doctor_id
        cursor.execute("""
        UPDATE trans SET doctor_id=NULL
        FROM cobol.doctor_key
        WHERE cobol.doctor_key.doctor_id=trans.doctor_id AND
              cobol.doctor_key.doc_key=%s AND
              (trans.doctor_dea_number = doctor_key.doc_key OR
               trans.doctor_npi_number = doctor_key.doc_key)
              """, (rec['doc_key'],))

        # Remove references to the doctor_id
        cursor.execute("""
        UPDATE history SET doctor_id=NULL
        FROM cobol.doctor_key
        WHERE cobol.doctor_key.doctor_id=history.doctor_id AND
              cobol.doctor_key.doc_key=%s AND
              (history.doctor_dea_number = doctor_key.doc_key OR
               history.doctor_npi_number = doctor_key.doc_key)
              """, (rec['doc_key'],))
        cursor.execute("DELETE FROM cobol.doctor_key WHERE doc_key=%s",
                       (rec['doc_key'],))
        yield line
    R.db.commit()

def key_parser():
    return Parser([
        ('modify_datetime', 16),    
        ('doc_key',  10),
        ('doctor_id', 8)],
        '001')

if __name__ == '__main__':
    R.db.setup()
    run(process_lines)
