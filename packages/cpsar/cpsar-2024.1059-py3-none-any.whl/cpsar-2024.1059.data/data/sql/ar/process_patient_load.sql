
/* Validate records */
UPDATE patient_load SET error_msg='Missing ssn' WHERE ssn IS NULL;

/* Clean up records */
UPDATE patient_load SET expiration_date=NULL
    WHERE expiration_date='000000' OR expiration_date='';
UPDATE patient_load SET effective_date=NULL
    WHERE effective_date='000000' OR effective_date='';
UPDATE patient_load SET dob=NULL WHERE dob='00000000';

UPDATE patient_load SET
  dob = replace(dob, ' ', '0'),
  effective_date = replace(effective_date, ' ', '0'),
  expiration_date = replace(expiration_date, ' ', '0');

/* Assign patient ID's for us to update */
UPDATE patient_load SET patient_id=patient.patient_id
  FROM patient
  WHERE patient_load.error_msg IS NULL AND
        patient_load.group_number = patient.group_number AND
        patient_load.ssn = patient.ssn AND
        to_date(patient_load.dob, 'YYYYMMDD') = patient.dob;
UPDATE patient_load SET patient_id=patient.patient_id
  FROM patient
  WHERE patient_load.error_msg IS NULL AND
        patient_load.group_number = patient.group_number AND
        patient_load.ssn = patient.ssn AND
        patient_load.dob IS NULL AND patient.dob IS NULL;

/* Clear out old geocodes for when the address has changed */
UPDATE patient SET geog=NULL, latitude=NULL, longitude=NULL,
                   failed_geocode=FALSE
  FROM patient_load AS L
  WHERE L.error_msg IS NULL AND
      L.patient_id = patient.patient_id AND
      geog IS NOT NULL AND (
      patient.address_1 != L.address_1 OR
      patient.address_2 != L.address_2 OR
      patient.city != L.city OR
      patient.state != L.state OR
      patient.zip_code != L.zip_code);

/* Perform Insert */
INSERT INTO patient (
    first_name, last_name, name, ssn, dob, group_number, division_code,
    status, tin, address_1, address_2, city, state, zip_code, phone,
    sex, jurisdiction, effective_date, expiration_date,
    uses_group_formulary, phcy_message_sw, print_card, ctime, add_date, source,
    allow_n_drug)
SELECT 
    first_name, last_name, first_name || ' ' || last_name, ssn,
    to_date_safe(dob, 'YYYYMMDD') AS dob,
    group_number, division_code, status, tin, address_1, address_2,
    city, state, zip_code, phone, sex, jurisdiction,
    to_date_safe(effective_date, 'YYMMDD') AS effective_date,
    to_date_safe(expiration_date, 'YYMMDD') AS expiration_date,
    case when uses_group_formulary = 'Y' then true else false end,
    phcy_message_sw, print_card, now(),
    to_date_safe(L.add_date, 'YYMMDD'), L.source,
    case when allow_n_drug = 'Y' then true else false end
FROM patient_load as L
WHERE L.error_msg IS NULL
ON CONFLICT ON CONSTRAINT patient_group_number_ssn_dob_key DO UPDATE SET
    first_name = EXCLUDED.first_name,
    last_name = EXCLUDED.last_name,
    division_code = EXCLUDED.division_code,
    status = EXCLUDED.status,
    tin = EXCLUDED.tin,
    address_1 = EXCLUDED.address_1,
    address_2 = EXCLUDED.address_2,
    city = EXCLUDED.city,
    state = EXCLUDED.state,
    zip_code = EXCLUDED.zip_code,
    phone = EXCLUDED.phone,
    sex = EXCLUDED.sex,
    jurisdiction = EXCLUDED.jurisdiction,
    effective_date = EXCLUDED.effective_date,
    expiration_date = EXCLUDED.expiration_date,
    uses_group_formulary = EXCLUDED.uses_group_formulary,
    phcy_message_sw = EXCLUDED.phcy_message_sw,
    print_card = EXCLUDED.print_card,
    mtime = NOW(),
    source = EXCLUDED.source,
    allow_n_drug = EXCLUDED.allow_n_drug
;

/* Populate patient_id's on the patient_tag table */
UPDATE patient_tag SET patient_id=p.patient_id
FROM patient p
WHERE p.group_number = patient_tag.group_number
  AND p.ssn = patient_tag.ssn
  AND to_char(p.dob, 'YYYYMMDD') = patient_tag.dob
  AND (patient_tag.patient_id IS NULL
       OR patient_tag.patient_id != p.patient_id);

