#!/usr/bin/env python
## Active virtualenv
activate_path = "/usr/local/srv/bd/bin/activate_this.py"
execfile(activate_path, dict(__file__=activate_path))
import os

from paste import httpexceptions
from paste.urlparser import make_url_parser
from werkzeug.debug import DebuggedApplication

from cpsar import session

import cpsar.apps
import cpsar.runtime as R
app_dir = os.path.dirname(cpsar.apps.__file__)

application = make_url_parser({}, app_dir, 'cpsar.apps')
application = R.message_middleware(application)
application = R.db(application)
application = httpexceptions.HTTPExceptionHandler(application)
application = session.middleware(application)
application = DebuggedApplication(application, evalex=True)
