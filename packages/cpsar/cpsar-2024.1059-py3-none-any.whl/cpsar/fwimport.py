""" File Import Library used by sync programs. Provides abstract base
classes for several types of text file syncronizations.

Also provides a facility to allow programs to track if they have
already processed a file or not.
"""
from builtins import map
from builtins import zip
from builtins import object
from six import StringIO
import glob
import io
import os
import re
import string
import struct
import sys

import cpsar.runtime as R
import cpsar.shell

from cpsar import pg
from cpsar.config import import_dir

###############################################################################
## Fixed width file path location functions
def path_for_resource(resource):
    return os.path.join(import_dir(), 'files', resource + ".txt")

def paths_for_glob(*pats):
    matches = []
    for pat in pats:
        exp = '%s/%s' % (import_dir(), pat)
        R.log.debug("Scanning %r for files" % exp)
        matches.extend(glob.glob(exp))
    return matches

def archive(fpath):
    """ Archive the given file. This is to be used for files that follow
    the FILE-BASE.YYYYMMDD naming convetion (like bd-transactions.YYYYMMDD)
    If the given name is not in the correct format a ValueError will be
    raised.
    """
    arc_fname = archive_fname(os.path.basename(fpath))
    if not arc_fname:
        raise ValueError('Could not determine archive zip file for %s' % fpath)

    arc_dir = "/server/corporate/bd-archive"
    arc_fpath = os.path.join(arc_dir, arc_fname)

    args = (arc_fpath, fpath)
    os.system("zip -j --move -q '%s' '%s'" % args)

def archive_fname(fname):
    """ Give the zip archive file name for the given data file """
    _fname_match = re.compile("([^\.]+)\.(\d{4})\d{4}$")
    _fname_yy_match = re.compile("([^\.]+)\.(\d{2})\d{4}$")
    mat = _fname_match.match(fname)
    base, year = '', ''
    if mat:
        base = mat.groups()[0]
        year = mat.groups()[1]
        return "%s.%s.zip" % (base, year)

    mat = _fname_yy_match.match(fname)
    if mat:
        base = mat.groups()[0]
        year = "20%s" % mat.groups()[1]
        return "%s.%s.zip" % (base, year)

    mat = re.match("^(.+?)(\d{4}).csv$", fname)
    if mat:
        base, year = mat.groups()
        return "%s.%s.zip" % (base.strip("_").strip("-"), year)

    return ''

###############################################################################
## Fixed width file parsing and SQL loading

def create_fw_table(table_name, fields, fd, cleanup_record=None, pk_field=None):
    """ Create a temporary table in the database that contains the 
    textual data from the fd file. Each column in the table is a VARCHAR
    of the specific width.

    Columns are given in the fields argument, which is a list of pairs
    (column_name, length).

    The length is the number of bytes in the data file to read for that
    particular column.

    if pk_field is given as a string, a column named id_field is created
    as a bigserial auto incrementing field to give a pk.
    """
    cursor = R.db.cursor()
    cursor.execute(create_table_sql(table_name, fields, pk_field))

    field_names = [f[0] for f in fields]
    cursor.copy_from(fw_table_buffer(fields, fd, cleanup_record), table_name, columns=field_names)
    R.db.commit()

def create_table_sql(table_name, fields, pk_field=None, temp=True):
    create_sql = StringIO()
    sql_frags = []
    if temp:
        create_sql.write("CREATE TEMP TABLE %s (" % table_name)
    else:
        create_sql.write("CREATE TABLE %s (" % table_name)
    if pk_field:
        sql_frags.append("%s BIGSERIAL PRIMARY KEY" % pk_field)
    for field, width in fields:
        sql_frags.append("%s VARCHAR(%d)" % (field, width))
    create_sql.write(",\n".join(sql_frags))
    create_sql.write(")")
    # This doesn't work because the transactions get commited beforehand
    #if temp:
    #    create_sql.write(" ON COMMIT DELETE ROWS")
    return create_sql.getvalue()

