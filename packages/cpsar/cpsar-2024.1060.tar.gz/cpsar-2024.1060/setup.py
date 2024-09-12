#!/usr/bin/env python
import os
import sys

from setuptools import setup
from glob import glob

here = os.path.abspath(os.path.join(__file__, ".."))
os.chdir(here)


def fglob(pat):
    return [f for f in glob(pat) if os.path.isfile(f)]


def data(*entries):
    """data_files helper to put everything in /usr/local/srv/cpsar"""
    return [("data/%s" % p, fglob("%s/*" % p)) for p in entries]


def data_files(*pairs):
    return [
        (target_dir, fglob("%s/*" % source_pat)) for target_dir, source_pat in pairs
    ]


if sys.version_info >= (3, 7, 0):
    mako_version = "1.2.0"
else:
    mako_version = "1.0.7"

setup(
    name="cpsar",
    version="2024.1060",
    provides=["cpsar"],
    description="Blue Diamond Backend Web System",
    readme="README.txt",
    license="",
    author="Jeremy Lowery",
    author_email="jeremy@bitrel.com",
    url="https://ar.corporatepharmacy.com",
    platforms="POSIX",
    package_dir={"": "py"},
    packages=["cpsar", "cpsar.apps", "cpsar.feed", "cpsar.sr", "cpsar.util"],
    scripts=fglob("bin/*"),
    requires_python=">=3.6",
    install_requires=[
        "attrs",
        "beaker==1.10.0",
        "fpdf==1.7.2",
        "humanize",
        "kcontrol",
        "mako==1.0.7; python_version < '3.7'",
        "mako==1.2.0; python_version >= '3.7'",
        "markdown",
        "openpyxl>=2.0.5",
        "paramiko",
        "paste",
        "pexpect",
        "pytz",
        "reclib",
        "reportlab",
        "requests",
        "six",
        "stypes==0.23.2",
        "twilio",
        "xlsxwriter",
        "webob",
        "werkzeug==2.0.3",
    ],
    data_files=data_files(
        ("doc/ar", "doc"),
        ("doc/ar/sr", "doc/sr"),
        ("doc/ar/mig_reporting_system_files", "doc/mig_reporting_system_files"),
        ("etc/ar", "etc"),
        ("files/ar", "files"),
        ("mako/ar", "mako"),
        ("res/ar", "res"),
        ("res/ar/fonts", "res/fonts"),
        ("sql/ar", "sql"),
        ("www/ar", "www"),
        ("www/ar/css", "www/css"),
        ("www/ar/css/redmond", "www/css/redmond"),
        ("www/ar/css/redmond/images", "www/css/redmond/images"),
        ("www/ar/html", "www/html"),
        ("www/ar/images", "www/images"),
        ("www/ar/images/facebox", "www/images/facebox"),
        ("www/ar/images/icons", "www/images/icons"),
        ("www/ar/js", "www/js"),
        ("www/repo/css", "www/repo/css"),
        ("www/repo/css/kcontrol", "www/repo/css/kcontrol"),
        ("www/repo/img", "www/repo/img"),
        ("www/repo/img/kcontrol", "www/repo/img/kcontrol"),
        ("www/repo/img/kcontrol/pager", "www/repo/img/kcontrol/pager"),
        ("www/repo/js", "www/repo/js"),
        ("www/repo/js/kcontrol", "www/repo/js/kcontrol"),
        ("www/repo/js/kcontrol/lang", "www/repo/js/kcontrol/lang"),
    )
    + [("etc", ["etc/uwsgi-ar.wsgi"])],
)
