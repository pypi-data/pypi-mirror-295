""" Mitchell smartadvisor file export module. Provides facilities to

- generate SBI files
- send SBI files, along with corresponding invoice pdf files, to mitchell's
  FTP server. The files are encrypted using PGP.
- archive existing files sent to Mitchell

The module exposes a command-line interface for batch processing as well as
procedures and object which can be reused by other Python programs.

The SBI file generation routines were written using the smart advisor standard
bill import HUB Bill Extract document, revision Feb 2011.

File Format Notes:
 - All dates are in CCYYMMDD format.
 - All records need to be terminated with a carriage return and a line feed.
 - All characters should be in upper case.
 - All numeric values are implied decimals.

"""
from __future__ import print_function
import datetime
import glob
import logging
import os
import string
import shutil
import sys
import textwrap
import zipfile

from decimal import Decimal

import cpsar.runtime as R

from cpsar import shell
from cpsar import print_invoice
from cpsar.runtime import db, dpath
from cpsar.util import unique
from cpsar.util.table import table_set

STAGE_DIR = dpath("companion/stage")
ARCHIVE_DIR = dpath("companion/archive")

log = logging.getLogger()

class Layout(object):
    """ Object which writes out a fixed-width text record to a file object
    using a declarative definition of the column specification given to the
    constructor. The layout is essentially stateless, only maintaining the
    field layout definitions. To use, pass a data source object and a file
    object to write_record.  """
    def __init__(self, *fields):
        self.fields = table_set(*fields)

    def write_record(self, data, fd):
        """ Write the given data to the file fd """
        for field in self.fields:
            if field.value:
                value = getattr(data, field.value)
            else:
                value = None

            fd.write(format_field_value(field, value))
        # DOS-style line feed
        fd.write("\r\n")

# This record layout is from the actual documentation
trans_header_layout = Layout(
('field', 'name', 'from', 'to', 'len', 'dt', 'filler', 'pad', 'req', 'value'),
# Field Name From To Field Length Data Type Filler Pad Value
    (1, 'RecType',                      1, 3, 3, 'C', 'Blank',   'R', 'R',  'rec_type'),
    (2, 'Trading Partner Sender ID',    4, 18, 15, 'C', 'Blank', 'R', 'O',  ),
    (3, 'Trading Partner Receiver ID', 19, 33, 15, 'C', 'Blank', 'R', 'O',  ),
    (4, 'File Transmission Date',      34, 41, 8, 'C', 'Blank',  'R', 'R',  'trans_date'),
    (5, 'File Transmission ID',        42, 56, 15, 'C', 'Blank', 'R', 'O',  'transmission_id'),
    (6, 'Total Record Count',          57, 63, 7, 'N', 'Zero',  'L', 'R',  'total_record_count'),
    (7, 'Bill Record Count',           64, 70, 7, 'N', 'Zero',  'L', 'R',  'bill_record_count'),
    (8, 'Line Record Count',           71, 77, 7, 'N', 'Zero',  'L', 'R',  'line_record_count'),
    (9, 'Provider Record Count',       78, 84, 7, 'N', 'Zero',  'L', 'R',  'provider_record_count'),
    (10, 'Bill Comment Record Count',  85, 91, 7, 'N', 'Zero',  'L', 'R',  'bill_comment_record_count'),
    (11, 'Provider Comment Count',     92, 98, 7, 'N', 'Zero',  'L', 'R',  'provider_comment_record_count'),
    (12, 'Practitioner Record Count',  99, 105, 7, 'N', 'Zero', 'L', 'O'),
    (13, 'Bill Attachment Ref Count', 106, 112, 7, 'N', 'Zero', 'L', 'O',   'bill_attachment_ref_count'),
    (14, 'File Transmission Time',    113, 118, 6, 'N', 'Zero', 'L', 'O'),
    (15, 'Filler',                    119, 153, 35, 'C', 'Blank', '',  'O'),
    (16, 'File Transmission Ack Code', 154, 154, 1, 'C', 'Blank','R', 'O'),
    (17, 'Acknowldegement Note Code', 155, 157, 3, 'C', 'Blank', 'R', 'O'),
    (18, 'Acknowledgement Note',      158, 237, 80, 'C', 'Blank','R', 'O'),
    (19, 'SBX Interface Version ID',  238, 287, 50, 'C', 'Blank','R', 'O'),
    (20, 'Request for File Transmission Ack', 288, 288, 1, 'C', 'Blank','', 'O'),
    (21, 'Request for LZ Detailed Ack', 289, 289, 1, 'C', 'Blank','', 'O'),
    (22, 'Set erred Bills to Rejected Status', 290, 290, 1, 'C', 'Blank','', 'O'),
    (23, 'Claim Record Count',         291, 297, 7, 'N', 'Zero','L', 'O'),
    (24, 'Claim UDF Record Count',    298, 304, 7, 'N', 'Zero','L', 'O'),
    (25, 'Filler',                    305, 2000, 1696, 'C', 'Blank', '', 'O')
)

class TransDataSource(object):
    layout = trans_header_layout
    rec_type = '001'
    trans_date = ''
    transmission_id = ''

    @property
    def total_record_count(self):
        return (self.bill_record_count
            + self.line_record_count
            + self.provider_record_count
            + self.bill_comment_record_count
            + self.provider_comment_record_count
            + self.bill_attachment_ref_count)

    bill_record_count = 0
    line_record_count = 0
    provider_record_count = 0
    bill_comment_record_count = 0
    provider_comment_record_count = 0
    bill_attachment_ref_count = 0

