"""
This is a copy of bd/db.py in order to provide the same interface to all
other cpsar code.
"""
import datetime
import json
import psycopg2

import cpsar.runtime as R

DataError = psycopg2.DataError
IntegrityError = psycopg2.IntegrityError

def site_config(name, d=None):
    """ Provide a site configuration value which
    is stored in the database
    """
    cur = dict_cursor()
    cur.execute("select * from site_config")
    if not cur.rowcount:
        return d
    return next(cur).get(name, d)

def mako_cursor(tmpl_name):
    return R.db.mako_cursor(tmpl_name)

def mako_dict_cursor(tmpl_name):
    return R.db.mako_dict_cursor(tmpl_name)

def connected():
    return bool(R.db)

def dict_cursor():
    return R.db.real_dict_cursor()

def real_dict_cursor():
    return R.db.real_dict_cursor()

def cursor():
    return R.db.cursor()

def commit():
    R.db.commit()

def rollback():
    R.db.rollback()

def setup():
    R.db.setup()

def teardown():
    R.db.teardown()

# Simple database cache that was written to handle group formularies
# create unlogged table cache_table ( key text primary key not null, value text, expires timestamp not null);
def set_cache_value(name, value, expires=None):
    if expires is None:
        expires = datetime.datetime.now() + datetime.timedelta(minutes=60)
    c = cursor()
    c.execute("""
        insert into cache_table (key, value, expires)
        values (%s, %s, %s)
        on conflict(key) do update set
            value=EXCLUDED.value,
            expires=EXCLUDED.expires
            """, (name, json.dumps(value), expires))
    commit()

def cache_value(name):
    c = cursor()
    c.execute("select value, expires from cache_table where key=%s", (name,))
    if not c.rowcount:
        return None
    value, expires = next(c)
    if expires > datetime.datetime.now():
        c.execute("delete from cache_table where key=%s", (key,))
        commit()
        return None
    return json.loads(value)

def clear_cache():
    c = cursor()
    c.execute("delete from cache_table where expires < now()")
    commit()

