from __future__ import absolute_import
import datetime
import decimal
import json

class ExtendedEncoder(json.JSONEncoder):
     def default(self, obj):
         if isinstance(obj, datetime.date):
             return obj.strftime("%Y%m%d")
         if isinstance(obj, datetime.datetime):
             return obj.ctime()
         if isinstance(obj, decimal.Decimal):
            return float(obj)
         return json.JSONEncoder.default(self, obj)

def write(obj):
    return json.dumps(obj, cls=ExtendedEncoder)

def read(s):
    return json.loads(s)

def loads(s):
    return json.loads(s)

def dumps(s):
    return json.dumps(s, cls=ExtendedEncoder)

def dump(s, f):
    return json.dump(s, f, cls=ExtendedEncoder)