bill_header_layout = Layout(
('field', 'name',             'from', 'to', 'len', 'dt', 'filler', 'pad', 'req', 'value'),
    (1, 'Record Type',           1, 3, 3, 'C', 'Blank', 'R', 'R',           'rec_type'),
    (2, 'Site Code',             4, 6, 3, 'C', 'Blank', 'R', 'O',           'site_code'),
    (3, 'Client Code',           7, 10, 4, 'C', 'Blank', 'R', 'O', 'client_code'),
    (4, 'Filler',               11, 13, 3, 'C', 'Blank', 'R', 'O'),
    (5, 'Adjuster',             14, 38, 25, 'C', 'Blank', 'R', 'O',         'adjuster'),
    (6, 'Admission Source',     39, 39, 1, 'C', 'Blank', 'R', 'O'),
    (7, 'Admission Type',       40, 40, 1, 'C', 'Blank', 'R', 'O'),
    (8, 'Admit Date',           41, 48, 8, 'C', 'Blank', 'R', 'O'),
    (9, 'Admit Hour',           49, 50, 2, 'C', 'Blank', 'R', 'O'),
    (10, 'App Assignee',        51, 51, 1, 'C', 'Blank', 'R', 'O'),
    (11, 'App Benefits',        52, 52, 1, 'C', 'Blank', 'R', 'O'), 
    (12, 'Already Repriced Flag', 53, 53, 1, 'C', 'Blank', 'R', 'C', 'already_repriced'),
    (13, 'Admitting Diagnosis Reference', 54, 55, 2, 'C', 'Blank', 'R', 'O'), 
    (14, 'Extended Diagnosis Code 1', 56, 63, 8, 'C', 'Blank', 'R', 'O', 'diagnosis_code_1'), 
    (15, 'Extended Diagnosis Code 2', 64, 71, 8, 'C', 'Blank', 'R', 'O', 'diagnosis_code_2'), 
    (16, 'Extended Diagnosis Code 3', 72, 79, 8, 'C', 'Blank', 'R', 'O', 'diagnosis_code_3'), 
    (17, 'Extended Diagnosis Code 4', 80, 87, 8, 'C', 'Blank', 'R', 'O'), 
    (18, 'Extended Diagnosis Code 5', 88, 95, 8, 'C', 'Blank', 'R', 'O'), 
    (19, 'Extended Diagnosis Code 6', 96, 103, 8, 'C', 'Blank', 'R', 'O'), 
    (20, 'Extended Diagnosis Code 7', 104, 111, 8, 'C', 'Blank', 'R', 'O'), 
    (21, 'Extended Diagnosis Code 8', 112, 119, 8, 'C', 'Blank', 'R', 'O'), 
    (22, 'Extended Diagnosis Code 9', 120, 127, 8, 'C', 'Blank', 'R', 'O'), 
    (23, 'Extended Diagnosis Code 10', 128, 135, 8, 'C', 'Blank', 'R', 'O'), 
    (24, 'Extended ICD9 Procedure Code 1', 136, 143, 8, 'C', 'Blank', 'R', 'O'), 
    (25, 'Extended ICD9 Procedure Code 2', 144, 151, 8, 'C', 'Blank', 'R', 'O'), 
    (26, 'Extended ICD9 Procedure Code 3', 152, 159, 8, 'C', 'Blank', 'R', 'O'), 
    (27, 'Extended ICD9 Procedure Code 4', 160, 167, 8, 'C', 'Blank', 'R', 'O'), 
    (28, 'Extended ICD9 Procedure Code 5', 168, 175, 8, 'C', 'Blank', 'R', 'O'), 
    (29, 'Extended ICD9 Procedure Code 6', 176, 183, 8, 'C', 'Blank', 'R', 'O'), 
    (30, 'Filler', 184, 195, 12, 'C', 'Blank', '', 'O'), 
    (31, 'External Bill ID', 196, 225, 30, 'C', 'Blank', 'R', 'O', 'external_bill_id'), 
    (32, 'Filler', 226, 226, 1, 'C', 'Blank', '', 'O'), 
    (33, 'Claim Number', 227, 261, 35, 'C', 'Blank', 'R', 'R', 'claim_number'), 
    (34, 'Claim Number Alternate', 262, 296, 35, 'C', 'Blank', 'R', 'O'), 
    (35, 'Filler', 297, 300, 4, 'C', 'Blank', '', 'O'), 
    (36, 'Client TOB (Type of Bill)', 301, 305, 5, 'C', 'Blank', 'R', 'O', 'tob'), 
    (37, 'Consult Date', 306, 313, 8, 'C', 'Blank', 'R', 'O'), 
    (38, 'Legacy Diagnosis Code 1', 314, 318, 5, 'C', 'Blank', 'R', 'O'), 
    (39, 'Legacy Diagnosis Code 2', 319, 323, 5, 'C', 'Blank', 'R', 'O'), 
    (40, 'Legacy Diagnosis Code 3', 324, 328, 5, 'C', 'Blank', 'R', 'O'), 
    (41, 'Legacy Diagnosis Code 4', 329, 333, 5, 'C', 'Blank', 'R', 'O'), 
    (42, 'Legacy Diagnosis Code 5', 334, 338, 5, 'C', 'Blank', 'R', 'O'), 
    (43, 'Discharge Date', 339, 346, 8, 'C', 'Blank', 'R', 'O'), 
    (44, 'Discharge Hour', 347, 348, 2, 'C', 'Blank', 'R', 'O'), 
    (45, 'Document Control ID', 349, 398, 50, 'C', 'Blank', 'R', 'O', 'document_control_id'), 
    (46, 'DOI', 399, 406, 8, 'C', 'Blank', 'R', 'O', 'doi'), 
    (47, 'Document Control Type', 407, 408, 2, 'C', 'Blank', 'R', 'O', 'document_control_type'),
    (48, 'Diagnosis 1 Present on Admission (POA) Code', 409, 409, 1, 'C', 'Blank', '', 'O'), 
    (49, 'Diagnosis 2 Present on Admission (POA) Code', 410, 410, 1, 'C', 'Blank', '', 'O'), 
    (50, 'Diagnosis 3 Present on Admission (POA) Code', 411, 411, 1, 'C', 'Blank', '', 'O'), 
    (51, 'Diagnosis 4 Present on Admission (POA) Code', 412, 412, 1, 'C', 'Blank', '', 'O'), 
    (52, 'Diagnosis 5 Present on Admission (POA) Code', 413, 413, 1, 'C', 'Blank', '', 'O'), 
    (53, 'Diagnosis 6 Present on Admission (POA) Code', 414, 414, 1, 'C', 'Blank', '', 'O'), 
    (54, 'Diagnosis 7 Present on Admission (POA) Code', 415, 415, 1, 'C', 'Blank', '', 'O'), 
    (55, 'Diagnosis 8 Present on Admission (POA) Code', 416, 416, 1, 'C', 'Blank', '', 'O'),
    (56, 'Diagnosis 9 Present on Admission (POA) Code', 417, 417, 1, 'C', 'Blank', '', 'O'), 
    (57, 'Diagnosis 10 Present on Admission (POA) Code', 418, 418, 1, 'C', 'Blank', '', 'O'), 
    (58, 'External Cause of Injury 1 Present on Admission (POA) Code', 419, 419, 1, 'C', 'Blank', '', 'O'), 
    (59, 'External Cause of Injury 2 Present on Admission (POA) Code', 420, 420, 1, 'C', 'Blank', '', 'O'), 
    (60, 'External Cause of Injury 3 Present on Admission (POA) Code', 421, 421, 1, 'C', 'Blank', '', 'O'), 
    (61, 'Filler', 422, 422, 1, 'C', 'Blank', '', 'O'), 
    (62, 'DRG', 423, 425, 3, 'C', 'Blank', 'R', 'O'), 
    (63, 'Due Date', 426, 433, 8, 'C', 'Blank', 'R', 'O', 'due_date'), 
    (64, 'Billing / Pay To External Provider ID', 434, 463, 30, 'C', 'Blank', 'R', 'O', 'billing_provider_id'), 
    (65, 'Fee Override', 464, 464, 1, 'C', 'Blank', 'R', 'C', 'fee_override'), 
    (66, 'Retail Bill Review Fees', 465, 473, 9, 'N', 'Zero', 'L', 'C', 'bill_review_fees'), 
    (67, 'Retail Complex Bill Review Fees', 474, 482, 9, 'N', 'Zero', 'L', 'C'), 
    (68, 'Retail PPO Fees', 483, 491, 9, 'N', 'Zero', 'L', 'C', 'retail_ppo_fees'), 
    (69, 'Retail Utilization Review Fees', 492, 500, 9, 'N', 'Zero', 'L', 'C'), 
    (70, 'Retail Negotiated Discount Fees', 501, 509, 9, 'N', 'Zero', 'L', 'C'), 
    (71, 'Retail Nurse Consultant Review Fee', 510, 518, 9, 'N', 'Zero', 'L', 'C'), 
    (72, 'Retail Physician Advisor Review Fee', 519, 527, 9, 'N', 'Zero', 'L', 'C'), 
    (73, 'Retail Specialty U&C Fee', 528, 536, 9, 'N', 'Zero', 'L', 'C'), 
    (74, 'Retail Out of Network Review Fee', 537, 545, 9, 'N', 'Zero', 'L', 'C'), 
    (75, 'Retail Bill Review Sales Tax Fee', 546, 554, 9, 'N', 'Zero', 'L', 'C', 'sales_tax'), 
    (76, 'Follow Up End Date', 555, 562, 8, 'C', 'Blank', 'R', 'O'), 
    (77, 'Follow Up Start Date', 563, 570, 8, 'C', 'Blank', 'R', 'O'), 
    (78, 'Filler', 571, 572, 2, 'C', 'Blank', '', 'O'), 
    (79, 'Import Bill ID', 573, 622, 50, 'C', 'Blank', 'R', 'R', 'import_bill_id'), 
    (80, 'Legacy ICD9Proc1', 623, 627, 5, 'C', 'Blank', 'R', 'O'), 
    (81, 'Legacy ICD9Proc2', 628, 632, 5, 'C', 'Blank', 'R', 'O'), 
    (82, 'Legacy ICD9Proc3', 633, 637, 5, 'C', 'Blank', 'R', 'O'), 
    (83, 'Other Data', 638, 667, 30, 'C', 'Blank', 'R', 'O'), 
    (84, 'Patient Account Number', 668, 687, 20, 'C', 'Blank', 'R', 'O'), 
    (85, 'Patient Status', 688, 689, 2, 'C', 'Blank', 'R', 'O'), 
    (86, 'Payment Auth', 690, 693, 4, 'C', 'Blank', 'R', 'O'), 
    (87, 'POS (Place of Service)', 694, 695, 2, 'C', 'Blank', 'R', 'R', 'pos'), 
    (88, 'PPO Contract ID', 696, 725, 30, 'C', 'Blank', 'R', 'C'), 
    (89, 'PPO Network ID', 726, 727, 2, 'C', 'Blank', 'R', 'O'), 
    (90, 'Provider Invoice', 728, 741, 14, 'C', 'Blank', 'R', 'O', 'provider_invoice'), 
    (91, 'Rendering Provider License Number', 742, 771, 30, 'C', 'Blank', 'R', 'O', 'rendering_provider_license_number'), 
    (92, 'Provider Medicare Number', 772, 791, 20, 'C', 'Blank', 'R', 'C'), 
    (93, 'Rendering Provider Specialty 1', 792, 799, 8, 'C', 'Blank', 'R', 'O', 'rendering_provider_specialty'), 
    (94, 'Rendering Provider Specialty 2', 800, 807, 8, 'C', 'Blank', 'R', 'O'), 
    (95, 'Rendering Provider Type', 808, 810, 3, 'C', 'Blank', 'R', 'C', 'rendering_provider_type'), 
    (96, 'Rendering Provider Zip', 811, 819, 9, 'C', 'Blank', 'R', 'O', 'rendering_provider_zip'), 
    (97, 'Reeval Flag', 820, 820, 1, 'C', 'Blank', 'R', 'C'), 
    (98, 'Filler', 821, 823, 3, 'C', 'Blank', '', 'O'), 
    (99, 'Repriced Review Date', 824, 831, 8, 'C', 'Blank', 'R', 'C'), 
    (100, 'Bill Review Received Date', 832, 839, 8, 'C', 'Blank', 'R', 'O'), 
    (101, 'Received Date', 840, 847, 8, 'C', 'Blank', 'R', 'O'), 
    (102, 'Referring Provider Name', 848, 877, 30, 'C', 'Blank', 'R', 'O', 'referring_provider_name'), 
    (103, 'Filler', 878, 879, 2, 'C', 'Blank', '', 'O'), 
    (104, 'Submit Date', 880, 887, 8, 'C', 'Blank', 'R', 'O', 'submit_date'), 
    (105, 'Sub Product Code', 888, 888, 1, 'C', 'Blank', 'R', 'O'), 
    (106, 'Sub Product ID', 889, 918, 30, 'C', 'Blank', 'R', 'O'), 
    (107, 'Sub Product Price', 919, 927, 9, 'N', 'Zero', 'R', 'O', 'sub_product_price'), 
    (108, 'Sub Product Price Net', 928, 936, 9, 'N', 'Zero', 'R', 'O', 'sub_product_price_net'), 
    (109, 'TOB (Type of Bill)', 937, 937, 1, 'C', 'Blank', 'R', 'R', 'tob'), 
    (110, 'TOS (Type of Service)', 938, 939, 2, 'C', 'Blank', 'R', 'O', 'type_of_service'), 
    (111, 'TX Bill Type', 940, 940, 1, 'C', 'Blank', 'R', 'O', 'tx_bill_type'), 
    (112, 'UB04 Proc Method', 941, 941, 1, 'C', 'Blank', 'R', 'O'), 
    (113, 'UB04 TOB (Type of Bill)', 942, 944, 3, 'C', 'Blank', 'R', 'O'), 
    (114, 'Billing / Pay To Provider Billing Address one', 945, 974, 30, 'C', 'Blank', 'R', 'O'), 
    (115, 'Billing / Pay To Provider Billing Address two', 975, 1004, 30, 'C', 'Blank', 'R', 'O'), 
    (116, 'Billing / Pay To Provider Billing City', 1005, 1024, 20, 'C', 'Blank', 'R', 'O'), 
    (117, 'Filler', 1025, 1038, 14, 'C', 'Blank', 'R', 'O'), 
    (118, 'Billing / Pay To Provider Billing Phone', 1039, 1048, 10, 'C', 'Blank', 'R', 'O'), 
    (119, 'Billing / Pay To Provider Billing State', 1049, 1050, 2, 'C', 'Blank', 'R', 'O'), 
    (120, 'Billing / Pay To Provider Billing Zip', 1051, 1059, 9, 'C', 'Blank', 'R', 'O'), 
    (121, 'Billing / Pay To Provider Group', 1060, 1089, 30, 'C', 'Blank', 'R', 'O'), 
    (122, 'Filler', 1090, 1100, 11, 'C', 'Blank', '', 'O'), 
    (123, 'Billing / Pay To Provider Practice Address one', 1101, 1130, 30, 'C', 'Blank', 'R', 'O'), 
    (124, 'Billing / Pay To Provider Practice Address two', 1131, 1160, 30, 'C', 'Blank', 'R', 'O'), 
    (125, 'Billing / Pay To Provider Practice City', 1161, 1180, 20, 'C', 'Blank', 'R', 'O'), 
    (126, 'Billing / Pay To Provider Practice Phone', 1181, 1190, 10, 'C', 'Blank', 'R', 'O'), 
    (127, 'Billing / Pay To Provider Practice State', 1191, 1192, 2, 'C', 'Blank', 'R', 'O'), 
    (128, 'Billing / Pay To Provider Practice Zip', 1193, 1201, 9, 'C', 'Blank', 'R', 'O'), 
    (129, 'Filler', 1202, 1209, 8, 'C', 'Blank', 'R', 'O'), 
    (130, 'Billing / Pay To Provider TIN', 1210, 1218, 9, 'C', 'Blank', 'R', 'O', 'billing_provider_tin'), 
    (131, 'Billing / Pay To Provider TIN Suffix', 1219, 1224, 6, 'C', 'Blank', 'R', 'O'), 
    (132, 'Resource Utility Group', 1225, 1228, 4, 'C', 'Blank', 'R', 'O'), 
    (133, 'Rendering Provider First Name', 1229, 1253, 25, 'C', 'Blank', 'R', 'O'), 
    (134, 'Rendering Provider Last Name', 1254, 1288, 35, 'C', 'Blank', 'R', 'O', 'rendering_provider_last_name'), 
    (135, 'Rendering Provider Middle Name', 1289, 1313, 25, 'C', 'Blank', 'R', 'O'), 
    (136, 'Rendering Provider Suffix', 1314, 1323, 10, 'C', 'Blank', 'R', 'O'), 
    (137, 'Legacy Diagnosis Code 6', 1324, 1328, 5, 'C', 'Blank', 'R', 'O'), 
    (138, 'Legacy Diagnosis Code 7', 1329, 1333, 5, 'C', 'Blank', 'R', 'O'), 
    (139, 'Legacy Diagnosis Code 8', 1334, 1338, 5, 'C', 'Blank', 'R', 'O'), 
    (140, 'Legacy Diagnosis Code 9', 1339, 1343, 5, 'C', 'Blank', 'R', 'O'), 
    (141, 'Legacy Diagnosis Code 10', 1344, 1348, 5, 'C', 'Blank', 'R', 'O'), 
    (142, 'Legacy ICD9Proc4', 1349, 1353, 5, 'C', 'Blank', 'R', 'O'), 
    (143, 'Legacy ICD9Proc5', 1354, 1358, 5, 'C', 'Blank', 'R', 'O'), 
    (144, 'Legacy ICD9Proc6', 1359, 1363, 5, 'C', 'Blank', 'R', 'O'), 
    (145, 'Provider Signature on File', 1364, 1364, 1, 'C', 'Blank', 'R', 'O'), 
    (146, 'Principal Procedure Code Date', 1365, 1372, 8, 'C', 'Blank', 'R', 'O'), 
    (147, 'Other Procedure Code Date 2', 1373, 1380, 8, 'C', 'Blank', 'R', 'O'), 
    (148, 'Other Procedure Code Date 3', 1381, 1388, 8, 'C', 'Blank', 'R', 'O'), 
    (149, 'Other Procedure Code Date 4', 1389, 1396, 8, 'C', 'Blank', 'R', 'O'), 
    (150, 'Other Procedure Code Date 5', 1397, 1404, 8, 'C', 'Blank', 'R', 'O'), 
    (151, 'Other Procedure Code Date 6', 1405, 1412, 8, 'C', 'Blank', 'R', 'O'), 
    (152, 'Referring Provider First Name', 1413, 1442, 30, 'C', 'Blank', 'R', 'O'), 
    (153, 'Referring Provider Middle Name', 1443, 1467, 25, 'C', 'Blank', 'R', 'O'), 
    (154, 'Referring Provider Last/Group Name', 1468, 1507, 40, 'C', 'Blank', 'R', 'O'), 
    (155, 'Referring Provider Suffix', 1508, 1517, 10, 'C', 'Blank', 'R', 'O'), 
    (156, 'Referring Provider DEA Number', 1518, 1526, 9, 'C', 'Blank', 'R', 'O', 'referring_provider_dea_number'), 
    (157, 'Referring Provider License Number', 1527, 1556, 30, 'C', 'Blank', 'R', 'O'), 
    (158, 'Wholesale Bill Review Fee', 1557, 1565, 9, 'N', 'Zero', 'L', 'C'), 
    (159, 'Wholesale Complex Bill Review Fee', 1566, 1574, 9, 'N', 'Zero', 'L', 'C'), 
    (160, 'Wholesale PPO Fee', 1575, 1583, 9, 'N', 'Zero', 'L', 'C'), 
    (161, 'Wholesale Utilization Fee', 1584, 1592, 9, 'N', 'Zero', 'L', 'C'), 
    (162, 'Wholesale Negotiated Discount Fee', 1593, 1601, 9, 'N', 'Zero', 'L', 'C'), 
    (163, 'Wholesale Nurse Review Fee', 1602, 1610, 9, 'N', 'Zero', 'L', 'C'), 
    (164, 'Wholesale Physician Review Fee', 1611, 1619, 9, 'N', 'Zero', 'L', 'C'), 
    (165, 'Wholesale Specialty U & C Fee', 1620, 1628, 9, 'N', 'Zero', 'L', 'C'), 
    (166, 'Wholesale Out of Network Fee', 1629, 1637, 9, 'N', 'Zero', 'L', 'C'), 
    (167, 'Wholesale Bill Review Sales Tax Fee', 1638, 1646, 9, 'N', 'Zero', 'L', 'C'), 
    (168, 'Wholesale Sales Tax Zip Code', 1647, 1655, 9, 'N', 'Zero', 'L', 'C'), 
    (169, 'Retail Sales Tax Zip Code', 1656, 1664, 9, 'N', 'Zero', 'L', 'C'), 
    (170, 'Admitting Diagnosis Code', 1665, 1672, 8, 'C', 'Blank', 'R', 'O'), 
    (171, 'Facility NPI', 1673, 1682, 10, 'C', 'Blank', 'R', 'C'), 
    (172, 'Billing Provider NPI', 1683, 1692, 10, 'C', 'Blank', 'R', 'C'), 
    (173, 'Attending Provider NPI', 1693, 1702, 10, 'C', 'Blank', 'R', 'C'), 
    (174, 'Operating Physician NPI', 1703, 1712, 10, 'C', 'Blank', 'R', 'O'), 
    (175, 'Other 1 Provider NPI', 1713, 1722, 10, 'C', 'Blank', 'R', 'O'), 
    (176, 'Other 2 Provider NPI', 1723, 1732, 10, 'C', 'Blank', 'R', 'O'), 
    (177, 'ECI Code 1', 1733, 1740, 8, 'C', 'Blank', 'R', 'O'), 
    (178, 'ECI Code 2', 1741, 1748, 8, 'C', 'Blank', 'R', 'O'), 
    (179, 'ECI Code 3 ', 1749, 1756, 8, 'C', 'Blank', 'R', 'O'), 
    (180, 'Occurrence Code 1', 1757, 1758, 2, 'C', 'Blank', 'R', 'O'), 
    (181, 'Occurrence Date 1', 1759, 1766, 8, 'C', 'Blank', 'R', 'O'), 
    (182, 'Occurrence Code 2', 1767, 1768, 2, 'C', 'Blank', 'R', 'O'), 
    (183, 'Occurrence Date 2', 1769, 1776, 8, 'C', 'Blank', 'R', 'O'), 
    (184, 'Occurrence Code 3', 1777, 1778, 2, 'C', 'Blank', 'R', 'O'), 
    (185, 'Occurrence Date 3', 1779, 1786, 8, 'C', 'Blank', 'R', 'O'), 
    (186, 'Occurrence Code 4', 1787, 1788, 2, 'C', 'Blank', 'R', 'O'), 
    (187, 'Occurrence Date 4', 1789, 1796, 8, 'C', 'Blank', 'R', 'O'), 
    (188, 'Referring Provider NPI', 1797, 1806, 10, 'C', 'Blank', 'R', 'O', 'referring_provider_npi'), 
    (189, 'Operating Physician License Number', 1807, 1836, 30, 'C', 'Blank', 'R', 'O'), 
    (190, 'DRG Discharge Fraction', 1837, 1847, 11, 'N', 'Zero', 'L', 'O'), 
    (191, 'DRG Inpatient Multiplier', 1848, 1858, 11, 'N', 'Zero', 'L', 'O'), 
    (192, 'DRG Composite Factor', 1859, 1869, 11, 'N', 'Zero', 'L', 'O'), 
    (193, 'DRG Weight', 1870, 1880, 11, 'N', 'Zero', 'L', 'O'), 
    (194, 'DRG Value', 1881, 1891, 11, 'N', 'Zero', 'L', 'O'), 
    (195, 'Re-Submission Reason Code', 1892, 1893, 2, 'C', 'Blank', 'R', 'O'), 
    (196, 'Contract Type', 1894, 1895, 2, 'C', 'Blank', 'R', 'O'), 
    (197, 'Contract Amount', 1896, 1906, 11, 'N', 'Zero', 'L', 'O'), 
    (198, 'Prior Authorization or Referral Number 1', 1907, 1936, 30, 'C', 'Blank', 'R', 'O'), 
    (199, 'Prior Authorization or Referral Number 2', 1937, 1966, 30, 'C', 'Blank', 'R', 'O'), 
    (200, 'eBilling Bill HUB ID', 1967, 2016, 50, 'C', 'Blank', 'R', 'O'), 
    (201, 'Filler', 2017, 2020, 4, 'C', 'Blank', '', ''), 
    (202, 'Other Billing Provider External ID', 2021, 2050, 30, 'C', 'Blank', 'R', 'O'), 
    (203, 'Other Billing Provider NPI', 2051, 2060, 10, 'C', 'Blank', 'R', 'O'), 
    (204, 'Other Billing Provider TIN', 2061, 2069, 9, 'C', 'Blank', 'R', 'O'), 
    (205, 'Other Billing Provider TIN Suffix', 2070, 2075, 6, 'C', 'Blank', 'R', 'O'), 
    (206, 'Other Billing Provider Group Name', 2076, 2115, 40, 'C', 'Blank', 'R', 'O'), 
    (207, 'Other Billing Provider First Name', 2116, 2140, 25, 'C', 'Blank', 'R', 'O'), 
    (208, 'Other Billing Provider Last Name', 2141, 2175, 35, 'C', 'Blank', 'R', 'O'), 
    (209, 'Other Billing Provider Middle Name', 2176, 2200, 25, 'C', 'Blank', 'R', 'O'), 
    (210, 'Other Billing Provider Suffix', 2201, 2210, 10, 'C', 'Blank', 'R', 'O'), 
    (211, 'Other Billing Provider Address One', 2211, 2240, 30, 'C', 'Blank', 'R', 'O'), 
    (212, 'Other Billing Provider Address Two', 2241, 2270, 30, 'C', 'Blank', 'R', 'O'), 
    (213, 'Other Billing Provider City', 2271, 2290, 20, 'C', 'Blank', 'R', 'O'), 
    (214, 'Other Billing Provider State', 2291, 2292, 2, 'C', 'Blank', 'R', 'O'), 
    (215, 'Other Billing Provider Zip', 2293, 2301, 9, 'C', 'Blank', 'R', 'O'), 
    (216, 'Other Billing Provider Phone', 2302, 2311, 10, 'C', 'Blank', 'R', 'O'), 
    (217, 'eBilling Transaction Acknowledgement', 2312, 2331, 20, 'C', 'Blank', 'R', 'C'), 
    (218, 'Reject Code', 2332, 2361, 30, 'C', 'Blank', 'R', 'C'), 
    (219, 'Reject Description', 2362, 2441, 80, 'C', 'Blank', 'R', 'C'), 
    (220, 'Paid Date', 2442, 2449, 8, 'C', 'Blank', 'R', 'O'), 
    (221, 'Check Number', 2450, 2479, 30, 'C', 'Blank', 'R', 'O'), 
    (222, 'Paid Amount', 2480, 2488, 9, 'N', 'Blank', 'L', 'O'), 
    (223, 'Diagnosis Code 11', 2489, 2496, 8, 'C', 'Blank', 'R', 'O'), 
    (224, 'Diagnosis Code 12', 2497, 2504, 8, 'C', 'Blank', 'R', 'O'), 
    (225, 'Diagnosis Code 13', 2505, 2512, 8, 'C', 'Blank', 'R', 'O'), 
    (226, 'Diagnosis Code 14', 2513, 2520, 8, 'C', 'Blank', 'R', 'O'), 
    (227, 'Diagnosis Code 15', 2521, 2528, 8, 'C', 'Blank', 'R', 'O'), 
    (228, 'Diagnosis Code 16', 2529, 2536, 8, 'C', 'Blank', 'R', 'O'), 
    (229, 'Diagnosis Code 17', 2537, 2544, 8, 'C', 'Blank', 'R', 'O'), 
    (230, 'Diagnosis Code 18', 2545, 2552, 8, 'C', 'Blank', 'R', 'O'), 
    (231, 'Diagnosis 11 Present on Admission (POA) Code', 2553, 2553, 1, 'C', 'Blank', '', 'O'), 
    (232, 'Diagnosis 12 Present on Admission (POA) Code', 2554, 2554, 1, 'C', 'Blank', '', 'O'), 
    (233, 'Diagnosis 13 Present on Admission (POA) Code', 2555, 2555, 1, 'C', 'Blank', '', 'O'), 
    (234, 'Diagnosis 14 Present on Admission (POA) Code', 2556, 2556, 1, 'C', 'Blank', '', 'O'), 
    (235, 'Diagnosis 15 Present on Admission (POA) Code', 2557, 2557, 1, 'C', 'Blank', '', 'O'), 
    (236, 'Diagnosis 16 Present on Admission (POA) Code', 2558, 2558, 1, 'C', 'Blank', '', 'O'), 
    (237, 'Diagnosis 17 Present on Admission (POA) Code', 2559, 2559, 1, 'C', 'Blank', '', 'O'), 
    (238, 'Diagnosis 18 Present on Admission (POA) Code', 2560, 2560, 1, 'C', 'Blank', '', 'O'), 
    (239, 'Third Party Submitter Bill ID', 2561, 2590, 30, 'C', 'Blank', 'R', 'O'), 
    (240, 'Billing Provider Taxonomy Code', 2591, 2601, 11, 'C', 'Blank', 'R', 'O'), 
    (241, 'Facility Provider Taxonomy', 2602, 2612, 11, 'C', 'Blank', 'R', 'O'), 
    (242, 'Rendering Provider Taxonomy Code', 2613, 2623, 11, 'C', 'Blank', 'R', 'O'), 
    (243, 'Filler', 2624, 7000, 4376, 'C', 'Blank', '', 'O'), 
)

