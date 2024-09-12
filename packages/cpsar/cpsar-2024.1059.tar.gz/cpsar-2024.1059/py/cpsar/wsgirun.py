"""
WSGI Toolkit and Utilities
==========================

Architecture
------------
This module was written to allow WSGI programs to be easily written without
having to repeat boiler-plate code over and over. It isn't a complete
framework, but it does provide request handler dispatching mechanisms,
request objects, mako templating responses and json responses.

It is used in a decorator-style, where a WSGI application function uses a
decorator to denote what "kind-of" application it is. Depending on which
decorator is used, the application function will take different arguments.

This decorator effectively adapts the function from the standard WSGI 
interface to something more specialized.

Application Decorators
----------------------
The most generic decorator is the @wsgi decorator. The application procedure
will take a request and response object. See `wsgi` for more information.
The two output control application handlers are `mako` and `json` which
will take as a second argument a template or json data object instead of a
response. The application procedure can interact with these objects to control
the output to the client.

Editor Note: I would prefer the interfaces to be WSGI between the dispatcher
and the request type adapters but this is how it is. If you want to use a
request type adapter without a dispatch, you must use the @wsgi decorator
first to convert it to the webob interface. -- JL

Environment
-----------
There is also the notion of a web environment, which is simply a thread-local
storage that can be used acrossed the request as a global bucket for handlers.

Editor Note: This steps on the toes of the responsibilities of cpsar.runtime so
I would like to get rid of it eventually. However, in cpsar.runtime, it is
assumed that all objects manage their own thread-local state internally. There
is no big global thread-local pool for everyone to play with. The objects on
the wsgirun.web object were not designed to be shared across threads (that is
why they are there!)
"""
import os
import functools
import pprint
import threading
import types
import urllib

import webob
import mako.exceptions as ME
from paste.httpexceptions import HTTPNotFound, HTTPFound

import cpsar.ajson as J
import cpsar.runtime as R
import cpsar.util as U
from cpsar.config import mako_template_dir, mako_cache_dir


#//////////////////////////////////////////////////////////////////////////////
# webob derivations

class Response(webob.Response):
    """ Customized webob Response object with extra utility methods like
    debug.
    """
    def __init__(self, *a, **k):
        self.errors = []
        webob.Response.__init__(self, *a, **k)

    def __call__(self, environ, start_response):
        return super(Response, self).__call__(environ, start_response)

    _weh = False
    def error(self, msg, *a):
        if not self._weh:
            self.write("<html><head><title>ERROR</title></head><body>")
            self.write("<h1>An Error Occured.</h1>")
            self.status = 500
            self._weh = True

        if a: msg %= a
        self.write("<div class='error'>%s</div>" % msg)

    def debug(self, obj):
        """ Dump out an HTML-viewable version of the given object to the
        browser.
        """
        self.write("<html><head><title>DEBUG</title></head><body><pre>")
        self.write(pprint.pformat(obj))
        self.write("</pre></body></html>")
        return self()

    def redirect(self, loc, *args):
        if args:
            loc = loc % args
        self.location = loc
        self.status = 303

    def not_found(self, msg='File Not Found'):
        self.status = 404
        self.write("""<html><head><title>404
        %s</title></head><body><h1>%s</h1></body></html>"""
            % (msg, msg))

    def csv_header(self, file_name):
        self.content_type = 'application/csv'
        self.headers.add("Content-Disposition", "attachment; filename='%s'" % file_name)

class Request(webob.Request):
    """ Customizable webobj Request object. Add more fun to me when you
    need it!
    """
    def get(self, param, default=None):
        return self.params.get(param, default)

#//////////////////////////////////////////////////////////////////////////////
# Dispatchers/webob adapters
#
def wsgi(proc):
    """ Decorator used to adapt a WSGI application into a webob
    Request/Response interface. This logic should be used first in the
    entry-point application. Dispatchers usually implement their own version
    of this logic. Use this decorator if you do not wish to have a
    dispatcher in your application module.
    """
    def wsgi_app(environ, start_response):
        request = Request(environ)
        response = Response()
        if not R.session.get('username'):
            url_args = (request.path, request.query_string)
            url = '/login?referer=%s' % urllib.parse.quote("%s?%s" % url_args)
            response.redirect(url)
            return response(environ, start_response)

        R.set_user_from_session()
        override = proc(request, response)
        if override is not None:
            response = override
        result = response(environ, start_response)
        return result
    wsgi_app.__name__ = proc.__name__
    wsgi_app.__doc__ = proc.__doc__
    wsgi_app.__dict__ = proc.__dict__
    return wsgi_app

class MethodDispatch(dict):
    """ Dispatches a request based on the HTTP method of the request. If
    the method is unknown, the dispatcher falls back to the GET method::

        application = app = MethodDispatch()

        @app.get
        def show_form(req, res):
            pass

        @app.post
        def form_submit_handler(req, res):
            pass
    """
    def __init__(self):
        self['GET'] = self.default

    def default(self, req, res):
        """ Called when nothing is registered at all on the dispatcher.
        """
        pass

    def post(self, proc):
        self['POST'] = proc
    def get(self, proc):
        self['GET'] = proc
    def put(self, proc):
        self['PUT'] = proc
    def head(self, proc):
        self['HEAD'] = proc
    def delete(self, proc):
        self['DELETE'] = proc
    def propfind(self, proc):
        self['PROPFIND'] = proc

    def dget(self, key, default=None):
        """ globbered the dict.get method. """
        return dict.get(self, key, default)

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = Response()
        if not R.session.get('username'):
            url_args = (request.path, request.query_string)
            url = '/login?referer=%s' % urllib.parse.quote("%s?%s" % url_args)
            response.redirect(url)
            return response(environ, start_response)
        R.set_user_from_session()

        proc = self.dget(request.method, self['GET'])

        override = proc(request, response)
        if override is not None:
            response = override
        return response(environ, start_response)

