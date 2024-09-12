import psycopg2

import cpsar.pg
import cpsar.runtime as R
import cpsar.wsgirun as W

@W.wsgi
@W.json
def application(req, res):
    fields = ['group_number', 'type_name', 'default_ref_no', 'expiration_date']
    params = [req.get(p) or None for p in fields]
    params = tuple(params)

    cursor = R.db.dict_cursor()
    try:
        cursor.execute("""
            INSERT INTO payment_type
                (group_number, type_name, default_ref_no, expiration_date)
            VALUES (%s, %s, %s, %s)
            RETURNING *
            """, params)
    except psycopg2.DatabaseError as e:
        return res.error(e)
    res['record'] = cpsar.pg.one(cursor)
    R.db.commit()