class BillHeaderDataSource(object):
    layout = bill_header_layout

    rec_type = '002'
    site_code = 'CPC'
    adjuster = ''
    external_bill_id = ''
    diagnosis_code_1 = '00000959'
    diagnosis_code_2 = ''
    diagnosis_code_3 = ''
    tob = 'MP'
    claim_number = ''           
    client_code = ''
    doi = ''
    due_date = ''
    bill_review_fees = 0
    retail_ppo_fees = 0
    import_bill_id = ''
    pos = '01'
    provider_invoice = ''
    fee_override = 'Y'
    rendering_provider_license_number = ''
    rendering_provider_specialty = 'A5'
    rendering_provider_type = 'PH'
    rendering_provider_zip = ''
    referring_provider_name = ''
    submit_date = ''
    sub_product_price = 0
    sub_product_price_net = 0
    tx_bill_type = ''
    type_of_service = '9'
    rendering_provider_last_name = ''
    referring_provider_dea_number = ''
    referring_provider_npi = ''
    tob = 'P'
    already_repriced = 'Y'
    sales_tax = 0
    billing_provider_id = '013254'
    billing_provider_tin = '880492251'
    document_control_type = 'EB'

    def __init__(self, invoice_id, items):
        self.invoice_id = invoice_id
        self.from_db(items)

    def from_db(self, items):
        """ Populate the header data source with a list of invoice items
        from the sql database. We use the first record to populate all the non
        total fields.
        """
        rec = items[0]
        totals = self._calc_totals(items)

        self.adjuster = "%s %s" % (
            rec.str("adjuster_first_name"),
            rec.str("adjuster_last_name"))

        self.claim_number = rec.str("ref_nbr_1")
        if not self.claim_number:
            self.claim_number = rec.str("claim_number")

        self.client_code = rec.str('client_code')
        if not self.claim_number:
            self.claim_number = '999999999'
        log.debug("%s-%s: %s %s claim number %s (%s) SOJ: %s", rec['invoice_id'], rec['line_no'],
                  rec['patient_first_name'], rec['patient_last_name'],
                  self.claim_number, len(self.claim_number), rec.str('jurisdiction'))

        self.sales_tax = totals.currency('sales_tax')
        self.bill_review_fees = totals.currency('processing_fee')
        self.external_bill_id = rec.str('invoice_id')
        self.import_bill_id = rec.str('invoice_id')
        self.provider_invoice = rec.str('invoice_id')
        self.document_control_id = "CPS%s" % rec.str('invoice_id')
        self.rendering_provider_zip = rec.str('pharmacy_zip')
        self.doi = rec.date('doi')
        # Paul said not to send this one as it causes warnings
        # self.due_date = rec.date('due_date')
        self.referring_provider_name = rec.str('doctor_name')
        self.submit_date = rec.date('create_date')

        if rec.str('jurisdiction') == '09':
            self.rendering_provider_license_number = rec.str('lic_number')
        elif rec.str('jurisdiction') == '42':
            self.rendering_provider_license_number = \
                rec.str('doctor_dea_number')

        self.rendering_provider_last_name = rec.str('pharmacy_name')
        self.referring_provider_dea_number = rec.str('doctor_dea_number')
        self.referring_provider_npi = rec.str('doctor_npi_number')

    def _calc_totals(self, items):
        """ The data source is given a list of items. We need to calculate the
        totals here.
        """
        totals = {'sales_tax': Decimal("0"),
                  'processing_fee': Decimal("0")}
        return DataRecord(totals)

