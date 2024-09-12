import functools
import getpass
import logging
import os
import sys
import threading

import cpsar.pg

import cpsar.session
from cpsar import config
from cpsar.util import Mako

CPS_NABP_NBR = '0123682'

here = os.path.abspath(os.path.dirname(__file__))
app_dir = os.path.dirname(os.path.dirname(here))

try:
    import urllib3
    urllib3.disable_warnings()
except (ImportError, AttributeError):
    pass

try:
    import requests.packages.urllib3
    requests.packages.urllib3.disable_warnings()
except (ImportError, AttributeError):
    pass

def app_path(*parts):
    parts = (app_dir,) + parts
    return os.path.join(*parts)

def dpath(*parts):
    """ Provide a path for the data directory with the provided contents.

    Ex: dpath('mitchell', 'out') -> "/server/ar/files/mitchell/out"
    """
    return os.path.join(config.data_dir(), *parts)

session = cpsar.session.get()
db = cpsar.pg.TLSDB()
log = logging.getLogger('')

def flash(msg=None, *a):
    global session
    import traceback, time
    if msg is None:
        try:
            v = session.pop('flash')
            session.save()
            return v
        except KeyError:
            return None
    else:
        if a: msg %= a
        session['flash'] = msg
        session.save()
 
def inject(name, value):
    globals()[name] = value

# Thread-local messaging storage. This was written when I realized that
# the simple error lists wouldn't work under WSGI, so this was written
# to maintain compatability with the existing CGI code.
_messages = threading.local()

def add_message(type, msg):
    if not hasattr(_messages, type):
        setattr(_messages, type, [])
    getattr(_messages, type).append(msg)

def get_messages(type):
    return getattr(_messages, type, [])

def reset_messages(type=None):
    if hasattr(_messages, type):
        delattr(_messages, type)

## Error Messages
def error(msg, *a):
    if a: msg %= a
    log.error(msg)
    add_message('error', msg)

def get_errors():
    return get_messages('error')

def has_errors():
    return bool(getattr(_messages, 'error', False))

def message_middleware(proc):
    def wsgi_app(environ, sr):
        try:
            return proc(environ, sr)
        finally:
            reset_messages('error')
            reset_messages('notice')
    return wsgi_app

## username management
_users = threading.local()
def set_user_from_session():
    try:
        _users.username = session['username']
    except KeyError:
        _users.username = None

def set_user_from_shell():
    _users.username = getpass.getuser()

def username():
    try:
        return _users.username
    except AttributeError:
        raise SystemError("Please call one of the set_user procedures")

def reset_user():
    try:
        del _users.username
    except AttributeError:
        pass

## module management
def pricing_module(group_number, use_db=True):
    """ A central place to pick which pricing module is used based off the group
    number. Didn't really have a good place to put this function so the runtime
    seemed sensible. Implemented for BD Issue 17792. """
    import json
    from cpsar import pricing
    from cpsar import pricing2
    if use_db:
        cursor = db.cursor()
        cursor.execute("""
            select pricing_module from client where group_number=%s
            """, (group_number,))
        if cursor.rowcount:
            name, = next(cursor)
        else:
            name = 'pricing'
    else:
        try:
            name = pricing._json_processing_data().get('pricing_module', {}).get(group_number, 'pricing')
        except (IOError, OSError):
            name = 'pricing'

    if name == 'pricing2':
        return pricing2
    else:
        return pricing


## A global mako object. This is ONLY to be used by CGI programs. This needs to
## be deleted when the entire system moves to WSGI.
mako = Mako()
