
/* Add working columns to the feed table */
ALTER TABLE history_feed ADD COLUMN doctor_dea_number varchar(9);
ALTER TABLE history_feed ADD COLUMN doctor_npi_number varchar(10);
ALTER TABLE history_feed ADD COLUMN history_id bigint;
ALTER TABLE history_feed ADD COLUMN patient_id bigint;
ALTER TABLE history_feed ADD COLUMN pharmacy_id bigint;
ALTER TABLE history_feed ADD COLUMN doctor_id bigint;
ALTER TABLE history_feed ADD COLUMN drug_id bigint;
ALTER TABLE history_feed ADD COLUMN claim_id bigint;
ALTER TABLE history_feed ADD COLUMN error_msg TEXT;

/* Get previous error records to reprocess */
INSERT INTO history_feed SELECT * FROM history_feed_error;

/* clear out the errors on the feed error table so we can try again.
 * this wasn't being done for a very long time so history records
 * could never get fixed
 */
UPDATE history_feed set error_msg = NULL where error_msg is not null;

/* Setup pkey */
CREATE TEMPORARY SEQUENCE history_feed_seq;
ALTER TABLE history_feed ADD COLUMN history_feed_id INT;

/* populate primary key */
UPDATE history_feed SET history_feed_id = nextval('history_feed_seq');

/* Forget the ones that don't have valid group numbers like EHO's patient
 * records. */
DELETE FROM history_feed WHERE group_nbr NOT IN
    (SELECT group_number FROM client
     UNION
     SELECT group_number FROM mjoseph.group_info);

/* Validate records */
UPDATE history_feed
  SET error_msg='Missing Group' WHERE group_nbr IS NULL;
UPDATE history_feed
  SET error_msg='Missing Claim Ref #' WHERE auth_nbr IS NULL;

/* Clean up records */
UPDATE history_feed SET reversal_date=NULL WHERE reversal_date='000000';
UPDATE history_feed SET birth_date=NULL WHERE birth_date='00000000';

/* Discard duplicate update/inserts for the same history records */
DELETE FROM history_feed WHERE history_feed_id NOT IN (
  SELECT MAX(history_feed_id) AS history_feed_id
  FROM history_feed
  GROUP BY group_nbr, auth_nbr);

/* Assign doctor keys. The doctor_dea field has dea numbers
   and npi numbers in it, so we split them apart.*/
UPDATE history_feed SET doctor_dea_number=doctor_dea
WHERE length(doctor_dea) = 9;

UPDATE history_feed SET doctor_npi_number=doctor_dea
WHERE length(doctor_dea) = 10;

/* Assign the NPI for records that gave us a DEA */
UPDATE history_feed SET doctor_npi_number=doctor_xref.npi
FROM doctor_xref
WHERE history_feed.doctor_dea_number = doctor_xref.dea;

/* Assign the DEA for records that gave us a NPI */
UPDATE history_feed SET doctor_dea_number=doctor_xref.dea
FROM doctor_xref
WHERE history_feed.doctor_npi_number = doctor_xref.npi;

UPDATE history_feed SET error_msg = 'Invalid Birth Date ' || birth_date
WHERE to_date_safe(history_feed.birth_date, 'YYYYMMDD') IS NULL;

UPDATE history_feed SET error_msg = 'Invalid date filled ' || datef
WHERE to_date_safe(history_feed.datef, 'YYMMDD') IS NULL;

UPDATE history_feed SET error_msg = 'Invalid date written ' || date_written
WHERE to_date_safe(history_feed.date_written, 'YYMMDD') IS NULL;

UPDATE history_feed SET error_msg = 'Invalid date processed ' || date_processed || time_processed
WHERE to_timestamp_safe(date_processed || time_processed, 'YYMMDDHH24MISS') IS NULL;

/* Assign Foreign Keys */
UPDATE history_feed SET patient_id=patient.patient_id
  FROM patient
  WHERE history_feed.error_msg is NULL AND
        history_feed.group_nbr = patient.group_number AND
        history_feed.cardholder_nbr = patient.ssn AND
        to_date_safe(history_feed.birth_date, 'YYYYMMDD') = patient.dob;
UPDATE history_feed SET patient_id=patient.patient_id
  FROM patient
  WHERE history_feed.error_msg is NULL AND
        history_feed.group_nbr = patient.group_number AND
        history_feed.cardholder_nbr = patient.ssn AND
        history_feed.birth_date IS NULL AND patient.dob IS NULL;

UPDATE history_feed SET drug_id=drug.drug_id
  FROM drug
  WHERE drug.ndc_number = history_feed.ndc_nbr;

UPDATE history_feed SET pharmacy_id=pharmacy.pharmacy_id
  FROM pharmacy
  WHERE history_feed.pharmacy = pharmacy.nabp;

UPDATE history_feed SET doctor_id=cobol.doctor_key.doctor_id
  FROM cobol.doctor_key
  WHERE history_feed.doctor_dea = cobol.doctor_key.doc_key;

