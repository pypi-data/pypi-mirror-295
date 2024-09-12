from six import StringIO
import decimal
import functools
import locale
import logging
import os
import re
import threading
import types

import mako.template as MT
import psycopg2
import psycopg2.extras
from psycopg2 import DataError
from psycopg2.extensions import cursor as _cursor
from psycopg2.extras import RealDictCursor as _RealDictCursor

from cpsar import config

locale.setlocale(locale.LC_ALL, 'en_US.UTF8')
log = logging.getLogger('sql_debug')

class TLSDB(object):
    _conn_str = None

    def __init__(self, conn_str=None):
        self._tls = threading.local()
        self.conn_str = conn_str

    @property
    def conn_str(self):
        if self._conn_str is not None:
            return self._conn_str
        else:
            return config.ar_conn_str()

    @conn_str.setter
    def conn_str(self, value):
        self._conn_str = value
        
    def __getattr__(self, attr):
        return getattr(self._tls.conn, attr)

    def setup(self):
        log.debug("pgsql connect: %s", self.conn_str)
        try:
            self._tls.conn = psycopg2.connect(self.conn_str)
        except Exception as e:
            log.error("Could not connect to postgresql using %r: %s",
                      self.conn_str, e)
            raise

    def __nonzero__(self):
        return getattr(self._tls, 'conn', False) and True
    def __bool__(self):
        return getattr(self._tls, 'conn', False) and True

    def teardown(self):
        if hasattr(self._tls, 'conn'):
            self._tls.conn.close()
            del self._tls.conn

    def mako_cursor(self, fname):
        cursor = self._tls.conn.cursor(cursor_factory=_MakoCursor)
        cursor.load_template(fname)
        return cursor

    def mako_dict_cursor(self, fname):
        cursor = self._tls.conn.cursor(cursor_factory=_MakoDictCursor)
        cursor.load_template(fname)
        return cursor

    def cursor(self):
        return self._tls.conn.cursor(cursor_factory=_MyCursor)

    def dict_cursor(self):
        return self._tls.conn.cursor(cursor_factory=_MyDictCursor)

    def real_dict_cursor(self):
        return self._tls.conn.cursor(cursor_factory=_MyRealDictCursor)

    def log_dict_cursor(self):
        return self._tls.conn.cursor(cursor_factory=_MyLoggingDictCursor)

    def log_cursor(self):
        return self._tls.conn.cursor(cursor_factory=_MyLoggingCursor)

    def __call__(self, proc):
        """ WSGI Middleware to connect the database on request"""
        # Had t comment this out because the next app up the chain is
        # the url dispatcher from paste which strangely does not have a
        # __name__ attribute
        #@functools.wraps(proc)
        def wsgi_app(environ, start_response):
            self.setup()
            try:
                return proc(environ, start_response)
            finally:
                try:
                    self.teardown()
                except:
                    pass
        return wsgi_app

class _ExecuteFileMixIn:
    def execute_file(self, fname, args=None):
        fpath = os.path.join(config.sql_dir(), fname)
        fd = open(fpath)
        sqlbuf = fd.read(-1)
        fd.close()
        self.execute(sqlbuf, args)

class _TextTableMixIn:
    def as_text_table(self):
        cols = [d[0] for d in self.description]
        col_widths = list(map(len, cols))
        vals = []
        for rec in self:
            v = list(map(self._as_string, rec))
            lens = list(map(len, v))
            col_widths = [max(*a) for a in zip(col_widths, lens)]
            vals.append(v)
        cols = [col.replace('%', '%%') for col in cols]
        vals = [[val.replace('%', '%%') for val in v] for v in vals]

        row_fmt = " | ".join("%% %ds" % c for c in col_widths)
        row_fmt = "%s" % row_fmt
        lines = "-+-".join(["-"*c for c in col_widths])

        buf = StringIO()
        wrln  = lambda s: buf.write("%s\n" % s)
        wrln(lines)
        wrln(row_fmt % tuple(cols))
        wrln(lines)
        for v in vals:
            wrln(row_fmt % tuple(v))
        wrln(lines)
        return buf.getvalue()

    def as_expanded_text(self):
        cols = [d[0] for d in self.description]
        col_width = max(map(len, cols))
        buf = StringIO()
        for rec in self:
            buf.write("-"*80)
            buf.write("\n")
            for value, col in zip(rec, cols):
                buf.write(col.rjust(col_width))
                buf.write(" : %s\n" % self._as_string(value))
        return buf.getvalue()

    def _as_string(self, value):
        if value is None:
            return r'\N'
        elif not isinstance(value, str):
            return str(value)
        else:
            return value

