# -*- coding: utf-8 -*-
import datetime
import csv
from six import StringIO

import cpsar.runtime as R

def bill_file(cur, status_flag, ctime):
    """ Mainline workflow for transaction-based submission """
    buf = StringIO()
    wr = csv.writer(buf)

    fname = "CPS_%s%s_0001.csv" % (
        ctime.strftime("%Y%m%d%H%M%S"),
        ctime.microsecond / 1000)

    cur.create_state_report_records(R.username(), status_flag, fname)
    sr_file_id = next(cur)[0]

    wr.writerow([
        "BET",          # Record ID
        "20E",          # File Version
        status_flag,    # Status flag
        "631040950",    # sender ETIN
        "113766",       # receiver ETIN
        ctime.strftime("%Y%m%d"),       # Creation Date
        ctime.strftime("%H%M%S"),       # Creation Time
        send_record_count(cur),         # Number of records
        "2",        # Submitter Entity Type
        "Corporate Pharamcy Services", # Organization Name
        "", # First Name
        "Tucker",
        "Lori",
        "lori@corporatepharmacy.com",
        "8005683784"
    ])
    for trans in cur.trans():
        write_bbr(wr, trans)
        write_blr(1, wr, trans)

    return buf.getvalue()

def manual_bill_file(sr_file, bills):
    """ Mainline workflow for manual submission
    bills= list of dict with 'lines' subdict """

    buf = StringIO()
    wr = csv.writer(buf)
    record_count = sum(len(b['lines']) for b in bills)
    wr.writerow([
        "BET",          # Record ID
        "1.9b",         # File Version
        sr_file['status_flag'],    # Status flag
        "631040950",    # sender ETIN
        "113766",       # receiver ETIN
        sr_file['create_time'].strftime("%Y%m%d"),       # Creation Date
        sr_file['create_time'].strftime("%H%M%S"),       # Creation Time
        record_count,                   # Number of records
        "2",                            # Submitter Entity Type
        "Corporate Pharamcy Services",  # Organization Name
        "",
        "Tucker",
        "Lori",
        "lori@corporatepharmacy.com",
        "8005683784"
    ])
    for bill in bills:
        write_bbr(wr, bill)
        for idx, line in enumerate(bill['lines']):
            write_blr(idx+1, wr, line)
    return buf.getvalue()

def send_record_count(cur):
    cur.send_record_count()
    return next(cur)[0]

