
class ConditionBuilder:
    """ Simple object to build up a list of SQL conditions that usually
    go in a WHERE clause (but could go in a JOIN clause if needed.

    To use, define the fields by invoking the eq or ilike methods.

    Then pass in a request object to populate the conditions.

    finally pull the conditions using the and_clause or or_clause
    """
    def __init__(self):
        self.field_defs = []
        self._clauses = []

    def ilike(self, param_field, sql_field=None, left_wc=False, right_wc=True):
        """ left_wc: Makes the left side of the string wildcard match.
        """
        if sql_field is None:
            sql_field = param_field
        c = ILikeCond(sql_field, left_wc, right_wc)
        self.field_defs.append((param_field, c))

    def eq(self, param_field, sql_field=None):
        """ left_wc: Makes the left side of the string wildcard match.
        """
        if sql_field is None:
            sql_field = param_field
        c = EqCond(sql_field)
        self.field_defs.append((param_field, c))

    def load_params(self, params):
        """ Load up the values in the given params. """
        found = False
        for param_field, loader in self.field_defs:
            if params.get(param_field):
                self._clauses.append(loader(params[param_field]))
                found = True
        return found
    
    def and_clause(self):
        return " AND ".join(self._clauses)

    def or_clause(self):
        return " AND ".join(self._clauses)


def qstr(s):
    return "'%s'" % s.replace("'", "''")

class ILikeCond:
    def __init__(self, sql_field, left_wc=False, right_wc=True):
        self.sql_field = sql_field
        self.left_wc = left_wc
        self.right_wc = right_wc

    def __call__(self, value):
        if self.left_wc:
            value = "%%%s" % value
        if self.right_wc:
            value = "%s%%" % value
        return "%s ILIKE %s" % (self.sql_field, qstr(value))
        
class EqCond:
    def __init__(self, sql_field):
        self.sql_field = sql_field

    def __call__(self, value):
        return "%s = %s" % (self.sql_field, qstr(value))
        
