#!/usr/bin/env python
""" Process EHO's blue history feed file in real time, loading it into the cpsar
database stage.blue_history_feed table and processing it.
"""
import logging; log=logging.getLogger('')
import time
import sys

from six import StringIO
from itertools import groupby

import cpsar.runtime as R
from .lib import run, Parser

def main():
    R.db.setup()
    run(process_lines)

def dump_feed_file():
    """ Debug procedure. replace call to main with this at bottom to
    analysis feed file. """
    fpath = sys.argv[1]
    parser = history_feed_parser()
    for line in open(fpath):
        payload = line[4:]
        rec = parser.parse(payload)
        place = 5
        print('len(line) -> %s' % len(line))
        for field in parser._fields:
            print(place, '-', place+field[1], str(field).rjust(30), repr(rec[field[0]]))
            place = place + field[1]

def process_lines(lines):
    for action, records in groupby(lines, lambda rec: rec.action):
        if action == 'S':
            for rec in store_records(records):
                yield rec

def store_records(lines):
    parser = history_feed_parser()
    copy_file = StringIO()
    processed = []
    for line in lines:
        record = parser.parse(line.payload)
        log.debug("Reading text record %(group_nbr)s:%(auth_nbr)s" % record)
        values = [record[f] or '' for f in feed_fields()]
        copy_file.write("\t".join(values))
        copy_file.write("\n")
        processed.append(line)
    copy_file.seek(0)
    cursor = R.db.cursor()
    log.info("Copying %s records to stage.blue_history_feed", len(processed))
    cursor.copy_from(copy_file, 'stage.blue_history_feed', columns=feed_fields())
    # Forget the ones that don't have valid group numbers like EHO's patient records.

    cursor.execute("""
        DELETE FROM stage.blue_history_feed WHERE group_nbr NOT IN
            (SELECT group_number FROM client)
        """)
    if cursor.rowcount:
        log.info("Cleaned out %s stage.blue_history_feed records that are not CPS group",
            cursor.rowcount)
    R.db.commit()
    start = time.time()
    cursor.execute("SELECT process_blue_history_feed()")
    rt = time.time() - start
    log.info("Processed stage.blue_history_feed records in %.04f secs" % rt)
    R.db.commit()
    return processed

def feed_fields():
    return [
        'group_nbr', 
        'auth_nbr', 
        'add_on',
        'tx_type', 
        'awp',
        'sfs']

def history_feed_parser():
    return Parser([
        ('modify_datetime', 16),
        ('group_nbr',        8),
        ('auth_nbr',         7),
        ('add_on',           8),
        ('tx_type',          2),
        ('awp',              8),
        ('sfs',              8),
        ('lic_state',        2),
        ('lic_number',      20) 
    ], '002')

if __name__ == '__main__':
    main()
