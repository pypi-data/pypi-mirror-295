""" The big utility module. Throw your helper classes and procedures in here!

"""
from typing import List
import subprocess
import csv
import datetime
import decimal
try:
    import email.utils as eutils
except ImportError:
    import email.Utils as eutils
import io
import logging
import os
import re
import smtplib
import sys
import time
import traceback
import urllib.request, urllib.parse, urllib.error

from decimal import Decimal, ROUND_HALF_UP
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from functools import partial

import mako.lookup as ML
import pexpect

from mako.exceptions import html_error_template as _html_error_template
from mako.exceptions import TopLevelLookupException

from cpsar import config

log = logging.getLogger('')

def parse_currency(value):
    pvalue = re.sub("[^\d\.\-]", "", value)
    try:
        return decimal.Decimal(pvalue)
    except decimal.InvalidOperation:
        raise ParseError("Invalid currency amount %s" % value)

class ParseError(Exception):
    pass

def parse_american_date(value):
    try:
        val = time.strptime(value, '%m/%d/%Y')
    except ValueError:
        raise ParseError("Invalid date value %s. Expected MM/DD/YYYY" % value)
    return datetime.date(*val[:3])

def parse_date(s, fmt=None):
    # type: (str, List[str]) -> datetime.date
    """ Converts a string into a date object, trying numerous different formats
    Returns None if unparsable.
    """
    if fmt is None:
        fmt = ["%Y%m%d", "%Y-%m-%d", "%y%m%d", "%m/%d/%Y"]
    elif not isinstance(fmt, list):
        fmt = [fmt]

    if s is None:
        return None

    for f in fmt:
        try:
            tup = time.strptime(s, f)[:3]
            return datetime.date(*tup)
        except ValueError:
            continue

def parse_date2(s: str, fmt: List[str]=None) -> datetime.date:
    """ Converts a string into a date object, trying numerous different formats
    Returns None if unparsable.
    """
    if fmt is None:
        fmt = ["%Y%m%d", "%Y-%m-%d", "%y%m%d", "%m/%d/%Y"]
    elif not isinstance(fmt, list):
        fmt = [fmt]

    if s is None:
        return None

    for f in fmt:
        try:
            tup = time.strptime(s, f)[:3]
            return datetime.date(*tup)
        except ValueError:
            continue

def last_day(d, day_name):
    days_of_week = ['sunday','monday','tuesday','wednesday',
                        'thursday','friday','saturday']
    target_day = days_of_week.index(day_name.lower())
    delta_day = target_day - d.isoweekday()
    if delta_day >= 0: delta_day -= 7 # go back 7 days
    return d + datetime.timedelta(days=delta_day)

class namespace(object):
    def __init__(self, **init):
        [setattr(self, k, v) for k, v in list(init.items())]

def dict2url(args, keys=None):
    qs = []
    for k, v in list(args.items()):
        if keys and k not in keys:
            continue
        qs.append(k + '=' + urllib.parse.quote(str(v)))
    return "&".join(qs)

def qstr(v):
    if isinstance(v, int):
        return v
    elif v is default:
        return "DEFAULT"
    elif v is None:
        return "NULL"
    else:
        return "'%s'" % str(v).replace("'", "''")

class _DefaultValue(object):
    pass
default = _DefaultValue()
del _DefaultValue

def insert_sql(table, values, returning=None):
    """ Create insert sql for the given table with the given values
    returning the given fields. Returning would be a list
    """

    items = list(values.items())
    fields = ", ".join(i[0] for i in items)
    values = ", ".join(str(qstr(x[1])) for x in items)
    sql = "INSERT INTO %s (%s) VALUES (%s)" % (table, fields, values)
    if returning:
        returning_frag = ", ".join(returning)
        sql = "%s RETURNING %s" % (sql, returning_frag)
    return sql

def multi_insert_sql(table, values):

    fields = list(values[0].keys())

    frags = []
    for items  in values:
        values = ", ".join(str(qstr(items[f])) for f in fields)
        frags.append("(%s)" % values)

    values = ", ".join(frags)
    fields = ", ".join(fields)

    return "INSERT INTO %s (%s) VALUES %s" % (table, fields, values)


class InsertSQL(object):
    def __init__(self, table):
        self.table = table
        self.values = {}
    
    def update(self, other, keys=None):
        if keys is None:
            keys = list(other.keys())
        for key in keys:
            self.values[key] = other.get(key)

    def __str__(self):
        return insert_sql(self.table, self.values)

