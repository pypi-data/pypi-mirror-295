/* Requires a temp table named claim_load to exist */

/* Clean up records */
UPDATE claim_load SET expiration_date=NULL WHERE expiration_date IN ('000000', '');
UPDATE claim_load SET effective_date=NULL WHERE effective_date IN ('000000', '');
UPDATE claim_load SET injury_date=NULL WHERE injury_date IN ('000000', '');
UPDATE claim_load SET dob=NULL WHERE dob IN ('00000000', '');
UPDATE claim_load SET doctor_on_file_required = ' ' WHERE doctor_on_file_required is NULL;

UPDATE claim_load SET error_msg = 'Missing Injury Date' WHERE injury_date IS NULL;

/* Discard duplicate update/inserts for the same claims */
DELETE FROM claim_load WHERE claim_load_id NOT IN (
  SELECT MAX(claim_load_id)
  FROM claim_load
  GROUP BY group_nbr, cardholder_nbr, dob, injury_date);

/* Calculate the correct DOI due to century differences */
UPDATE claim_load SET doi=to_date_safe(claim_load.injury_date, 'YYMMDD');
UPDATE claim_load SET doi=doi - '100 years'::interval WHERE doi > NOW();

/* Assign patient ID's */
UPDATE claim_load SET patient_id=patient.patient_id
  FROM patient
  WHERE claim_load.error_msg IS NULL AND
        claim_load.group_nbr = patient.group_number AND
        claim_load.cardholder_nbr = patient.ssn AND
        to_date_safe(claim_load.dob, 'YYYYMMDD') = patient.dob;
UPDATE claim_load SET patient_id=patient.patient_id
  FROM patient
  WHERE claim_load.error_msg IS NULL AND
        claim_load.group_nbr = patient.group_number AND
        claim_load.cardholder_nbr = patient.ssn AND
        claim_load.doi IS NOT NULL AND
        claim_load.dob IS NULL AND patient.dob IS NULL;

UPDATE claim_load SET error_msg='Patient not on file'
  WHERE patient_id IS NULL;

-- Assign username
UPDATE claim_load SET username=user_info.username
  FROM user_info 
  WHERE user_info.email = claim_load.email_address1;

UPDATE claim_load SET username=user_info.username
  FROM user_info 
  WHERE claim_load.username IS NULL
    AND user_info.email = claim_load.email_address2;

insert into claim (
  patient_id, doi, claim_number, policy_number, status,
    ref_nbr_1, ref_nbr_2,
    effective_date, expiration_date, jurisdiction,
    injury_desc, employer_tin, doctor_on_file_required,
    ctime, username, email1, email2, keep_open)
SELECT 
    patient_id,
    doi,
    claim_nbr,
    policy_nbr,
    claim_status,
    reference_1,
    reference_2,
    to_date_safe(effective_date, 'YYMMDD'),
    to_date_safe(expiration_date, 'YYMMDD'),
    jurisdiction_code,
    injury_desc,
    employer_tin,
    doctor_on_file_required,
    NOW(),
    username,
    email_address1,
    email_address2,
    keep_open
FROM claim_load
WHERE error_msg IS NULL
  AND doi IS NOT NULL
ON CONFLICT (patient_id, doi) DO UPDATE SET
    claim_number=EXCLUDED.claim_number,
    policy_number=EXCLUDED.policy_number,
    status=EXCLUDED.status,
    ref_nbr_1=EXCLUDED.ref_nbr_1,
    ref_nbr_2=EXCLUDED.ref_nbr_2,
    effective_date=EXCLUDED.effective_date,
    expiration_date=EXCLUDED.expiration_date,
    jurisdiction=EXCLUDED.jurisdiction,
    injury_desc=EXCLUDED.injury_desc,
    employer_tin=EXCLUDED.employer_tin,
    doctor_on_file_required=EXCLUDED.doctor_on_file_required,
    mtime=NOW(),
    username=EXCLUDED.username,
    email1=EXCLUDED.email1,
    email2=EXCLUDED.email2,
    keep_open=EXCLUDED.keep_open;

