""" The TX Type library provides transaction type procedures to the system.
In implementation, this module encapsulates the nabp_tt_prefix table.
"""
import cpsar.runtime as R

_lookup = None
def get_tx_type(record):
    """ calculates the transaction types for transaction records. Required keys
    in record are:
        - group_number
        - pharmacy_nabp
        - compound_code
        - drug_ndc_number
    """
    global _lookup
    if _lookup is None:
        _lookup = TXTypeLookup()
    return _lookup(record)

def all_tx_types():
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT DISTINCT prefix
        FROM nabp_tt_prefix
        """)
    types = []
    for prefix, in cursor:
        for suffix in ['G', 'B', 'C']:
            types.append(prefix + suffix)
    return sorted(types)

def tx_types_for_group(group_number):
    """ Produce a list of transaction types available to be used for the
    given group number. This does not take into account the actual used
    transaction types for the group currently in the system.
    """
    cursor = R.db.cursor()
    cursor.execute("""
        SELECT DISTINCT prefix
        FROM nabp_tt_prefix
        WHERE group_number=%s OR group_number=''
        """, (group_number,))

    prefixes = [c[0] for c in cursor] + ['R']
    prefixes.sort()
    for p in prefixes:
        yield p + 'G'
        yield p + 'B'

    yield 'MP'
    yield 'MC'

_tx_type_rule_cache = {}
def tx_type_has_rules(tx_type, group_number):
    """ Does the given transaction type have any distribution rules defined
    for the given group?
    """
    global _tx_type_rule_cache
    if group_number not in _tx_type_rule_cache:
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT DISTINCT tx_type, 1
            FROM distribution_rule
            WHERE group_number = %s
            """, (group_number,))
        _tx_type_rule_cache[group_number] = dict(list(cursor))
    return tx_type in _tx_type_rule_cache[group_number]

class TXTypeLookup:
    """ Looks up the transaction type for a transaction record. This object
    implements a cache of the database values and is optimized for mass
    update operations.
    """
    def __init__(self, ndc_cache_override=None):
        """
        To speed up access, a dictionary can be passed into ndc_cache_override that
        maps NDC to B/G. This saves the library from loading all NDC's from the
        database into memory.
        """

        self.one = _PositionOneLookup()
        self.two = _PositionTwoLookup(ndc_cache_override)

    def __call__(self, record):
        return self.one.get(record) + self.two.get(record)

class _PositionOneLookup:
    """ Calculates position one of the transaction type. This field is decided
    by the NABP of the transaction.
    """
    def __init__(self):
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT group_number, nabp, prefix
            FROM nabp_tt_prefix""")

        self._cache = dict((c[:2], c[2]) for c in cursor)

    def get(self, record):
        keys = [
            (record['group_number'], record['pharmacy_nabp']),
            ('', record['pharmacy_nabp'])]

        for key in keys:
            try:
                return self._cache[key]
            except KeyError:
                pass
        return 'R'

class _PositionTwoLookup:
    """ Calculates position two of the transaction type. This field is decided
    by the drug's brand status.
    """
    def __init__(self, ndc_cache_override=None):
        cursor = R.db.cursor()
        if ndc_cache_override is None:
            cursor.execute("SELECT ndc_number, brand FROM drug")
            self.drugs = dict(list(cursor))
        else:
            self.drugs = ndc_cache_override

    def get(self, record):
        if record['compound_code'] == '2' and \
           record['pharmacy_nabp'] == R.CPS_NABP_NBR:
            return 'C'
        b = self.drugs[record['drug_ndc_number']]
        if b == 'B':
            return 'B'
        else:
            return 'G'