def write_bbr(wr, t):
    wr.writerow([
        "BBR",      # Record Id. Identifies the record type. Must always be set
                    # to "BBR" for Bishop Bill Record
        t['item_count'], # Number of Lines. Report the number of BLR records
                    # associated with this bill.
        "0",        # Attachment Count. Number of attachment records (BAR)
                    # associated with this bill.
        t['unique_originator_record_id'],  # Unique Originator Record Id. Created by the Billing
                    # Provider. This value should be a unique value specific to
                    # the Billing Provider. Bishop will return this value to
                    # Billing Provider when sending Remittance and
                    # Acknowledgments
        t['intermediary_id'], # Intermediary Transaction Identification Number 
                    # This value may be set by a Clearinghouses or other
                    # Transmission Intermediaries for internal tracking
                    # purposes and reconciliation. This number is not set by
                    # the Billing Provider. Bishop will return this value to
                    # when sending Remittance and Acknowledgements.
        t['bill_type'],  # Bill Type.  Identify the type of Bill
                    # Options:  P=Professional (HCFA), I=Institutional (UB),
                    # D=Dental (ADA)
                    # B025: P=9 R=10 I=90
        t['icd_code'],        # ICD version. 09 for ICD9 and 010 for ICD10 codes.
        t['bill_date'],       # Bill Date. This is the invoice date; the date
                              # the biller is creating the bill. This is not
                              # the Date of Service, Date of Injury or Date of
                              # Statements. Format: CCYYMMDD
        t['bill_number'],     # Bill Number. The Billing Provider's unique
                              # invoice number also commonly referred to as the
                              # Patient Account Number.  This number is Biller defined.
                              # On a HCFA this is Box 26 Patient Account #
        t['claim_number'],    # Claim Number. This is the Payor’s Claim Number
                              # associated with the injured Patient. The Biller
                              # retrieves this value from Payer before sending
                              # the bill to Bishop. If the Biller cannot obtain
                              # the claim number, the word “UNKNOWN” in this
                              # field is acceptable.
        '',                   # B050 Original Bill Number. Include the original Bill
                              # number from B030 when that bill is being
                              # corrected/reconsidered, voided, or is a
                              # duplicate so that the link is established
                              # between the bill being corrected/reconsidered
                              # and the corrected/reconsidered bill.
        t['bill_total'],      # B055 Total Claim Charge Amount. This is the total
                              # claim charge amount and must balance to the sum
                              # of all service line charge amounts.
        t['insurer_paid_amount'],   # Insurer Paid Amount
        t['juris'],           # Jurisdiction State.  Rule: Use the
                              # two-character abbreviation for the U.S. State
                              # governing over the worker compensation claim.
        t['claim_freq'],      # Claim Frequency Type Code. Code that specifies
                              # how often the claim is submitted 
                              # Options: 1=original claim, 7=replacement or
                              # corrected claim, 8= voided/canceled claim.
        "2",                  # Billing Provider Entity Type.
                              # Options: 1=Person, 2=Entity
        "Corporate Pharmacy Services",  # Billing Provider Last Name or Organization Name.
                              # If the Billing Provider is a person, provide
                              # last name of the individual else provide the
                              # organization name. 
        "",                   # Billing Provider First Name.
        "",                   # Billing Provider Middle Name.
        "1437194933",         # Billing Provider NPI. If unknown send all 9999999999
        "631040950",          # Billing Provider Tax Id.
        "",                   # Billing Provider State License Number
        "3336M0003X",         # Billing Provider Taxonomy Code.
        "319 Broad Street",   # Billing Provider Address.
        "",                   # Billing Provider Address 2
        "Gadsden",            # Billing Provider City
        "AL",                 # Billing Provider State/Province
        "35901",              # B125 Billing Provider Zip Code. 
        "",                   # B130 Billing Provider Country Code.
        t['control_number'],  # B135 Repurposed from Other Payor Claim Control Number
                              # Only applicable when submitting a void, correction or replacement.
                              # (Field after Billing Provider Country Code)
        "Lori Tucker",        # Billing Provider Contact Last Name. Enter the
                              # Last name of a person or the full name of a
                              # department that is to be contacted regarding
                              # this bill by anyone downstream. 
        "",               # Billing Provider Contact First Name.
        "lori@corporatepharmacy.com",     # Billing Provider Contact E-Mail Address.
        "8005683784",         # Billing Provider Contact Phone Number.
        "",                   # Pay-To Address. This is the street address
        "",                   # Pay-To Address2.
        "",                   # Pay-To City.
        "",                   # Pay-To State/Province
        "",                   # Pay-To Zip Code.
        "",                   # B185 Pay-To Country Code. Code identifying the country.
        t['insurer_code_number'],   # B187 Other Payer ID
        t['insurer_fein'],    # Insurer FEIN
        t['payor_name'],     # Payor Name. To include TPA, Carrier,
                              # or Insurer who is responsible to
                              # remit against the bill.
        t['payor_id'],        # Payor ID. This is the Payor's unique ID as
                              # defined and provided by the Payor. 
        t['payor_fein'],    # Add field B197 for Payer FEIN 591229569 after the Payer ID.
        t['payor_address_1'],# Payor Address
        t['payor_address_2'],# Payor Address 2
        t['payor_city'],     # Payor City
        t['payor_state'],    # Payor State/Province
        t['payor_zip_code'], # Payor Zip Code
        "",                   # Payor Country Code. Code identifying the country. 
        t['payor_receive_date'], # Payor Receive Date
        t['payment_date'],       # Payment Date
        "M",                     # Payment Code
        "2",                     # Receipt and Payment Arrangement Code
        t['patient_last_name'],  # Patient Last Name
        t['patient_first_name'], # Patient First Name
        '',                      # Patient Middle Name
        t['patient_ssn'],        # Patient Social Security Number. Must be a
                                 # valid SSN number. If the number is not
                                 # known, enter all 9’s (i.e., 999999999)
        t['patient_dob'],        # Patient's Date of Birth. Format: CCYYMMDD 
        t['patient_sex'],        # Patient Gender.  Options: F=Female, M=Male, U=Unknown
        t['patient_address_1'],  # Patient Address
        t['patient_address_2'],  # Patient Address 2
        t['patient_city'],       # Patient City. 
        t['patient_state'],      # Patient State/Province. 
        t['patient_zip_code'],   # Patient Zip Code. 
        "",                      # Patient Country Code
        "20",                    # Patient Relationship Code. This code
                                 # identifies the patient’s relationship to the
                                 # subscriber.  Options:
                                    # 01 	Spouse
                                    # 19 	Child
                                    # 20 	Employee
                                    # 21 	Unknown
                                    # 39 	Organ Donor
                                    # 40 	Cadaver Donor
                                    # 53 	Life Partner
                                    # G8 	Other Relationship
        "2",                     # Insured Entity Type
                                 # Options: 1=Person, 2=Entity
        t['insured_name'],       # Insured Last Name or Organization Name. If
                                 # the Insured is a person, provide last name
                                 # of the individual else provide the
                                 # organization name such as Employer Name for
                                 # Workers Compensation bills.  Rule: Must be a
                                 # valid name. Letters only (numbers and
                                 # symbols invalid).
        "",                      # Insured First Name
        "",                      # Insured Middle Name
        "",                      # Insured Street Address.
        "",                      # Insured Additional address information.
        "",                      # Insured City
        "",                      # Insured State/Province
        "",                      # B335 Insured Zip Code.
        "",                      # B340 Insured Country Code. Code identifying the country
  t['insurer_code_number'],      # B343 Subscriber Member Number - Repurposed from Other Payor ID
        t['doctor_last_name'],   # Referring Provider Last Name. 
        t['doctor_first_name'],  # Referring Provider First name.
        "",                      # Referring Provider Middle name.
        t['doctor_npi'],         # Referring Provider NPI.
        "",                      # Referring Provider Degree.
  t['doctor_state_lic_number'],  # Referring Provider State License Number. 
        t['pharmacist_last_name'],   # Rendering Provider Last Name.
        t['pharmacist_first_name'],  # Rendering Provider First name.
        "",                      # Rendering Provider Middle name.
        "",                      # Rendering Provider Degree. 
        "9999999999",            # Rendering Provider NPI.  # If the number is
                                 # not known, enter all 9’s  (i.e., 9999999999). 
        t['pharmacist_lic_number'] or "ZZ99999999999", # Rendering Provider State License Number
        t['pharmacist_taxonomy_code'],   # Rendering Provider Taxonomy Code.
        t['pharmacy_name'],      # Service Facility Name. This is the legal
                                 # name of the facility that provided the service. 

        t['pharmacy_address_1'], # Service Facility Address.
        t['pharmacy_address_2'], # Service Facility Address 2
        t['pharmacy_city'],      # Service Facility City
        t['pharmacy_state'],     # Service Facility State/Province. 
        t['pharmacy_zip_code'].replace("-", ""),  # Service Facility Zip Code. 
        "",                      # Service Facility Country Code.
        t['pharmacy_npi'],       # Service Facility NPI.
        t['pharmacy_state_license_number'], # Service Facility State License Number. 
        "",                      # Attending Physician Last Name. Must be a valid name.
        "",                      # Attending Physician First Name. Must be a valid name.
        "",                      # Attending Physician NPI.
        "",                      # Attending Physician's State License #.
        "",                      # Operating Physician Last Name. 
        "",                      # Operating Physician First Name. 
        "",                      # Operating Physician NPI.
        "",                      # Operating Physician State License Number
        "WC",                    # Claim Indicator Code.  Options: WC=Workers Compensation
        "P",                     # Payer Sequence Responsibility Number Code.
                                    #Options:
                                    #A	Payer Responsibility Four
                                    #B 	Payer Responsibility Five
                                    #C 	Payer Responsibility Six
                                    #D 	Payer Responsibility Seven
                                    #E 	Payer Responsibility Eight
                                    #F 	Payer Responsibility Nine
                                    #G 	Payer Responsibility Ten
                                    #H 	Payer Responsibility Eleven
                                    #P 	Primary
                                    #S 	Secondary
                                    #T 	Tertiary
                                    #U	Unknown
        "",                      # Provider / Signature on File Indicator. 
                                 # Options: Y= provider signature is on file, else N
        "I",                     # Release of Information Code.
        "EM",                    # Related Cause Code.
        "",                      # Clinical Improvement Amendment (CLIA) Number.
        "C",                     # Provider Accept Assignment Code.
        "W",                     # Benefits Assignment Certification Indicator. 
        "",                      # Patient Signature Source Code. Code indicating how
        "1",                     # Facility Code/Place of Service Code.
        "1",                     # Claim Frequency Code.
        t['doi'],                # Date of Injury/Accident
        t['date_of_admission'],  # B545 Date of Admission.  Format: CCYYMMDD 
        "",                      # Hour of Admission.  Format: HHMM
        t['date_of_discharge'],  # B555 Date of Discharge.  Format: CCYYMMDD
        "",                      # Hour of Discharge.  Format: HHMM
        "",                      # Date of First Contact.
        "",                      # Date of Statement Start.  Format: CCYYMMDD
        "",                      # Date of Statement End.  Format: CCYYMMDD  
        "",                      # Repricer Receipt Date. 
        t['principal_diagnosis_code'],                  # Principal Diagnosis Code.  (Unspecified other)
        t['diagnosis_code_2'],   # Diagnosis Code 2.
        t['diagnosis_code_3'],   # Diagnosis Code 3.
        t['diagnosis_code_4'],   # Diagnosis Code 4.
        t['diagnosis_code_5'],   # Diagnosis Code 5.
        "",                      # Diagnosis Code 6.
        "",                      # Diagnosis Code 7.
        "",                      # Diagnosis Code 8.
        "",                      # Diagnosis Code 9.
        "",                      # Diagnosis Code 10
        "",                      # Diagnosis Code 11
        "",                      # Diagnosis Code 12
        "",                      # Diagnosis Related Group (DRG) Code.
        "",                      # Other Procedure Code – Principle.
        "",                      # Other Procedure Date - Principle. Format: CCYYMMDD 
        "",                      # Other Procedure Code 2.
        "",                      # Other Procedure Date 2. Format: CCYYMMDD 
        "",                      # Other Procedure Code 3.
        "",                      # Other Procedure Date 3. Format: CCYYMMDD 
        "",                      # Other Procedure Code 4.
        "",                      # Other Procedure Date 4. Format: CCYYMMDD 
        "",                      # Other Procedure Code 5.
        "",                      # Other Procedure Date 5. Format: CCYYMMDD 
        "",                      # Other Procedure Code 6.
        "",                      # Other Procedure Date 6. Format: CCYYMMDD 
        "",                      # B710 - Facility Type Code. Code identifying the
                                 # type of facility where services were performed. 
                                 # Options: Non-Person Entity = 2
        "",                      # Occurrence Code 1. Code from a specific industry code list.
        "",                      # Occurrence Date 1. Format: CCYYMMDD 
        "",                      # Occurrence Code 2. Code from a specific industry code list.
        "",                      # Occurrence Date 2. Format: CCYYMMDD 
        "",                      # Occurrence Code 3. Code from a specific industry code list.
        "",                      # Occurrence Date 3. Format: CCYYMMDD 
        "",                      # Occurrence Code 4. Code from a specific industry code list.
        "",                      # Occurrence Date 4. Format: CCYYMMDD 
        "",                      # Occurrence Code 5. Code from a specific industry code list.
        "",                      # Occurrence Date 5. Format: CCYYMMDD 
        "",                      # Occurrence Code 6. Code from a specific industry code list.
        "",                      # Occurrence Date 6. Format: CCYYMMDD 
        "",                      # Occurrence Code 7. Code from a specific industry code list.
        "",                      # Occurrence Date 7. Format: CCYYMMDD 
        "",                      # Occurrence Code 8. Code from a specific industry code list.
        "",                      # Occurrence Date 8. Format: CCYYMMDD 
        "",                      # Occurrence Span Code 1.
        "",                      # Occurrence Span From Date 1. Format: CCYYMMDD 
        "",                      # Occurrence Span Through Date 1. Format: CCYYMMDD 
        "",                      # Occurrence Span Code 2.
        "",                      # Occurrence Span From Date 2. Format: CCYYMMDD 
        "",                      # Occurrence Span Through Date 2. Format: CCYYMMDD 
        "",                      # Occurrence Span Code 3.
        "",                      # Occurrence Span From Date 3. Format: CCYYMMDD 
        "",                      # Occurrence Span Through Date 3. Format: CCYYMMDD 
        "",                      # Occurrence Span Code 4.
        "",                      # Occurrence Span From Date 4. Format: CCYYMMDD 
        "",                      # Occurrence Span Through Date 4. Format: CCYYMMDD 
        "",                      # Value Information Code 1.
        "",                      # Value Information Amount 1.
        "",                      # Value Information Code 2.
        "",                      # Value Information Amount 2.
        "",                      # Value Information Code 3.
        "",                      # Value Information Amount 3.
        "",                      # Value Information Code 4.
        "",                      # Value Information Amount 4.
        t['pharmacy_nabp'],      # National Council for Prescription Drug Programs ID - unique identifier
        "",                      # First Date Patient Unable to Work.  Format: CCYYMMDD 
        "",                      # Last Date Patient Unable to Work.  Format: CCYYMMDD 
        "",                      # Prior Authorization Number. 
        "",                      # Type of Admission. 
        "",                      # Admit Source Code. 
        "",                      # Patient Status Code. Code indicating patient status as of the “statement covers through date”
        "",                      # Admit Diagnosis. 
        "",                      # Patient Reason for Visit. 
        "",                      # External Cause of Injury 1.
        "",                      # External Cause of Injury 2.
        "",                      # External Cause of Injury 3.
        "",                      # Contract Type Code. Code identifying a contract type. 
        "",                      # Contract Amount. 
        "",                      # Contract Code. 
        "",                      # Pricing Methodology. 
        "",                      # Repriced Allowed Amount. 
        "",                      # Repriced Savings Amount. 
        "",                      # Patient Paid Amount. The total amount of money paid by the payer
                                 #    to the patient (rather than to the provider) on the claim. 
        "FLORIDA DWC",           # B990 Other Payer Name
        "FLDWC",                 # B995 State Agency Id
        "",                      # B996 Other payer address
        "",                      # B997 Other payer address
        "",                      # B998  "      "   city
        "",                      # B999  "      "   state
        ""                      # B1000 "      "   zip
#        ""                       # B1005 "      "   country code
    ])


