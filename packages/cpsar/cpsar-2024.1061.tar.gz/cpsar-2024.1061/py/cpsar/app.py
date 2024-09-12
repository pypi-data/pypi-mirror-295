import os

from paste import httpexceptions
from paste.exceptions.errormiddleware import ErrorMiddleware
from paste.urlparser import make_url_parser
from werkzeug.debug import DebuggedApplication
from werkzeug.middleware.shared_data import SharedDataMiddleware

import cpsar.apps
import cpsar.runtime as R
from cpsar import config
from cpsar import session
app_dir = os.path.dirname(cpsar.apps.__file__)

application = make_url_parser({}, app_dir, 'cpsar.apps')
application = SharedDataMiddleware(application, {
  '/css': config.virtualenv_root('www/css'),
  '/doc': config.virtualenv_root('www/doc'),
  '/html': config.virtualenv_root('www/html'),
  '/images': config.virtualenv_root('www/images'),
  '/js': config.virtualenv_root('www/js'),
  '/repo': config.virtualenv_root('www/repo'),
})
application = R.message_middleware(application)
application = R.db(application)
application = httpexceptions.HTTPExceptionHandler(application)
application = session.middleware(application)
if config.dev_mode():
    application = DebuggedApplication(application, evalex=True)
else:
    application = ErrorMiddleware(application,
        error_email=['tech@drugbenefit.com'],
        error_subject_prefix="Exception Raised in A/R Backend",
        error_message=("Oops...An error has occured in our system! We have been notified "
                "and will do our best to remedy the situation as quickly as possible. "
                "Please try your request again."),
        error_log='/var/log/wsgi/ar.corporatepharmacy.com-error')
