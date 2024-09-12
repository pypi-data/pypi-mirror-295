from six import StringIO
import datetime
from glob import glob
import os
import shutil
import sys

from cpsar import config
from cpsar.util import X12File, send_email
import cpsar.runtime as R
import cpsar.shell

scan_dir = R.dpath("sr/ca824")
archive_dir = R.dpath("sr/ca824/archive")
error_codes = {
    '001' :    'Mandatory field not present',
    '028' :    'Must be numeric (0-9)',
    '029' :    'Must be a valid date (CCYYMMDD)',
    '030' :    'Must be A-Z, 0-9, or spaces',
    '033' :    'Must be <= Date of Injury',
    '034' :    'Must be >= Date of Injury',
    '039' :    'No match on database',
    '040' :    'All digits cannot be the same',
    '041' :    'Must be <= Current date',
    '042' :    'Not statutorily valid',
    '044' :    'Value is > than required by jurisdiction',
    '045' :    'Value is < than required by jurisdiction',
    '050' :    'No matching Subsequent report (A49)',
    '053' :    'No matching FROI (148)',
    '054' :    'Must be valid occurrence for segment',
    '057' :    'Duplicate transmission/transaction',
    '058' :    'Code/ID invalid',
    '059' :    'Value not consistent with value previously reported',
    '061' :    'Event Criteria not met',
    '062' :    'Required segment not present',
    '063' :    'Invalid event sequence/relationship',
    '064' :    'Invalid data sequence/relationship',
    '065' :    'Corresponding report/data not found',
    '066' :    'Invalid record count',
    '070' :    "Must be <= 'From' Service Date",
    '071' :    "Must be >= 'Thru' Service Date",
    '072' :    "Must be > Date of Bill",
    '073' :    "Must be >= Date payer received bill",
    '074' :    "Must be >= 'From' Service Date",
    '075' :    "Must be <= 'Thru' Service Date"
}

