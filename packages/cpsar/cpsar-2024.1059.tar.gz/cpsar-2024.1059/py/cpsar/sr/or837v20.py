"""
Produces an 837 file to send to Texas Remote Server

The program queries the state_report_entry table for transactions that do
not have file_id's or entries that are pending cancelation and do not have
cancel_file_id's.

Records are inserted into state_report_file table and the file_id's are
set on the entry records.

detects current working env
_testing allows for dme/mo billing set to false for production


"""
import datetime
import os
import zipfile

from cpsar.runtime import db, dpath
from cpsar.sr.model import DataService
from cpsar.util import update_sql
from cpsar.config import development

def create_837_file():
    db.setup()
    data = DataService(db, 'OR')
    items = data.unreported_items()

    dev = development()
    working_env = 'P'
    if dev == True:
        working_env = 'T'

    if not items:
        return

    control_number = next_control_number(db)
    file_date = datetime.datetime.now()
    sequence_number = next_sequence_number(db, file_date)
    xfile = X12File(items, file_date, working_env, control_number, sequence_number)
    writer = X12Writer(xfile.path)
    isa = ISA(xfile)
    isa.write_segments(writer)
    sfile = data.new_state_report_file(xfile.name, '837')

    cursor = db.cursor()
    if items:
        for item in items:
            if item.entry.file_id is None:
                cursor.execute(update_sql("state_report_entry",
                    {'file_id': sfile.file_id},
                    {'entry_id': item.entry.entry_id}))
            else:
                cursor.execute(update_sql("state_report_entry",
                    {'cancel_file_id': sfile.file_id},
                    {'entry_id': item.entry.entry_id}))

    writer.close()
    store_837_file_data(db, sfile.file_id, xfile.path)

    # Toggle commits for dev
    #  db.commit()

    if working_env == 'P':
        db.commit()

# ----------------------------------------------------------------------
def next_control_number(db):
    cursor = db.cursor()
    cursor.execute("SELECT nextval('tx_837_control_number')")
    return cursor.fetchone()[0]

def next_sequence_number(db, file_date):
    cursor = db.cursor()
    cursor.execute("""
                SELECT COUNT(*)+1 
                FROM state_report_file
                WHERE create_date::date=%s
                AND reportzone='OR'
                """, (file_date,))
    return cursor.fetchone()[0]

def store_837_file_data(db, file_id, fpath):
    cursor = db.cursor()
    file_data = open(fpath).read(-1).replace("~", "\n")
    cursor.execute("""
        UPDATE state_report_file
        SET file_data = %s
        WHERE file_id = %s 
        """, (file_data, file_id,))

# ---------------------------------------------------------------------
class X12File(object):
    def __init__(self, items, file_date, usage_indicator,
                 control_number, sequence_number):
        self._items = items
        self._file_date = file_date
        self.usage_indicator = usage_indicator.upper()
        self.control_number = control_number
        self._sequence_number = sequence_number
        self._writer = None
        self.st_control_number = 1

    ## File Properties
    @property
    def items(self):
        return self._items

    @property
    def path(self):
        return dpath("sr/or837", self.name)

    @property
    def yyyymmdd(self):
        return self._file_date.strftime("%Y%m%d")

    @property
    def yymmdd(self):
        return self._file_date.strftime("%y%m%d")

    @property
    def hhmm(self):
        return self._file_date.strftime("%H%M")

    @property
    def hhmmss(self):
        return self._file_date.strftime("%H%M%S")

    @property
    def name(self):
        return (
           'OR_631040950_' +
           self.usage_indicator + "_" +
           self.yyyymmdd + "_" +
           self.hhmmss + "_" +
           self._sequence_number_nnn +
           "_837")

    @property
    def _sequence_number_nnn(self):
        return "%03d" % self._sequence_number