class DeleteSQL(object):
    def __init__(self, table):
        self.table = table
        self.conditions = {}
    
    def update_conditions(self, other, keys=None):
        if keys is None:
            keys = list(other.keys())
        for key in keys:
            self.conditions[key] = other.get(key)

    def __str__(self):
        cond_frag = []
        for key, value in list(self.conditions.items()):
            cond_frag.append("%s=%s" % (key, qstr(value)))
        cond_frag = " AND ".join(cond_frag)
        items = list(self.conditions.items())
        fields = ", ".join(i[0] for i in items)
        values = ", ".join(str(qstr(x[1])) for x in items)
        return "DELETE FROM %s WHERE %s" % (self.table, cond_frag)

def dict2commalist(d, joiner=", "):
    """ helper for update_sql. turns the given dictionary into a command
    separated SQL fragment.
    """
    d = ["%s=%s" % (x[0], qstr(x[1])) for x in list(d.items())]
    return joiner.join(d)

def update_sql(table, values, match, keys=None):
    return "UPDATE %s SET %s WHERE %s" % (
        table,
        dict2commalist(values),
        dict2commalist(match, " AND "))

def update_sql2(table, values, keys):
    uvals = dict((k, values[k]) for k in values if k not in keys)
    match = dict((k, values[k]) for k in keys)

    return "UPDATE %s SET %s WHERE %s" % (
        table,
        dict2commalist(uvals),
        dict2commalist(match, " AND "))

def delete_sql(table, match):
    match = " AND ".join("%s=%s" % (k, str(qstr(v))) for k, v in list(match.items()))
    return "DELETE FROM %s WHERE %s" % (table, match)

class CursorWrapper(object):
    """ Wrapper around a cursor that logs all SQL and errors to a file and
    provide auxillary services """
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()
        self.handle = None

    def __del__(self):
        try:
            self.handle.close()
        except:
            pass

    def execute(self, sql, params=()):
        log.debug("SQL: %s\nParams: %s", sql, params)
        try:
            self.cursor.execute(sql, params)
        except:
            log.error("Error occured:\n%s\n", traceback.format_exc())
            raise

    def __getattr__(self, attr):
        return getattr(self.cursor, attr)

def send_email(body, subject, recipients, sender=None):
    """ tired of rewriting this code """
    if sender is None:
        sender = config.site_sender_email()
    outer = MIMEMultipart()
    outer['Subject'] = subject
    outer['From'] = sender
    outer['To'] = ", ".join(recipients)
    outer['Date'] = eutils.formatdate()
    outer.attach(MIMEText(body))
    smtp = smtplib.SMTP(config.smtp_host())
    smtp.sendmail(sender, recipients, outer.as_string())
    smtp.close()

class Mailer(object):
    """ Stateful abstraction on top of sending an email. """
    subject = 'Message from CPS AR System'
    recipients = [ 'root' ]
    bcc = None
    sender = None
    smtp_server = config.smtp_host()
    auto_line_feed = True
    log_message = False
    def __init__(self, subject=None, recipients=None):
        self.bcc = []
        self.body = io.StringIO()
        if subject is not None:
            self.subject = subject
        if recipients is not None:
            self.recipients = recipients

        self._attachments = []
        if self.sender is None:
            self.sender = config.site_sender_email()

    def set_billing_recipients(self):
        self.recipients = config.billing_recipients()

    def set_billing_bcc(self):
        self.bcc = config.billing_recipients()

    def set_customer_care_recipients(self):
        self.recipients = [config.customer_service_email()]

    def __call__(self, msg, *args):
        """ Write the data to the body of the message. """
        if args: msg %= args
        self.body.write(msg)
        if self.auto_line_feed:
            self.body.write("\n")
        if self.log_message:
            log.debug("MI: %s", msg)

    def write(self, buf):
        """ Implement a file-like interface """
        self(buf)

    def add_attachment(self, fname, payload, mime=('application', 'octet-stream')):
        part = MIMEBase(*mime)
        part.set_payload(payload)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment;filename="%s"' % fname)
        self._attachments.append(part)

    def send(self):
        """ Send out the message. """
        smtp = smtplib.SMTP(self.smtp_server)
        smtp.sendmail(self.sender, self.recipients + self.bcc, 
                      self._msg().as_string())
        smtp.close()

    def debug(self):
        print(self._msg().as_string())

    def _msg(self):
        outer = MIMEMultipart()
        outer['Subject'] = self.subject
        outer['From'] = self.sender
        outer['To'] = ", ".join(self.recipients)
        outer['Date'] = eutils.formatdate()
        outer.attach(MIMEText(self.body.getvalue()))
        for attachment in self._attachments:
            outer.attach(attachment)
        return outer