data_elements = {
    110: 'ACKNOWLEDGMENT TRANSACTION SET ID',
    513: 'ADMISSION DATE',
    535: 'ADMITTING DIAGNOSIS CODE',
    111: 'APPLICATION ACKNOWLEDGMENT CODE',
    564: 'BASIS OF COST DETERMINATION CODE',
    532: 'BATCH CONTROL NUMBER',
    545: 'BILL ADJUSTMENT AMOUNT',
    543: 'BILL ADJUSTMENT GROUP CODE',
    544: 'BILL ADJUSTMENT REASON CODE',
    546: 'BILL ADJUSTMENT UNITS',
    508: 'BILL SUBMISSION REASON CODE',
    503: 'BILLING FORMAT CODE',
    629: 'BILLING PROVIDER FEIN',
    528: 'BILLING PROVIDER LAST/GROUP NAME',
    542: 'BILLING PROVIDER POSTAL CODE',
    537: 'BILLING PROVIDER PRIMARY SPECIALTY CODE',
    630: 'BILLING PROVIDER STATE LICENSE NUMBER',
    523: 'BILLING PROVIDER UNIQUE BILL IDENTIFICATION NUMBER',
    502: 'BILLING TYPE CODE',
    15: 'CLAIM ADMINISTRATOR CLAIM NUMBER',
    187: 'CLAIM ADMINISTRATOR FEIN',
    188: 'CLAIM ADMINISTRATOR NAME',
    515: 'CONTRACT TYPE CODE',
    512: 'DATE INSURER PAID BILL',
    511: 'DATE INSURER RECEIVED BILL',
    510: 'DATE OF BILL',
    31: 'DATE OF INJURY',
    108: 'DATE PROCESSED',
    100: 'DATE TRANSMISSION SENT',
    554: 'DAYS/UNITS BILLED',
    553: 'DAYS/UNITS CODE',
    557: 'DIAGNOSIS POINTER',
    514: 'DISCHARGE DATE',
    562: 'DISPENSE AS WRITTEN CODE',
    567: 'DME BILLING FREQUENCY CODE',
    518: 'DRG CODE',
    563: 'DRUG NAME',
    572: 'DRUGS/SUPPLIES BILLED AMOUNT',
    579: 'DRUGS/SUPPLIES DISPENSING FEE',
    571: 'DRUGS/SUPPLIES NUMBER OF DAYS',
    570: 'DRUGS/SUPPLIES QUANTITY DISPENSED',
    116: 'ELEMENT ERROR NUMBER',
    115: 'ELEMENT NUMBER',
    152: 'EMPLOYEE EMPLOYMENT VISA',
    44: 'EMPLOYEE FIRST NAME',
    43: 'EMPLOYEE LAST NAME',
    45: 'EMPLOYEE MIDDLE NAME',
    153: 'EMPLOYEE GREEN CARD',
    156: 'EMPLOYEE PASSPORT NUMBER',
    42: 'EMPLOYEE SOCIAL SECURITY NUMBER',
    504: 'FACILITY CODE',
    679: 'FACILITY FEIN',
    681: 'FACILITY MEDICARE NUMBER',
    678: 'FACILITY NAME',
    688: 'FACILITY POSTAL CODE',
    680: 'FACILITY STATE LICENSE NUMBER',
    737: 'HCPCS BILL PROCEDURE CODE',
    714: 'HCPCS LINE PROCEDURE BILLED CODE',
    726: 'HCPCS LINE PROCEDURE PAID CODE',
    717: 'HCPCS MODIFIER BILLED CODE',
    727: 'HCPCS MODIFIER PAID CODE',
    626: 'HCPCS PRINCIPAL PROCEDURE BILLED CODE',
    522: 'ICD_9 CM DIAGNOSIS CODE',
    525: 'ICD_9 CM PRINCIPAL PROCEDURE CODE',
    736: 'ICD_9 CM PROCEDURE CODE',
    6: 'INSURER FEIN',
    7: 'INSURER NAME',
    105: 'INTERCHANGE VERSION ID',
    5: 'JURISDICTION CLAIM NUMBER',
    718: 'JURISDICTION MODIFIER BILLED CODE',
    730: 'JURISDICTION MODIFIER PAID CODE',
    715: 'JURISDICTION PROCEDURE BILLED CODE',
    729: 'JURISDICTION PROCEDURE PAID CODE',
    547: 'LINE NUMBER',
    704: 'MANAGED CARE ORGANIZATION FEIN',
    208: 'MANAGED CARE ORGANIZATION ID NUMBER',
    209: 'MANAGED CARE ORGANIZATION NAME',
    712: 'MANAGED CARE ORGANIZATION POSTAL CODE',
    721: 'NDC BILLED CODE',
    728: 'NDC PAID CODE',
    102: 'ORIGINAL TRANSMISSION DATE',
    103: 'ORIGINAL TRANSMISSION TIME',
    555: 'PLACE OF SERVICE BILL CODE',
    600: 'PLACE OF SERVICE LINE CODE',
    527: 'PRESCRIPTION BILL DATE',
    604: 'PRESCRIPTION LINE DATE',
    561: 'PRESCRIPTION LINE NUMBER',
    521: 'PRINCIPAL DIAGNOSIS CODE',
    550: 'PRINCIPAL PROCEDURE DATE',
    524: 'PROCEDURE DATE',
    507: 'PROVIDER AGREEMENT CODE',
    99: 'RECEIVER ID',
    526: 'RELEASE OF INFORMATION CODE',
    642: 'RENDERING BILL PROVIDER FEIN',
    638: 'RENDERING BILL PROVIDER LAST/GROUP NAME',
    656: 'RENDERING BILL PROVIDER POSTAL CODE',
    651: 'RENDERING BILL PROVIDER PRIMARY SPECIALTY CODE',
    649: 'RENDERING BILL PROVIDER SPECIALTY LICENSE NUMBER',
    643: 'RENDERING BILL PROVIDER STATE LICENSE NUMBER',
    592: 'RENDERING LINE PROVIDER NATIONAL ID',
    586: 'RENDERING LINE PROVIDER FEIN',
    589: 'RENDERING LINE PROVIDER LAST/GROUP NAME',
    593: 'RENDERING LINE PROVIDER POSTAL CODE',
    595: 'RENDERING LINE PROVIDER PRIMARY SPECIALTY CODE',
    599: 'RENDERING LINE PROVIDER STATE LICENSE NUMBER',
    615: 'REPORTING PERIOD',
    559: 'REVENUE BILLED CODE',
    576: 'REVENUE PAID CODE',
    98: 'SENDER ID',
    733: 'SERVICE ADJUSTMENT AMOUNT',
    731: 'SERVICE ADJUSTMENT GROUP CODE',
    732: 'SERVICE ADJUSTMENT REASON CODE',
    509: 'SERVICE BILL DATE(S) RANGE',
    605: 'SERVICE LINE DATE(S) RANGE',
    104: 'TEST/PRODUCTION INDICATOR',
    109: 'TIME PROCESSED',
    101: 'TIME TRANSMISSION SENT',
    516: 'TOTAL AMOUNT PAID PER BILL',
    574: 'TOTAL AMOUNT PAID PER LINE',
    501: 'TOTAL CHARGE PER BILL',
    566: 'TOTAL CHARGE PER LINE - PURCHASE',
    565: 'TOTAL CHARGE PER LINE - RENTAL',
    552: 'TOTAL CHARGE PER LINE -OTHER',
    266: 'TRANSACTION TRACKING NUMBER',
    500: 'UNIQUE BILL ID NUMBER',
    699: 'REFERRING PROVIDER NATIONAL PROVIDER ID'
}
ack_code2 = {
    'A': 'Accept',
    'E': 'Accept with Errors',
    'R': 'Reject'
}