bill_detail_layout = Layout(
('field', 'name', 'from', 'to', 'len', 'dt', 'filler', 'pad', 'req', 'value'),
    (1, 'Record Type', 1, 3, 3, 'C', 'Blank', 'R', 'R', 'rec_type'), 
    (2, 'Charge_L', 4, 12, 9, 'N', 'Zero', 'L', 'O', 'charge_l'), 
    (3, 'Diagnosis Reference 1', 13, 13, 1, 'C', 'Blank', 'R', 'O'), 
    (4, 'Diagnosis Reference 2', 14, 14, 1, 'C', 'Blank', 'R', 'O'), 
    (5, 'Diagnosis Reference 3', 15, 15, 1, 'C', 'Blank', 'R', 'O'), 
    (6, 'Diagnosis Reference 4', 16, 16, 1, 'C', 'Blank', 'R', 'O'), 
    (7, 'Diagnosis Reference 5', 17, 17, 1, 'C', 'Blank', 'R', 'O'), 
    (8, 'DOS', 18, 25, 8, 'C', 'Blank', 'R', 'R', 'dos'), 
    (9, 'Filler', 26, 33, 8, 'C', 'Blank', '', 'O'), 
    (10, 'Import Bill ID', 34, 83, 50, 'C', 'Blank', 'R', 'R', 'import_bill_id'), 
    (11, 'Modifier/Message Code 1', 84, 89, 6, 'C', 'Blank', 'R', 'C'), 
    (12, 'Modifier/Message Code 2', 90, 95, 6, 'C', 'Blank', 'R', 'C'), 
    (13, 'Modifier/Message Code 3', 96, 101, 6, 'C', 'Blank', 'R', 'C'), 
    (14, 'Modifier/Message Code 4', 102, 107, 6, 'C', 'Blank', 'R', 'C'), 
    (15, 'Modifier/Message Code 5', 108, 113, 6, 'C', 'Blank', 'R', 'C'), 
    (16, 'Modifier/Message Code 6', 114, 119, 6, 'C', 'Blank', 'R', 'C'), 
    (17, 'Modifier/Message Code 7', 120, 125, 6, 'C', 'Blank', 'R', 'C'), 
    (18, 'Modifier/Message Code 8', 126, 131, 6, 'C', 'Blank', 'R', 'C'), 
    (19, 'Modifier/Message Code 9', 132, 137, 6, 'C', 'Blank', 'R', 'C'), 
    (20, 'Modifier/Message Code 10', 138, 143, 6, 'C', 'Blank', 'R', 'C'), 
    (21, 'POS_L', 144, 145, 2, 'C', 'Blank', 'R', 'O', 'pos'), 
    (22, 'Procedure Code Billed', 146, 175, 30, 'C', 'Blank', 'R', 'O', 'procedure_code_billed'), 
    (23, 'Procedure Code', 176, 205, 30, 'C', 'Blank', 'R', 'C', 'procedure_code'), 
    (24, 'Proc Type', 206, 206, 1, 'C', 'Blank', 'R', 'R', 'proc_type'), 
    (25, 'Revenue Code', 207, 210, 4, 'C', 'Blank', 'R', 'C'), 
    (26, 'Days Supply', 211, 213, 3, 'C', 'Blank', 'R', 'O', 'days_supply'), 
    (27, 'Rx Number', 214, 233, 20, 'C', 'Blank', 'R', 'O', 'rx_number'), 
    (28, 'Bill Review Reductions', 234, 242, 9, 'N', 'Zero', 'L', 'O', 'bill_review_reductions'), 
    (29, 'Complex Bill Review Reductions', 243, 251, 9, 'N', 'Zero', 'L', 'O', 'complex_bill_review_reductions'), 
    (30, 'PPO Reductions', 252, 260, 9, 'N', 'Zero', 'L', 'O', 'ppo_bill_review_reductions'), 
    (31, 'Utilization Review Reductions', 261, 269, 9, 'N', 'Zero', 'L', 'O', 'utilization_review_reductions'), 
    (32, 'Negotiated Discount Reductions', 270, 278, 9, 'N', 'Zero', 'L', 'O', 'negotiated_discount_reductions'), 
    (33, 'Nurse Consultant Review Reductions', 279, 287, 9, 'N', 'Zero', 'L', 'O', 'nurse_consultant_review_reductions'), 
    (34, 'Physician Advisor Review Reductions ', 288, 296, 9, 'N', 'Zero', 'L', 'O', 'physician_advisor_review_reductions'), 
    (35, 'Specialty U&C Reductions ', 297, 305, 9, 'N', 'Zero', 'L', 'O', 'specialty_uc_review_reductions'), 
    (36, 'Out of Network Review Reductions', 306, 314, 9, 'N', 'Zero', 'L', 'O', 'oon_review_reductions'), 
    (37, 'ReductionAmount10', 315, 323, 9, 'N', 'Zero', 'L', 'O', 'reduction_amount_10'), 
    (38, 'TOS', 324, 325, 2, 'C', 'Blank', 'R', 'O'), 
    (39, 'Units', 326, 329, 4, 'N', 'Zero', 'L', 'O', 'units'), 
    (40, 'New / Refill', 330, 330, 1, 'C', '', '', 'O', 'new_refill'), 
    (41, 'Rendering Provider Secondary Identifier ', 331, 360, 30, 'C', 'Blank', 'R', 'O'), 
    (42, 'Certification / DAW', 361, 361, 1, 'N', '', '', 'O', 'daw'), 
    (43, 'Message Code/Modifier Jurisdiction 1', 362, 363, 2, 'C', 'Blank', 'R', 'O'), 
    (44, 'Message Code/Modifier Jurisdiction 2', 364, 365, 2, 'C', 'Blank', 'R', 'O'), 
    (45, 'Message Code/Modifier Jurisdiction 3', 366, 367, 2, 'C', 'Blank', 'R', 'O'), 
    (46, 'Message Code/Modifier Jurisdiction 4', 368, 369, 2, 'C', 'Blank', 'R', 'O'), 
    (47, 'Message Code/Modifier Jurisdiction 5', 370, 371, 2, 'C', 'Blank', 'R', 'O'), 
    (48, 'Message Code/Modifier Jurisdiction 6', 372, 373, 2, 'C', 'Blank', 'R', 'O'), 
    (49, 'Message Code/Modifier Jurisdiction 7', 374, 375, 2, 'C', 'Blank', 'R', 'O'), 
    (50, 'Message Code/Modifier Jurisdiction 8', 376, 377, 2, 'C', 'Blank', 'R', 'O'), 
    (51, 'Message Code/Modifier Jurisdiction 9', 378, 379, 2, 'C', 'Blank', 'R', 'O'), 
    (52, 'Message Code/Modifier Jurisdiction 10', 380, 381, 2, 'C', 'Blank', 'R', 'O'), 
    (53, 'Message Reduction Code 1', 382, 385, 4, 'C', 'Blank', 'R', 'O'), 
    (54, 'Message Reduction Code 2', 386, 389, 4, 'C', 'Blank', 'R', 'O'), 
    (55, 'Message Reduction Code 3', 390, 393, 4, 'C', 'Blank', 'R', 'O'), 
    (56, 'Message Reduction Code 4', 394, 397, 4, 'C', 'Blank', 'R', 'O'), 
    (57, 'Message Reduction Code 5', 398, 401, 4, 'C', 'Blank', 'R', 'O'), 
    (58, 'Message Reduction Code 6', 402, 405, 4, 'C', 'Blank', 'R', 'O'), 
    (59, 'Message Reduction Code 7', 406, 409, 4, 'C', 'Blank', 'R', 'O'), 
    (60, 'Message Reduction Code 8', 410, 413, 4, 'C', 'Blank', 'R', 'O'), 
    (61, 'Message Reduction Code 9', 414, 417, 4, 'C', 'Blank', 'R', 'O'), 
    (62, 'Message Reduction Code 10', 418, 421, 4, 'C', 'Blank', 'R', 'O'), 
    (63, 'Basis of Cost Determination', 422, 422, 1, 'C', 'Blank', '', 'O'), 
    (64, 'Filler', 423, 423, 1, 'C', 'Blank', '', ''), 
    (65, 'DME Billing Frequency Code', 424, 424, 1, 'C', 'Blank', '', 'O'), 
    (66, 'Filler', 425, 425, 1, 'C', 'Blank', '', ''), 
    (67, 'Drug/Supply Dispensing Fee', 426, 434, 9, 'N', 'Zero', 'L', 'O', 'drug_dispensing_fee'), 
    (68, 'Rendering Provider NPI', 435, 444, 10, 'N', 'Zero', 'L', 'O'), 
    (69, 'Qualifier (for Rendering Provider Secondary Identifier)', 445, 446, 2, 'C', 'Blank', 'R', 'C'), 
    (70, 'Diagnosis Reference List', 447, 476, 30, 'C', 'Blank', 'R', 'O'), 
    (71, 'Line External ID', 477, 506, 30, 'C', 'Blank', 'R', 'O', 'line_external_id'), 
    (72, 'Future Use (Patient Paid Amount', 507, 517, 11, 'C', 'Blank', 'R', ''), 
    (73, 'Filler', 518, 2000, 1483, 'C', 'Blank', '', ''), 
)

