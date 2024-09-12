#!/usr/bin/env python
""" WSGI Script to run on EHO's processor terra (dev halley) which writes
certain text files to disk. This program exists because I don't trust
RW NFS due to deadlocking.
"""
import os
import shutil
import tempfile

import webob

_TARGET_DIR = "/server/export/bd/"
_FILES = ["blue-addon-rules.txt", "corp-tt-prefix.txt"]

def application(environ, start_response):
    req = webob.Request(environ)
    res = webob.Response()
    fname = req.path_info[1:]
    if fname not in _FILES:
        res.status = 404
        res.write("Unknown file %s" % fname)
        return res(environ, start_response)
    if req.method != "PUT":
        res.status = 405
        res.write("Invalid method %s" % req.method)
        return res(environ, start_response)
    target_path = os.path.join(_TARGET_DIR, fname)
    fd = tempfile.NamedTemporaryFile("a+t")
    fd.write(req.body)
    fd.flush()
    shutil.copy(fd.name, target_path)
    fd.close()
    os.chmod(target_path, 0o664)
    return res(environ, start_response)
