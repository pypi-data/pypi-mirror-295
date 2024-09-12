DELETE FROM hit_feed WHERE group_nbr NOT IN
  (SELECT group_number FROM group_info
   UNION
   SELECT group_number FROM mjoseph.group_info
   UNION
   SELECT group_number FROM sunrise.group_info
   UNION
   SELECT group_number FROM msq.group_info);

ALTER TABLE hit_feed ADD COLUMN process_timestamp varchar(17);
UPDATE hit_feed SET process_timestamp=process_date || ' ' || process_time;

ALTER TABLE hit_feed ADD COLUMN patient_id BIGINT;
UPDATE hit_feed SET patient_id=patient.patient_id
  FROM patient
  WHERE hit_feed.group_nbr = patient.group_number
    AND hit_feed.pat_cardholder_nbr = patient.ssn
    AND hit_feed.pat_dob = to_char(patient.dob, 'YYYYMMDD');

ALTER TABLE hit_feed ADD COLUMN drug_id BIGINT;
UPDATE hit_feed SET drug_id=drug.drug_id
  FROM drug
  WHERE hit_feed.ndc_nbr = drug.ndc_number;

ALTER TABLE hit_feed ADD COLUMN doi DATE;
UPDATE hit_feed SET doi=to_date_safe(substring(prior_auth_nbr from 3), 'YYMMDD')
  WHERE prior_auth_nbr ~ E'^\\d{8}$';

UPDATE hit_feed SET doi = doi - '100 years'::interval
  WHERE doi > now();

ALTER TABLE hit_feed ADD COLUMN rx_date DATE;
UPDATE hit_feed SET doi=to_date_safe(date_filled, 'YYYYMMDD')
  WHERE date_filled ~ E'^\\d{8}$';

ALTER TABLE hit_feed ADD COLUMN claim_id BIGINT;
UPDATE hit_feed SET claim_id=claim.claim_id
  FROM claim
  WHERE hit_feed.patient_id = claim.patient_id
    AND hit_feed.doi = claim.doi;

ALTER TABLE hit_feed ADD COLUMN pharmacy_id BIGINT;
UPDATE hit_feed SET pharmacy_id=pharmacy.pharmacy_id
  FROM pharmacy
  WHERE pharmacy.nabp = hit_feed.phcy_nabp;

ALTER TABLE hit_feed ADD COLUMN history_id BIGINT;
UPDATE hit_feed SET history_id=history.history_id
  FROM history
  WHERE hit_feed.group_nbr = history.group_number
    AND hit_feed.claim_ref_nbr::int = history.group_auth;

ALTER TABLE hit_feed ADD COLUMN hit_id_int BIGINT;
UPDATE hit_feed SET hit_id_int=hit_id::int;

UPDATE hit SET
    record_type=L.record_type,
    process_timestamp=regexp_replace(L.process_timestamp,
        '^(.{4})(.{2})(.{2}) (.{2})(.{2})(.{2})(.{2})$',
        '\1-\2-\3 \4:\5:\6.\7')::timestamp, 
    source=L.source,
    phcy_name=L.phcy_name,
    phcy_city=L.phcy_city,
    phcy_state=L.phcy_state,
    phcy_nabp=L.phcy_nabp,
    phcy_npi=L.phcy_npi,
    group_nbr=L.group_nbr,
    group_desc=L.group_desc,
    claim_ref_nbr=L.claim_ref_nbr::int,
    rx_nbr=L.rx_nbr::bigint,
    refill_nbr=L.refill_nbr::int,
    pat_dob=L.pat_dob,
    pat_cardholder_nbr=L.pat_cardholder_nbr,
    pat_first_name=L.pat_first_name,
    pat_last_name=L.pat_last_name,
    pat_special_id=L.pat_special_id,
    ndc_nbr=L.ndc_nbr,
    drug_name=L.drug_name,
    qty=L.qty,
    days_supply=L.days_supply,
    sponsor_cost=L.sponsor_cost,
    dispense_fee=L.dispense_fee,
    sales_tax=L.sales_tax,
    copay=L.copay,
    usual_customary=L.usual_customary,
    state_fee=L.state_fee,
    awp=L.awp,
    processor_fee=L.processor_fee,
    msg1=L.msg1,
    msg2=L.msg2,
    response_code=L.response_code,
    prior_auth_nbr=L.prior_auth_nbr,
    access_code=L.access_code,
    doctor_id=L.doctor_id,
    date_filled=L.date_filled,
    adjuster1_email=L.adjuster1_email,
    paladin_review=L.paladin_review,
    patient_id=L.patient_id,
    drug_id=L.drug_id,
    claim_id=L.claim_id,
    pharmacy_id=L.pharmacy_id,
    history_id=L.history_id,
    doi=L.doi,
    level_of_effort=L.level_of_effort,
    bin=L.bin,
    trans_code=L.trans_code,
    person_code=L.person_code,
    sex=L.sex,
    relationship=cast(nullif(L.relationship, '') as smallint),
    compound_code=cast(nullif(L.compound_code, '') as smallint),
    disp_as_written=L.disp_as_written,
    doctor_last_name=L.doctor_last_name,
    doctor_first_name=L.doctor_first_name,
    doctor_address=L.doctor_address,
    doctor_city=L.doctor_city,
    doctor_state=L.doctor_state,
    doctor_zip_code=L.doctor_zip_code,
    doctor_telephone=L.doctor_telephone,
    refills_authorized=cast(nullif(L.refills_authorized, '') as smallint),
    other_payer_paid_amt=cast(nullif(L.other_payer_paid_amt, '') as numeric),
    dur_intervention=L.dur_intervention,
    pharmacist_id_qualifier=L.pharmacist_id_qualifier,
    pharmacist_id=L.pharmacist_id,
    patient_paid_amt=cast(nullif(L.patient_paid_amt, '') as numeric),
    place_of_service=L.place_of_service,
    pat_residence_code=L.pat_residence_code,
    prescribed_qty=cast(nullif(L.prescribed_qty, '') as numeric),
    gross_amt_due=cast(nullif(L.gross_amt_due, '') as numeric),
    rts=L.rts,
    reject_code_2=L.reject_code_2,
    cost_submitted=to_numeric(L.cost_submitted),
    fee_submitted=to_numeric(l.fee_submitted),
    mtime=NOW(),
    date_written=L.date_written
