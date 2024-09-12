import datetime
import csv
import functools
from six import StringIO

def bill_file(cur, status_flag, ctime):
    """ Core step in work flow """
    buf = StringIO()

    batch_number = ctime.strftime("%y%j")
    write_processor_record(buf, batch_number, ctime)

    for trans in cur.trans():
        write_pharmacy_record(buf, trans, batch_number)
        write_claim_record(buf, trans, batch_number)

    return buf.getvalue()

def write_processor_record(buf, batch_number, ctime):
    """ Processor Record - 0 Identifies the sender of the claims tape format.
    One per transmission """
    h = Helper(buf)

    #Field    Name    Format    Length    Position    Req    Description    Corporate
    h.s('0', 1)                          # 843-5Z    Record Identifier    N    1    1-1    Y    '0' - Processor Record
    h.n(0, 10)                           # 840-5W    Processor Number    N    10    2-11    Y    Unique ID Number
    h.s(batch_number, 5)                      # 806-5C    Batch Number    N    5    12-16    Y
                                            # Format = YYDDD YY=Year DDD=Julian Date
    h.s("CPS", 20)                            # 839-5V    Processor Name    A/N    20    17-36    Y
    h.s("319 Broad Street", 20)               # 836-5S    Processor Address    A/N    20    37-56    Y
    h.s("Gadsden", 18)                        # 837-5T    Processor Location City    A/N    18    57-74    Y
    h.s("AL", 2)                              # 838-5U    Processor Location Sate    A/N    2    75-76    Y
    h.s("35906", 9)                           # 842-5Y    Processor Zip Code    A/N    9    77-85    Y
    h.s("2565439000", 10)                     # 841-5X    Processor Telephone Number    N    10    86-95    Y
    h.d(ctime)                                # 845-6B    Run Date    N    8    96-103    Y
        # Date on which carrier generated tape.  Format = CCYYMMDD
    h.s("", 1)                                # 846-6C    Third Party Type    A/N    1    104-104    N    Space
    h.s("", 2)                                # 102-A2    Version / Release Number    N    2    105-106    N    Spaces
    h.s("631040950", 9)                       #  PBM Federal Tax ID    A/N    9    107-115    Y    PBM Federal Tax ID
    h.s("", 385)                              # 874-GD    Unique Free Form    A/N    385    116-500    N    Filler
    h.w('\n')


def write_pharmacy_record(buf, r, batch_number):
    """ Pharmacy Record - 2 Based on ver 2.0 NCPDP
    Identifies the pharmacy that created the claim records.  One per pharmacy
    h.name    Format    Length    Position    Req    Description    Notes
    """
    h = Helper(buf)
    h.s("2", 1)                               # 843-5Z    Record Identifier    N    1    1-1    Y    2 - Pharmacy Record
    h.n(0, 10)                                # 840-5W    Processor Number    N    10    2-11    Y    Unique ID Number
    h.s(batch_number, 5)                      # 806-5C    Batch Number    N    5    12-16    Y
    h.s(r['pharmacy_nabp'], 12)               # 201-B1    Dispensing Pharmacy Number    A/N    12    17-28    Y
                                              #           ID assigned to a pharmacy
    h.s(r['pharmacy_name'], 20)               # 833-5P    Dispensing Pharmacy Name    A/N    20    29-48    Y
    h.s(r['pharmacy_address'], 20)            # 829-5L    Dispensing Pharmacy Address    A/N    20    49-68    Y
    h.s(r['pharmacy_city'], 18)               # 831-5N    Dispensing Pharmacy Location City    A/N    18    69-86    Y
    h.s(r['pharmacy_state'], 2)               # 832-5O    Dispensing Pharmacy Location State    A/N    2    87-88    Y
    h.s(r['pharmacy_zip_code'], 9)            # 835-5R    Dispensing Pharmacy Zip Code    A/N    9    89-97    Y
    h.s(r['pharmacy_phone'], 10)              # 834-5Q    Dispensing Pharmacy Telephone Number    N    10    98-107    N
    h.w('Y')                                  # In PBM Network (Default=Y)    A/N    1    108-108    Y
    h.s(r['pharmacy_nabp'], 12)               # Pay to Pharmacy Number    A/N    12    109-120    Y    ID Assigned to a pharmacy
    h.s(r['pharmacy_name'], 20)               # Pay to Pharmacy Name    A/N    20    121-140    Y    Name of pharmacy
    h.s(r['pharmacy_address'], 20)            # Pay to Pharmacy Address    A/N    20    141-160    Y    Address of pharmacy
    h.s(r['pharmacy_city'], 18)               # Pay to Pharmacy Location City    A/N    18    161-178    Y    City of pharmacy
    h.s(r['pharmacy_state'], 2)               # Pay to Pharmacy Location State    A/N    2    179-180    Y
    h.s(r['pharmacy_zip_code'], 9)            # Pay to Pharmacy Zip Code    A/N    9    181-189    Y
    h.s(r['pharmacy_phone'], 10)              # Pay to Pharmacy Telephone Number    N    10    190-199    N
    h.s('', 30)                               # Pharmacy Specialty License SR    A/N    30    200 - 229    Y
    h.s("", 30)                               # Pharmacy Specialty Code SR    A/N    30    230 - 259    Y
    h.s("", 59)                               # 874-GD    Expansion Area    A/N    59    260 -318    N    Filler
    h.s(r['pharmacy_tax_id'], 9)              # Dispensing Pharmacy Federal Tax ID    N    9    319-327    Y
    h.s(r['pharmacy_npi'], 10)                # Pharmacy NPI    A/N    10    328-337    Y    Pharmacy NPI
    h.s('', 163)                              # Unique Free Form    A/N    163    338-500    N    Filler
    h.w('\n')

