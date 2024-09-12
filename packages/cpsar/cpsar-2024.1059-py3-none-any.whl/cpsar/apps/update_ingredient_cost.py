import decimal

import cpsar.runtime as R
import cpsar.wsgirun as W

@W.wsgi
@W.json
def application(req, res):
    ingredient_id = req.get('ingredient_id')
    try:
        cost = decimal.Decimal(req.get('cost'))
    except decimal.InvalidOperation:
        res.error('Invalid cost %s' % cost)
        return

    cursor = R.db.dict_cursor()
    cursor.execute("""
      update history_ingredient set cost=%s
      where ingredient_id=%s
      """, (cost, ingredient_id))

    R.db.commit()
