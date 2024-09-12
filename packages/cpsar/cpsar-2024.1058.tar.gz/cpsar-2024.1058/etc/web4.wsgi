#!/usr/bin/env python

## Active virtualenv
activate_path = "/usr/local/srv/bd/bin/activate_this.py"
execfile(activate_path, dict(__file__=activate_path))

import os

from beaker.middleware import SessionMiddleware
from paste import httpexceptions
from paste.exceptions.errormiddleware import ErrorMiddleware
from paste.urlparser import make_url_parser

os.environ.update({
     'CPSAR_DATA_DIR': '/data',
     'CPSAR_DBURI': 'postgres://xhandler:this()is$pe14l@bd/cpsar',
     'CPSAR_INV_BASE': '/usr/local/srv/cpsar/data/www',
     'CPSAR_MAKO_CACHE_DIR': '/tmp/ar.corporatepharmacy.com_mako',
     'CPSAR_MAKO_TEMPLATE_DIR': '/usr/local/srv/cpsar/data/mako',
     'SESSION_DIR': '/tmp/session_ar.corporatepharmacy.com'
})

import cpsar.apps
import cpsar.runtime as R
app_dir = os.path.dirname(cpsar.apps.__file__)

application = make_url_parser({}, app_dir, 'cpsar.apps')
#application = SessionMiddleware(application, {
#    'session.cookie_expires': 30000,
#    'session.type' : 'file',
#    'session.data_dir' : '/tmp/session_ar.cps.local',
#    'session.key' : '_sid'
#})
application = R.db(application)
application = httpexceptions.HTTPExceptionHandler(application)
application = ErrorMiddleware(application,
    error_email=['jeremy@ehorx.com', 'scott@ehorx.com'],
    error_subject_prefix="Exception Raised in A/R Backend",
    error_message=("Oops...An error has occured in our system! We have been notified "
            "and will do our best to remedy the situation as quickly as possible. "
            "Please try your request again."),
    error_log='/var/log/wsgi/ar.corporatepharmacy.com-error')
