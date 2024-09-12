select
       patient.group_number,
       patient.first_name,
       patient.last_name,
       to_char(patient.dob, 'YYYYMMDD'),
       patient.ssn,
       to_char(patient.effective_date, 'YYYYMMDD'),
       to_char(patient.expiration_date, 'YYYYMMDD'),
       claim.email1 as adjuster_email,
       'P' as expiring_record
from patient
join group_info using(group_number)
join claim using(patient_id)
where group_info.deactivate_group = false
  and patient.delete_date is null
  and patient.expiration_date = ${expiration_date|e}
union
select 
       patient.group_number,
       patient.first_name,
       patient.last_name,
       to_char(patient.dob, 'YYYYMMDD'),
       patient.ssn,
       to_char(claim.effective_date, 'YYYYMMDD'),
       to_char(claim.expiration_date, 'YYYYMMDD'),
       claim.email1 as adjuster_email,
       'C' as expiring_record
from patient
join group_info using(group_number)
join claim using(patient_id)
where group_info.deactivate_group = false
  and patient.delete_date is null
  and claim.expiration_date = ${expiration_date|e}

order by last_name, first_name;

