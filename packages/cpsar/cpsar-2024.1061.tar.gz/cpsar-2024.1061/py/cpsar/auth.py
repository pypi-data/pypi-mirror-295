import urllib.parse

import cpsar.runtime as R
from cpsar.runtime import db


def internal(username):
    cursor = db.cursor()
    cursor.execute("""
        SELECT internal
        FROM user_info
        WHERE username=%s""",
        (username,))
    if not cursor.rowcount:
        return False
    return cursor.fetchone()[0]
