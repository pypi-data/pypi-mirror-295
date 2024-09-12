
ALTER TABLE reject_feed ADD COLUMN patient_id BIGINT;
UPDATE reject_feed SET patient_id=patient.patient_id
  FROM patient
  WHERE reject_feed.group_nbr = patient.group_number
    AND reject_feed.cardholder_id = patient.ssn
    AND reject_feed.birth_date = to_char(patient.dob, 'YYYYMMDD');

/* Drug */
ALTER TABLE reject_feed ADD COLUMN drug_id BIGINT;
UPDATE reject_feed SET drug_id=drug.drug_id
  FROM drug
  WHERE reject_feed.ndc_nbr = drug.ndc_number;

/* Date Filled */
ALTER TABLE reject_feed ADD COLUMN date_filled_ts TIMESTAMP;
UPDATE reject_feed SET date_filled_ts=
  to_timestamp(date_filled_timestamp,
        'YYMMDDHH24MISSMS');


/* Hit ID */
ALTER TABLE reject_feed ADD COLUMN hit_id BIGINT;
UPDATE reject_feed SET hit_id=reject_hits_number::bigint
  WHERE reject_hits_number ~ E'^\\d+$';

ALTER TABLE reject_feed ADD COLUMN pharmacy_id BIGINT;
UPDATE reject_feed SET pharmacy_id=pharmacy.pharmacy_id
  FROM pharmacy
  WHERE pharmacy.nabp = reject_feed.nabp;

ALTER TABLE reject_feed ADD COLUMN reject_ts TIMESTAMP;
UPDATE reject_feed SET reject_ts=regexp_replace(reject_timestamp,
        '^(.{4})(.{2})(.{2})(.{2})(.{2})(.{2})(.{2})$',
        '\1-\2-\3 \4:\5:\6.\7')::timestamp;

UPDATE reject_feed SET rx_nbr='' WHERE rx_nbr IS NULL;
UPDATE reject_feed SET nabp='' WHERE nabp IS NULL;

INSERT INTO reject (
  reject_timestamp, nabp, date_filled_timestamp, rx_nbr, version, group_nbr,
  cardholder_id, birth_date, sex, new_refill, qty, days_supply, compound_code,
  ndc_nbr, disp_as_written, cost, doctor_dea_nbr, date_written, authorized,
  denial_override, usual_customary, fee, sales_tax, prior_auth_nbr,
  metric_quantity, doctor_name, doctor_street, doctor_city, doctor_state,
  doctor_zip_code, carrier_id, wc_claim_nbr, reject_nbr, reject_code1, reject_code2,
  reject_message, reject_additional1, reject_additional2, reject_additional3,
  reject_additional4, reject_hits_number, patient_id, drug_id, pharmacy_id,
  hit_id, rts_sequence
)
SELECT
  reject_ts, nabp, date_filled_ts, rx_nbr, version, group_nbr,
  cardholder_id, birth_date, sex, new_refill, qty, days_supply, compound_code,
  ndc_nbr, disp_as_written, cost, doctor_dea_nbr, date_written, authorized,
  denial_override, usual_customary, fee, sales_tax, prior_auth_nbr,
  metric_quantity, doctor_name, doctor_street, doctor_city, doctor_state,
  doctor_zip_code, carrier_id, wc_claim_nbr, reject_nbr, reject_code1, reject_code2,
  reject_message, reject_additional1, reject_additional2, reject_additional3,
  reject_additional4, hit_id, patient_id, drug_id, pharmacy_id,
  hit_id, rts_sequence
FROM reject_feed
ON CONFLICT(nabp, date_filled_timestamp, rx_nbr) DO UPDATE SET
    version=EXCLUDED.version,
    group_nbr=EXCLUDED.group_nbr,
    cardholder_id=EXCLUDED.cardholder_id,
    birth_date=EXCLUDED.birth_date,
    sex=EXCLUDED.sex,
    new_refill=EXCLUDED.new_refill,
    qty=EXCLUDED.qty,
    days_supply=EXCLUDED.days_supply,
    compound_code=EXCLUDED.compound_code,
    ndc_nbr=EXCLUDED.ndc_nbr,
    disp_as_written=EXCLUDED.disp_as_written,
    cost=EXCLUDED.cost,
    doctor_dea_nbr=EXCLUDED.doctor_dea_nbr,
    date_written=EXCLUDED.date_written,
    authorized=EXCLUDED.authorized,
    denial_override=EXCLUDED.denial_override,
    usual_customary=EXCLUDED.usual_customary,
    fee=EXCLUDED.fee,
    sales_tax=EXCLUDED.sales_tax,
    prior_auth_nbr=EXCLUDED.prior_auth_nbr,
    metric_quantity=EXCLUDED.metric_quantity,
    doctor_name=EXCLUDED.doctor_name,
    doctor_street=EXCLUDED.doctor_street,
    doctor_city=EXCLUDED.doctor_city,
    doctor_state=EXCLUDED.doctor_state,
    doctor_zip_code=EXCLUDED.doctor_zip_code,
    carrier_id=EXCLUDED.carrier_id,
    wc_claim_nbr=EXCLUDED.wc_claim_nbr,
    reject_nbr=EXCLUDED.reject_nbr,
    reject_code1=EXCLUDED.reject_code1,
    reject_code2=EXCLUDED.reject_code2,
    reject_message=EXCLUDED.reject_message,
    reject_additional1=EXCLUDED.reject_additional1,
    reject_additional2=EXCLUDED.reject_additional2,
    reject_additional3=EXCLUDED.reject_additional3,
    reject_additional4=EXCLUDED.reject_additional4,
    reject_hits_number=EXCLUDED.reject_hits_number,
    modify_timestamp=NOW(),
    patient_id=EXCLUDED.patient_id,
    drug_id=EXCLUDED.drug_id,
    pharmacy_id=EXCLUDED.pharmacy_id,
    hit_id=EXCLUDED.hit_id,
    rts_sequence=EXCLUDED.rts_sequence;