class Program(cpsar.shell.Program):
    def setup_options(self):
        super(Program, self).setup_options()
        self.add_option('-n', '--no-email', dest='no_email',
                        action='store_true',
                        help='Do not send email report')

    def main(self):
        for file in glob("%s/*ATM" % scan_dir):
            R.log.info("Parsing %s" % os.path.basename(file))
            data = open(file).read(-1)
            self.parse(data, file)

    def parse(self, data, filepath):
        cursor = R.db.cursor()
        buf = StringIO()
        buf.write("824 Report\n\n")
        segments = X12File(StringIO(data))
        file_name = os.path.basename(filepath)
        file_824_id = None
       
        # CREATE the file_data for state_report_824.file_data 
        file_segments = []
        for line in segments:
            file_segments.append("*".join(line))
        file_data = ("\n".join(file_segments))
        
        # Create an entry in the 824 table or update the existing one
        cursor.execute("""
            UPDATE state_report_824
            SET file_data = %s
            WHERE file_name = %s
            returning file_824_id
            """, (file_data, file_name,))
        if cursor.rowcount == 0:
            cursor.execute("""
                INSERT INTO state_report_824 
                (file_data, file_name)
                VALUES(%s, %s)
                returning file_824_id
                """, (file_data, file_name,))
        file_824_id, = cursor.fetchone()

        segments.next()     # GS
        segments.next()     # ST
        segments.next()     # BGN
        segments.next()     # N1 (submitter)
        segments.next()     # N4
        segments.next()     # N1 (Receiver)
        segments.next()     # N4
        segments.next()     # OTI

        while segments.cur[0] == 'OTI':
            R.log.debug("Parsing OTI")
            code = segments.cur[1] #second segment of OTI line
            code_msg = ack_code2[code[1]] #BA/TA/TE/TR
            cur_date = datetime.date.today()
            entry_id = segments.cur[3]

            if code[0] == 'T':
                cursor.execute("""
                    UPDATE state_report_entry
                    SET file_824_id=%s
                    WHERE entry_id=%s
                    AND (file_824_id!=%s
                        OR file_824_id IS NULL)
                    """, (file_824_id, segments.cur[3], file_824_id,))

                # Get the trans id
                cursor.execute("""
                    SELECT trans_id
                    FROM state_report_entry
                    WHERE entry_id=%s 
                    """, (segments.cur[3],))
                trans_id = cursor.fetchone()

                # Get the ack code for entry
                cursor.execute("""
                    SELECT ack_code
                    FROM state_report_entry
                    WHERE entry_id=%s
                    AND ack_code = 'R'
                    """, (segments.cur[3],))
                buf.write(" Transaction ID = %s " % trans_id)

                if cursor.rowcount == 0:
                    # Mark as orig or update rejection
                    cursor.execute("""
                        UPDATE state_report_entry 
                        SET ack_code=%s,
                            response_date=%s
                        WHERE entry_id=%s
                        """, (code[1], cur_date, entry_id))
                    buf.write("Transaction ")
                else:
                    # update a cancel or update canceled rejection
                    cursor.execute("""
                        UPDATE state_report_entry 
                        SET cancel_ack_code=%s,
                            pending_cancel=False,
                            cancel_date=%s
                        WHERE entry_id=%s
                        """, (code[1], cur_date, segments.cur[3]))
                    buf.write("Cancellation ")
            elif code[0] == 'B':
                buf.write(" Batch ")
            else:
                raise ValueError("Unknown code %r in OTI" % code[0])

            if code[1] == 'A':
                buf.write("Accepted ")
            elif code[1] == 'E':
                buf.write("Accepted with Errors ")
            elif code[1] == 'R':
                buf.write("Rejected ")
                # increase rejection count for record
                cursor.execute("""
                    UPDATE state_report_entry
                    SET rejection_count = rejection_count + 1
                    WHERE entry_id=%s 
                    """, (segments.cur[3],))
            else:
                raise ValueError("Unexpected code for %s, of value %s" 
                                % segments.cur[3], code[1])
            buf.write("\n")
            
            #SEGMENTS BELOW WOULD BE WHERE WE'D UPDATE THE WORK-QUE
            segments.next()   # DTM Don't care about when it was processed
                              # with multiple errors there's no DTM line

            # IF this line is a 'DTM' space again to get to LM otherwise check ot
            # We should be on the LM
            if segments.cur[0] == 'DTM':
                segments.next()   # LM

            if segments.cur[0] == 'LM': 
                R.log.debug("Processing %s" % segments.cur)
                segments.next()   # LQ
                if segments.cur[0] != 'LQ':
                    raise ValueError("Expected LQ got %s" % segments.cur[0])
                error_code = segments.cur[2]
                error_msg = error_codes[error_code]

                response_list = []
                while segments.cur[0] == 'LQ':
                    segments.next()   # RED
                    while segments.cur[0] == 'RED' and segments.cur[5] == 'A9':
                        field = int(segments.cur[6])
                        field_name = data_elements[field]
                        segments.next()
                    
                    while segments.cur[0] == 'RED':
                        field = int(segments.cur[6])
                        field_name = data_elements[field]
                        response_desc = ("    DN %04d %s - CODE: %s %s" % (
                                  field, field_name, error_code, error_msg))
                        buf.write("%s\n" % response_desc) 
                        response_list.append(response_desc)
                        segments.next()
                        if segments.cur[0] == 'LM':
                            segments.next()

                cursor.execute("""
                    UPDATE state_report_entry
                    SET response_desc = %s
                    WHERE entry_id = %s
                    """, (response_list, entry_id))

        segments.next()     # SE
        segments.next()     # GE
        segments.next()     # IEA

        segments = X12File(StringIO(data))
        buf.write("\nRAW X12 DATA\n" + "-" * 80 + "\n")
        for line in segments:
            buf.write("*".join(line) + "\n")

        filename = os.path.basename(filepath)
        buf.seek(0)
        msg = buf.getvalue()

        if not self.opts.no_email:
            send_email(msg, 'CA DWC 824 Message: %s' % filename, config.customer_service_email())
        else:
            print(msg)

        if not self.opts.dry_run:
            shutil.move(filepath, os.path.join(archive_dir, filename))
            R.db.commit()

if __name__ == '__main__':
    Program().run()
