""" Command Line Program Writing Toolkit

cpsar.shell provides abstract base classes that can be imported into your own
python scripts to enhance their functionality with the following features:

 - automatic built-in logging module configuration by means of command-line
   options. Calls of the program can provide -v to enable INFO level logging
   to standard error and -vv to enable DEBUG level logging to standard error.
 - A new date type to option parse to validate dates and provide them as
   datetime objects
 - A convinence method to access the username of the logged in user
 - Automatic configuration of the standard library optparse OptionParser

An example usage:

from cpsar.shell import Program

class MyProgram(Program):
    def setup_options(self):
        super(MyProgram, self).setup_options()
        # See optparse.OptionParser in the Python Library Reference for more
        # information. Use self.add_option as a shortcut to the option parser's
        # add_option

    def main(self):
        # Write the body of your program here

The Command base class is also provided which allows program to easily
implement sub commands.

Take the following example program named ar-test

class MyProgram(Command):
    def do_sub1(self, args):
        # Write body of sub1

This program can be invoked from the command line as

ar-test sub1. For more information on implementing subcommands, see the
built-in cmd module, which Command inherits from.

Command is also backwards compatabile with the Program class, so a main
method can be implemented. If a main method is implemented, it is
considered the default command and is ran if no sub command is given
on the command line.

## ar-night-job
class NightlyJob(Command):
    def main(self):
        # Code to perform the nightly job

    def do_test(self):
        # Code to be ran interactively to test out features of the
        # nightly job

In this program, calling ar-night-job by itself will invoke the main
procedure, but the sub command can be ran as ar-night-job test.
"""
from __future__ import print_function
import cmd
import copy
import datetime
import logging
import logging.handlers
import optparse
import os
import sys
import time

from cpsar.config import set_private_label
from cpsar.runtime import db, dpath, username, set_user_from_shell

def check_date(option, opt, value):
    formats = ["%Y-%m-%d", "%Y%m%d", "%m/%d/%Y"]
    for fmt in formats:
        try:
            ttuple = time.strptime(value, fmt)
            break
        except ValueError:
            pass
    else:
        raise optparse.OptionValueError(
            "option %s: invalid date value: %r. try CCYY-MM-DD" %
            (opt, value))

    return datetime.date(*ttuple[:3])

class MyOption(optparse.Option):
    TYPES = optparse.Option.TYPES + ("date",)
    TYPE_CHECKER = copy.copy(optparse.Option.TYPE_CHECKER)
    TYPE_CHECKER["date"] = check_date

class Program:
    _args = None
    _opts = None
    _log = None

    verbose_map = {
        0 : logging.WARNING,
        1 : logging.INFO,
        2 : logging.DEBUG,
        3 : 5
    }
    
    name = os.path.basename(sys.argv[0])
    log_stream = sys.stderr

    def __init__(self):
        self.option_parser = optparse.OptionParser(option_class=MyOption)
        self.add_option = self.option_parser.add_option

    def run(self):
        if os.environ.get('PRIVATELABEL'):
            set_private_label(os.environ['PRIVATELABEL'])
        set_user_from_shell()
        self.setup_options()
        self.opts, self.args = self.option_parser.parse_args()
        self.setup_logging()
        self._setup_db()
        try:
            self.main()
        finally:
            try:
                db.teardown()
            except:
                pass
    
    def main(self):
        pass

    def _setup_db(self):
        db.setup()

    def setup_options(self):
        self.add_option('-v', action="count", dest="verbose", default=0,
            help='Verbose mode.  Causes program to print debugging messages '
                 'about its progress. Multiple -v options increase the '
                 'verbosity.  The maximum is 3.')
        self.add_option('--long', action="store_true", default=False,
            help='Output logging in long format, including dates')
        self.add_option('-d', '--dry-run', action="store_true", dest="dry_run",
            default=False,
            help='Simulation mode. Do not save or commit any chances to the '
                 'physical system.')

    def setup_logging(self):
        self.log_level = self.verbose_map[self.opts.verbose]
        self.log = logging.getLogger('')
        self.log.setLevel(self.log_level)

        if self.opts.long:
            stdout_fmt = '%(asctime)s %(filename)-15s ' + \
                       username().ljust(9) + '%(levelname)-7s: %(message)s'
        else:
            stdout_fmt = '%(levelname)-7s: %(message)s'

        handler = logging.handlers.SysLogHandler('/dev/log', 'local3')
        self.log.addHandler(handler)

        handler = logging.StreamHandler(self.log_stream)
        handler.setFormatter(logging.Formatter(stdout_fmt))
        self.log.addHandler(handler)

class Command(cmd.Cmd, Program):
    """ If you want you application to support a command interface, derive
    from me and implement do_ and help_ procedures. All other common shell
    conventions are implemented, like standard arguments -vv, and a command
    may be passed in as argument.
    """
    def __init__(self):
        Program.__init__(self)
        cmd.Cmd.__init__(self)

    ### Public interface
    def run(self):
        """ Execute the command application. Call from __main__"""
        set_user_from_shell()
        self.setup_options()
        self.opts, self.args = self.option_parser.parse_args()
        self.setup_logging()
        self._setup_db()
        self.setup()

        if self.args:
            self.onecmd(" ".join(self.args))
        else:
            self.main()

    def main(self):
        self.cmdloop()

    def setup(self):
        """ Override me to have code run before we call command handlers """
        pass

    def do_EOF(self, args):
        print()
        return True

class MJosephMixIn(object):
    def _setup_db(self):
        set_private_label("mjoseph")
        db.setup()

class MSQMixIn(object):
    def _setup_db(self):
        set_private_label("msq")
        db.setup()

class PrivateLabelMixIn(object):
    def __init__(self, *args, **kwargs):
        super(PrivateLabelMixIn, self).__init__(*args, **kwargs)
        if not os.environ.get('PRIVATELABEL'):
            sys.stderr.write("Cannot run private label application without "
            "PRIVATELABEL environmental variable set\n")
            sys.exit(-10)
        set_private_label(os.environ['PRIVATELABEL'])

class PrivateLabelProgram(PrivateLabelMixIn, Program):
    pass

class PrivateLabelCommand(PrivateLabelMixIn, Command):
    pass

class MJosephProgram(MJosephMixIn, Program):
    pass

class MJosephCommand(MJosephMixIn, Command):
    pass

class MSQProgram(MSQMixIn, Program):
    pass