def fw_table_buffer(fields, fd, cleanup_record=None):
    if cleanup_record is None:
        cleanup_record = _copy_scrubbed_record

    copy_data = io.BytesIO()
    widths = [f[1] for f in fields]
    fmtstring = ''.join('%ds' % f for f in widths)
    correct_linelen = sum(widths)
    parse = struct.Struct(fmtstring).unpack_from
    for idx, line in enumerate(fd):
        line_no = idx + 1
        if len(line) < correct_linelen:
            raise ParseError('line %s is %s bytes, excepted %s bytes: %r' % (
                line_no, len(line), correct_linelen, line))
        record = parse(line)
        record = cleanup_record(record)
        copy_data.write(b"\t".join(record))
        copy_data.write(b"\n")

    copy_data.seek(0)
    return copy_data

class ParseError(Exception):
    pass

class UpdateInsertProgram(cpsar.shell.Program):
    """ An SQL update program that checks against a set of keys if the record
    needs to be updated or if not found, inserted.
    """
    resource = ''
    """ The resource the data is imported from. Subclasses must override. """

    parser = None
    """ The parser used to parse the resource. Must implement reclib.IParser.
    If no fields are set and no _scan_record implemented, the field names
    must match the column names of the table. 
    Subclasses must override. """

    table_name = ''
    """ The table to erase and reload. Subclasses must override.  """

    keys = None
    """ A list of tuples which represent the values that are already in the
    table and should be updated, not inserted. If None are provided, the
    _build_keys() method will be invoked once to populate them.
    """

    key_fields = None
    """ A list of fields from the record that will provide the key to match
    against keys. Subclasses must override.
    """

    non_key_fields = None
    """  Fields that are not keys that should be updated. If not given,
    they will be calculated as all keys in the first record that are not
    in key_fields.
    """

    _insert_fields = None
    """ All the fields inserted. These are calculated as key_fields +
    non_key_fields """

    @property
    def insert_fields(self):
        if self._insert_fields is None:
            self._insert_fields = self.key_fields + self.non_key_fields
        return self._insert_fields

    def setup_options(self):
        super(UpdateInsertProgram, self).setup_options()
        self.add_option('-s', '--sql-file', help='File path to dump the SQL '
            'that is ran on the database. Added for debugging purposes when '
            'the SQL fails.')

    def main(self):
        self._in_file = open(self._load_fpath, 'r')

        self._sqlbuf = StringIO()
        for record in self.parser.parse_iter(self._in_file):
            self._write_sql(record)

        R.log.debug(self._sqlbuf.getvalue())
        if self.opts.sql_file:
            f = open(self.opts.sql_file, 'w')
            f.write(self._sqlbuf.getvalue())
            f.close()
        cursor = R.db.cursor()
        cursor.execute(self._sqlbuf.getvalue())
        if not self.opts.dry_run:
            R.db.commit()

    ## Overridable
    @property
    def _load_fpath(self):
        """ The file that we are loading into the table """
        return path_for_resource(self.resource)

    def _write_sql(self, record):
        if record.errors:
            R.log.error(record.format_errors())
            return

        if not self._scan_record(record):
            return

        if self._key_exists(record):
            self._write_update_sql(record)
        else:
            self._write_insert_sql(record)

    def _scan_record(self, record):
        """ Scan record, fixing any broken data, before the SQL is
        generated. Common operations include formatting values,
        removing fields that aren't inserted and added new
        computed fields. If _scan_record returns False, the
        record is not inserted.
        """
        return True

    def _key_exists(self, record):
        if self.keys is None:
            self._build_keys()
        if self.non_key_fields is None:
            self._build_non_key_fields(record)
        key = tuple(record[k] for k in self.key_fields)
        R.log.debug("Checking for key %s", key)
        return key in self.keys

    def _build_keys(self):
        """ Populate self.keys with a list of tuples of existing records.
        """
        sql = "SELECT %s FROM %s" % (", ".join(self.key_fields), self.table_name)
        cursor = R.db.cursor()
        cursor.execute(sql)
        self.keys = list(map(tuple, cursor))
        R.log.info("Build key map with %s entries", len(self.keys))

    def _build_non_key_fields(self, record):
        """ Populate self.non_key_fields """
        self.non_key_fields = [k for k in list(record.keys()) if k not in self.keys]

    def _write_update_sql(self, record):
        self._sqlbuf.write("UPDATE %s SET " % self.table_name)

        vals = _get_sql_vals(record, self.non_key_fields)
        ufields = ["%s=%s" % x for x in zip(self.non_key_fields, vals)]
        ufields = ", ".join(ufields)

        vals = _get_sql_vals(record, self.key_fields)
        mfields = ["%s=%s" % x for x in zip(self.key_fields, vals)]
        mfields = " AND ".join(mfields)

        self._sqlbuf.write("%s WHERE %s;\n" % (ufields, mfields))
        R.log.debug("UPDATE for %s", mfields)

    def _write_insert_sql(self, record):
        self._sqlbuf.write("INSERT INTO %s " % self.table_name)
        self._sqlbuf.write("(%s) VALUES (" % ", ".join(self.insert_fields))
        vals = _get_sql_vals(record, self.insert_fields)
        self._sqlbuf.write(", ".join(vals))
        self._sqlbuf.write(");\n")

        kv = list(zip(self.insert_fields, vals))
        kv = ["%s=%s" % v for v in kv]
        kv = ", ".join(kv)
        R.log.debug("INSERT for %s" % kv)

