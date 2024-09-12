""" Application to manage transaction types
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
@mako('tx_types.tmpl')
def index(req, tmpl):
    cursor = R.db.dict_cursor()
    cursor.execute("""
        SELECT nabp, prefix, client.group_number, client.client_name
        FROM nabp_tt_prefix
        LEFT JOIN client USING (group_number)
        ORDER BY client.group_number, nabp
    """)
    tmpl['nabp_tt_prefixes'] = [dict(c) for c in cursor]

@reg
@json
def add(req, res):
    sql = U.InsertSQL('nabp_tt_prefix')
    sql.update(req, ('nabp', 'prefix', 'group_number'))

    cursor = R.db.dict_cursor()
    try:
        cursor.execute(str(sql))
    except psycopg2.DatabaseError as e:
        return res.error(e)
    
    R.db.commit()

@reg
@json
def delete(req, res):
    nabp = req.get('nabp')
    if not nabp:
        return res.error("NO NABP GIVEN")
    cursor = R.db.dict_cursor()
    try:
        cursor.execute("""
            DELETE FROM nabp_tt_prefix WHERE nabp=%s
            """, (nabp,))
    except psycopg2.DatabaseError as e:
        return res.error(e)
    R.db.commit()

application = reg.get_wsgi_app()