class ISA(object):
    def __init__(self, xfile):
        self._xfile = xfile
        self._items = xfile.items

    @property
    def control_number_fmt_9n(self):
        return "%09d" % self._xfile.control_number

    def write_segments(self, writer):
        xfile = self._xfile
        xfile.control_number = self.control_number_fmt_9n
        writer.write_segment([
            'ISA',              # Authorization Information Qualifier
            '00',               # Code to identify the type of information in
                                    # the Authorization Information
            '          ',       # Authorization Information
            '00',               # Security Information Qualifier
            '          ',       # Security Information
            'ZZ',               # Interchange ID Qualifier
            '631040950      ',  # Interchange Sender ID -  FEIN
            'ZZ',               # Interchange ID Qualifier
            '930952020      ', # Interchange Receiver ID
            xfile.yymmdd,       # Interchange Date (YYMMDD)
            xfile.hhmm,         # Interchange Time (HHMM)
            '^',                # Interchange Control Standards Identifier
            '00501',            # Interchange Control Version Number
            xfile.control_number,  # Interchange Control Number
            '0',                # Acknowledgment Requested
            xfile.usage_indicator, # Usage Indicator
            ':'                 # Component Element Separator
        ])

        #///////////////////////////////////////////////////////////////////////
        # FUNCTIONAL GROUP HEADER
        writer.write_segment([
            'GS',
            'HC',               # Functional Identifier Code
            '631040950',        # Application Sender's Code (CPS FEIN)
            '930952020',        # Application Receiver's Code
            xfile.yyyymmdd,     # Use this date for the functional group
                                # creation date. 
            xfile.hhmm,         # Time
            '00001',            # Group Control Number
            'X',                # Responsible Agency Code
            '005010I20'         # Version / Release / Industry Identifier Code
        ])



        #///////////////////////////////////////////////////////////////////////
        # SOURCE OF HIERARCHICAL LEVEL INFORMATION   (REPEAT >1)
        # We output one of these levels for every batch that we have to
        # report on. A batch is a batch date and group number
        #XXX WARNING! Texas says they don't like more than one HL1 in the
        # same set. says we should start over with ST/SE. This is not a
        # problem right now since we only have Texas Builders.
        for carrier in self._carriers():
            carrier.write_segments(writer, xfile )
            xfile.st_control_number +=1


        #///////////////////////////////////////////////////////////////////////
        # FUNCTIONAL GROUP TRAILER
        writer.write_segment([
            'GE',
            '1',                # Number of Transaction Sets Included
            '00001',                # Control Number
        ])

        #///////////////////////////////////////////////////////////////////////
        # INTERCHANGE CONTROL TRAILER
        writer.write_segment([
            'IEA',              # Interchange Control Trailer
            '1',                # Number of Included Functional Groups
            xfile.control_number  # Interchange Control Number
        ])

    def _carriers(self):
        for client, client_items in self._items.grouped_by('client'):
            yield Carrier(client, client_items)

