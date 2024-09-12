""" Support Library for writing feeder applications. The main usage of this module is to
pass a callable object to the run function. The passed in callable should be an iterator
which takes in lists of lines and yields out each line as it is processed.

The run() function enables command line argument parsing. A text file is expected to be given
as a single argument to the program. A special case is the string -, which instructs the program
to read from standard in. This is the preferred way to use the programs and piped from the
tail program, creates a very efficient feeding process.

Additionally, the following options are supported:

-b, --boomark a file that stores the last processed line in the feed file, so that subsequent
restarts of the process will not rerun past ran lines.

-q, --quit Quit running after the end of the file is reached. If not given, the program will
continue to scan the feed file indefinitely (similar to tail).

-P, --profile enable the cProfile code and save the profile data to the given file. A lot of
effort has been put into this code to make it as efficient as convinently possible.

An example usage of a program written which uses this library:

ar-feed-patient -b/tmp/patient.bm /server/export/feed/patient.txt
"""
from six import StringIO
import cProfile
import copy
import logging
import optparse
import os
import select
import struct
import sys
import time

log = logging.getLogger('')

###############################################################################
## Public Interface
def run(reader):
    """ Continuously run the reader with processed lines from the command line
    arguments. The reader should yield each line as it is successfully processed.
    """
    app = _Application(reader)
    app.run()

class Parser(object):
    """ A very efficient text file parser which does not type conversion. Provide
    a list of pairs (name, field_length) to the constructor to create the parser
    object.
    """
    version = ''
    _fields = []

    def __init__(self, fields=None, version=None):
        if fields is not None:
            self._fields = fields
        if version is not None:
                self.version = version
        self._fmtstring = ''.join('%ds' % l for name, l in self._fields)
        self._parse_fun = struct.Struct(self._fmtstring).unpack_from
        self._field_names = [f[0] for f in self._fields]

    field_names = property(lambda s: s._field_names)
    fields = property(lambda s: s._fields)

    def delimited_record(self, record, delim="\t"):
        """ Return a delimited version of the provided record which
        came from parse """
        return "\t".join(record[f] for f in self._field_names)

    def parse(self, line):
        vals = self._parse_fun(line)
        out = _Record()
        for field, val in zip(self._field_names, vals):
            val = val.strip()
            if not val:
                out[field] = None
            else:
                out[field] = val
        return out

    def __str__(self):
        """ Shows the parser spec, with the columns in the text file it
        uses
        """
        buf = StringIO()
        cnt = 5
        for field, size in self._fields:
            buf.write("%s % 5d -% 5d % 5s\n" % (field.ljust(25), cnt,
                        cnt+size-1, size))
            cnt += size
        return buf.getvalue()

###############################################################################
## Private module implementation

def _strip_non_ascii(s):
    return "".join(i for i in s if ord(i) < 127 and ord(i) > 31)

class _Record(dict):
    """ A record provided by a Parser object. This is provided because we try
    to maintain interface capatability with the reclib Record object although
    we do not support any of its functionality.
    """
    errors = None
    def format_errors(self):
        return ''

class _Application(object):
    ## Public Interface
    def __init__(self, reader):
        self._reader = reader
        self._cfg = _CLIConfig()

    def run(self):
        """ Run the feeder application. """
        reader, cfg = self._reader, self._cfg
        # Configuration provides values to construct other collaborators
        if not cfg.valid:
            sys.stderr.write(cfg.help())
            return

        if cfg.print_parser_version:
            print(reader.parser_for_version(cfg.print_parser_version))
            return

        self._configure_logging()
        if cfg.profile_file:
            cProfile.runctx('self._main()', globals(), locals(), cfg.profile_file)
        else:
            self._main()

    ## Private Implementation
    _verbose_map = {
        0 : logging.INFO,
        1 : logging.DEBUG,
        2 : 5
    }

    def _configure_logging(self):
        level = self._verbose_map.get(self._cfg.verbose, 0)
        logging.basicConfig(level=level,
            format='%(asctime)s: %(message)s')

    def _main(self):
        """ Entry point procedure which will be profiled if profiling is
        enabled.
        """
        reader, cfg = self._reader, self._cfg

        if cfg.feed_fpath == '-':
            feeder = StdinLineFeeder()
        elif cfg.quit_on_finish:
            feeder = OneTimeLineFeeder(cfg.feed_fpath)
        else:
            feeder = ContinuousLineFeeder(cfg.feed_fpath)

        feeder.try_open()
        while not feeder.opened:
            feeder.try_open(1)

        if cfg.bookmark_fpath:
            log.debug("Using bookmark file %r", cfg.bookmark_fpath)
            bookmark = Bookmark(cfg.bookmark_fpath)
        else:
            bookmark = NullBookmark()

        for lines in bookmark(feeder):
            if cfg.load_only:
                suc = reader(lines, True)
            else:
                suc = reader(lines)
            for successful in suc:
                log.debug("Successful from reader %s", successful)
                bookmark.mark(successful)

