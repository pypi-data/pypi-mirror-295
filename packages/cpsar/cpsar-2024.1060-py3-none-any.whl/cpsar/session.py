""" Module exposing Thread local session object which wraps beaker. """
import datetime
import mimetypes
import os
import time
import threading
import urllib
import uuid

import webob
from beaker.middleware import SessionMiddleware

from cpsar import config

def middleware(app):
    return SessionMiddleware(_instance(app), {
        'session.type': 'file',
        'session.data_dir': config.session_dir(),
        'session.cookie_expires': True,
        'session.auto': True,
        'session.samesite': 'None',
        'session.secure': True
    })

class _TLSSession:
    """ The TLS session wraps a Session object for a specific user in a 
    given thread. This object is an enhancement introduced when the library
    was made to support a multi-threaded environment.
    """
    def __init__(self):
        self.__dict__['_tls'] = threading.local()

    def __getattr__(self, attr):
        """ Pass off all unhandlable messages to the session defined in the
        session in the current thread.
        """
        return getattr(self._tls.session, attr)

    def __setattr__(self, attr, value):
        setattr(self.__dict__['_tls'], attr, value)

    def __getitem__(self, key):
        return self._tls.session[key]

    def __setitem__(self, key, value):
        self._tls.session[key] = value
    def get(self, key, defaultv=None):
        return self._tls.session.get(key, defaultv)

    def __delitem__(self, key):
        del self._tls.session[key]

    def __call__(self, proc):
        """ WSGI Middleware to manage the session with a cookie"""
        def wsgi_app(environ, start_response):
            # sessionfile hook
            self.start_request(environ)
            try:
                if environ['PATH_INFO'] == "/user_session_file":
                    return self.session_file(environ, start_response)
                return proc(environ, start_response)
            finally:
                self.end_request()
        return wsgi_app

    def save(self):
        """ Hold over from old interface to beaker """
        self._tls.session.persist()

    def start_request(self, environ):
        """ Call at the beginning of the request. """
        session = environ['beaker.session']
        self._tls.session = session
        if session.get('current_group'):
            environ['bd.current_group'] = session['current_group']
        if session.get('username'):
            environ['bd.username'] = session['username']

    def end_request(self):
        """ We get rid of the session at the end of the request for the next
        request.
        """
        if not hasattr(self._tls, 'session'):
            return
        self._tls.session.persist()
        del self._tls.session

    @property
    def active(self):
        """ Is there an active session for the current thread? """
        return hasattr(self._tls, 'session')

    @property
    def user(self):
        return CurrentUser(self)

    def session_file(self, environ, start_response):
        req = webob.Request(environ)
        u = req.params.get("u")
        files = self.get("files", {})
        file = files.get(u)
        if not file:
            start_response('404 Not Found', [('Content-type', 'text/plain')])
            return [b'Not found']
        _, file_name, payload = file
        mt = mimetypes.guess_type(file_name)
        content_type = mt[0] if mt else "application/octet-stream"
        headers = [
            ("Content-Disposition", f"attachment; filename={urllib.parse.quote(file_name)}"),
            ("Content-Type", content_type)
        ]
        start_response('200 OK', headers)
        del files[u]
        return [payload]


_instance = _TLSSession()

def get():
    global _instance
    return _instance


class CurrentUser:
    def __init__(self, session):
        self.session = session

    @property
    def group_number(self):
        return self.session.get('current_group')

    @property
    def username(self):
        return self.session.get('username')

    def push_file(self, file_name, payload):
        f = self.session.setdefault("files", {})
        u = str(uuid.uuid1())
        f[u] = (time.time(), file_name, payload)
        return u
