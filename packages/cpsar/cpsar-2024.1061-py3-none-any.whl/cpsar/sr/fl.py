""" Florida State Reporting Library """
import cpsar.runtime as R

def lookup_provider(id):
    if id is None:
        return
    if id.startswith('P'):
        id = id[2:]
    cursor = R.db.dict_cursor()
    cursor.execute("SELECT * FROM fl_provider WHERE license_number=%s", (id,))
    if cursor.rowcount:
        return cursor.fetchone()

