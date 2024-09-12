""" State Reporting Library """
import glob
import os
import re

from cpsar import config
from cpsar.util import send_email

SEND_DIR = "/var/tmp/sr-outbound"
ARCHIVE_DIR = "/server/ar/files/sr/"

PULL_DIR = "/var/tmp/sr-inbound"

def archive_path(*args):
    if not os.path.isdir(ARCHIVE_DIR):
        os.mkdir(ARCHIVE_DIR)
    return os.path.join(ARCHIVE_DIR, *args)

def send_path(*args):
    if not os.path.isdir(SEND_DIR):
        os.mkdir(SEND_DIR)
    return os.path.join(SEND_DIR, *args)

def pull_path(*args):
    if not os.path.isdir(PULL_DIR):
        os.mkdir(PULL_DIR)
    return os.path.join(PULL_DIR, *args)

def add2report(rz, msg, *args):
    """ Append the given message to the given report zone's report
    """

    file_path = '/tmp/ar-sr-%s-report' % rz

    file_exists = os.path.isfile(file_path)
    file = open(file_path, 'a')

    if not file_exists:
        file.write('State Reporting Report for Report Zone %s\n' % rz)
        file.write('-'*80 + '\n')

    if args:
        msg %= args

    file.write(msg + "\n")
    file.close()

def send_reports():
    """ Send out all of the queued up reports to administrators. """
    for file in glob.glob('/tmp/ar-sr-*-report'):
        rz = re.match('.*?(..)-report$', file).groups()[0]
        f = open(file)
        send_email(f.read(-1),
                   'cpsar: State Reporting Report for %s' % rz,
                   config.billing_recipients())

        f.close()
        os.remove(file)


