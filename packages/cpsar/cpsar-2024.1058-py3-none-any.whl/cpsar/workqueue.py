"""
The Workqueue system is in place to do data edits on transactions that have
errors which must be fixed for billing purposes. It is a data audit process.

WorkQueue - The location where jobs stay. Implemented as a table

Job - A problem with a particular history record that requires work from an
employee. Jobs are tied to a group number and claim reference number. The
history file is the file that is audited, not the trans file.

JobClass - A type of problem that a history record can have. the job class is a
definition of not only the problem itself but also what all types of history
records can have those problems.

Priority - A level of importance on a job, defined by its job class. The possible values
are::

    10 - Haults processing of batch
    9  - Haults processing of claims for a single group
    8  - Claim is held back and not billed by EHO
    7  - Claim is skipped in auxiliary business function (State Reporting)
    4  - Required to maintain consistency of internal records
    2  - Internal
    1  - Importance Unknown but required by external entity

The workqueue system is implemented by creating a set of container
objects and functions and then specifying a job for each possible error
in data files.

A temporary table is created that contains all of the transactions that
need to be properly validated along with all of the possible data fields
that would need to be validated.

Once a job is put in the work_queue table it stays there until the the
job_class is removed

If a transaction has been reversed then we do not audit it at all.

All programs that submit data to third parties should check for the
reversal flag and not send if it has been reversed.

"""
import logging

import cpsar.runtime as R
import cpsar.txtype as TT

__metaclass__ = type
log = logging.getLogger('')

###############################################################################
## Utility/Architecture Section

