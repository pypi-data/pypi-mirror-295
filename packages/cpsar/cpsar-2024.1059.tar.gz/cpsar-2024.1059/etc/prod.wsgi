#!/usr/bin/env python

## Active virtualenv
activate_path = "/usr/local/srv/bd/bin/activate_this.py"
execfile(activate_path, dict(__file__=activate_path))

import os

from paste import httpexceptions
from paste.exceptions.errormiddleware import ErrorMiddleware
from paste.urlparser import make_url_parser

from cpsar import session
import cpsar.apps
import cpsar.runtime as R
app_dir = os.path.dirname(cpsar.apps.__file__)

application = make_url_parser({}, app_dir, 'cpsar.apps')
application = R.message_middleware(application)
application = R.db(application)
application = httpexceptions.HTTPExceptionHandler(application)
application = session.middleware(application)
application = ErrorMiddleware(application,
    error_email=['tech@drugbenefit.com'],
    error_subject_prefix="Exception Raised in A/R Backend",
    error_message=("Oops...An error has occured in our system! We have been notified "
            "and will do our best to remedy the situation as quickly as possible. "
            "Please try your request again."),
    error_log='/var/log/wsgi/ar.corporatepharmacy.com-error')
