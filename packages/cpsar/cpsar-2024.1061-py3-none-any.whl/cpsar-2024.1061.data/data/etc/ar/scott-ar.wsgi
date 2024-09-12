#!/usr/bin/env python
## Active virtualenv
activate_path = "/usr/local/srv/bd/bin/activate_this.py"
execfile(activate_path, dict(__file__=activate_path))
import os

from beaker.middleware import SessionMiddleware
from paste import httpexceptions
from paste.exceptions.errormiddleware import ErrorMiddleware
from paste.urlparser import make_url_parser

import cpsar.apps
import cpsar.runtime as R
app_dir = os.path.dirname(cpsar.apps.__file__)

application = make_url_parser({}, app_dir, 'cpsar.apps')
application = R.db(application)
application = httpexceptions.HTTPExceptionHandler(application)
application = ErrorMiddleware(application, debug=True)
