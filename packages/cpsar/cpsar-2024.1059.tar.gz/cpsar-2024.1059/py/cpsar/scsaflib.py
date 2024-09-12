""" SCSAF EDI Export Library. This module's purpose is to centralize the logic
that creates the proprietary SCSAF CSV file ands sends it off to SCSAF's
servers. This code was originally in a batch script, but has been pulled out
and refactored because the web interface now generates SCSAF files as well
with the rebill feature.
"""
import csv
import datetime
import email.utils
import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

import paramiko

import cpsar.runtime as R

from cpsar import config
from cpsar import txlib

class EDIWriter(object):
    output_dir = R.dpath('scsaf/pickup/outgoing')

    query_tmpl = """
SELECT
      trans.trans_id,
      trans.invoice_id,
      trans.line_no,
      'PHAR',                                   --  A Bill Type (HCFA or PHAR)
      claim.claim_number,                       --  B SAF Claim #
      patient.last_name,                        --  C Patient's Last Name
      patient.first_name,                       --  D Patient's First Name
      '',                                       --  E Patient's Middle Initial
      patient.ssn,                              --  F Patient's SSN
      to_char(claim.doi, 'MM/DD/YY'),           --  G Patient's DOI
      'CPS' || trans.invoice_id,                --  H Account Number
      trans.line_no as bill_line_item_number,   --  I Bill Line Item #
      to_char(history.rx_date, 'MM/DD/YY'),     --  J Service Effective Date mm/dd/yyyy)
      to_char(history.rx_date, 'MM/DD/YY'),     --  K Service End Date mm/dd/yyyy)
      '',                                       --  L Medical Place of Service Code
      '',                                       --  M CPT Code
      '',                                       --  N CPT Code Description
      '',                                       --  O CPT Code Modifier 1
      '',                                       --  P CPT Code Modifier 2
      '',                                       --  Q HCPC Code
      '',                                       --  R HCPC Code Description
      '',                                       --  S Diagnosis ICD9 Code
      '',                                       --  T Medical Type of Service Code
      '',                                       --  U Medical Expense Code From SAF provided list)
      drug.ndc_number,                          --  V National Drug Code
      drug.name,                                --  W Drug Description name and dosage
      to_char(history.rx_date, 'MM/DD/YY'),     --  X Drug Filled Date mm/dd/yyyy
      history.quantity,                         --  Y Drug Units
      '',                                       --  Z CDT Code
      (trans.total*100)::int,                   -- AA Billed Amount no $ signs, no decimals)
      history.days_supply,                      -- Units or anesthesia minutes)
      '631040950',                              -- Billing Provider FEIN digits only)
      'Corporate Pharmacy',                     -- Billing Provider Name
      'P.O. Box 1950',                          -- Billing Provider Address
      'Gadsden',                                -- Billing Provider City
      'AL',                                     -- Billing Provider State
      '35902',                                  -- Billing Provider ZIP digits only)
      pharmacy.tax_id,                          -- Service Provider FEIN digits only)
      pharmacy.name,                            -- Service Provider Name
      TRIM(COALESCE(pharmacy.address_1, '') || ' '
         || COALESCE(pharmacy.address_2, '')),  -- Service Provider Address
      pharmacy.city,                            -- Service Provider City
      pharmacy.state,                           -- Service Provider State
      substring(pharmacy.zip_code, 0, 6),       -- Service Provider ZIP digits only
      COALESCE(doctor.name, ''),                -- Treating Physician Name
      '',                                       -- Treating Physician Credentials UPIN
      '',                                       -- CPT Group Code
      '',                                       -- red_rsn_1
      '',                                       -- red_rsn_desc
      '',                                       -- red_rsn_2
      '',                                       -- red_rsn2_desc
      '',                                       -- red_rsn_3
      '',                                       -- red_rsn3_desc
      '',                                       -- red_rsn_4
      '',                                       -- red_rsn4_desc
      '',                                       -- reduction_amount1
      '',                                       -- reduction_amount2
      '',                                       -- bill_lvl_comment1
      '',                                       -- bill_line_item_cm
      ''                                        -- receive_date
    FROM trans
    JOIN history ON
       trans.history_id = history.history_id
    JOIN patient ON
       history.patient_id = patient.patient_id
    LEFT JOIN claim ON
        history.claim_id = claim.claim_id
    LEFT JOIN drug ON
       history.drug_id = drug.drug_id
    LEFT JOIN pharmacy ON
       history.pharmacy_id = pharmacy.pharmacy_id
    LEFT JOIN doctor ON
       history.doctor_id = doctor.doctor_id
    WHERE %(cond)s
    ORDER BY trans.invoice_id, trans.line_no
    """

    send_status = None

    def __init__(self, batch_date):
        self.batch_date = batch_date

    @property
    def batch_file_path(self):
        return os.path.join(self.output_dir, self.batch_file_name)

    @property
    def batch_file_name(self):
        return "companion%s.csv" % self.batch_date.strftime("%m%d%y%H%M%S")

    ## File Creation and helper methods
    def create_file(self):
        with open(self.batch_file_path, 'w') as fd:
            self.write_file(fd)

    def write_file(self, handle):
        handle.write(";".join(config.billing_recipients()))
        handle.write("\r\n")
        writer = csv.writer(handle, lineterminator='\r\n')
        recs = self.records()
        self.tx_count = recs.rowcount
        if not self.tx_count:
            raise NoTransactionsError

        cursor = R.db.cursor()
        for rec in recs:
            trans_id, invoice_id, line_no = rec[:3]
            rec = rec[3:]
            writer.writerow(rec)
            self.log_record(cursor, trans_id)


    def records(self):
        cursor = R.db.cursor()
        sql = self.query_tmpl % {'cond' : "trans.batch_date=%s"}
        cursor.execute(sql, (self.batch_date,))
        return cursor

    def log_record(self, cursor, trans_id):
        txlib.log(trans_id, 'Added to EDI file %s' % self.batch_file_path)

    ## File Sending
    def send_file(self):
        hostname = 'ftp.saf.sc.gov'
        port = 22
        username = "companion"
        password = "eb29saf"

        t = paramiko.Transport((hostname, port))
        t.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(self.batch_file_path, self.batch_file_name)
        sftp.close()
        self.send_status = 0


class RebillEDIWriter(EDIWriter):
    """ Writes an EDI file for all of the tx's marked as rebill. """
    def records(self):
        cursor = R.db.cursor()
        sql = self.query_tmpl % {
            'cond' : """
                trans.rebill=TRUE AND
                trans.group_number IN ('56600', '70300', '70303', '70483', '70081', '70888', '70891')

                """}
        cursor.execute(sql)
        return cursor

    def reset_rebill(self):
        cursor = R.db.cursor()
        cursor.execute("""
            UPDATE trans SET rebill=FALSE
            WHERE group_number IN ('56600', '70300', '70303', '70483', '70081', '70888', '70891')

                AND rebill=TRUE""")

class NoTransactionsError(Exception):
    """ Error marking that an attempt is being made to create a blank
    EDI file.
    """
    pass