class BillDetailDataSource(object):
    layout = bill_detail_layout

    rec_type = '003'
    charge_l = 0
    dos = ''
    import_bill_id = ''
    proc_type = 'N'
    days_supply = ''
    rx_number = ''
    bill_review_reductions = 0
    complex_bill_review_reductions = 0
    ppo_bill_review_reductions = 0
    utilization_review_reductions = 0
    negotiated_discount_reductions = 0
    nurse_consultant_review_reductions = 0
    physician_advisor_review_reductions = 0
    specialty_uc_review_reductions = 0
    oon_review_reductions = 0
    reduction_amount_10 = 0
    units = 1
    new_refill = 'N'
    daw = ''
    pos = '01'
    line_external_id = ''
    procedure_code_billed = ''
    procedure_code = ''
    drug_dispensing_fee = ''

    def __init__(self, rec):
        #self.charge_l = currency(rec['cost_submitted'] + rec['dispense_fee'])
        if rec['state_fee'] > rec['total']:
            self.charge_l = rec.currency('state_fee')
            self.ppo_bill_review_reductions = currency(rec['state_fee'] - rec['total'])
        else:
            self.charge_l = rec.currency('total')
            self.ppo_bill_review_reductions = currency(0)

        #self.bill_review_reductions = currency(
        #    rec['cost_submitted'] + rec['eho_network_copay'] - rec['cost_allowed'])

        self.dos = rec.date('date_processed')
        self.import_bill_id = rec.str('invoice_id')
        self.days_supply = rec.str('days_supply')
        self.rx_number = rec.str('rx_number')
        if rec['refill_number'] % 20 != 0:
            self.new_refill = 'R'
        try:
            self.daw = int(rec['daw'])
        except ValueError:
            self.daw = 0
        self.line_external_id = rec.str('invoice_id')
        self.procedure_code_billed = rec.str('drug_name')
        self.procedure_code = rec.str('ndc_number')
        self.drug_dispensing_fee = rec.currency('dispense_fee')

