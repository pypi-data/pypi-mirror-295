/* Discard duplicate update/inserts for the same key */
DELETE FROM doctor_key_feed WHERE doctor_key_feed_id NOT IN (
  SELECT MAX(doctor_key_feed_id) AS doctor_key_feed_id
  FROM doctor_key_feed
  GROUP BY doc_key);

INSERT INTO cobol.doctor_key (doctor_id, doc_key, modify_datetime)
  SELECT doctor_id::int as doctor_id, doc_key, modify_datetime
  FROM doctor_key_feed
  ON CONFLICT (doc_key) DO UPDATE SET
     doctor_id=EXCLUDED.doctor_id,
     modify_datetime=EXCLUDED.modify_datetime;


/* Set trans.doctor_id from DEA # */
UPDATE trans SET doctor_id=L.doctor_id::int
FROM doctor_key_feed as L
WHERE trans.doctor_dea_number = L.doc_key
    AND trans.doctor_id IS NULL;

/* Set trans.doctor_id from NPI # */
UPDATE trans SET doctor_id=L.doctor_id::int
FROM doctor_key_feed as L
WHERE trans.doctor_npi_number = L.doc_key
    AND trans.doctor_id IS NULL;

/* Set history.doctor_id from DEA # */
UPDATE history SET doctor_id=L.doctor_id::int
FROM doctor_key_feed as L
WHERE history.doctor_dea_number = L.doc_key
    AND history.doctor_id IS NULL;

/* Set history.doctor_id from NPI # */
UPDATE history SET doctor_id=L.doctor_id::int
FROM doctor_key_feed as L
WHERE history.doctor_npi_number = L.doc_key
    AND history.doctor_id IS NULL;

/* back populate history table with dea numbers from the doctor_key
 * table */
UPDATE history SET doctor_dea_number = K.doc_key
FROM doctor_key K, doctor_key_feed L
WHERE L.doctor_id::int = K.doctor_id
  AND history.doctor_id = K.doctor_id
  AND LENGTH(K.doc_key) = 9
  AND history.doctor_dea_number is null;

/* back populate history table with npi numbers from the doctor_key
 * table */
UPDATE history SET doctor_npi_number = K.doc_key
FROM doctor_key K, doctor_key_feed L
WHERE L.doctor_id::int = K.doctor_id
  AND history.doctor_id = K.doctor_id
  AND LENGTH(K.doc_key) = 10
  AND history.doctor_npi_number is null;
