import psycopg2

import cpsar.runtime as R
import cpsar.wsgirun as W

@W.wsgi
@W.json
def application(req, res):
    ptype_id = req.get('ptype_id')
    cursor = R.db.dict_cursor()
    try:
        cursor.execute("""
          DELETE FROM payment_type
          WHERE ptype_id=%s
          """, (ptype_id,))
    except psycopg2.DatabaseError as e:
        res.error(e)
    else:
        R.db.commit()
