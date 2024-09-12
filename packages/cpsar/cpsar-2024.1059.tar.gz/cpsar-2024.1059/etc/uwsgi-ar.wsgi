#!/usr/bin/env python3
""" Application entry point. Loaded by uwsgi/supervisord """

import importlib
import os
import pkgutil

from paste import httpexceptions
from paste.urlparser import make_url_parser
from werkzeug.debug import DebuggedApplication
from werkzeug.middleware.shared_data import SharedDataMiddleware

from cpsar import session
from cpsar import config
from cpsar import ws

import cpsar.apps
import cpsar.runtime as R
app_dir = os.path.dirname(cpsar.apps.__file__)

debug = os.environ.get('DEBUG')


# import all of the wsgi modules to get around a bug in paste where
# the initial import isn't thread safe
for _, modname, ispkg in pkgutil.iter_modules(cpsar.apps.__path__):
    fullname = 'cpsar.apps.%s' % modname
    importlib.import_module(fullname)

application = make_url_parser({}, app_dir, 'cpsar.apps')
application = SharedDataMiddleware(application, {
      '/css': config.virtualenv_root('www/ar/css'),
      '/doc': config.virtualenv_root('www/doc/ar'),
      '/images': config.virtualenv_root('www/ar/images'),
      '/html': config.virtualenv_root('www/ar/html'),
      '/js': config.virtualenv_root('www/ar/js'),
      '/repo': config.virtualenv_root('www/repo'),
})
application = R.message_middleware(application)
application = R.db(application)
application = httpexceptions.HTTPExceptionHandler(application)
application = session.middleware(application)

if debug:
    application = DebuggedApplication(application, evalex=True)
else:
    application = ws.EmailExceptionHandlerMiddleware(application)