class WorkQueue:
    """ A programmatic interface for storing and retrieving jobs
    that need to be done.
    """
    def visible(self):
        """ Provide a list of all jobs that need to be done that have not
        been hidden by a user.
        """
        cursor = R.db.dict_cursor()
        cursor.execute("""
            SELECT work_queue.*, patient.patient_id,
                   patient.first_name, patient.last_name,
                   client.client_name, patient.ssn, history.doi, 
                   trans.invoice_id,
                   history.rx_number,
                   history.date_processed,
                   trans.trans_id
            FROM work_queue
            JOIN history ON
                work_queue.group_number = history.group_number AND
                work_queue.group_auth = history.group_auth
            JOIN patient ON
                history.patient_id = patient.patient_id
            LEFT JOIN client ON
                work_queue.group_number = client.group_number
            LEFT JOIN trans ON
                history.history_id = trans.history_id
            WHERE work_queue.hidden = FALSE
            ORDER BY priority DESC, group_number, group_auth
            """)
        return cursor

    def visible_by_job_class(self):
        job_classes = {}
        for rec in self.visible():
            job_classes.setdefault(rec['job_class'], [])
            job_classes[rec['job_class']].append(rec)
        jc = []
        for key in sorted(job_classes.keys()):
            jc.append((key, job_classes[key]))
        return jc

    def hide(self, job_class, gn, ga):
        cursor = R.db.cursor()
        cursor.execute("""
            UPDATE work_queue SET hidden=TRUE
            WHERE job_class=%s AND group_number=%s AND group_auth=%s
            """, (job_class, gn, ga))

    def add(self, job_class, gn, ga, msg, priority):
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT hidden
            FROM work_queue
            WHERE job_class=%s AND
                  group_number=%s AND
                  group_auth=%s
            """, (job_class, gn, ga))

        if cursor.rowcount:
            hidden, = cursor.fetchone()
            if hidden:
                cursor.execute("""
                    UPDATE work_queue
                    SET hidden=FALSE, item_description=%s
                    WHERE job_class=%s AND
                          group_number=%s AND
                          group_auth=%s
                    """, (msg, job_class, gn, ga))
        else: 
            cursor.execute("""
                INSERT INTO work_queue (
                    job_class, 
                    group_number, 
                    group_auth,
                    item_description,
                    priority,
                    hidden)
                VALUES (%s, %s, %s, %s, %s, FALSE)
                """, (job_class, gn, ga, msg, priority))
 
    def clear_except(self, job_class, keys):
        """ Remove all items for the given job class except those provided.
        """
        cursor = R.db.cursor()
        cursor.execute("""
            SELECT group_number, group_auth
            FROM work_queue
            WHERE job_class=%s
            """, (job_class,))

        cnt = 0
        for gn, ga in list(cursor):
            if (gn, ga) not in keys:
                cursor.execute("""
                    DELETE FROM work_queue
                    WHERE job_class=%s AND 
                          group_number=%s AND
                          group_auth=%s
                    """, (job_class, gn, ga))
                cnt += 1
        return cnt

    def delete(self, job_class, gn, ga):
        cursor = R.db.cursor()
        cursor.execute("""
            DELETE FROM work_queue
            WHERE job_class=%s AND 
                  group_number=%s AND
                  group_auth=%s
            """, (job_class, gn, ga))

    def reset(self):
        cursor = R.db.cursor()
        cursor.execute("DELETE FROM work_queue")

    def refresh(self):
        """ Update queue:
        - add new jobs that need to be done
        - remove jobs that have been done
        - leave jobs that haven't been done yet
        """
        for jclass in JobClassManager.run_set():
            R.log.debug("Processing job class %s", jclass.name)
            jclass()

        cursor = R.db.cursor()
        cursor.execute(
        """
        UPDATE work_queue SET trans_id = trans.trans_id
        FROM trans
        WHERE work_queue.group_number = trans.group_number 
            AND work_queue.group_auth = trans.group_auth
        """)

WorkQueue = WorkQueue()

class JobClassManager:
    """ Manages all of the job classes and the environment they need
    to execute. Provides an environment for job classes.
    """

    jclass_lookup = {}
    jclasses = []

    def add_jclass(self, jclass):
        if jclass.name in self.jclass_lookup:
            raise ValueError('job class %s already registered' % name)
        self.jclass_lookup[jclass.name] = jclass
        self.jclasses.append(jclass)

    def run_jclass(self, name):
        self.create_working_claim_table()
        jclass = self.jclass_lookup[name]
        jclass()
        self.drop_working_claim_table()
        
    def run_set(self):
        """ Provides a list of job classes to run with their proper
        envirnoment setup and torn down.
        """
        self.create_working_claim_table()
        for jclass in self.jclasses:
            yield jclass
        self.drop_working_claim_table()

    def create_working_claim_table(self):
        cursor = R.db.log_cursor()
        R.log.debug("Creating working table working_claim")

        cursor.execute("""
            CREATE TEMP TABLE working_claim AS
             SELECT
                ehistory.group_number,
                ehistory.group_auth,
                ehistory.doi,

                ehistory.state_fee,
                ehistory.usual_customary,
                ehistory.doctor_dea_number,
                ehistory.pharmacy_id,
                history.tx_type,
                history.date_processed,

                pharmacist.lic_number AS pharmacist_lic_number,

                pharmacy.name as pharmacy_name,
                pharmacy.nabp as pharmacy_nabp,
                pharmacy.address_1 as pharmacy_address_1,
                pharmacy.address_2 as pharmacy_address_2,
                pharmacy.city as pharmacy_city,
                pharmacy.state as pharmacy_state,
                pharmacy.zip_code as pharmacy_zip_code,
                pharmacy.phone as pharmacy_phone,
                pharmacy.tax_id as pharmacy_tax_id,
                pharmacy.npi as pharmacy_npi,

                user_info.username,
                user_info.initials,

                claim.claim_number,
                claim.policy_number,
                claim.status as claim_status,

                client.client_name as client_name,
                client.send_ca_state_reporting,
                client.send_fl_state_reporting,
                client.send_mg_state_reporting,
                client.send_or_state_reporting,
                client.send_tx_state_reporting,
                client.send_nc_state_reporting,
                client.tin as client_tin,
                client.insurer,
                client.insurer_tin,
                client.insurer_zip,
                client.wq_claim_number_required,
                client.wq_phcy_tax_id_required,
                client.wq_policy_number_required,
                client.wq_adjuster_required,
                client.wq_adjuster_inital_required,

                sr_carrier.state as carrier_state,
                sr_carrier.carrier_name,
                sr_carrier.carrier_fein,
                sr_carrier.carrier_zip,

                state_report_entry.sr_file_id as sr_file_id,

                patient.patient_id,
                patient.dob AS patient_dob,
                patient.ssn as patient_ssn,
                patient.first_name as patient_first_name,
                patient.last_name as patient_last_name,
                patient.address_1 as patient_address_1,
                patient.address_2 as patient_address_2,
                patient.city as patient_city,
                patient.state as patient_state,
                patient.zip_code as patient_zip_code,
                patient.jurisdiction as patient_jurisdiction,

                employer.tin as employer_tin,
                employer.name as employer_name,
                employer.city as employer_city,

                doctor.doctor_id,
                doctor.name AS doctor_name,

                drug.ndc_number AS drug_ndc_number,
                trans.trans_id,
                history.history_id,
                history.claim_id

             FROM ehistory
             LEFT JOIN client ON
                client.group_number = ehistory.group_number
             LEFT JOIN patient ON
                ehistory.patient_id = patient.patient_id
             LEFT JOIN claim ON
                ehistory.claim_id = claim.claim_id
             LEFT JOIN user_info ON
                claim.email1 = user_info.email
             LEFT JOIN pharmacy ON
                ehistory.pharmacy_id = pharmacy.pharmacy_id
             LEFT JOIN doctor ON
                ehistory.doctor_id = doctor.doctor_id
             LEFT JOIN employer ON
                COALESCE(claim.employer_tin, client.tin) = employer.tin
             LEFT JOIN drug ON
                ehistory.drug_id = drug.drug_id
             LEFT JOIN history ON
                ehistory.history_id = history.history_id
             LEFT JOIN pharmacist ON 
                history.pharmacist_id = pharmacist.pharmacist_id
             LEFT JOIN trans ON 
                history.history_id = trans.history_id
            LEFT JOIN soj ON
                patient.jurisdiction = soj.jurisdiction
            LEFT JOIN sr_carrier ON
               ehistory.group_number = sr_carrier.group_number AND
               soj.abbr = sr_carrier.state
            LEFT JOIN state_report_entry
                ON state_report_entry.trans_id = trans.trans_id
             WHERE
                ehistory.workqueue_candidate = TRUE
                AND ehistory.reverse_date IS NULL
                AND ehistory.group_number NOT IN ('70420', '70414', '70417', '80003')
                AND ((NOW() - ehistory.date_processed) < interval '90 days'
                  OR (
                    (send_ca_state_reporting = TRUE AND patient.jurisdiction = '07') OR
                    (send_or_state_reporting = TRUE AND patient.jurisdiction = '36') OR
                    (send_tx_state_reporting = TRUE AND patient.jurisdiction = '42') OR
                    (send_fl_state_reporting = TRUE AND patient.jurisdiction = '09'
                )))
             """)

        cursor.execute("""
            DELETE FROM working_claim
            USING mjoseph.group_info
            WHERE working_claim.group_number = mjoseph.group_info.group_number
            """)

    def drop_working_claim_table(self):
        cursor = R.db.log_cursor()
        cursor.execute("DROP TABLE working_claim")

JobClassManager = JobClassManager()

class qjob:
    job_count = 0

    def __init__(self, name, priority, query):
        self.name = name
        self.priority = priority
        self.query = query
        JobClassManager.add_jclass(self)

    def __call__(self):
        cursor = R.db.log_cursor()
        assert self.query, 'QueryJobClass %s must have query attr set' % self
        cursor.execute(self.query)

        keys = {}
        for rec in cursor:
            gn, ga, msg = rec[:3]
            if len(rec) == 3:
                priority = self.priority
            else:
                priority = rec[3]
            keys[(gn, ga)] = True
            WorkQueue.add(self.name, gn, ga, msg, priority)

        self.job_count = len(keys)
        WorkQueue.clear_except(self.name, keys)

###############################################################################
## Begin Job Definition

qjob("group_number_nof", 10, """
    SELECT group_number, group_auth,
           'Group # ' || group_number || ' not on file'
    FROM working_claim
    WHERE client_name IS NULL""")

qjob("unlinked_pa_number", 7, """
    SELECT 
        group_number, 
        group_auth, 
        'Unlinked Meadowbrook pa number'
    FROM working_claim
    WHERE group_number = '70036'
      AND claim_id IS NULL """)

#----------------------------------------------------------------

qjob("dp_in_future", 7, """
    SELECT group_number, group_auth, 
        'Date processed ' || to_char(date_processed, 'MM/DD/YYYY') || ' in future'
    from working_claim
    where date_processed > now()
