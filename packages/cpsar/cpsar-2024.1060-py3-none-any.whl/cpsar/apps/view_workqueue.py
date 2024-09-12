from cpsar.wsgirun import wsgi
from cpsar.wsgirun import json
from cpsar.wsgirun import mako

@wsgi
@mako("view_workqueue.tmpl")
def application(req, res):
    pass