def _get_sql_vals(record, fields):
    """ Retrieve a list of values suitable for SQL for the given fields.
    We handle escaping here. """
    vals = [record.get(v, None) for v in fields]
    vals = list(map(_to_none, vals))
    return list(map(pg.qstr, vals))

def _to_none(x):
    """ We don't allow empty strings into the database. We insert NULLs instead
    """
    if hasattr(x, 'strip') and x.strip() == '':
        return None
    else:
        return x

class ClearInsertProgram(cpsar.shell.Program):
    """ This type of program erases everything in a table and then
    reinserts all of the data. It is expected to be subclasses and
    selectively overridden.
    """

    resource = ''
    """ The resource the data is imported from. Subclasses must override. """

    parser = None
    """ The parser used to parse the resource. Must implement reclib.IParser.
    If no fields are set and no _scan_record implemented, the field names
    must match the column names of the table. 
    Subclasses must override. """

    table = ''
    """ The table to erase and reload. Subclasses must override.  """

    table_fields = None
    """ The fields parsed from the resouce that are to be inserted. If not
    given, then the keys in the first record returned will be used. If
    a record does not have a particular field, NULL will be inserted.
    """

    _written_sql_insert_header = False

    def main(self):
        """ Application procedure """
        assert self.table_name, "derived classes must override table attribute"

        self._in_file = open(path_for_resource(self.resource), 'r')

        self._sqlbuf = StringIO()
        self._sqlbuf.write("TRUNCATE %s;\n" % self.table_name)

        for record in self.parser.parse_iter(self._in_file):
            self._write_insert_sql(record)

        self._cursor = R.db.cursor()
        self._cursor.execute(self._sqlbuf.getvalue())
        if not self.opts.dry_run:
            R.db.commit()

    def _write_insert_sql(self, record):
        """ Write the SQL to self._sqlbuf for the given record. """
        if record.errors:
            R.log.error(record.format_errors())
            return

        if not self._scan_record(record):
            return

        if not self.table_fields:
            self.table_fields = list(record.keys())
            
        if not self._written_sql_insert_header:
            field_frag = ", ".join(self.table_fields)
            self._sqlbuf.write("INSERT INTO %s (%s)" % (
                self.table_name, field_frag))
            self._sqlbuf.write(" VALUES ")
            self._written_sql_insert_header = True
        else:
            self._sqlbuf.write(", ")
        values = [record.get(f, None) for f in self.table_fields]
        values = [pg.qstr(v) for v in values]
        values = ", ".join(values)
        self._sqlbuf.write("(%s)\n" % values)

    def _scan_record(self, record):
        """ Scan record, fixing any broken data, before the SQL is
        generated. Common operations include formatting values,
        removing fields that aren't inserted and added new
        computed fields. If _scan_record returns False, the
        record is not inserted.
        """
        return True

