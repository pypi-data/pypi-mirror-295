
<%def name="select_post_contacts()">
CREATE TEMP TABLE teamsupport_patient_constraint AS
  SELECT patient.patient_id
  FROM patient
  JOIN client USING(group_number)
  WHERE client.teamsupport_org_id IS NOT NULL AND
        patient.status = 'A' AND
        patient.teamsupport_contact_id IS NULL;
</%def>

<%def name="select_put_contacts()">
CREATE TEMP TABLE teamsupport_patient_constraint AS
  SELECT patient.patient_id
  FROM patient
  JOIN client USING(group_number)
  WHERE client.teamsupport_org_id IS NOT NULL AND
        patient.teamsupport_contact_id IS NOT NULL AND
        patient.mtime > patient.teamsupport_update_time;
</%def>

<%def name="select_post_addresses()">
CREATE TEMP TABLE teamsupport_patient_constraint AS
  SELECT patient.patient_id
  FROM patient
  JOIN client USING(group_number)
  WHERE client.teamsupport_org_id IS NOT NULL AND
        patient.teamsupport_contact_id IS NOT NULL AND
        patient.teamsupport_address_id IS NULL AND
        patient.city IS NOT NULL;
</%def>

<%def name="select_put_addresses()">
    CREATE TEMP TABLE teamsupport_patient_constraint AS
      SELECT patient.patient_id
      FROM patient
      JOIN client USING(group_number)
      WHERE client.teamsupport_org_id IS NOT NULL AND
            patient.teamsupport_contact_id IS NOT NULL AND
            patient.teamsupport_address_id IS NOT NULL AND
            patient.mtime > patient.teamsupport_update_time;
</%def>

<%def name="fetch_patients()">
  CREATE TEMP TABLE teamsupport_patient AS
  SELECT client.teamsupport_org_id, 
       patient.patient_id,
       patient.teamsupport_contact_id,
       patient.teamsupport_address_id,
       patient.status,
       patient.first_name,
       patient.last_name,
       patient.group_number,
       patient.division_code,
       patient.dob,
       patient.ssn,
       patient.tin,
       CASE WHEN patient.sex='1' THEN 'M'
           WHEN patient.sex='2' THEN 'F'
           ELSE patient.sex
           END
           AS sex,
       patient.jurisdiction,
       patient.effective_date,
       patient.expiration_date,
       patient.address_1,
       patient.address_2,
       patient.city,
       patient.state,
       patient.zip_code
  FROM patient
  JOIN teamsupport_patient_constraint USING(patient_id)
  JOIN client USING(group_number);

  SELECT *
  FROM teamsupport_patient
  ORDER BY group_number, patient_id;
</%def>

<%def name="cleanup()">
  DROP TABLE teamsupport_patient_constraint;
  DROP TABLE teamsupport_patient;
</%def>

