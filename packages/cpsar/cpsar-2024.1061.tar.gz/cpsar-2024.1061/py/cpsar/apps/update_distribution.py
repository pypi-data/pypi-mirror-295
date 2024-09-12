""" Application to manage distribution rules.
"""
import cpsar.runtime as R
import cpsar.util as U
import psycopg2

from cpsar.wsgirun import json, wsgi

@wsgi
@json
def application(req, res):
    if req.get("show_on_invoice"):
        show_on_invoice = True
    else:
        show_on_invoice = False

    f = req.get
    record = {"dr_id": req.get("dr_id")}
    if f("show_on_invoice"):
        record["show_on_invoice"] = bool(f("show_on_invoice"))
    if f("priority"):
        record["priority"] = int(f("priority"))

    sql = U.update_sql2("distribution_rule", record, ["dr_id"])
    cursor = R.db.cursor()
    try:
        cursor.execute(str(sql))
    except psycopg2.DatabaseError as e:
        return res.error(e)
    R.db.commit()