class _MakoMixIn(object):
    # Set by friend PgConn class
    _tmpl = None

    # Inspection read only value
    _last_executed_sql = None

    @property
    def last_executed_sql(self):
        return self._last_executed_sql

    def load_template(self, fname):
        fpath = os.path.join(config.sql_dir(), fname)
        with open(fpath) as fd:
            self._tmpl = MT.Template(fd.read(-1))

    def __getattr__(self, defname):
        """ Used to execute a function on the template """
        if not self._tmpl:
            raise AttributeError(defname)

        def runner(self, *args, **kargs):
            kargs.update(self._mako_defaults())
            sql = self._tmpl.get_def(defname).render(*args, **kargs)
            self._last_executed_sql = sql
            super(_MakoMixIn, self).execute(sql)
            return self
        runner.__name__ = defname
        return types.MethodType(runner, self)

    def execute_template(self, **args):
        assert self._tmpl, 'Cannot call .execute() on Mako cursor without _tmpl set'
        args.update(self._mako_defaults())
        sql = self._tmpl.render(**args)
        self._last_executed_sql = sql
        self.execute(sql)
        return self

    def _mako_defaults(self):
        return {
            'e': self._escape,
            'pg_copy': self._pg_copy,
            'insert_values': self._insert_values}

    def _escape(self, value):
        return self.mogrify("%s", (value,)).decode()

    def _insert_values(self, recs):
        lines = [",".join(map(self._escape, g)) for g in recs]
        return ",\n".join("(%s)" % s for s in lines)

    def _pg_copy(self, table_name, records, cols=None):
        """ This doesnt seem to work b/c you cant put a COPY like this in the
        middle of the string
        """
        buf = StringIO()
        buf.write("COPY %s" % table_name)
        if cols:
            buf.write("(%s)" % ", ".join(cols))
        buf.write(" FROM stdin;\n")
        for rec in records:
            vals = list(map(str, rec)) #[self.mogrify("%s", (r,)) for r in rec]
            buf.write("%s\n" % "\t".join(vals))
        buf.write("\.")
        return buf.getvalue()

class _MyCursor(_cursor, _ExecuteFileMixIn, _TextTableMixIn):
    pass

class _MyDictCursor(psycopg2.extras.DictCursor, _ExecuteFileMixIn, _TextTableMixIn):
    pass

class _MyRealDictCursor(_RealDictCursor, _ExecuteFileMixIn, _TextTableMixIn):
    pass

class _MakoCursor(_MakoMixIn, _cursor, _TextTableMixIn):
    pass

class _MakoDictCursor(_MakoMixIn, psycopg2.extras.DictCursor, _TextTableMixIn):
    pass

class _MyLoggingDictCursor(_MyDictCursor):
    def execute(self, query, vars=None):
        logger = logging.getLogger('sql_debug')
        logger.info(self.mogrify(query, vars))

        try:
            psycopg2.extras.DictCursor.execute(self, query, vars)
        except Exception as exc:
            logger.error("%s: %s" % (exc.__class__.__name__, exc))
            raise
 
class _MyLoggingCursor(_MyCursor):
    def execute(self, sql, args=None):
        logger = logging.getLogger('sql_debug')
        logger.info(self.mogrify(sql, args))

        try:
            psycopg2.extensions.cursor.execute(self, sql, args)
        except Exception as exc:
            logger.error("%s: %s" % (exc.__class__.__name__, exc))
            raise

def qstr(v):
    """ I am an inferior version of cursor.mogrify """
    if isinstance(v, (tuple, list)):
        return tuple(map(qstr, v))
    if isinstance(v, dict):
        return dict((k, qstr(s)) for k, s in v.items())
    if v is None:
        return "NULL"
    else:
        if isinstance(v, str):
            # Strip out non-ascii. Don't support unicode
            v = v.encode().decode('ascii', 'ignore')
        else:
            v = str(v)
        return "'%s'" % v.replace("'", "''")


_debug_handler = None

