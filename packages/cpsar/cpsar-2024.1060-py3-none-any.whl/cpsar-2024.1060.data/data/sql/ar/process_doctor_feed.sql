/* Discard duplicate update/inserts for the same doctors */
DELETE FROM doctor_feed WHERE doctor_feed_id NOT IN (
  SELECT MAX(doctor_feed_id) AS doctor_feed_id
  FROM doctor_feed
  GROUP BY doctor_id);

UPDATE cobol.doctor SET
    modify_datetime=L.modify_datetime,
    name=L.name,
    status=L.status,
    bac=L.bac,
    bac_description=L.bac_description,
    drug_schedule=L.drug_schedule,
    expiration_date=L.expiration_date,
    address_1=L.address_1,
    address_2=L.address_2,
    address_3=L.address_3,
    city=L.city,
    state=L.state,
    zip_code=L.zip_code,
    phone=L.phone,
    specialty=L.specialty,
    med_school=L.med_school,
    graduation_yr=L.graduation_yr
FROM doctor_feed AS L
WHERE cobol.doctor.doctor_id=L.doctor_id::int;


INSERT INTO cobol.doctor (
    doctor_id,
    modify_datetime,
    name,
    status,
    bac,
    bac_description,
    drug_schedule,
    expiration_date,
    address_1,
    address_2,
    address_3,
    city,
    state,
    zip_code,
    phone,
    specialty,
    med_school,
    graduation_yr)
SELECT 
    doctor_id::int,
    modify_datetime,
    name,
    status,
    bac,
    bac_description,
    drug_schedule,
    expiration_date,
    address_1,
    address_2,
    address_3,
    city,
    state,
    zip_code,
    phone,
    specialty,
    med_school,
    graduation_yr
FROM doctor_feed
WHERE doctor_id::int NOT IN (
    SELECT doctor_id
    FROM cobol.doctor);

