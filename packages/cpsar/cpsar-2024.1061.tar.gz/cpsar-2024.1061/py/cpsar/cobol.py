""" Client library for our custom COBOL <-> HTTP Gateway application server.
Also provides an alternative access to the server which uses the simple WSGI
gateway interface which doesn't involve any server parsing.
"""
import os
from io import StringIO
import time
import urllib.request, urllib.error, urllib.parse
import urllib.parse

import requests
from cpsar import config
from cpsar import ajson

class CHTTPRequest(object):
    headers = {'Content-Type' : 'text/json'}

    error_msg = ''

    def __init__(self, program, args):
        self.program = program
        self.args = args

    @property
    def url(self):
        return "%s/%s" % (config.cobol_server_url(), self.program)

    def open(self):
        json_args = ajson.write(self.args).encode()
        self.req = urllib.request.Request(self.url, json_args, self.headers)
        try:
            self.res = urllib.request.urlopen(self.req)
            self.info = self.res.info()
        except urllib.error.HTTPError as exc:
            if exc.code == 500:
                self.handle_500(exc)
            elif exc.code == 404:
                self.handle_404(exc)
            elif exc.code == 412:
                self.handle_412(exc)
            else:
                self.handle_http_error(exc)
        except urllib.error.URLError as e:
            raise CobolNotAvailableError(e)

        if self.res.code != 200:
            raise ValueError('Unknown response code %s' % self.res.code)

    def parse(self):
        b = self.res.read()
        self.results = ajson.read(b.decode())

    def handle_404(self, exc):
        raise NotFoundError(exc.msg)

    def handle_412(self, exc):
        raise DataError(exc.msg, exc.fp.read())

    def handle_500(self, exc):
        raise InternalServerError2(exc.filename, self.args, exc.fp.read())

    def handle_http_error(self, exc):
        raise InternalServerError(getattr(exc, 'reason', exc))

class CobolNotAvailableError(Exception): pass

def query(program, uparams, media_type=None, out_headers=None):
    req = CHTTPRequest(program, uparams)
    req.open()
    req.parse()
    if out_headers is not None:
        out_headers.update(req.info)
    return req.results

def delayed_query(program, uparams, slee_time=1):
    req = CHTTPRequest(program, uparams)
    req.open()
    req.parse()
    time.sleep(slee_time)
    return req.results

class RemoteError(Exception):
    pass

class NotFoundError(RemoteError):
    pass

class InternalServerError(RemoteError):
    def __getattr__(self, attr):
        try:
            return self.args[0][attr]
        except KeyError:
            raise AttributeError(attr)

class InternalServerError2(RemoteError):
    def __init__(self, path, remote_args, response):
        self.path = path
        self.remote_args = remote_args
        self.response = response
        self.args = (path, remote_args, response)

class UnknownServerError(InternalServerError):
    def __init__(self, *args):
        self.args = args

class DataError(RemoteError):
    def __init__(self, msg, body=None):
        Exception.__init__(self, msg)
        self.txt_body = body
        try:
            self.json = ajson.read(self.txt_body)
            self.body = self.json['results']
        except:
            self.body = self.txt_body