FROM hit_feed AS L
WHERE hit.hit_id = L.hit_id_int;

INSERT INTO hit (
    hit_id, record_type, process_timestamp, source, phcy_name, phcy_city,
    phcy_state, phcy_nabp, phcy_npi, group_nbr, group_desc, claim_ref_nbr,
    rx_nbr, refill_nbr, pat_dob, pat_cardholder_nbr, pat_first_name,
    pat_last_name, pat_special_id, ndc_nbr, drug_name, qty, days_supply,
    sponsor_cost, dispense_fee, sales_tax, copay, usual_customary,
    state_fee, awp, processor_fee, msg1, msg2, response_code,
    prior_auth_nbr, access_code, doctor_id, date_filled, adjuster1_email,
    paladin_review, patient_id, drug_id, claim_id, pharmacy_id, history_id,
    doi, level_of_effort,
    bin,
    trans_code,
    person_code,
    sex,
    relationship,
    compound_code,
    disp_as_written,
    doctor_last_name,
    doctor_first_name,
    doctor_address,
    doctor_city,
    doctor_state,
    doctor_zip_code,
    doctor_telephone,
    refills_authorized,
    other_payer_paid_amt,
    dur_intervention,
    pharmacist_id_qualifier,
    pharmacist_id,
    patient_paid_amt,
    place_of_service,
    pat_residence_code,
    prescribed_qty,
    gross_amt_due,
    rts,
    reject_code_2,
    cost_submitted,
    fee_submitted,
    date_written,
    ctime
)
SELECT
    hit_id_int, record_type,
    regexp_replace(process_timestamp,
        '^(.{4})(.{2})(.{2}) (.{2})(.{2})(.{2})(.{2})$',
        '\1-\2-\3 \4:\5:\6.\7')::timestamp,
    source, phcy_name, phcy_city, phcy_state, phcy_nabp, phcy_npi,
    group_nbr, group_desc, claim_ref_nbr::int, rx_nbr::bigint,
    refill_nbr::int, pat_dob, pat_cardholder_nbr, pat_first_name,
    pat_last_name, pat_special_id, ndc_nbr, drug_name, qty, days_supply,
    sponsor_cost, dispense_fee, sales_tax, copay, usual_customary,
    state_fee, awp, processor_fee, msg1, msg2, response_code,
    prior_auth_nbr, access_code, doctor_id, date_filled, adjuster1_email,
    paladin_review, patient_id, drug_id, claim_id, pharmacy_id, history_id,
    doi, level_of_effort,
    bin,
    trans_code,
    person_code,
    sex,
    cast(nullif(relationship, '') as smallint),
    cast(nullif(compound_code, '') as smallint),
    disp_as_written,
    doctor_last_name,
    doctor_first_name,
    doctor_address,
    doctor_city,
    doctor_state,
    doctor_zip_code,
    doctor_telephone,
    cast(nullif(refills_authorized, '') as smallint),
    cast(nullif(other_payer_paid_amt, '') as numeric),
    dur_intervention,
    pharmacist_id_qualifier,
    pharmacist_id,
    cast(nullif(patient_paid_amt, '') as numeric),
    place_of_service,
    pat_residence_code,
    cast(nullif(prescribed_qty, '') as numeric),
    cast(nullif(gross_amt_due, '') as numeric),
    rts,
    reject_code_2,
    to_numeric(cost_submitted),
    to_numeric(fee_submitted),
    date_written,
    NOW()
FROM hit_feed
WHERE NOT EXISTS (
  SELECT 1
  FROM hit
  WHERE hit_feed.hit_id_int = hit.hit_id
);

DROP TABLE hit_feed;