UPDATE history_feed SET claim_id=claim.claim_id
  FROM claim
  WHERE history_feed.patient_id=claim.claim_id AND
        to_date_safe(substring(history_feed.prior_auth_nbr FROM 3), 'YYYYMMDD') = claim.doi;

/* Validate foreign keys */
UPDATE history_feed SET error_msg = 'Patient not on file ' || coalesce(group_nbr, '') || '-' ||
        coalesce(cardholder_nbr, '') || '-' ||
        coalesce(birth_date, '')
WHERE patient_id IS NULL;

UPDATE history_feed SET error_msg = 'Drug not on file ' || ndc_nbr
WHERE drug_id IS NULL;

UPDATE history_feed SET error_msg = 'Pharmacy not on file'
WHERE pharmacy_id IS NULL;

/* Assign History ID's for us to update */
UPDATE history_feed SET history_id=history.history_id
  FROM history
  WHERE history_feed.error_msg IS NULL AND
        history_feed.group_nbr = history.group_number AND
        to_number(history_feed.auth_nbr, '9999999') = history.group_auth;

/* Perform Update */    
UPDATE history SET
    patient_id = L.patient_id,
    pharmacy_id = L.pharmacy_id,
    doctor_id = L.doctor_id,
    drug_id = L.drug_id,
    doi = substring(L.prior_auth_nbr from 3),
    rx_date = to_date_safe(L.datef, 'YYMMDD'),
    rx_number = to_number(L.rx_nbr, '9999999'),
    date_written = to_date_safe(L.date_written, 'YYMMDD'),
    daw = L.disp_as_written,
    quantity = to_number(L.qty, '99999999')/1000,
    days_supply = to_number(L.days_supply, '9999'),
    compound_code = L.compound_code,
    refill_number = to_number(L.refill_nbr, '99'),
    cost_allowed = to_number(L.cost_allowed, '99999999')/100,
    dispense_fee = to_number(L.fee, '99999999')/100,
    sales_tax = to_number(L.sales_tax, '99999999')/100,
    eho_network_copay = to_number(L.copay, '99999999')/100,
    cost_submitted = to_number(L.cost_submitted, '99999999')/100,
    processing_fee = coalesce(to_number(L.process_fee, '9999')/100, 0),
    usual_customary = to_number(L.total_submitted, '99999999')/100,
    date_processed = to_timestamp(L.date_processed || L.time_processed, 'YYMMDDHH24MISS'),
    reverse_date = to_date_safe(L.reversal_date, 'YYMMDD'),
    doctor_dea_number = L.doctor_dea_number,
    doctor_npi_number = L.doctor_npi_number,
    inv_class = L.wc_invoice_class,
    level_of_effort = L.level_of_effort,
    mtime=NOW()
  FROM history_feed as L
  WHERE L.error_msg IS NULL AND
      L.history_id = history.history_id;

/* Perform Insert */
INSERT INTO history (
    group_number, group_auth, patient_id, pharmacy_id, doctor_id, drug_id, doi,
    rx_date, rx_number, date_written, daw, quantity, days_supply,
    compound_code, refill_number, cost_submitted, cost_allowed, dispense_fee,
    sales_tax, eho_network_copay, processing_fee, usual_customary,
    date_processed, reverse_date, doctor_dea_number, doctor_npi_number, inv_class,
    level_of_effort, ctime)
SELECT 
    L.group_nbr,
    to_number(L.auth_nbr, '9999999'),
    L.patient_id,
    L.pharmacy_id,
    L.doctor_id,
    L.drug_id,
    substring(L.prior_auth_nbr FROM 3),
    to_date_safe(L.datef, 'YYMMDD'),
    to_number(L.rx_nbr, '9999999'),
    to_date_safe(L.date_written, 'YYMMDD'),
    L.disp_as_written,
    to_number(L.qty, '99999999')/1000,
    to_number(L.days_supply, '9999'),
    L.compound_code,
    to_number(L.refill_nbr, '99'),
    to_number(L.cost_submitted, '99999999')/100,
    to_number(L.cost_allowed, '99999999')/100,
    to_number(L.fee, '99999999')/100,
    to_number(L.sales_tax, '99999999')/100,
    to_number(L.copay, '99999999')/100,
    coalesce(to_number(L.process_fee, '9999')/100, 0),
    to_number(L.total_submitted, '99999999')/100,
    to_timestamp(L.date_processed || L.time_processed, 'YYMMDDHH24MISS'),
    to_date_safe(L.reversal_date, 'YYMMDD'),
    L.doctor_dea_number,
    L.doctor_npi_number,
    L.wc_invoice_class,
    level_of_effort,
    NOW()
FROM history_feed as L
WHERE L.error_msg IS NULL AND L.history_id IS NULL;

/* Put the bad records back into the error table */
ALTER TABLE history_feed DROP COLUMN history_feed_id;
TRUNCATE history_feed_error;

INSERT INTO history_feed_error
  SELECT * FROM history_feed WHERE error_msg IS NOT NULL;

DROP SEQUENCE history_feed_seq;
/*
vim: filetype=sqlpostgres
*/
