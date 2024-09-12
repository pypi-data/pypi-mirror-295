
class ltuple(tuple):
    def __new__(cls, tdef, rel):
        return tuple.__new__(cls, rel)

    def __init__(self, tdef, rel):
        self.tdef = tdef

    def __getattr__(self, attr):
        return self[self.tdef[attr]]

def table_set(tdef, *rels):
    tlookup = dict((x, y) for y, x in enumerate(tdef))

    field_def_len = len(tdef)
    nrels = []
    for rel in rels:
        # Ensure the relation has at least as many elements as the definition
        if len(rel) < field_def_len:
            rel += (None,) * (field_def_len - len(rel))
        nrels.append(ltuple(tlookup, rel))
    return nrels