class _CLIConfig(object):
    def __init__(self):
        parser = optparse.OptionParser('usage: %prog [OPTIONS] file_file')
        parser.add_option('-b', '--bookmark',
            help='File to save the last line processed in the event that the '
                 'program is restarted and needs to continue where it left off')
        parser.add_option('-v', action="count", dest="verbose", default=0,
            help='Verbose mode.  Causes program to print debugging messages '
                 'about its progress. Multiple -v options increase the '
                 'verbosity.  The maximum is 3.')
        parser.add_option('-q', '--quit', action='store_true',
            help='quit processing the text file once it has reached the end. Do '
                 'no wait for more lines.')
        parser.add_option('-p', '--print-parser',
            help='print the parser information for the given version')
        parser.add_option('-P', '--profile',
            help='Profile the execution of the profiler. Provide a file name '
                 'to save the profile data for analysis. Implies -q.') 
        parser.add_option('-L', '--load-only', action='store_true',
            help='Only load the data into whatever temporary/stage table is '
                 'used. Useful for debugging. Not supported by all feed '
                 'programs.')
        opts, args = parser.parse_args()
        if len(args) != 1:
            self.feed_fpath = None
        else:
            self.feed_fpath = args[0]

        self.bookmark_fpath = opts.bookmark
        self.verbose = opts.verbose
        self.quit_on_finish = opts.quit
        self.print_parser_version = opts.print_parser
        self.profile_file = opts.profile
        if self.profile_file:
            self.quit_on_finish = True

        self.load_only = opts.load_only

    @property
    def valid(self):
        if self.print_parser_version:
            return True
        else:
            return self.feed_fpath is not None

    def help(self): 
        return __doc__

class StdinLineFeeder(object):
    def try_open(self, sleep_time=0):
        self._fd = os.fdopen(sys.stdin.fileno(), 'r', 1)

    opened = property(lambda s: True)

    def __iter__(self):
        try:
            while True:
                if not self._has_data(5.0):
                    continue
                yield self._stdin_lineset()
        except KeyboardInterrupt:
            return

    def _has_data(self, pause=0.0):
        return select.select([self._fd], [], [], pause)[0]

    def _stdin_lineset(self):
        try:
            while self._has_data():
                yield _LineRecord(self._fd.readline())
        except KeyboardInterrupt:
            return

class OneTimeLineFeeder(object):
    _fd = None
    def __init__(self, fpath):
        self._fpath = fpath

    @property
    def opened(self):
        return self._fd is not None

    def try_open(self, sleep_time=0):
        self._fd = open(self._fpath)
        if sleep_time:
            time.sleep(sleep_time)

    def __iter__(self):
        yield self._next_set()
    
    def _next_set(self):
        for line in self._fd:
            yield _LineRecord(line)

class ContinuousLineFeeder(object):
    """ An iterator for clients to continuously process a
    text file line by line. Each iteration is a successful
    read of lines from the file, as lists. IOW, each iteration
    produces a list of lines. This is written in an attempt to be more
    efficient than the obvious implementation of one iteration per
    line that blocks.
    """
    _fd = None
    _fdstat = None
    def __init__(self, fpath):
        self._fpath = fpath

    @property
    def opened(self):
        return self._fd is not None

    def try_open(self, sleep_time=0):
        try:
            self._fd = open(self._fpath, "rb")
            self._fdstat = os.fstat(self._fd.fileno())
            log.debug("opened %r inode: %s", self._fpath, self._fdstat.st_ino)
        except IOError as e:
            # We let file not found slide, other errors are fatal
            # like permission denied.
            if e.errno != 2:
                raise
            else:
                log.info("%r not found. will retry.", self._fpath)

        if sleep_time:
            time.sleep(sleep_time)

    def __iter__(self):
        while True:
            yield self._next_set()
            time.sleep(0.1)

    def _next_set(self):
        while True:
            try:
                line = next(self._fd)
                #line = bline.decode("ascii", "ignore")
            except UnicodeDecodeError as s:
                log.info("Decode error %s on line" % s)
            except StopIteration:
                break
            yield _LineRecord(line)
        self._clear_eof()
        self._check_file_state()

    def _clear_eof(self):
        self._fd.seek(0, 1) 

    def _check_file_state(self):
        """ See http://stackoverflow.com/questions/12690281/check-if-an-open-file-has-been-deleted-after-open-in-python
        For a discussion of the file detection logic.
        """
        try:
            disk_stat = os.stat(self._fpath)
        except OSError:
            raise IOError("%s has disappeared")

        if disk_stat.st_ino == self._fdstat.st_ino and \
           disk_stat.st_dev == self._fdstat.st_dev:
            # The file on disk is the same one we have an open fd for
            return

        log.debug("inode: %s is stale. reopening.", self._fdstat.st_ino)
        # The file has been removed and recreated on disk
        self._fd.close()
        self.open()

class _LineRecord(object):
    """ The line record represents the entire line composed of the
    version, the action and the payload.
    """
    def __init__(self, line):
        self._line = line
        self.action = line[0:1]
        self.version = line[1:4]
        self.payload = line[4:]

    @property
    def line(self):
        return self._line

    def __str__(self):
        return self._line

    def __repr__(self):
        return repr(self._line)

    def report_invalid(self, message):
        logging.error("%s %s" % (message, self._line))

    def __cmp__(self, o):
        if isinstance(o, _LineRecord):
            return cmp(self.payload, o.payload)
        else:
            return cmp(self.payload, o)

class Bookmark(object):
    def __init__(self, fpath):
        """ Assumes fpath is rw on disk """
        self._fpath = fpath
        try:
            self._mark = _LineRecord(open(fpath).readline())
        except (IOError, OSError):
            self._mark = None

    def mark(self, lrec):
        self._mark = lrec
        log.debug("BOOKMARK LINE: %r" % lrec.payload[:20])
        fd = open(self._fpath, 'w')
        fd.write(lrec.line)
        fd.close()

    def __call__(self, feeder):
        for lines in feeder:
            yield self._filter_lines(lines)

    def _filter_lines(self, lines):
        for lrec in lines:
            if not self._mark:
                yield lrec
            elif self._mark < lrec:
                yield lrec
            else:
                log.debug('SKIPPING PROCESSED LINE: %r', lrec.payload[:20])

class NullBookmark(object):
    """ I pass through all the records """
    def mark(self, line):
        log.debug("BOOKMARK LINE: %r" % line.payload[:20])

    def __call__(self, feeder):
        for line in feeder:
            yield line