class X12File(list):
    """ Representation of an X12File being parsed off disk. Implements 
    iterator interface along with X12-specific functions.
    """

    cur_pos = 0
    
    def __init__(self, file):
        x = file.read(-1).split('~')
        x = [i.split('*') for i in x]
        self.extend(x)

    @property
    def cur(self):
        return self[self.cur_pos]

    @property
    def id(self):
        """ Segment identifier """
        return self[self.cur_pos][0]

    @property
    def qualifier(self):
        return self[self.cur_pos][1]

    @property
    def args(self):
        return self[self.cur_pos][2:]

    def next(self, type_check=None):
        """ Move to the next segment from the file. If type_check is given,
        assert that the type is of the type.
        """
        if self.cur_pos + 1 == len(self):
            raise IndexError('At end')
        self.cur_pos += 1
        seg = self[self.cur_pos]

        log.debug('Parsed %s', seg[0])
        if type_check:
            assert seg[0] == type_check, ('Segment type check failed. '
                'Expected %s. Got %s' % (type_check, seg[0]))
        return seg

    def prev(self):
        if self.cur_pos == 0:
            raise IndexError('Already at beginning')
        self.cur_pos -= 1
        return self[self.cur_pos]
    
    def __iter__(self):
        for i in range(self.cur_pos, len(self)):
            yield self[i]

class X12Writer(object):
    """ A file wrapper that provides an X12 writing interface
    Category: Tool
    """
    def __init__(self, file):
        self.file = file
        self.set_counter()
        self.hlevel = 0

    def __getattr__(self, attr):
        return getattr(self.file, attr)

    def set_counter(self, value=0):
        self.counter = value

    def write(self, data):
        if isinstance(data, list):
            data = list(data)
            while not data[-1]:
                del data[-1]
            data = "%s~" % "*".join(data)
        self.file.write(data)
        self.counter += 1

    def write_hl(self, parent, level_code, child_code):
        self.hlevel += 1
        self.write([
            'HL',
            str(self.hlevel),   # HL01: Hierarchical ID Number
            str(parent),        # HL02: Parent ID Number
            level_code,         # HL03: Hierarchical Level Code
            child_code          # HL04: Hierarchical Child Code
        ])


class CallList(list):
    def __call__(self, s, *a):
        if a: s %= a
        self.append(s)

class Mako(dict):
    """ A mako publishing object which stores state that is accessible to
    the template plus default template name detecting from the process name.
    Treat as a dictionary and then evaluate the template by calling the object

    >>> t = Mako("test.tmpl")
    >>> t['val'] = 'cool'
    >>> print t()
    """

    # Some commonly checked attributes in templates
    errors = []

    def __init__(self, template_name=None):
        if template_name is None:
            self.template_name = "%s.tmpl" % os.path.basename(sys.argv[0])
        else:
            self.template_name = template_name
    
    def __call__(self, values=None):
        if values:
            self.update(values)
        lookup = mako_template_lookup()
        self.setdefault('m', self)
        tmpl = lookup.get_template(self.template_name)
        return tmpl.render(**self)

    @classmethod
    def expand(cls, tmpl_name, namespace):
        """ Convinence method to just expand a template """
        return cls(tmpl_name)(namespace)

def mako_template_lookup():
    """ A mako template lookup for this system. All mako users should call me.
    Do not make a templatelookup yourself.
    """
    args = dict(
       directories=[config.mako_template_dir()],
       default_filters=['none_to_blank', 'str'],
       output_encoding='utf-8',
       input_encoding='utf-8',
       encoding_errors='replace',
       imports=['from cpsar.util import none_to_blank']
    )
    if config.mako_cache_dir():
        args['module_directory'] = config.mako_cache_dir()
    return ML.TemplateLookup(**args)