class FileImporter(cpsar.shell.Program):
    """ Importer specification that uses a file on disk in the
    import directory
    """
    resource = ''

    parser = None

    insert_sql = None
    insert_params = None
    update_sql = None
    update_params = None

    _cursor = None

    def main(self):
        self.in_file = open(path_for_resource(self.resource), 'rb')

        self._cursor = R.db.cursor()
        for idx, record in enumerate(self.parser.parse_iter(self.in_file)):
            self.line_no = line_no = idx + 1
            self._load_record(record)
        R.db.commit()

    def _load_record(self, record):
        """ Load the given record into the database. """
        if record.errors:
            R.log.error(record.format_errors())
            return

        if not self.record_scan(record):
            return

        if self.update_params:
            uparams = [record[r] for r in self.update_params]
            uparams = tuple(uparams)
            self._execute(self.update_sql, uparams)

        if not self.update_params or not self._cursor.rowcount:
            if self.insert_log:
                R.log.info(self.insert_log % record)
            iparams = [record[r] for r in self.insert_params]
            iparams = tuple(iparams)
            self._execute(self.insert_sql, iparams)
        elif self.update_log:
            R.log.info(self.update_log % record)

    def _execute(self, sql, params):
        """ Run a query and give decent error reporting """
        try:
            self._cursor.execute(sql, params)
        except:
            R.log.error("Error on line %s", self.line_no)
            R.log.exception("Error running %s", sql % params)
            raise

    def record_scan(self, record):
        """Override me to update record before loading. Return False if the
        record is not to be loaded.
        """
        return True

class FWParser(object):
    """ fast, unsmart string parser that implements partial interface
    of reclib parser
    """

    def __init__(self, fields):
        self._field_names = [f[0] for f in fields]
        self.fields = fields

    @property
    def field_names(self):
        return self._field_names

    def parse_iter(self, fd):
        """ Parse the contents of the file-like object into records
        """
        for line in fd:
            yield self._parse_line(line)

    def _parse_line(self, data):
        stream = StringIO(data)
        stream.seek(0)
        out = Record()
        for field, width in self.fields:
            s = stream.read(width)
            s = s.rstrip()
            R.log.debug('Read %r for field %s(%s)', s, field, width)
            out[field] = s
        self._none_nulls(out)
        return out

    def _none_nulls(self, record):
        for k, v in list(record.items()):
            if v == '':
                record[k] = None

class Record(dict):
    ## This parser doesn't support error matching, but we maintain the
    ## reclib.parse.fw.Parser interface
    errors = None
    def format_errors(self):
        return ''

###############################################################################
class ListFWParser(object):
    """ List-based record parsing instead of dictionary. This is much faster.
    Use for feed and load programs. """
    def __init__(self, fields):
        self._field_names = [f[0] for f in fields]
        widths = [f[1] for f in fields]
        fmtstring = ''.join('%ds' % f for f in widths)
        self._parse = struct.Struct(fmtstring).unpack_from

    @property
    def field_names(self):
        return self._field_names

    def parse_file(self, fd):
        return list(map(self._parse, fd))

def copybuf_from_list(records, delim="\t"):
    """ Convert an iterable of lists (as returned from ListFWParser.parse_file)
    into a copy buffer suitable for psycopg2 copy_from """
    buf = io.BytesIO()
    for record in records:
        record = _copy_scrubbed_record(record)
        buf.write(b"\t".join(record))
        buf.write(b"\n")
    buf.seek(0)
    return buf

def _copy_scrubbed_record(record):
    """ Scrub out all of the values in the record that
    SQL COPY command does not like, and convert
    """
    nrecord = []
    for value in record:
        value = value.rstrip()
        if b"\x00" in value:
            value = value.replace("\x00", "")
        if b"\t" in value:
            value = value.replace("\t", " ")
        # If the string ends in \ then the tab after it will be escaped and
        # this will throw off the column numbers
        if b"\\" in value:
            value = value.replace(b"\\", b"\\\\")
        if not value:
            value = b"\\N"
        nrecord.append(value)
    return nrecord

if __name__ == '__main__':
    for fpath in sys.argv[1:]:
        if os.path.exists(fpath):
            archive(fpath)
