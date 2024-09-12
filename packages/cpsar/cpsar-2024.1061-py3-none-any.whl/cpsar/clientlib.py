import kcontrol
import cpsar.runtime as R

class GroupListBox(kcontrol.ListBox):
    """ A special client list box that only includes groups that
    the current user has access to.
    """
    def __init__(self, name, **kwargs):
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT group_number, group_number || ' ' || client_name
            FROM client
            ORDER BY group_number
            """)
        values = list(cursor)
        kcontrol.ListBox.__init__(self, name, values=values, **kwargs)
