/* Validate records */
UPDATE stage.address_feed
  SET error_msg='Missing group_number'
  WHERE group_number IS NULL;
UPDATE stage.address_feed
  SET error_msg='Missing ssn'
  WHERE error_msg IS NULL AND ssn IS NULL;

/* Clean up records */
UPDATE stage.address_feed SET dob=NULL WHERE dob='00000000';

/* Discard duplicate update/inserts for the same patients */
DELETE FROM stage.address_feed WHERE address_feed_id NOT IN (
  SELECT MAX(address_feed_id) AS address_feed_id
  FROM stage.address_feed
  GROUP BY group_number, dob, ssn);

/* Assign patient ID's for us to update */
UPDATE stage.address_feed SET patient_id=patient.patient_id
  FROM patient
  WHERE stage.address_feed.error_msg IS NULL AND
        stage.address_feed.group_number = patient.group_number AND
        stage.address_feed.ssn = patient.ssn AND
        to_date(stage.address_feed.dob, 'YYYYMMDD') = patient.dob;
UPDATE stage.address_feed SET patient_id=patient.patient_id
  FROM patient
  WHERE stage.address_feed.error_msg IS NULL AND
        stage.address_feed.group_number = patient.group_number AND
        stage.address_feed.ssn = patient.ssn AND
        stage.address_feed.dob IS NULL AND patient.dob IS NULL;

/* Mark off which addresses have actually changed */
UPDATE stage.address_feed SET address_changed = TRUE
  FROM patient
  WHERE address_feed.patient_id = patient.patient_id AND (
      COALESCE(patient.address_1, '') != address_feed.address_1 OR
      COALESCE(patient.address_2, '') != address_feed.address_2 OR
      COALESCE(patient.city, '') != address_feed.city OR
      COALESCE(patient.state, '') != address_feed.state OR
      COALESCE(patient.zip_code, '') != address_feed.zip_code);

/* Perform Update */    
UPDATE patient SET
    address_1=L.address_1,
    address_2=L.address_2,
    city=L.city,
    state=L.state,
    zip_code=L.zip_code,
    phone=L.phone,
    mtime=NOW()
  FROM stage.address_feed as L
  WHERE L.error_msg IS NULL AND
      L.patient_id = patient.patient_id;

/* Clear out old geocodes for when the address has changed */
UPDATE patient SET geog=NULL, latitude=NULL, longitude=NULL,
                   failed_geocode=FALSE
  FROM stage.address_feed AS L
  WHERE L.patient_id = patient.patient_id AND
        L.address_changed = TRUE;

/* Mark all the ones with missing patient id's as errors */
UPDATE stage.address_feed SET error_msg='Patient key not found'
WHERE patient_id IS NULL;

/* Clean out all of the records that we have loaded */
DELETE FROM stage.address_feed WHERE error_msg IS NULL RETURNING *;
