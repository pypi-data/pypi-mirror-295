"""
WSGI Infrastructure utility library, written to emulate the old
kg.cgilib Mix-In based Application Library. For a python module which
exposes a WSGI application, the difference between the CGI version
and the WSGI version is that the CGI version has the following block
of code at the bottom:

if __name__ == '__main__':
    Program().run()

while the WSGI module will have the following instead:

application = Program.app

"""
from email.mime.text import MIMEText
from email.header import Header
import json
import smtplib
import traceback
import threading
import urllib
from urllib.parse import quote

import webob
from paste.httpexceptions import HTTPNotFound

import cpsar.runtime as R
import cpsar.util as U

class Res(webob.Response):
    """ Wrapper around webob.Response which provides a few extra 
    convinience methods
    """
    def redirect(self, loc, *args):
        """ Redirect the user's browser to another page. args are
        interpolated in the location string
        """
        if args:
            loc = loc % args
        self.location = loc
        self.status = 303

    _written_error_header = False
    def error(self, msg, *a):
        """ Write an error out to the browser in HTML. The first call
        will print out the HTML preamble along with an ERROR title.
        Subsequent calls will only print the provided messages.
        The given arguments are interpolated.
        """
        if not self._written_error_header:
            self.write("<html><head><title>ERROR</title></head><body>")
            self.write("<h1>An Error Occured.</h1>")
            self.status = 500
            self._written_error_header = True

        if a:
            msg %= a
        self.write("<div class='error'>%s</div>" % msg)

    def write_json(self, o):
        self.content_type = 'application/json'
        json.dump(o, self)

class Program(object):
    """ Abstract Base Class for WSGI programs. This class provides a pluggable
    scheme for Mix-In's to add additional logic to the stages of a web
    request's execution. In other words: hooks.

    The Program also provides request and response objects which are derived
    from webob's Request and Response.

    Web handlers wishing to use this class should derive a new Program class
    and override the main() method, which will run on each request. A new
    program instance is created for each request.

    The WSGI entry point is the app classmethod Program.app. The standard
    usage is::

    class MyProgram(Program):
        def main(self):
            self._res.write("Hello World")

    application = MyProgram.app
    """

    fs = None
    """ DEPCREATED: Use self._req """

    _req = None
    _res = None

    ## Overrideable
    def main(self):
        """ Main method to override by base classes to implement work to be
        done to handle request
        """
        pass

    def publish(self):
        """ Display-oriented overridable which is usually provided by a 
        Mix In which runs after main. Overriders should have publish
        send the response data to the browser using self._res
        """
        pass

    ## Private Methods
    def _mixin_pre_init(self):
        """ gives mix-in's a chance to run code at the very beginning of the
        request. pre_init code should not depend on any other state on the
        application save for the existence of the _req and _res objects.
        Mix-ins should implement a pre_init method which is guaranteed to run.
        """
        for base in type(self).__mro__:
            if 'pre_init' in base.__dict__:
                base.pre_init(self)

    def _mixin_init(self):
        """ give mix-in's a chance to run initialization code. Mix-ins should
        implement an init method which is guaranteed to run before the main()
        method.
        """
        for base in type(self).__mro__:
            if 'init' in base.__dict__:
                base.init(self)

    def _mixin_finalize(self):
        """ give mix-in's a chance to run finalization code after main() and
        publish(). This code is not guarnateed to run if an unhandled exception
        propogates out of the main() or publish() method.
        """
        for base in type(self).__mro__:
            if 'finalize' in base.__dict__:
                base.finalize(self)

    ## Public Interface
    def redirect(self, url, *a, **k):
        """ DEPRECATED: redirect the browser to the given url, expanding and
        arguments a and k with URL escaping
        """
        self._res.redirect(url, *a, **k)

    @classmethod
    def app(cls, environ, start_response):
        """ Used to construct an instance for each invocation providing a WSGI
        interface
        """
        return cls().run(environ, start_response)

    def run(self, environ, start_response):
        """ External public entry point for the program instance. The server/
        caller should call run on the program instance as a WSGI compatible
        interface. However, the normal mode of execution is to use the app()
        class method and let it call run()
        """

        self._req = webob.Request(environ).decode('ascii', 'ignore')
        self._res = Res()
        self._process(environ, start_response)
        return self._res(environ, start_response)

    def _process(self, environ, start_response):
        """ Process the request, handling all mix-in code and the main control
        flow
        """
        self.fs = FieldStorage(self._req)
        self._mixin_pre_init()
        self._mixin_init()
        self.main()
        self.publish()
        self._mixin_finalize()