bill_comment_layout = Layout(
('field', 'name',             'from', 'to', 'len', 'dt', 'filler', 'pad', 'req', 'value'),
    (1, 'Record Type',           1, 3, 3, 'C', 'Blank', 'R', 'R',           'rec_type'),
    (2, 'Import Bill ID',        4, 53, 50, 'C', 'Blank', 'R', 'R',         'import_bill_id'),
    (3, 'Comment Type',          54, 54, 1, 'C', 'Blank', 'R', 'O',         'comment_type'),
    (4, 'Comment',               55, 6054, 6000, 'C', 'Blank', 'R', 'O',    'comment'),
    (5, 'Filler',              6055, 7000, 946, 'C', 'Blank', 'R', 'O'))

class BillCommentDataSource(object):
    layout = bill_comment_layout
    rec_type = '004'
    import_bill_id = ''
    comment_type = 'C'
    comment = ''

    comment_tmpl = textwrap.dedent("""\
        PATIENT: %(patient_first_name)s %(patient_last_name)s
        ID: %(patient_ssn)s
        DOB: %(patient_dob)s
        POLICY #: %(policy_number)s""").replace("\n", " ")

    def __init__(self, rec):
        self.import_bill_id = rec.str('invoice_id')
        self.comment = self.comment_tmpl % rec