def write_blr(line_no, wr, t):
    eobs = [''] * 3
    next = t['eob_review_code'] or ''
    for i in range(3):
        eobs[i], _, next = next.partition(',')
    eobs = [e.strip() for e in eobs]

    wr.writerow([
        "BLR",                   # Record Id. Identifies the record type. Must always be set to “BLR” for Simple Bill Layout
        line_no,                 # Line Number. Starts with 1 to 99
        t['date_of_service'],    # Date of Service Start. The date that the service happened.  Format: CCYYMMDD 
        t['date_of_service'],    # Date of Service End. The date that the service happened.  Format: CCYYMMDD
        "1",                     # Place of Service.  Place of Service from professional bill. 
        "",                      # Revenue Code. Identifying number for a product or service.
        t['hcpcs'],              # "J8499" CPT Proc/ HCPCS Code. (Oral unspecified)
        "",                      # Primary Modifier. This gives further specification of the HCPCS or CPT code. 
        "",                      # Modifier. This gives further specification of the HCPCS or CPT code. 
        "",                      # Modifier. This gives further specification of the HCPCS or CPT code. 
        "",                      # Modifier. This gives further specification of the HCPCS or CPT code. 
        t['drug_name'],          # Description. A free-form description to clarify the related data elements and their content. 
        "UN",                    # Unit of Measure.  Options: MJ = Minutes, UN = Unit
                                 # Ben told us(Lori) to put the days supply here 9/16/2019
        t['days_supply'],        # Quantity. The max integer value is 8 characters, but if you provide a decimal then your allowed up to 3 digits to the right.
        "A",                     # Primary Points to Diagnosis Code.
        "",                      # Points to Diagnosis Code.
        "",                      # Points to Diagnosis Code.
        "",                      # Points to Diagnosis Code.
        t['total'],              # Line Charge. The charge amount for this service line.
                                 # It is inclusive of the base charge and any applicable tax and/or postage claimed amounts reported.
        t['sales_tax'],          # Sales Tax. This is the sales tax. If you are not charging for or recovering sales tax leave this blank.
        "",                      # Patient Paid
        "",                      # Contract Amount Allowable. 
        t['state_fee'],          # Fee Schedule Allowable. 
        t['insurer_paid'],       # Insurer Paid Amount Implied decimal
        t['ndc'],                # National Drug Code. Original National Drug
        # Code in 5-4-2 Format. Required when government regulation mandates that
        # prescribed drugs and biologics are reported with NDC numbers. OR
        # Required when the provider or submitter chooses to report NDC numbers
        # to enhance the claim reporting or adjudication processes. If not
        # required, do not send.
        t['repackaged_ndc'],     # Repackaged National Drug Code. 
        t['refill_number'],      # Type of Prescription. Line item data in "Fill #” 
                                 # Options: 0=the first dispensing, or, 1=through 99 (refill count)
        t['rx_number'],          # Prescription Number.
        t['quantity'],           # National Drug Unit Count. 
        t['entry_doctor_last_name'],          # L140: Rendering Provider Last Name
        t['entry_doctor_first_name'],         # L145: Rendering Provider First Name
        t['entry_doctor_state_lic_number'],   # L150: Rendering Provider State License Number
        t['entry_doctor_npi'],                # L155: Rendering Provider NPI
        t['hcpcs_paid'],            # L160: HCPCS/CTP Code Paid
        "",                         # Tooth Surface.  Identifies one or more tooth surface codes.
        "",                         # Tooth Number.
        eobs[0],                    # Explaination of Benefit Review Code 1
        eobs[1],                    # Explaination of Benefit Review Code 2
        eobs[2],                    # Explaination of Benefit Review Code 3
        t['daw'],                   # dispense as written
        "",                         # purchase rental code
        "",                         # purchase rental date
        "",                         # Paid Modifier 1
        "",                         # Paid Modifier 2
        "",                         # Paid Modifier 3
        ""                          # Paid Modifier 4
    ])

