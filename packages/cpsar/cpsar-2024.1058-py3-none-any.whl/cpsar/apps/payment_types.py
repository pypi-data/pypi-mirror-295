""" Application to manage payment types
"""
import psycopg2

import cpsar.runtime as R
import cpsar.util as U

## Pick your adapters
from cpsar.wsgirun import json
from cpsar.wsgirun import mako

from cpsar.wsgirun import PathDispatch

reg = PathDispatch()

@reg
@mako('payment_types.tmpl')
def index(req, tmpl):
    pass

@reg
@json
def list(req, res):
    cursor = R.db.dict_cursor()
    cursor.execute("""
        SELECT ptype_id, group_number, type_name, default_ref_no, expiration_date
        FROM payment_type
        ORDER BY ptype_id
    """)
    res['ptypes'] = [dict(c) for c in cursor]

@reg
@json
def add(req, res):
    sql = U.InsertSQL('payment_type')
    sql.update(req, ('group_number', 'type_name', 'default_ref_no', 'expiration_date'))

    cursor = R.db.dict_cursor()
    try:
        cursor.execute(str(sql))
    except psycopg2.DatabaseError as e:
        return res.error(e)

    R.db.commit()

@reg
@json
def delete(req, res):
    ptype_id = req.get('ptype_id')
    if not ptype_id:
        return res.error("no ptype id given")
    cursor = R.db.dict_cursor()
    try:
        cursor.execute("""
            DELETE FROM payment_type WHERE ptype_id=%s
            """, (ptype_id,))
    except psycopg2.DatabaseError as e:
        return res.error(e)
    R.db.commit()

@reg
@json
def update(req, res):
    ptype_id = req.get('ptype_id')
    if not ptype_id:
        return res.error("no ptype id given")

    fields = ('group_number', 'type_name', 'default_ref_no', 'expiration_date')
    values = dict((f, req.get(f)) for f in fields)
    sql = U.update_sql("payment_type", values, {"ptype_id": ptype_id})

    cursor = R.db.dict_cursor()
    try:
        cursor.execute(sql)
    except psycopg2.DatabaseError as e:
        return res.error(e)
    R.db.commit()

application = reg.get_wsgi_app()