class Carrier(object):
    def __init__(self, client, client_items):
        self._client = client
        self._client_items = client_items

        """
        output = []
        for item in self._client_items:
            output.append(item.client.client_name)
        raise ValueError(output)
        """
    @property
    def st_control_number_fmt_9n(self):
        return str(self._xfile.st_control_number).zfill(5)

    def write_segments(self, writer, xfile):
        client = self._client
        self._xfile = xfile
        self._st_control_number = self.st_control_number_fmt_9n

        
        #///////////////////////////////////////////////////////////////////////
        # TRANSACTION SET 

        ## TRANSACTION SET HEADER
        writer.start_segment_counting()
        writer.write_segment([
            'ST',
            '837',                   # The version of the set
            self._st_control_number, # Set Control Number
            '005010I20'              # Set Control Number
        ])

        ## BEGINNING OF HIERARCHICAL TRANSACTION
        writer.write_segment([
            'BHT',
            '0080',             # Hierarchical Structure Code
            '00',               # Transaction Set Purpose Code
            self._xfile.control_number,     # Originator Transaction Identifier
            self._xfile.yyyymmdd,     # Transaction Set Creation Date
            self._xfile.hhmm,          # Transaction Set Creation Time
            'rp'
        ])

        "1000A ########################################################"
        # SENDER INFORMATION
        ## SUBMITTER NAME
        ## Corporate Pharmacy Information
        writer.write_segment([
            'NM1',
            '41',               # NM101: Entity Identifier Code (2.0)
            '2',                 # NM102: Entity Type Qualifier
            '', '', '', '', '', # NM103-NM107 Blank
            '46',               # NM108: Identification Code Qualifier (FEIN)
            '631040950'         # NM109: Identification Code 
            '', '', ''          # NM1010-12 (2.0)
        ])

        "1000B #######################################################"
        # RECEIVER INFORMATION
        ## RECEIVER NAME
        writer.write_segment([
            'NM1',
            '40',               # NM101: Entity Identifier Code
            '2',                 # NM102: Entity Type Qualifier
            '', '', '', '', '', # NM103-NM107 Blank
            '46',               # NM108: Identification Code Qualifier (FEIN)
            '930952020'         # NM109: Identification Code 
        ])

        #2000A
        writer.write_hl_segment('', '20', '1')

        ## REPORTING PERIOD DATE OR TIME PERIOD
        writer.write_segment([
            'DTP',
            '582',              # DTP01: Date/Time Qualifier XXX: What is this?
            'RD8',              # DTP02: Range of dates expressed in format 
                                #        CCYYMMDD-CCYYMMDD
            self._time_period,  # DTP03: Date/Time Period
                                #        (DN615 Reporting Period)
        ])

        "2010AA ######################################################"
        ## Client Information (Insurer / Self-Insured)
        # if there is no client.insurer use client.client_name and tin
        writer.write_segment([
            'NM1',
            'CA',               # NM101: Entity Identifier Code
                                #        (Billing Provider)
            '2',                # NM102: Entity Type Qualifier (Company)
            client.insurer,     # NM103: Last Name or Organization Name
            '', '', '', '',     # NM104-NM107: Blank
            'FI',               # NM108: Identification Code Qualifier (FEIN)
            client.insurer_tin  # NM109: Identification Code
        ])

        ##  - Zip Code
        writer.write_segment([
            'N4',
            '', '',             # N401-N402: Blank
            client.insurer_zip  # N403: Postal Code
        ])

        ## Claim Administrator Information (Insurer / Self-Insured) - Carrier
        writer.write_segment([
            'NM1',
            'CX',               # NM101: Entity Identifier Code
                                #        (Billing Provider)
            '2',                # NM102: Entity Type Qualifier (Company)
            client.claim_admin_name, # NM103: Last Name or Organization Name
            '', '', '', '',     # NM104-NM107: Blank
            'FI',               # NM108: Identification Code Qualifier (FEIN)
            client.claim_admin_fein          # NM109: Identification Code
        ])

        ## Claim Administrator - Postal Code
        writer.write_segment([
            'N4',
            '', '',             # N401-N402: Blank
            client.claim_admin_zip     # N403: Postal Code
        ])

        my_hlevel = writer.hlevel
        for employer in self._employers():
            employer.write_segments(writer, my_hlevel)

        #///////////////////////////////////////////////////////////////////////
        # TRANSACTION SET TRAILER
        writer.write_segment([
            'SE',
            writer.segment_count+1,     # Number of segments between ST and SE (inc)
            self._st_control_number # Set Control Number
        ])

    @property
    def _time_period(self):
        batch_dates = [i.trans.batch_date for i in self._client_items]
        min_date = min(batch_dates).strftime("%Y%m%d")
        max_date = max(batch_dates).strftime("%Y%m%d")
        return "%s-%s" % (min_date, max_date)

    def _employers(self):
        for employer, employer_items in self._client_items.grouped_by('employer'):
            yield Employer(employer, employer_items)

