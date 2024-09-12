begin;
/*
drop table if exists bd.patient_payer cascade;

create table bd.patient_payer (
    patient_payer_id serial primary key not null,
    group_number varchar(8),
    first_name varchar(20),
    last_name varchar(40),
    patient_id varchar(12),
    dob date,
    doi date,
    employer varchar(50),
    payer_name varchar(50),
    payer_address varchar(100),
    payer_address_2 varchar(50),
    payer_city varchar(25),
    payer_state varchar(2),
    payer_zip varchar(10),
    unique (group_number, patient_id, dob, doi)
);
*/
drop view if exists bd.ar_payer;

create view bd.ar_payer as
  with p as (
    select distinct on (patient.patient_id)
        patient.patient_id,
        patient_payer.payer_name,
        patient_payer.payer_address,
        patient_payer.payer_address_2,
        patient_payer.payer_city,
        patient_payer.payer_state,
        patient_payer.payer_zip
    from patient_payer
    join patient on
        patient_payer.group_number = patient.group_number and
        patient_payer.patient_id = patient.ssn and
        patient_payer.dob = patient.dob
    order by patient.patient_id, patient_payer.doi, patient_payer.payer_name)
  select
    patient.patient_id,
    coalesce(p.payer_name,
        client.billing_name || ' #' || client.group_number, '') as billing_name,
    coalesce(
      case when p.payer_name is not null then p.payer_address
        else client.address_1
        end, '') as billing_address_1,
    coalesce(
      case when p.payer_name is not null then p.payer_address_2
         else client.address_2
         end, '') as billing_address_2,
    coalesce(
      case when p.payer_name is not null then p.payer_city
         else client.city
         end, '') as billing_city,
    coalesce(
      case when p.payer_name is not null then p.payer_state
         else client.state
         end, '') as billing_state,
    coalesce(
      case when p.payer_name is not null then p.payer_zip
         else client.zip_code
         end, '') as billing_zip_code
  from patient
  join client using(group_number)
  left join p using(patient_id)
;


commit;

/* test data
begin;

insert into patient_payer (group_number, patient_id, dob, doi, payer_name, payer_address,
    payer_city, payer_state, payer_zip)
    values
    ('54010', '458745394', '19471024', '20101201', 'Disney World', '111 Magic Kingdom Dr',
     'Orlando', 'FL', '11101'),
    ('54010', '458745394', '19471024', '20150421', '7-Eleven', '333 Taco St',
     'Cinncinati', 'OH', '44334');

commit;
*/
