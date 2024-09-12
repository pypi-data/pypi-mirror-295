
import paramiko

from cpsar import controls
import cpsar.runtime as R
import cpsar.wsgirun as W

from cpsar import db
from cpsar.pg import qstr
from cpsar.sr import bishop
from cpsar.wsgirun import json, mako, wsgi

@wsgi
@mako('sr_bsr.tmpl')
def application(req, res):
    search_terms = ['trans_id', 'bishop_number', 'source_ref', 'ctime',
        'patient_first_name', 'patient_last_name', 'claim_number']
    search_params = {}
    for t in search_terms:
        v = req.params.get(t)
        if v:
            search_params[t] = v
    if not search_params:
        return

    controls.update_store(search_params)

    cursor = db.mako_dict_cursor('ar/state_reporting.sql')
    cursor.create_bsr_search(search_params)
    cursor.execute("""
        select distinct * from bsr_search order by bsr_id
        """)
    res['fields'] = [c[0] for c in cursor.description]
    res['results'] = list(cursor)
    cursor.execute("drop table bsr_search")