class Employer(object):
    def __init__(self, employer, employer_items):
        self._employer = employer
        self._employer_items = employer_items

    _testing = False 

    def write_segments(self, writer, parent_hlevel):
        employer = self._employer
        writer.write_hl_segment(parent_hlevel, 'EM', '1')

        "2010BA #######################################################"
        writer.write_segment([
            'NM1',
            '36',               # NM101: Entity Identifier Code
            '2',                # NM102: Entity Type Qualifier
            employer.name,      # NM103: Organization  Name (Employer Name)
            '', '', '', '',     # NM104-NM107: Blank
            '',                 # NM108: Identification Code Qualifier (FEIN)
            ''                  # NM109: Identification Code
        ])

        ## Employer's Address
        if employer.address_1 or employer.address_2:
            writer.write_segment([
                'N3',
                employer.address_1,        # N301: Address
                employer.address_2         # N302: Address
            ])

            ## Employer's City, State, Zip
            writer.write_segment([
                'N4',
                employer.city,             # N401: City
                employer.state,            # N402: State
                employer.zip_code,         # N403: Postal Code
                'USA'                      # N404: Country Code
            ])

        my_hlevel = writer.hlevel

        for item in self._employer_items:
            service_item = ServiceItem(item)
            service_item.write_segments(writer, my_hlevel)

