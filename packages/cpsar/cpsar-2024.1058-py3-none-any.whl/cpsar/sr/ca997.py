from glob import glob
import os
import shutil
import sys
from zipfile import ZipFile

from cpsar import config
from cpsar import util
from cpsar import shell
import cpsar.runtime as R


scan_dir = '/home/scott/data/ar/inbound/ca/997'
archive_dir = '/home/scott/data/ar/inbound/ca/997/archive'
ak5_status_map = {
    'A': 'Accepted',
    'E': 'Accepted But Errors Were Noted',
    'R': 'Rejected'
}
ak5_message_map = {
    '1': 'Transaction Set Not Supported',
    '2': 'Transaction Set Trailer Missing',
    '3': 'Transaction Set Control Number in ' +
         'Header and Trailer Do Not Match',
    '4': 'Number of Included Segments Does Not Match Actual Count',
    '5': 'One or More Segments in Error',
    '6': '6 Missing or Invalid Transaction Set Identifier',
    '7': 'Missing or Invalid Transaction Set Control Number',
   '23': 'Transaction Set Control Number Not Unique within ' +
         'the Functional Group'
}
ak9_status_map = {
    'A': 'Accepted',
    'E': 'Accepted, But Errors Were Noted.',
    'P': 'Partially Accepted, At Least One Transaction Set Was Rejected',
    'R': 'Rejected'
}
ak9_syntax_error_map = {
    '1': 'Functional Group Not Supported',
    '2': 'Functional Group Version Not Supported',
    '3': 'Functional Group Trailer Missing',
    '4': 'Group Control Number in the Functional Group Header and '
         'Trailer Do Not Agree',
    '5': 'Number of Included Transaction Sets Does Not Match Actual Count',
    '6': 'Group Control Number Violates Syntax'
}
ak3_error_map = {
    '2': 'Unexpected segment',
    '8': 'Segment has data element errors'
}
ak4_error_map = {
    '1': 'Mandatory data element missing',
    '3': 'Too many data elements',
    '4': 'Date element too short',
    '5': 'Data element too long',
    '6': 'Invalid character in data element',
    '8': 'Invalid date',
    '9': 'Invalid time'
}

class Program(shell.Program):
    def setup_options(self):
        super(Program, self).setup_options()
        self.add_option('-e', '--email', action='store_true',
                        help='send message in email')
        self.add_option('-a', '--no-archive', action='store_true',
                        default=False,
                        help='do not archive messages after processing')

    def main(self):
        for fpath in glob("%s/*.ATM" % scan_dir):
            self.parse(fpath)

    def parse(self, fpath):
        s = util.X12File(open(fpath))

        assert s.next()[0] == 'GS'     # GS
        assert s.next()[0] == 'ST'     # ST
        s.next()
        assert s.cur[:2] == ['AK1', 'HC'], s.cur
        s.next()

        # Transaction Set Response Loop. Could be more than one AK2
        assert s.id == 'AK2'
        assert s.qualifier == '837'
        set_control_number = s.args[0]

        messages = util.CallList()

        s.next()
        while s.id != 'SE':
            if s.id == 'AK5':
                messages("Status: %s %s", ak5_status_map[s.qualifier], s.id)
                if s.args:
                    messages("\t%s", ak5_message_map[s.args[0]])
                else:
                    messages('\tNo arguments given to AK5')
                if len(s.args) > 1:
                    messages("\tExtra arguments: %s", "*".join(s.args[1:]))
            elif s.id == 'AK3':
                messages.extend([
                    "AK3 Data Segment Error",
                    "\tSegment ID Code: %s" % s.qualifier,
                    "\tSegment Position: %s" % s.args[0],
                    "\tLoop Identifier: %s" % s.args[1],
                    "\tError Code: %s (%s)" % (ak3_error_map[s.args[2]], s.args[2])
                ])
            elif s.id == 'AK4':
                messages.extend([
                    "\tAK4 Data Element Error",
                    "\t\tPosition in Segment: %s" % s.qualifier,
                    "\t\tData Element Ref. Number: %s" % s.args[0],
                    "\t\tError Code: %s (%s)" % (ak4_error_map[s.args[1]],
                                                 s.args[1])
                ])
                if len(s.args) > 2:
                    messages("\t\tExtra Data: %s", s.args[2:])
            elif s.id == 'AK9':
                messages.append("Status: %s %s " % 
                    (ak9_status_map[s.qualifier], s.id))
                messages.extend([
                     "\tNumber of Transaction Sets Included: %s" % s.args[0],
                     "\tNumber of Received Transaction Sets: %s" % s.args[1],
                     "\tNumber of Accepted Transaction Sets: %s" % s.args[2],
                     ])
                if len(s.args) > 3:
                    messages.append("\tSyntax %s" % 
                        ak9_syntax_error_map[s.args[3]])
            else:
                messages.append("Unknown segment %s" % s.cur)
            s.next()
     
        fname = os.path.basename(fpath)
        msg = util.Mako.expand('ca997.tmpl', {
            'set_control_number': set_control_number,
            'filename': fname,
            'messages': messages,
            'segments': util.X12File(open(fpath))})

        if self.opts.email:
            util.send_email(msg, 'CA DWC 997 Message: %s' % fname,
                            [config.customer_service_email()])
        else:
            print(msg)
        if not self.opts.no_archive:
            shutil.move(fpath, os.path.join(archive_dir, fname))

if __name__ == '__main__':
    Program().run()