""")

qjob("employer_nof", 7, """
    SELECT group_number, group_auth,
           'Employer not on file'
    FROM working_claim
    WHERE (
        (send_ca_state_reporting = TRUE AND patient_jurisdiction = '07') OR
        (send_or_state_reporting = TRUE AND patient_jurisdiction = '36') OR
        (send_tx_state_reporting = TRUE AND patient_jurisdiction = '42') OR
        (send_fl_state_reporting = TRUE AND patient_jurisdiction = '09')
       ) AND (employer_tin IS NULL)
       """)

qjob("client_name_nof", 7, """
    SELECT group_number, group_auth,
           'Employer name not on file'
    FROM working_claim
    WHERE (
        (send_ca_state_reporting = TRUE AND patient_jurisdiction = '07') OR
        (send_or_state_reporting = TRUE AND patient_jurisdiction = '36') OR
        (send_tx_state_reporting = TRUE AND patient_jurisdiction = '42') OR
        (send_fl_state_reporting = TRUE AND patient_jurisdiction = '09'))
        AND employer_tin IS Not NULL AND employer_name IS NULL
        """)

qjob("employer_address_nof", 7, """
    SELECT group_number, group_auth,
           'Employer address not on file'
    FROM working_claim
    WHERE (
        (send_ca_state_reporting = TRUE AND patient_jurisdiction = '07') OR
        (send_or_state_reporting = TRUE AND patient_jurisdiction = '36') OR
        (send_tx_state_reporting = TRUE AND patient_jurisdiction = '42') OR
        (send_fl_state_reporting = TRUE AND patient_jurisdiction = '09'))
        AND employer_tin IS Not NULL AND employer_name IS NULL
        """)
#----------------------------------------------------------------

qjob("pharmacy_npi_nof", 7, """
    SELECT group_number, group_auth,
            'Pharmacy NPI # not on file'
    FROM working_claim
    WHERE (
        (send_ca_state_reporting = TRUE AND patient_jurisdiction = '07') OR
        (send_or_state_reporting = TRUE AND patient_jurisdiction = '36') OR
        (send_tx_state_reporting = TRUE AND patient_jurisdiction = '42') OR
        (send_fl_state_reporting = TRUE AND patient_jurisdiction = '09')
       ) AND
       pharmacy_npi IS NULL""")

## Internal Accounting Jobs
qjob("trans_over_payment", 4, """
    SELECT trans.group_number, trans.group_auth,
           'Overpayment of ' || payment.amount - trans.total
    FROM trans
    JOIN (
        SELECT trans_id, SUM(trans_payment.amount) as amount
        FROM trans_payment
        GROUP BY trans_id
        ) AS payment USING(trans_id)
    WHERE payment.amount > trans.total
    """)

qjob("trans_duplicate_payment", 4, """
    SELECT group_number,
           group_auth,
           'Transaction has ' || cnt || ' duplicate ' ||
           'payments of ' || amount
    FROM (        
        SELECT group_number, group_auth, COUNT(*) AS cnt,
               amount, ptype_id, ref_no
        FROM trans_payment
        JOIN trans ON trans_payment.trans_id = trans.trans_id
        GROUP BY group_number, group_auth, amount, ptype_id, ref_no
        HAVING COUNT(*) > 1
    ) AS x""")

## Customer Billing Requirements Jobs

qjob("adjuster_nof", 9, """
     SELECT group_number, group_auth, 'Email not found in users'
     FROM working_claim
     WHERE wq_adjuster_required = TRUE AND 
           username IS NULL
     """)

qjob("adjuster_initials_nof", 9, """
    SELECT
        group_number, group_auth, 'Adjuster initials not on file'
    FROM working_claim
    WHERE wq_adjuster_inital_required = TRUE 
      AND initials IS NULL""")

qjob("policy_number_nof", 7, """
      SELECT group_number, group_auth, 'Policy # not on file'
      FROM working_claim
      WHERE policy_number IS NULL
        AND wq_policy_number_required = TRUE
      """)

qjob("claim_number_nof", 8, """
      SELECT group_number, group_auth, 'Claim # not on file'
      FROM working_claim
      WHERE claim_number IS NULL
        AND wq_claim_number_required = TRUE
      """)

qjob("pharmacy_tax_id_nof", 8, """
      SELECT group_number, group_auth, 'Pharmacy Tax ID# not on file'
      FROM working_claim
      WHERE pharmacy_tax_id IS NULL
        AND wq_phcy_tax_id_required = TRUE
      """)

## Client-specific one offs
qjob("59000_claim_number", 9, """
     SELECT group_number, group_auth,
            'Invalid NCIGA Claim # ' || COALESCE(claim_number, '')
     FROM working_claim 
     WHERE 
        group_number = '59000' AND
        COALESCE(claim_number, '') !~ '^W..-[0-9]{3,}$'""")

qjob("70076_claim_number", 9, """
     SELECT group_number, group_auth,
            'Invalid LIGA Claim # ' || COALESCE(claim_number, '')
     FROM working_claim 
     WHERE 
        group_number = '70076' AND
        COALESCE(claim_number, '') !~ '^[0-9]{2}-[0-9]{5}-[0-9]{6}-.+$' AND
        COALESCE(claim_number, '') !~ '^[0-9]{3}-[0-9]{5}-[0-9]{6}-.+$'
        """)

qjob("70020_uc_sfs_diff", 2, """
    SELECT group_number, group_auth, 
           'State Fee and U/C differ by ' || usual_customary - state_fee
    FROM working_claim
    WHERE (usual_customary - state_fee) > 5 AND
        group_number IN ('70017', '70014', '70020') AND
        pharmacy_nabp = '%s'
    """ % R.CPS_NABP_NBR)


if __name__ == '__main__':
    R.db.setup()
    WorkQueue.refresh()