class spawn_ftps(pexpect.spawn):
    """ pexpect interface that wraps the ftp-ssl command for ftps protocol
    """
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        super(spawn_ftps, self).__init__('ftp-ssl -i -p %s' % host)
        self.expect('Name')
        self.sendline(username)
        self.expect('Password:')
        self.sendline(password)
        index = self.expect(["230", "530"])
        self.expect("ftp> ")
        if index == 1:
            raise ValueError("Login Failed: %s" % self.before)

    def cd(self, dir):
        self.sendline('cd "%s"' % dir)
        self.expect("ftp> ")
        if "250" not in self.before:
            raise ValueError("Could not change directory to %r: %s" %
                             (dir, self.before))

    def lcd(self, ldir):
        self.sendline('lcd "%s"' % ldir)
        index = self.expect([
            "Local directory now .*?",
            "local: .*?: No such file or directory"
            ])

        self.expect("ftp> ")
        if index == 1:
            raise ValueError("Could not lcd to %r:%s" % (ldir, self.before))

    def ls(self, dir=''):
        self.sendline('nlist %s' % dir)
        self.expect("125.*?\r\n")
        self.expect("226.*?\r\n")
        files = self.before.split("\r\n")
        self.expect("ftp> ")
        files = [f for f in files if f]
        return files

    def get(self, rfile, lfile=''):
        if lfile:
            cmd = 'get "%s" "%s"' % (rfile, lfile)
        else:
            cmd = 'get "%s"' % rfile
        self.sendline(cmd)
        index = self.expect(["226", "550"])
        self.expect("ftp> ")
        if index == 1:
            raise ValueError("Could not get %r: %s" % 
                             (rfile, self.expect.before))
    
    def put(self, lfile):
        self.sendline('put "%s"' % lfile)
        self.expect("ftp> ")

    def delete(self, rfile):
        self.sendline('del "%s"' % rfile)
        index = self.expect(["250", "550"])
        self.expect("ftp> ")
        if index == 1:
            raise ValueError("Could not delete %r: %s" % 
                             (rfile, self.expect.before))

    def quit(self):
        self.sendline("quit")

class spawn_sftp(pexpect.spawn):
    """ pexpect interface which wraps the sftp command for file 
    transfer.
    """
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        super(spawn_sftp, self).__init__('sftp %s@%s' % (username, host))
        index = self.expect([
            "password:",
            "Are you sure you want to continue connecting"
            ])
        if index == 1:
            self.sendline("yes")

        self.sendline(password)
        index = self.expect([
            "sftp> ",
            "Permission denied",
            ])
        if index == 1:
            raise ValueError("Login Failed: %s" % self.before)

    def cd(self, dir):
        self.sendline('cd "%s"' % dir)
        index = self.expect([
            "sftp> ",
            "No such file or directory"
            ])
        if index == 1:
            raise ValueError("Could not change directory to %r: %s" %
                             (dir, self.before))

    def put(self, lfile):
        self.sendline('put "%s"' % lfile)
        self.expect("sftp> ")

    def get(self, rfile, lfile=''):
        if lfile:
            cmd = 'get "%s" "%s"' % (rfile, lfile)
        else:
            cmd = 'get "%s"' % rfile
        self.sendline(cmd)
        index = self.expect([
            "sftp> ",
            "Couldn't stat remote file",
            "Cannot download non-regular file"])
        if index > 0:
            raise ValueError("Could not get %r: %s" % 
                             (rfile, self.expect.before))
    
    def ls(self, dir=''):
        self.sendline('ls %s' % dir)
        index = self.expect([
            "sftp> ",
            "Couldn't stat remote file"
            ])
        if index > 0:
            raise ValueError('Could not list %r: %s' % 
                             (dir, self.expect.before))
        lines = self.before.split("\r\n")[1:]
        lines = [f for f in lines if f]

        files = []
        for l in lines:
            files.extend([y for y in l.split()])

        return files

    def delete(self, rfile):
        self.sendline('rm "%s"' % rfile)
        index = self.expect([
            "sftp> ",
            "Couldn't delete file"
            ])
        if index == 1:
            raise ValueError("Could not delete %r: %s" % 
                             (rfile, self.expect.before))

    def quit(self):
        self.sendline("quit")


# Used to calculate the last quarter for the current date
q_lookup_map =  {
    1: (10, 1, -1, 4, 12, 31),
    2: (10, 1, -1, 4, 12, 31),
    3: (10, 1, -1, 4, 12, 31),
    4: ( 1, 1,  0, 1,  3, 31),
    5: ( 1, 1,  0, 1,  3, 31),
    6: ( 1, 1,  0, 1,  3, 31),
    7: ( 4, 1,  0, 2,  6, 30),
    8: ( 4, 1,  0, 2,  6, 30),
    9: ( 4, 1,  0, 2,  6, 30),
   10: ( 7, 1,  0, 3,  9, 30),
   11: ( 7, 1,  0, 3,  9, 30),
   12: ( 7, 1,  0, 3,  9, 30)}