bill_attachment_layout = Layout(
('field', 'name', 'from', 'to', 'len', 'dt', 'filler', 'pad', 'req', 'value'),
    (1, 'Record Type', 1, 2, 2, 'C', 'Blank', 'R', 'R', 'rec_type'), 
    (2, 'Client Code', 3, 6, 4, 'C', 'Blank', 'R', 'C', 'client_code'),
    (3, 'Bill Sequence Number', 7, 16, 10, 'C', 'Blank', 'R', 'C'),
    (4, 'Import Bill ID', 17, 66, 50, 'C', 'Blank', 'R', 'C', 'import_bill_id'),
    (5, 'Filler', 67, 76, 10, 'C', 'Blank', 'R', 'O'),
    (6, 'Attachment Paperwork (PWK) Type Code', 77, 80, 4, 'C', 'Blank', 'R', 'O'),
    (7, 'Bill Doc Control Type', 81, 82, 2, 'C', 'Blank', 'R', 'C', 'bill_doc_control_type'),
    (8, 'Bill DCN', 83, 132, 50, 'C', 'Blank', 'R', 'R'),
    (9, 'Provider Doc Control Type', 133, 134, 2, 'C', 'Blank', 'R', 'O'),
    (10, 'Provider DCN', 135, 184, 50, 'C', 'Blank', 'R', 'O', 'provider_dcn'),
    (11, 'Trading Partner Doc Control Type', 185, 186, 2, 'C', 'Blank', 'R', 'O'),
    (12, 'Trading Partner DCN', 187, 236, 50, 'C', 'Blank', 'R', 'O'),
    (13, 'HUB Doc Control Type', 237, 238, 2, 'C', 'Blank', 'R', 'O'),
    (14, 'HUB Attachment ID', 239, 288, 50, 'C', 'Blank', 'R', 'O'),
    (15, 'Document Management System (DMS) Doc Control Type', 289, 290, 2, 'C', 'Blank', 'R', 'O', 'doc_management_system_type'),
    (16, 'Document Management System (DMS) DCN', 291, 340, 50, 'C', 'Blank', 'R', 'O', 'dcn'),
    (17, 'Create Date', 341, 348, 8, 'C', 'Blank', 'R', 'O'),
    (18, 'Create User ID', 349, 350, 2, 'C', 'Blank', 'R', 'O'),
    (19, 'Mod Date', 351, 358, 8, 'C', 'Blank', 'R', 'O'),
    (20, 'Mod User ID', 359, 360, 2, 'C', 'Blank', 'R', 'O'),
    (21, 'Filler', 361, 1000, 640, 'C', 'Blank', 'R', 'O')
)

class BillAttachmentDataSource(object):
    layout = bill_attachment_layout
    bill_doc_control_type = 'EB'
    doc_management_system_type = 'EB'
    rec_type = 'BA'
    client_code = ''
    import_bill_id = ''
    dcn = ''
    provider_dcn = ''

    def __init__(self, rec):
        self.import_bill_id = rec.str('invoice_id')
        self.dcn = rec.str('invoice_id')
        self.provider_dcn = rec.str('invoice_id')
        self.client_code = rec.str('client_code')

def currency(val):
    if val is None:
        return '0'
    else:
        return int(val*100)

class DataRecord(dict):
    """ Utility object to provides data services for a record returned from
    a database query.
    """
    def currency(self, f):
        return currency(self[f])

    def date(self, f):
        val = self[f]
        if val is None:
            return ''
        else:
            return self[f].strftime("%Y%m%d")

    def str(self, f):
        x = self[f]
        if x is None:
            return ''
        if isinstance(x, int):
            if x == 0:
                return ''
            else:
                x = str(x)
        return x.upper()

class RecordParser(object):
    """ Give me a definition from the schema and I will parse a 
    file for you.
    """
    def __init__(self, layout):
        self.layout = layout

    def parse(self, fd):
        """ Parse a single record off the FD """
        value = {}
        for field in self.layout.fields:
            print("%s: %s" % (field.name, fd.read(field.len)))
        return value

def data_for_batch_date(batch_date):
    """ Provide a list of all the data objects for the given
    batch_date.
    """
    cursor = db.dict_cursor()
    cursor.execute("""
        SELECT
            trans.total,
            history.date_processed,
            pharmacist.lic_number,
            trans.total,
            trans.state_fee,
            trans.invoice_id,
            trans.days_supply,
            trans.rx_number,
            trans.refill_number,
            trans.daw,
            trans.trans_id,
            trans.create_date,
            trans.create_date::date + '15 days'::interval AS due_date,
            claim.claim_number,
            claim.ref_nbr_1,
            claim.ref_nbr_2 as client_code,
            trans.policy_number,
            user_info.first_name AS adjuster_first_name,
            user_info.last_name AS adjuster_last_name,
            drug.name AS drug_name,
            drug.ndc_number,
            pharmacy.zip_code AS pharmacy_zip,
            pharmacy.name AS pharmacy_name,
            trans.doi,
            trans.doctor_dea_number,
            trans.doctor_npi_number,
            trans.dispense_fee,
            trans.line_no,
            doctor.name AS doctor_name,
            patient.first_name AS patient_first_name,
            patient.last_name AS patient_last_name,
            patient.dob AS patient_dob,
            patient.ssn AS patient_ssn,
            patient.jurisdiction
        FROM trans
        JOIN drug USING(drug_id)
        JOIN pharmacy USING(pharmacy_id)
        JOIN patient USING(patient_id)
        JOIN history USING(history_id)
        JOIN claim USING(claim_id)
        JOIN client ON trans.group_number = client.group_number
        LEFT JOIN doctor ON trans.doctor_id = doctor.doctor_id
        LEFT JOIN user_info ON trans.adjuster1_email = user_info.email
        LEFT JOIN pharmacist ON history.pharmacist_id = pharmacist.pharmacist_id
        WHERE client.send_in_companion_edi = TRUE AND trans.batch_date=%s
            AND claim.ref_nbr_2 IS NOT NULL
        ORDER BY trans.invoice_id, trans.line_no
        """, (batch_date,))

    if not cursor.rowcount:
        # No transactions for the group, bail.
        return None
    # First we build a compound data structure
    sql_records = {}
    for rec in cursor:
        sql_records.setdefault(rec['invoice_id'], [])
        sql_records[rec['invoice_id']].append(DataRecord(rec))

    sql_records = sorted(sql_records.items())

    # Build list of output records
    theader = TransDataSource()
    theader.trans_date = datetime.date.today().strftime("%Y%m%d")
    records = [theader]
    for invoice_id, items in sql_records:
        theader.bill_record_count += 1
        bheader = BillHeaderDataSource(invoice_id, items)
        records.append(bheader)
        for item in items:
            theader.line_record_count += 1
            records.append(BillDetailDataSource(item))
            theader.bill_comment_record_count += 1
            records.append(BillCommentDataSource(item))
        #records.append(BillAttachmentDataSource(item))
    return records

