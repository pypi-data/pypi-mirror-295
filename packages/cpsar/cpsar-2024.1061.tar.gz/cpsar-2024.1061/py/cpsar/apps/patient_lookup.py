""" Search for patients in the system and display links to view the patients.

"""

import cpsar.runtime as R

from cpsar import pg
from cpsar import sql
from cpsar.wsgirun import MethodDispatch
from cpsar.wsgirun import mako

application = app = MethodDispatch()

@app.get
@mako('patient_lookup.tmpl')
def show_search_form(req, res):
    pass

@app.post
@mako('patient_lookup.tmpl')
def perform_search(req, res):

    error = validate(req.params)
    if error:
        R.flash('Invalid Patient ID')
        return

    b = sql.ConditionBuilder()
    b.ilike('first_name')
    b.ilike('last_name')
    b.eq('group_number')
    b.eq('patient_id')
    if not b.load_params(req.params):
        return

    query = """
        SELECT patient_id,
               group_number, 
               first_name, 
               last_name, 
               ssn, 
               dob
        FROM patient
        WHERE %s
        ORDER BY last_name, first_name
        LIMIT 10000
        """ % b.and_clause()
    cursor = R.db.dict_cursor()
    cursor.execute(query)

    res['query'] = query
    res['results'] = pg.all(cursor)

def validate(params):
    if params['patient_id']:
        try: 
            int(params['patient_id'])
        except ValueError: 
            return True 