def calc_last_quarter(date):
    """ provide the first and last day of the previous quarter from date
    """
    mon, day, yr_offset, quarter, em, ed = q_lookup_map[date.month]
    yr = date.year + yr_offset
    return {
        'start_date': datetime.datetime(yr, mon, 1),
        'end_date': datetime.datetime(yr, em, ed),
        'quarter': quarter,
        'year': yr,
        'month': mon}


def dump_cursor(cursor, fpath):
    f = open(fpath, "w")
    writer = csv.writer(f)
    writer.writerow([c[0] for c in cursor.description])
    list(map(writer.writerow, cursor))
    f.close()

def fmt_cursor_text(cursor):
    cols = [d[0] for d in cursor.description]
    buf = io.StringIO()
    for c in cursor:
        for col, val in zip(cols, c):
            buf.write("%s: %s\n" % (col.ljust(15), val))
        buf.write("\n")
    return buf.getvalue()


class Tracer(object):
    """ My own little trace module. Use me to trace your code! """

    def __init__(self, fname=None):
        if fname is None:
            fname = "/tmp/tracer.txt"
        self.fname = fname
        self._fd = None

    def __call__(self, msg, *args):
        if self._fd is None:
            self._fd = open(self.fname, 'a')
            self._fd.write("Tracer started %s from %s\n" % (
                time.asctime(), sys.argv[0]))
            self._fd.write("-"*80)
            self._fd.write("\n")
        if args:
            msg %= args
        self._fd.write(msg)
        self._fd.write("\n")
    
    def __del__(self):
        if self._fd is not None:
            self._fd.close()

class benchmark(object):
    """ Use me as a context to get a log of how long it takes """
    def __init__(self, name, level=logging.INFO):
        self.name = name
        self._level = level
    def __enter__(self):
        self.start = time.time()
    def __exit__(self,ty,val,tb):
        end = time.time()
        log.log(self._level, "%s : %0.3f seconds" % (self.name, end-self.start))
        return False

def count_money(amt, quantifier=Decimal("0.01")):
    return amt.quantize(quantifier, rounding=ROUND_HALF_UP)

def unique(seq, idfun=None):  
    # order preserving 
    if idfun is None: 
        idfun = lambda x: x
    seen = {} 
    result = [] 
    for item in seq: 
        marker = idfun(item) 
        # in old Python versions: 
        # if seen.has_key(marker) 
        # but in new ones: 
        if marker in seen: continue 
        seen[marker] = 1 
        result.append(item) 
    return result

RX_ISOTIME = re.compile("^(\d+)-(\d+)-(\d+)T(\d+):(\d+):(\d+)(\.\d+)?")
def iso2datetime(isostring):
    m = RX_ISOTIME.search(isostring)
    if m:
        return datetime.datetime(*[(int(v.lstrip('.'))) for v in m.groups() if v is not None])

def none_to_blank(value):
    """ Mako default filter used to not show Nones everywhere """
    if value is None:
        return ""
    else:
        return value

class memoize(object):
    def __init__(self, f):
        self.f = f
        self.memo = {}

    def __call__(self, *args):
        if not args in self.memo:
            self.memo[args] = self.f(*args)
        return self.memo[args]

class imemoize(object):
    """cache the return value of a method
    
    This class is meant to be used as a decorator of methods. The return value
    from a given method invocation will be cached on the instance whose method
    was invoked. All arguments passed to a method decorated with memoize must
    be hashable.
    
    If a memoized method is invoked directly on its class the result will not
    be cached. Instead the method will be invoked like a static method:
    class Obj(object):
        @imemoize
        def add_to(self, arg):
            return self + arg
    Obj.add_to(1) # not enough arguments
    Obj.add_to(1, 2) # returns 3, result is not cached

    http://code.activestate.com/recipes/577452-a-memoize-decorator-for-instance-methods/
    """
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self.func
        return partial(self, obj)

    def __call__(self, *args, **kw):
        obj = args[0]
        cache = obj.__dict__.setdefault('_imemoize_cache', {})
        key = (self.func.__name__, args[1:], frozenset(list(kw.items())))
        try:
            res = cache[key]
        except KeyError:
            res = cache[key] = self.func(*args, **kw)
        return res