def format_field_value(field, value):
    """ with the given field specification from a layout, format then
    given value into a string. We have to take into consideration the
    data type, filler, length and which side to pad on. This is the work horse
    of getting the data into the SA format.
    """
    if field.dt == 'C' and value is not None:
        assert isinstance(value, str), (field, value)
    if field.dt == 'N' and value is not None:
        assert isinstance(value, int), (field, value)

    if value is None:
        # The field isn't required and we have no data so just give spaces
        # regardless of the type
        if field.req != 'R':
            return ' ' * field.len
        else:
            value = ''
    elif isinstance(value, int):
        value = str(value)

    if field.filler == 'Zero':
        padder = '0'
    else:
        padder = ' '
    
    just = string.ljust
    if field.pad in (None, '') and field.dt == 'N':
        just = string.rjust
    elif field.pad == 'L':
        just = string.rjust

    if len(value) > field.len:
        # truncate
        value = value[:field.len]
    return just(value, field.len, padder)


def get_sbi_file_name(fdir, date=datetime.date.today()):
    """ Create the next SBI file name for the given directory. 
    Helper to stage_sbi_file"""
    idx = 1
    for i in range(1, 10000):
        fname = "%s%04d.SBI" % (date.strftime("%y%j"), i)
        path = os.path.join(fdir, fname)
        if not os.path.exists(path):
            return path

class Stage(object):
    """ The stage is where all of the files are created, archived, encrypted
    and sent to the remote server.
    """
    dir = STAGE_DIR
    create_date = datetime.date.today()
    _sbi_path = None

    @property
    def sbi_path(self):
        """ Return the full path of the sbi file we are creating. We ensure that
        the file path is unique and does not exist on disk the first time the
        property is accessed. This property value is computed lazily.

        @rtype: str
        """
        if self._sbi_path is not None:
            return self._sbi_path
        idx = 1
        dt = self.create_date.strftime("%y%j")
        for i in range(1, 10000):
            fname = "%s%04d.SBI" % (dt, i)
            path = os.path.join(self.dir, fname)
            if not os.path.exists(path):
                self._sbi_path = path
                return self._sbi_path

    @property
    def zip_path(self):
        return os.path.splitext(self.sbi_path)[0] + ".zip"

    def __init__(self, working_dir=None):
        self.data = []
        if working_dir:
            self.dir = working_dir

    def load(self, data):
        """
        @param data: An iterable of data source objects which will be fed to
                     the layout to create the SBI file. 
        """
        self.data.extend(data)

    def setup(self):
        """ Set up the directory used to stage the creation of the files. It
        is ensured that the directory is empty.
        """
        if not os.path.exists(self.dir):
            os.mkdir(self.dir)

    def create_sbi_file(self):
        log.debug("Writing SBI file %r", self.sbi_path)
        f = open(self.sbi_path, 'w')
        for rec in self.data:
            rec.layout.write_record(rec, f)
        f.close()

    def copy_attachments(self):
        """ We send not only the sbi file, but also all of the pdf invoice files.
        We want to copy these all to a directory so that we can sync that directory
        with the remote server.
        """
        factory = print_invoice.Factory()
        invoice_factory = factory.invoice_factory(include_paid_items=False)
        file_factory = factory.disk_file_factory()
        for dcn in self._dcn_list():
            fpath = os.path.join(self.dir, "%s.pdf" % dcn)
            log.debug("Writing invoice file for DCN %s to %s", dcn, fpath)
            # dcn is CPS invoice_id, cut off the CPS
            invoice_id = int(dcn[3:])
            invoice = invoice_factory.for_invoice_id(invoice_id)
            file = file_factory.for_invoice(invoice)
            file.write(fpath)

    def zip(self):
        """ Create a zip file that contains the SBI file along with all of the
        attached PDF files in the stage directory.

        """
        z = zipfile.ZipFile(self.zip_path, 'w')
        z.write(self.sbi_path, os.path.basename(self.sbi_path))
        for dcn in self._dcn_list():
            z.write(os.path.join(self.dir, dcn + ".pdf"), dcn + ".pdf")
        z.close()

    def encrypt(self):
        """ Encrypt the zip file in the staging directory with PGP """
        return self._gpg_file(self.zip_path)

    def upload(self):
        encrypted_fpath = self.zip_path + ".asc"
        cmd = "lftp -c 'put -O ftp://CPS_test:cuVa4ust@192.234.216.66/internal/uploads %s'"
        cmd %= encrypted_fpath

        log.debug("Executing %s", cmd)
        if os.system(cmd):
            log.error("Could not send files to remote server")
            return False
        return True

    @property
    def archive_path(self):
        archive_path = os.path.basename(self.zip_path)
        return os.path.join(ARCHIVE_DIR, archive_path)

    def archive(self):
        """ Copy the created zip file to the archive directory for storage.
        """
        shutil.copy(self.zip_path, self.archive_path)

    def _gpg_file(self, fpath):
        return not os.system(
            "gpg --sign --encrypt --armor "
            "--recipient sasupport@mitchellsmartadvisor.com '%s'" % fpath)

    def _dcn_list(self):
        """ Calculate a list of all unique document control id's across all of
        the data sources in self.data. This was originally looking at dcn's,
        but those are gone now because we do not add the bill attachment
        records as per Greg Mills, so we had to get the numbers from 
        another field.

        @rtype: generator of str
        """
        copied = {}
        for d in self.data:
            if not hasattr(d, 'document_control_id'):
                continue
            if d.document_control_id in copied:
                continue
            copied[d.document_control_id] = True
            yield d.document_control_id

class Program(shell.Command):
    """ Command line interface """
    prompt = 'sa> '

    doc_header = textwrap.dedent("""\
        The smartadvisor file generation program. The most common usage
        will call the following commands:

        sa> batch YYMMDD
        sa> sbi
        sa> attach
        sa> zip
        sa> encrypt
        sa> upload""")

    _stage = None

    @property
    def stage(self):
        if self._stage is None:
            self._stage = Stage()
            self._stage.setup()
        return self._stage

    def do_check(self, args):
        [assert_schema_field(f) for f in trans_header_layout.fields]
        [assert_schema_field(f) for f in bill_header_layout.fields]
        [assert_schema_field(f) for f in bill_detail_layout.fields]
        [assert_schema_field(f) for f in bill_comment_layout.fields]
        [assert_schema_field(f) for f in bill_attachment_layout.fields]

    def do_batch(self, args):
        """ batch YYYYMMDD
        Load the claim data for the given batch.
        """
        self.stage.load(data_for_batch_date(args))

    def do_sbi(self, args):
        """ Create the SBI file in the working directory """
        self.stage.create_sbi_file()

    def do_attach(self, args):
        """ Copy invoice PDF files from the invoice web archive to the
        working directory """
        self.stage.copy_attachments()

    def do_zip(self, args):
        self.stage.zip()

    def do_encrypt(self, args):
        """ Encrypt all of the files in the working directory using the
        PGP public key of mitchell
        """
        self.stage.encrypt()

    def do_upload(self, args):
        """ Send the data to mitchell's server """
        self.stage.upload()

    def do_archive(self, args):
        self.stage.archive()

    def help_archive(self):
        print(Stage.archive.__doc__)
        print("Current archive directory:", ARCHIVE_DIR)

def assert_schema_field(row):
    """ Ensure that the field definition of the schema is good. This was a lot
    of data entry. A lot of chances for mistakes!
    """
    assert len(row) == 10, row
    assert isinstance(row.field, int), row
    assert isinstance(row.len, int), row
    assert row.dt in ('C', 'N'), row
    assert row.req in (None, '', 'O', 'R', 'C'), row
    assert row.pad in (None, '', 'L', 'R'), row
    assert row.filler in (None, '', 'Zero', 'Blank'), row

if __name__ == '__main__':
    Program().run()