class ServiceItem(object):
    def __init__(self, item):
        self._item = item

    _claim_type_code="RX"
    _service_date_qualifier="471" #Only changes for DM items

    @property
    def _reason_code(self):
        entry = self._item.entry
        if entry.file_id is None:
            return '00'
        else:
            return '01'

    def write_segments(self, writer, parent_hlevel):
        patient = self._item.patient
        claim = self._item.claim
        trans = self._item.trans
        entry = self._item.entry
        pharmacy = self._item.pharmacy
        history = self._item.history
        doctor = self._item.doctor
        drug = self._item.drug
        reason_code = self._reason_code
        type_code = self._claim_type_code
        service_date_qualifier = self._service_date_qualifier

        #///////////////////////////////////////////////////////////////////////
        # Patient Hierarchical Level   ( Repeat >1)
        writer.write_hl_segment(parent_hlevel, 'CL', '0')

        "2000C ########################################################"
        # Date of Injury
        writer.write_segment([
            'DTP',
            '558',              # DTP01: Date/Time Qualifier (Injury or Illness)
            'D8',               # DTP02: Date Time Period Format Qualifier
                                #        (Date Expressed in Format CCYYMMDD)
            claim.doi_yyyymmdd  # DTP03: Date Time Period (DN31 Date of Injury)
        ])

        "2010CA #######################################################"
        # Patient (Employee) Information
        writer.write_segment([
            'NM1',
            'CC',               # NM101: Entity Identifier Code (Claimant)
            '1',                # NM102: Entity Type Qualifier: 1 = person
            patient.last_name,  # NM103: Last Name
            patient.first_name, # NM104: First Name
            '',                 # NM105: Middle Name
            '',                 # NM106: Blank
            '',                 # NM107: Name Suffix
            '34',               # NM108: Identification Code Qualifier
                                #        (34 = SSN)
            patient.ssn         # NM109: 
        ])

        # Patient Address
        patient_address_1 = ''
        patient_address_2 = ''

        if patient.address_1: 
            patient_address_1 = patient.address_1

        if patient.address_2:
            if patient_address_1 == '':
                patient_address_1 =  patient.address_2
            else: 
                patient_address_2 = patient.address_2

        writer.write_segment([
            'N3',
            patient_address_1,   # N301: Employee Mailing Primary Address
            patient_address_2    # N302: Employee Mailing Secondary Address
        ])

        writer.write_segment([
            'N4',
            patient.city,             # N401: City
            patient.state,            # N402: State
            patient.zip_code,         # N403: Zip Code
            'USA'                     # N404: Country Code
        ])

        # Patient Demographic Information
        gender = 'U'
        if patient.sex == '1':
            gender = 'M'
        if patient.sex == '2':
            gender = 'F'
        patient_dob = patient.dob.strftime("%Y%m%d")
        writer.write_segment([
            'DMG',
            'D8',               # DMG01: Date Time Period Format Qualifier
            patient_dob,        # DMG02: Birth Date
            gender              # DMG03: Geneder Code (F/M/U)
        ])

        # REFERENCE IDENTIFICATION
        writer.write_segment([
            'REF',              
            'Y1',                   # 1
            claim.claim_number      # 2 CLAIM ADMINISTRATOR CLAIM NUMBER - DN15
            ])

        "2010CA #######################################################"
        # Claim Information      ( Repeat 100)
        writer.write_segment([
            'CLM',
            entry.entry_id,     # CLM01: Claim Submitter Identifier (Provider
                                #        Unique Bill Identification Number)
            trans.total,        # CLM02: DN501 Total Charge Per Bill
            '',                 # CLM03: Blank
            '',                 # CLM04: Non-Institutional Claim Type Code
                                #        (DM/MO/RX
            '99:D',             # CLM05: Facility Code Value ( Facility Code or
                                #        Place of Service Bill Code)
            'Y',                # CLM06: Provider Signature on File
            '', '',             # CLM07-CLM08: Blank
            '',                 # CLM09: Release of Information Code
            '', '', '', '', '', # CLM10-CLM14: Blank
            '',                 # CLM15: Blank
            'N',                # CLM16: Provider Agreement Code (DN507)
            '', '',             # CLM17-CLM18: Blank
            reason_code         # CLM19: Claims Submission Reason Codes
        ])

        #///////////////////////////////////////////////////////////////////////
        # Date Insurer Received Bill
        writer.write_segment([
            'DTP',
            '050',              # DTP01: Date/Time Qualifier (Received)
            'D8',               # DTP02: Date Time Period Format Qualifier
            trans.received_bill_date_yyyymmdd # DTP03: Date Insurer Received Bill (DN511)
        ])

        #///////////////////////////////////////////////////////////////////////
        # Date of Bill
        writer.write_segment([
            'DTP',
            '434',                      # DTP01: Date/Time Qualifier (Received)
            'D8',                       # DTP02: Date Time Period Format Qualifier
            trans.create_date_yyyymmdd  # DTP03: Date/Time Period (DN510)
        ])

        #///////////////////////////////////////////////////////////////////////
        # Service Date
        writer.write_segment([
            'DTP',
            '472',              # 01: Date/Time Qualifier (Received)
            'D8',               # 02: Date Time Period Format Qualifier
            history.rx_date.strftime("%Y%m%d") # 03: SERVICE DATE (DN521)
        
        ])

        #///////////////////////////////////////////////////////////////////////
        # Date Insurer Paid Bill
        writer.write_segment([
            'DTP',
            '666',              # 01: Date/Time Qualifier (Received)
            'D8',               # 02: Date Time Period Format Qualifier
            trans.paid_date_yyyymmdd  # 03: Date Insurer Received Bill (DN511)
        ])

        #///////////////////////////////////////////////////////////////////////
        # Amount Qualifier Code (Total Payment Amount)
        writer.write_segment([
            'AMT',
            'TP',               # 01: Amount Qualifier Code Total Payment
                                #     Amount
            trans.paid_amount   # 02: Total Amount Paid Per Bill (DN516)
        ])

        #///////////////////////////////////////////////////////////////////////
        # Unique Bill ID Number
        writer.write_segment([
            'REF',
            'DD',               # REF01: Reference Identification Qualifier
                                #        (Document Identification Number)
            entry.entry_id,     # REF02: Reference Identification
                                #        (Unique Bill ID Number - DN500)
        ])

        #///////////////////////////////////////////////////////////////////////
        # Transaction Tracking Number
        writer.write_segment([
            'REF',
            '2I',               # 01: Reference Identification Qualifier
                                #        (Tracking Number)
            trans.trans_id,     # 02: Reference Identification
                                #        (Transaction Tracking Number - DN266)
        ])

        "2310A #######################################################"
        # Billing Provider Information - CPS
        writer.write_segment([
            'NM1',
            '85',             # NM101: Entity Identifier Code (Billing Provider)
            '2',                # NM102: Entity Type Qualifier (2 = company)
            'Corporate Pharmacy', # NM103: Last Name or Organization Name
            '',                 # NM104: First Name
            '',                 # NM105: Middle Name
            '',                 # NM106: Blank
            '',                 # NM107: Suffix
            '',                 # NM108: Identification Code Qualifier
            '',                 # NM109: Identification Code
            '',                 # NM110: Entity Relationship Code
            ''                  # NM111: Gateway Provider
        ])

        #///////////////////////////////////////////////////////////////////////
        # Billing Provider Address
        writer.write_segment([
            'N3',
            '319 Broadstreet',  # N301: Billing Provider Primary Address
            ''                  # N302: Billing Provider Secondary Address
        ])

        writer.write_segment([
            'N4',
            'Gadsden',          # N401: City
            'AL',               # N402: State
            '35901',            # N403: Zip Code
            'USA',              # N404: Country Code
        ])

        # Billing provider FEIN
        writer.write_segment([
            'REF',
            'EI',
            '631040950'
        ])

        "2310B #######################################################"
        # Rendering Provider
        pharmacy_tax_idc = ''   # Not required if we don't have it blank it out
        pharmacy_tax_id = ''
        if pharmacy.npi:
            pharmacy_npi_idc = 'XX'
            pharmacy_npi = pharmacy.npi
        writer.write_segment([
            'NM1',
            '82',               # NM101: Entity Identifier Code (Rendering)
            '2',                # NM102: Entity Type Qualifier
            pharmacy.name,      # NM103: Last Name or Organization Name
            '',                 # NM104: First Name
            '',                 # NM105: Middle Name
            '',                 # NM106: Blank
            '',                 # NM107: Suffix
            pharmacy_npi_idc,   # NM108: Identification Code Qualifier
            pharmacy_npi,       # NM109: Identification Code
            '',                 # NM110: Entity Relationship Code
            ''                  # NM111: Gateway Provider
        ])

        "2310C #######################################################"
        "2310D #######################################################"
        "2310E #######################################################"
        # Referring Provider's Information
        writer.write_segment([
            'NM1',
            'DN',               # 01: Entity Identifier Code (Referring)
            '1',                # 02: Entity Type Qualifier (Person)
            doctor.name,        # 03: Last Name
            'Dr',               # 04: First Name
            '',                 # 05: Middle Name
            '',                 # 06: Blank
            '',                 # 07: Suffix
            '',                 # 08: Identification Code Qualifier
            ''                  # 09: Identification Code
        ])

        "2400 #######################################################"
        # Service Lines  (Repeat >1)
        writer.write_segment([
            'LX',
            '1'                 # LX01: Line Number
        ])
        ## Prescription Drug Service
        self._write_SV_segment(writer)

        ## date prescription was written 
        writer.write_segment([
            'DTP',
            '472',  # DTP01: Date/Time Qualifier (Service)
            'D8',                    # DTP02: Date Time Period Format Qualifier
            trans.date_written.strftime("%Y%m%d")     # DTP03: Service Date(s)
        ])

        ## Service Date(s)
        history_rx_date = history.rx_date.strftime("%Y%m%d")
        writer.write_segment([
            'DTP',
            service_date_qualifier,  # DTP01: Date/Time Qualifier (Service)
            'D8',                    # DTP02: Date Time Period Format Qualifier
            history_rx_date     # DTP03: Service Date(s)
        ])



        ## Quantity
        writer.write_segment([
            'QTY',
            'SP',                # QTY01: Quantity Qualifier
            history.days_supply  # QTY02: Days Supply
        ])
        writer.write_segment([
            'QTY',
            'QB',               # QTY01: Quantity Qualifier
            history.quantity    # QTY02: Days Supply
        ])

        ## DRUGS/SUPPLIES DISPENSING FEE
        billed_amt =  trans.total
        if trans.dispense_fee > 0 :
            writer.write_segment([
                'AMT',
                'D7',               # AMT01
                trans.dispense_fee  # AMT02: DN579 DRUG/SUPPLY DISPENSE FEE ])
            ])

        ## Drug/Supply Billed Amount
        writer.write_segment([
            'AMT',
            'PB',               # AMT01: Amount Qualifier Code (Billed Amount)
            billed_amt 
        ])
        # 2420
        # didn't include

        ## Total amount paid per line (service = one drug)
        ## 2430
        writer.write_segment([
            'SVD',              
            'XX',                       # SVD01: Identification Code
            trans.paid_amount          # SVD02: Total Amount Paid Per Line
        ])

        # When 570 and 554 are not equal we have to include the CAS Line
        # this only happens for SV5 (DME records)
        # _service_adjustment_amount = 570 - 554
        # 570 and 554 will always be the same
        #
        #if self._claim_type_code=="DM":
        #    writer.write_segment([
        #        'CAS',
        #        'OA',                      # CAS01: Claim Adjustment Group Code
        #        '45',                      # CAS02: Claim Adjustment Reason Code
        #        trans.writeoff_total,      # CAS03: Service Adjustment Amount
        #        history.quantity           # DN734 CAS04: Units
        #    ])

    def _write_SV_segment(self, writer):
        history = self._item.history
        drug = self._item.drug
        writer.write_segment([
            'SV4',
            history.rx_number,              # SV401: Prescription Line Number
            "N4:%s" % drug.ndc_number,      # SV402: Composite Medical Procedure Identifier
            '', '',                         # SV403-SV404: Blank
            history.daw,                    # SV405: Dispense as Written Code
            '', '',                         # SV406-SV407: Blank
            drug.name                       # SV408: Drug Name
        ])