class PathDispatch(dict):
    """ Dispatch on the extra PATH_INFO of the request. If no match is
    made, then the default handler is ran::
        reg = PathDispatch()

        @reg
        def index(req, res):
            pass

        @reg
        def honk(req, res):
            pass

        application = reg.get_wsgi_app()
    """

    def __call__(self, func):
        self['/%s' % func.__name__] = func
        return func

    def lookup(self, path_info):
        if not path_info.strip() or path_info == '/':
            path_info = '/index'
        try:
            return self[path_info]
        except KeyError:
            return None

    def get_wsgi_app(self):
        return wsgi(self.app)

    def app(self, req, res):
        proc = self.lookup(req.path_info)
        if not proc:
            res.status = 404
            res.write('%s not found' % req.path_info)
        else:
            proc(req, res)

#//////////////////////////////////////////////////////////////////////////////
# response-type adapters
#

class JsonRecord(dict):
    """ A JSON record that stands in for a webob response object. The record
    is a dictionary that can be manipulated by the handling application which
    will be serialized to JSON after the handler runs.
    """
    def __init__(self, response):
        self['errors'] = []
        self.response = response
        self.response.content_type = 'application/json'
        self.response.charset = 'UTF-8'

    def error(self, msg, *args):
        if isinstance(msg, (tuple, list)):
            self['errors'].extend(msg)
        else:
            if not isinstance(msg, str):
                msg = str(msg)
            if args:
                msg %= args
            self['errors'].append(msg)

    def has_error(self):
        return len(self['errors']) > 0

    _not_found_msg = None
    def not_found(self, msg='Resource not found'):
        """ If the response needs to stop and send off a not found call 
        me.
        """
        self._not_found_msg = msg

    def __call__(self):
        if self._not_found_msg:
            msg = {'errors': [self._not_found_msg]}
        else:
            msg = self
        self.response.write(J.write(msg))

def json(proc):
    """ JSON request-type adapter. Use as a decorator to create a json
    response handler.
    """
    def app(req, res):
        json_res = JsonRecord(res)
        proc(req, json_res)
        json_res()
    app.__name__ = proc.__name__
    app.__doc__ = proc.__doc__
    app.__dict__ = proc.__dict__
    return app

class MakoRecord(dict):
    """ A Mako object which is injected into an application request handler as the
    second argument by the @mako decorator defined below. """
    def __init__(self, request, response, tmpl_name=None):
        self.request = request
        self['request'] = request
        self.response = response
        self['response'] = response
        self['args'] = self
        self.tmpl_name = tmpl_name
        self._lookup = U.mako_template_lookup()
        self.cancel = False

    def __getattr__(self, attr):
        """ Pass-thru attributes to the response """
        return getattr(self.response, attr)

    def redirect(self, *a, **k):
        self.cancel = True
        return self.response.redirect(*a, **k)

    errors = None
    def error(self, error, *args):
        """ Use a stop error to cancel the mako template from being
        displayed and showing the stop error instead. The error is shown
        in html markup. This is usually for assert-type checks or "die"

        Multiple stop errors can be called, althoug it's more common to
        simply return a first stop error. You may access the has_errors
        property to determine if a stop error has occured.
        """
        if self.errors is None:
            self.errors = []
        if args: error %= args
        self.errors.append(error)

    @property
    def has_errors(self):
        return self.errors is not None

    _not_found_msg = None
    def not_found(self, msg='Resource not found'):
        """ If the response needs to stop and send off a not found call 
        me.
        """
        self._not_found_msg = msg

    def __call__(self):
        if self.cancel:
            return
        if self.has_errors:
            self.response.status = 500
            self.response.write("<html><body><h1>Error Occured</h1>")
            for e in self.errors:
                self.response.write("<div>%s</div>" % e)
            self.response.write("</body></html>")
            return
        if self._not_found_msg is not None:
            self.response.status = 404
            self.response.write("<html><body><h1>404 %s</h1></body></html>" 
                                % self._not_found_msg)
            return
        if self.tmpl_name is None:
            raise AttributeError("No tmpl_name has been set")
        try:
            tmpl = self._lookup.get_template(self.tmpl_name)
            self.response.write(tmpl.render(**self))
        except ME.SyntaxException:
            self.response.write(ME.html_error_template().render())

    def render(self):
        if self.tmpl_name is None:
            raise AttributeError("No tmpl_name has been set")
        tmpl = self._lookup.get_template(self.tmpl_name)
        return tmpl.render(**self)

def mako(tmpl_name=None, mod_name=None):
    """ Mako request-type adapter. Use to have a mako template
    evaluated after a handler runs::

        @mako("my_template.tmpl")
        def application(req, tmpl):
            tmpl['param'] = 'value'
    """
    if isinstance(tmpl_name, types.FunctionType):
        tmpl_name, proc = tmpl_name.__name__ + ".tmpl", tmpl_name
        #  Didn't call in decorator statement
        def app(req, res):
            tmpl = MakoRecord(req, res, tmpl_name=tmpl_name)
            proc(req, tmpl)
            tmpl()
        functools.update_wrapper(app, proc)
        return app
    else:
        if mod_name is not None:
            tmpl_name = mod_name.split(".")[-1] + ".tmpl"
        def inner(proc):
            def app(req, res):
                tmpl = MakoRecord(req, res, tmpl_name=tmpl_name)
                proc(req, tmpl)
                tmpl()
            functools.update_wrapper(app, proc)
            return app
        return inner