def table_exists(conn, table_name, schema_name='public'):
    """ Does the given table exist in the database in the given schema? """
    cursor = conn.cursor()
    if config.dev_mode():
        dbname = 'bd'
    else:
        dbname = 'cpsar'
    cursor.execute("""
    SELECT EXISTS(SELECT 1 FROM information_schema.tables
              WHERE table_catalog=%s AND
                    table_schema=%s AND
                    table_name=%s )
        """, (dbname, schema_name, table_name))
    return next(cursor)[0]

def debug_sql_to_file(fpath):
    """ Send all SQL executed using the log_ cursors to the given file """
    global _debug_handler
    handler = _debug_handler = logging.FileHandler(fpath, mode='w')
    formatter = logging.Formatter('%(message)s;')
    handler.setFormatter(formatter)
    logger = logging.getLogger('sql_debug')
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

def stop_debugging_sql_to_file():
    global _debug_handler
    if _debug_handler:
        logger = logging.getLogger('sql_debug')
        logger.removeHandler(_debug_handler)
        _debug_handler = None

def scan_currency(v):
    v = re.sub('[^0-9.]', '', v)
    return decimal.Decimal(v)

def one(cursor):
    """ Grat one formatted record from the cursor. """
    return auto_format(cursor.description, cursor.fetchone())

def all(cursor):
    """ Grat one formatted record from the cursor. """
    return [auto_format(cursor.description, c) for c in cursor]

def auto_format(desc, record):
    """ Give a cursor.description and a record and we will
    automatically format the claim.
    """
    if record is None:
        return None
    type_map = {
        1082 : format_date,
        1114 : format_timestamp,
        1700 : format_currency,
        16   : format_bool
    }
    record = dict(record)
    for f in desc:
        fkey = '%s_fmt' % f.name
        value = record[f.name]
        if f.type_code in type_map:
            record[fkey] = type_map[f.type_code](value)
        elif value is None:
            record[fkey] = ''
        else:
            record[fkey] = value
    return record

def auto_format_inline(desc, record):
    if record is None:
        return
    type_map = {
        1082 : format_date,
        1114 : format_timestamp,
        1700 : format_currency,
        16   : format_bool
    }
    for f in desc:
        fkey = '%s_fmt' % f.name
        try:
            value = record[f.name]
        except KeyError:
            continue
        if f.type_code in type_map:
            record[fkey] = type_map[f.type_code](value)
        elif value is None:
            record[fkey] = ''
        else:
            record[fkey] = value

def format_date(value):
    if value:
        try:
            return value.strftime('%m/%d/%Y')
        except ValueError:
            # prior to 1900 probably
            return "??/??/????"
    else:
        return ''

def format_timestamp(value):
    if value:
        return value.strftime('%m/%d/%Y %I:%M%p')
    else:
        return ''

def format_percent(value):
    if value:
        return "%.02f%%" % (value*100)
    else:
        return "0.00%%"

def format_bool(value):
    if value is None:
        return ''
    elif value == False:
        return 'N'
    else:
        return 'Y'

def format_currency(s):
    if s is None:
        return ''
    elif not s:
        return "$0.00"
    else:
        return "$%s" % locale.format('%.2f', s, True)

def format_dollars(s):
    if s is None:
        return ''
    elif not s:
        return "$0"
    else:
        return "$%s" % locale.format('%.0f', s, True)

def execute_mako(cursor, fname, args=None):
    if args is None:
        args = {}
    fpath = os.path.join(config.sql_dir(), fname)
    with open(fpath) as fd:
        tmpl = MT.Template(fd.read())

    args['e'] =  lambda value: cursor.mogrify("%s", (value,)).decode()
    args['pg_copy'] = _pg_copy
    args['insert_values'] = functools.partial(_insert_values, cursor)

    sql = tmpl.render(**args)
    cursor.execute(sql)

def _insert_values(cursor, recs):
    e = lambda value: cursor.mogrify("%s", (value,)).decode()
    lines = [",".join(map(e, g)) for g in recs]
    return ",\n".join("(%s)" % s for s in lines)

def _pg_copy(table_name, records, cols=None):
    """ This doesnt seem to work b/c you cant put a COPY like this in the
    middle of the string
    """
    buf = StringIO()
    buf.write("COPY %s" % table_name)
    if cols:
        buf.write("(%s)" % ", ".join(cols))
    buf.write(" FROM stdin;\n")
    for rec in records:
        vals = list(map(str, rec))
        buf.write("%s\n" % "\t".join(vals))
    buf.write("\.")
    return buf.getvalue()
