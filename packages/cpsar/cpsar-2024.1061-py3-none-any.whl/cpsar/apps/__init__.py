from cpsar.runtime import db
from cpsar.runtime import session
from cpsar import controls

def urlparser_wrap(environ, start_response, app):
    app = db(app)       # database middleware registration
    app = session(app)  # session middleware registration
    app = controls.middleware(app)
    return app(environ, start_response)