def write_claim_record(buf, r, batch_number):
    """ Claim Record - 4 Based on ver 2.0 NCPDP
    Contains the necessary data elements that need to be submitted for payment
    by the carrier or processor.  Multiple per pharmacy.
    One bill created per 4 record
    """
    h = Helper(buf)
    # Name    Format    Length    Position    Req    Description    Notes
    h.s('4', 1)                         # 843-5Z    Record Identifier    N    1    1-1    Y    4 Claim Record
    h.n(0, 10)                          # 840-5W    Processor Number    N    10    2-11    Y    Unique ID Number
    h.s(batch_number, 5)                # 806-5C    Batch Number    N    5    12-16    Y
    h.s(r['pharmacy_nabp'], 12)         # 201-B1    Dispensing Pharmacy Number    A/N    12    17-28    Y    ID assigned to a pharmacy
    h.n(r['rx_number'], 7)              # 402-D2    Prescription Number    N    7    29-35    Y
    h.s(r['rx_date'], 8)                # 401-D1    Date Filled    N    8    36-43    Y    Dispensing Date of RX Format=CCYYMMDD
    h.s(r['ndc_number'], 11)            # 407-D7    NDC Number    N    11    44-54    Y    "For Legend Compounds Use:
                    # 99999999999
                    # Schedule   II:     99999999992
                    # Schedule   III:    99999999993
                    # Schedule   IV:     99999999994
                    # Schedule   V:      99999999995
                    # Compounds:         99999999996
    h.s(r['drug_name'], 30)             # 516-FG    Drug Description    A/N    30    55-84    Y
                                        # Necessary for Compounds and those Items not in Carrier Drug File
    h.n(r['refill_number'], 2)          # 403-D3    New/Refill Code    N    2    85-86    Y    "00=New Prescription
                                                # 01-99= Number OF REFILLS"
    h.n(r['quantity'], 5)               # 404-D4    Metric Quantity    N    5    87-91    Y    Number of Metric Units of Medication Dispensed
    h.n(r['days_supply'], 3)            # 405-D5    Days Supply    N    3    92-94    Y    Estimated Number of Days the Prescription will Last
    h.n(0, 2)                           # 423-DN    Basis of Cost Determination    A/N    2    95-96    Y    "00=Not Specified
                        # 01=AWP 02=Local Wholesaler 03=Direct 04=EAC 05=Acquisition 06=MAC 6X=Brand Medically Necessary
                        # 07=Usual and Customary 08=Unit Dose 09=Other Used on Tape and Diskette Only"
    h.n(0, 7)                           # 409-D9    Ingredient Cost    D    7    97-103    Y    Cost of the Drug Dispensed  Format = s$$$$cc
    h.n(0, 7)                           # 412-DC    Dispensing Fee D    D    7    104-110    Y    Format =s$$$$cc
    h.n(r['eho_network_copay'], 7)      # 817-5E    Co-Pay Amount    D    7    111-117    N    Correct Co-Pay for Plan Billed  Format =s$$$$cc
    h.n(r['sales_tax'], 7)              # 410-DA    Sales Tax    D    7    118-124    N    "Sales Tax for the Prescription Dispensed
                                        # Format =s$$$$cc"
    h.n(r['total'], 7)                # 804-5B    Amount Billed    D    7    125-131    Y    Format =s$$$$cc (SEQ 42,43,44,45)
    h.s(r['patient_first_name'], 12)  # 310-CA    Patient First Name    A/N    12    132-143    Y    First Name of Patient
    h.s(r['patient_last_name'], 15)   # 311-CB    Patient Last Name    A/N    15    144-158    Y    Last Name of Patient
    h.s(r['patient_dob'], 8)          # 304-C4    Date of Birth    N    8    159-166    Y    Date of Birth of Patient  Format =CCYYMMDD
    h.s(r['patient_sex_code'], 1)     # 305-C5    Sex Code    N    1    167-167    N    "0=Not Specified 1=Male 2=Female"
    h.s(r['patient_ssn'], 18)         # 302-C2    "Cardholder ID Number Doi+ssn+3 blank spaces 'Yymmdd999999999bbb'
                                                # A/N    18    168-185    Y    ID Assigned to Cardholder
    h.s('', 1)                        # 306-C6    Relationship Code    N    1    186-186    N    1=Cardholder
    h.s(r['group_number'], 15)        # 301-C1    Group Number    A/N    15    187-201    N
    h.n(r['state_fee'], 7)            #           Reference Price    D    7    202-208    Y    "State Fee Schedule Format =s$$$$cc"
    h.s(r['doctor_dea'], 10)          # 411-D8    Prescriber ID (DEANumber)    A/N    10    209-218    Y    Id Assigned to the Prescriber
    h.s(r['pharmacist_lic_number'], 15)    #           License SR    A/N    15    219- 233    Y    License # for State Reporting
    h.s('', 3)                        #           Filler    A/N    3    234-236    N    Spaces
    h.s(r['claim_number'], 25)        #           Claim Number    A/N    25    237-261    Y    Claim Number
    h.s(r['juris'], 2)                # State of Jurisdiction    A/N    2    262-263    Y    Postal Abbreviation for State
    h.s('', 7)                        # Filler - NEW 4/26/11 Sedgwick Client ID    A/N    7    264-270    N    Spaces -
    h.s(r['is_reversal'], 1)          # Credit/Debit Flag    A/N    1    271-271    N    "Code Indicating Payable or Rejected
                                      #(Values to be Determined)"    If 'Y' then bill dollar values to be imported as negatives
    h.s('', 1)                        # Filler    A/N    1    272-272    N    T =PBM      M=Medaudit
    h.n(0, 2)                         # 844-6A    Filler    N    2    273-274    Y    "0=Original Submission
                                      #       1=First Re-Submission
                                      #       2=Second Re-Submission"
    h.s(r['date_written'], 8)         # s414-DE    Date Prescription Written    N    8    275-282    Y    Date Prescription was Written
    h.s(r['daw'], 1)                  # 408-D8    Dispense as Written (DAW)/Product Selection Code    A/N    1    283-283    Y
    h.n(0, 3)                         # Refills Remaining SR    N    3    284-286    Y    "Refills Remaining for SR
                                            # Right justified, leading zeroes
    h.s('', 1)                        # New / Refill SR    A/N    1    287-287    Y    "New / Refill Indicator for State Reporting
    h.s(r['brand'], 1)                # Generic / Brand SR    A/N    1    288-288    Y    "Generic / Brand Indicator for State Reporting
    h.s('', 1)                        # Generic Available SR    A/N    1    289-289    Y    "Generic available indicator for State Reporting
    h.s('', 2)                        # 415-DF    Number of Refills Authorized    N    2    290-291    Y   
                                      #           "Number of Refills Authorized by Prescriber "
    h.s('', 2)                        # 418-DI    Filler    N    2    292-293    N    "00= Not Specified
    h.s('', 1)                        # 419-DJ    Filler    N    1    294-294    N    "0= Not Specified"
    h.n(0, 2)                         # UM (unit of measure)    N    2    295-296    N    Zeros
    h.s('', 10)                       # 421-DL    Primary Prescriber    A/N    10    297-306    Y 
                                      # ID Assigned to Primary Prescriber used when Dispensing Prescriber was Referred
    h.s('', 5)                        #           Filler    N    5    307-311    N    Zeros
    h.s('', 1)                        # 425-DP    Filler    N    1    312-312    N    0= Not Specified
    h.s(r['doctor_last_name'], 15)    # 427-DR    Prescriber Last Name    A/N    15    313-327    Y    Prescriber Last Name
    h.s('', 4)                        #           Filler        4    328-331    N    Zeros
    h.s('', 1)                        # 429-DT    Filler    N    1    332-332    N    0= Not Specified
    h.s('', 7)                        #           Filler    A/N    7    333-339    N    "Reduction Amount Format =s$$$$cc"
    h.s('', 1)                        # 432-DW    Filler    N    1    340-340    N    0= Not Specified
    h.s(r['client_tin'], 18)          # Employer ID / Name    A/N    18    341-358    Y    Filler
    h.n(r['record_id'], 10)           # Invoice Number    N    10    359-368    Y    PBM Invoice Number
    h.s(r['doctor_first_name'], 25)   # PRESCRIBER First Name SR    A/N    25    369 - 393    Y    Prescriber First Name for State Reporting
    h.s(r['doctor_last_name'], 25)    # PRESCRIBER Last Name SR    A/N    25    394 - 418    Y    Prescriber Last name for State Reporting
    h.s(r['date_processed'], 8)       # PBM Pharmacy Receive Date    N    8    419 - 426    Y    PBM Receive Date   Format =CCYYMMDD
    h.s('', 8)                        # Pharmacy Paid Date    N    8    427 - 434    Y    Pharmacy Paid Date Format =CCYYMMDD
    h.s(r['pharmacist_lic_number'], 15) # Pharmacist License Number    A/N    15    435 - 449    Y    "AANNNNNNNNNNN or
                                     # AAANNNNNNNNNN or AAAANNNNNNNNN Left Justify, and pad with spaces to the right."
    h.s(r['doctor_npi'], 10)          # Prescribing Doctor's NPI    A/N    10    450-459    Y    Prescribing Doctor's NPI
    h.n(0, 10)                        # Admin Fee    A/N    10    460 - 469    N    Admin Fee Format =s$$$$$$$cc
    h.s('', 31)                       # Unique Free Form Field    A/N    31    470-500    N    Filler
    h.w('\n')


class Helper(object):
    def __init__(self, buf):
        self._buf = buf

    def w(self, b):
        self._buf.write(b)

    def s(self, s, l):
        """ simple fixed text writing """
        if s is None:
            return self._buf.write(' '*l)
        if not isinstance(s, basestring):
            s = str(s)
        if len(s) > l:
            self._buf.write(s[:l])
        elif len(s) < l:
            self._buf.write(s.ljust(l, ' '))
        else:
            self._buf.write(s)

    def n(self, s, l):
        """ numeric text writing """
        if s is None:
            return self._buf.write('0'*l)
        if not isinstance(s, basestring):
            s = str(s)
        if len(s) > l:
            self._buf.write(s[:l])
        elif len(s) < l:
            self._buf.write(s.rjust(l, '0'))
        else:
            self._buf.write(s)

    def d(self, s):
        if s is None:
            self._buf.write(" " * 8)
        else:
            self._buf.write(s.strftime("%Y%m%d"))