class FieldStorage(object):
    """ Provides the cgi.FieldStorage interface for a webob Request. Adapter
    """
    def __init__(self, req):
        self.req = req

    def keys(self):
        """ Provide a list of all form fields submitted by the browser that
        have non-empty values.
        """
        return [key for key in self.req.params
                if self.req.params[key] != '']

    def has_key(self, key):
        """ Did the browser submit a form field of the given name? """
        value = key in self.req.params
        return value

    def getvalue(self, key, default=None):
        """ Get the value of the given form field key that the browser
        submitted.  If the key was not submitted by the browser (or the browser
        submitted a blank value), then default is returned.
        """
        try:
            value = self.req.params.get(key)
            # cgi.FieldStorage will return None if no actual value
            # is assigned to the query string paramter. We want to
            # maintain that behavior. Especially for inserting NULL's
            # into the database from empty browser arguments.
            if value == '' or value is None:
                return default
            return value
        except KeyError:
            return default

    def getfirst(self, key, default=None):
        """ DEPRECATED: Old CGI FieldStorage compatable method to provide a
        single value for a field, opposed to either a string or list.
        """
        return self.getvalue(key, default)

    def getlist(self, key):
        """ DEPRECATED: Provide a list of values for the given key, even if
        only one value (or no value) was submitted by the browser.
        """
        # webob 1.2 > always encodes querystring into utf-8
        return list(map(str, self.req.params.getall(key)))

class UserRegisterMixIn(object):
    """ Enable cpsar.runtime.username() to function properly. """

    authentication_required = True
    def pre_init(self):
        if self.authentication_required:
            # Force user to be authenticated
            if not R.session.get('username'):
                url_args = (self._req.path, self._req.query_string)
                url = '/login?referer=%s' % urllib.parse.quote("%s?%s" % url_args)
                self.redirect(url)
                return
        else:
            return
        self._req.environ['REMOTE_USER'] = R.session['username']
        R.set_user_from_session()

    def finalize(self):
        R.reset_user()


class MakoMixIn(object):
    """ WSGI-enabled version of cs.html.MakoMixIn
    """

    template_name = None
    """ File Name of the template to render. Defaults to the last part of the
    path_info given by the browser.
    """

    mako_auto_publish = True
    """ automatically render the mako template or make the program class call
    self.mako explicitly
    """

    tmpl = None
    # Some commonly checked attributes in templates
    errors = None
    messages = None

    def init(self):
        """ Initialize the atrributes needed for the mako template """
        self.errors = []
        self.messages = {}
        self.tmpl = U.Mako()

        self._auto_assign_template_name()

    def _auto_assign_template_name(self):
        """
        Assign the template_name of the mako template from the script_name
        submitted by the browser. This is possibly a security hole?
        """
        
        path_name = self._req.script_name
        if path_name.startswith("/"):
            path_name = path_name[1:]

        if path_name:
            self.tmpl.template_name = path_name.split("/")[-1] + ".tmpl"
        else:
            self.tmpl.template_name = "index.tmpl"

    def get_message(self):
        """ DEPRECATED """
        try:
            return self.messages[self.fs.getvalue('m')]
        except KeyError:
            return None

    def populate_template(self):
        """ Default template population puts the application object
        as q in the template
        """
        self.tmpl['q'] = self

    def _mixin_populate_template(self):
        """ give mix-in's a chance to populate values for the template """
        for base in type(self).__mro__:
            if 'populate_template' in base.__dict__:
                ret = base.populate_template(self)
                if ret:
                    self.tmpl.update(ret)

    def publish(self):
        """ Render the mako template as long as mako_auto_publish is True
        and the response is still in a valid state.
        """
        if self.mako_auto_publish and self._res.status == '200 OK':
            self.mako()

    def mako(self):
        """ Evaluate the mako template in the response """
        self._mixin_populate_template()
        self._res.body = self.tmpl()

class PIMixIn(object):
    """ Dispatch based on the Path Info method of the request. Be sure to assign
    the publish attribute of the methods that are available to True.
    """
    def main(self):
        """ Invoke the method on the class that matches the given path_info
        or index() if none given. """
        handler = getattr(self, self._requested_path(), None)
        if not handler:
            raise HTTPNotFound(self._requested_path())
        if not getattr(handler, 'publish', False):
            raise HTTPNotFound(self._requested_path())
        return handler()

    def _requested_path(self):
        """ Provide the requested path from the browser """
        path = self._req.path_info
        if path.startswith('/'):
            path = path[1:]
        if path == '':
            return 'index'
        else:
            return path

    def index(self):
        """ Override me in the program to handle the default case """
        pass
    index.publish = True