class DMEServiceItem(ServiceItem):
    _claim_type_code="DM"
    _service_date_qualifier="472" #Only changes for DM items

    def _write_SV_segment(self, writer):
        history = self._item.history
        drug = self._item.drug
        trans = self._item.trans
        writer.write_segment([
            'SV5',
            'HC:J1120:RR',      # SV501 Composite Medical Procedure Identifier 
            'UN',               # SV502 Unit or Basis for Measurement Code
            history.quantity,   # DN554 SV503 Quantity
            trans.total,            # SV504 Monetary Amount
            '',                 # SV505 Monetary Amount
            '4'                 # SV506 Frequency Codem
        ])

class MOServiceItem(ServiceItem):
    _claim_type_code="MO"

class X12Writer(object):
    def __init__(self, path):
        self._fd = open(path, 'w')
        self._segment_counter = None
        self._hlevel = 0

    def close(self):
        self._fd.close()

    @property
    def segment_count(self):
        return self._segment_counter

    @property
    def hlevel(self):
        return self._hlevel

    def start_segment_counting(self):
        self._segment_counter = 0

    def write_segment(self, data):
        if isinstance(data, list):
            data = list(data)
            while not data[-1]:
                del data[-1]
            data = "%s~" % "*".join(map(str, data))
        self._fd.write(data)
        self._count_segment()

    def write_hl_segment(self, parent, level_code, child_code):
        self._inc_hlevel()
        self.write_segment([
            'HL',
            str(self._hlevel),  # HL01: Hierarchical ID Number
            str(parent),        # HL02: Parent ID Number
            level_code,         # HL03: Hierarchical Level Code
            child_code          # HL04: Hierarchical Child Code
        ])

    def _count_segment(self):
        if self._segment_counter is not None:
            self._segment_counter += 1

    def _inc_hlevel(self):
        self._hlevel += 1

if __name__ == '__main__':
    create_837_file()