def publish(proc):
    """ Decorator to tell PIMixIn that a particular method is
    published to the web.
    """
    proc.publish = True
    return proc

class HTTPMethodMixIn(object):
    """ WSGI-based version of Method Dispatch based on the HTTP method of the
    request. """
    def main(self):
        """ Dispatch to a do_METHOD method on self depending on the HTTP
        method. """
        method = self._req.method
        method_map = {
            'GET' : self.do_get,
            'POST' : self.do_post,
            'PUT' : self.do_put,
            'HEAD' : self.do_head
        }
        method_handler = method_map.get(method, 'GET')
        method_handler()

    def do_get(self):
        """ Handle HTTP GET """
        pass
    def do_post(self):
        """ Handle HTTP POST """
        pass
    def do_put(self):
        """ Handle HTTP PUT """
        pass
    def do_head(self):
        """ Handle HTTP HEAD """
        pass

class ActionMixIn(object):
    """ Dispatch based on the value of an 'action' param
    that comes in from a user form.
    """
    @property
    def action(self):
        return self.fs.getvalue('action')

    def main(self):
        a = self.fs.getvalue('action')
        if a and hasattr(self, a):
            attr = getattr(self, a)
            if hasattr(attr, 'action'):
                if callable(attr):
                    attr()
                else:
                    # showing a string or data structure
                    self._res.body = str(attr)
        else:
            self.default()

    def default(self):
        pass

def action(f):
    """ Decorator to mark a method as an action. """
    f.action = True
    return f

class MakoProgram(MakoMixIn, UserRegisterMixIn, Program):
    """ Convinence base class which provides a single extension point for
    program that publish mako templates
    """
    pass

class GProgram(UserRegisterMixIn, Program):
    """ Public base class which will inherit other mandatory mix-ins as they
    become required.
    """
    pass

#/////////////////////////////////////////////////////////////////////////////
## middleware
class TakeDownMiddleware(object):
    """ WSGI middleware which checks for a redirect file on disk and sends the
    user to that file if it exists. This is for nightly maintenance, upgrades,
    etc.  """
    def __init__(self, app, fpath):
        self.app = app
        self.fpath = fpath

    def __call__(self, environ, start_response):
        try:
            fd = open(self.fpath)
        except (IOError, OSError):
            return self.app(environ, start_response)

        body = fd.read(-1)
        fd.close()
        if body.startswith('REDIRECT:'):
            loc = body.split(':', 1)[1].strip()
            res = Res(status=302)
            res.location = loc
        else:
            res = Res(body=body)
        return res(environ, start_response)



class EmailExceptionHandlerMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        try:
            # Try running the application
            return self.app(environ, start_response)
        except Exception as e:
            # If an exception occurs, send an email
            exc_info = traceback.format_exc()
            url = self.construct_url(environ)
            self.send_exception_email(exc_info, url)

            # Start the response with a 500 status and content-type
            start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])

            # Return the error message to the browser
            return [b'Internal Server Error - the server encountered an unexpected condition.']

    def construct_url(self, environ):
        scheme = environ.get('wsgi.url_scheme', 'http')
        host = environ.get('HTTP_HOST', '')
        script_name = quote(environ.get('SCRIPT_NAME', ''))
        path_info = quote(environ.get('PATH_INFO', ''))
        query_string = environ.get('QUERY_STRING', '')
        if query_string:
            query_string = '?' + query_string
        return f'{scheme}://{host}{script_name}{path_info}{query_string}'

    def send_exception_email(self, message, url):
        sender = f'root'
        receivers = ['root']

        msg = MIMEText(message, 'plain', 'utf-8')
        msg['From'] = Header(sender, 'utf-8')
        msg['To'] = Header(", ".join(receivers), 'utf-8')
        msg['Subject'] = Header(f'Unhandled Exception at {url}', 'utf-8')

        try:
            smtpObj = smtplib.SMTP('localhost')
            smtpObj.sendmail(sender, receivers, msg.as_string())
            print("Successfully sent email")
        except smtplib.SMTPException:
            print("Error: unable to send email")

