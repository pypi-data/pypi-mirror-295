
begin;

with p as (
    SELECT patient_id,
           group_number,
           ssn,
           dob,
           ROW_NUMBER() OVER (PARTITION BY group_number, ssn, dob ORDER BY patient_id) as rn
    FROM patient
), dups as (
    select p1.patient_id as small, p2.patient_id as large
    from p p1, p p2
    where
    p1.rn = 1 and p2.rn != 1 and
    p1.group_number = p2.group_number and
    p1.dob = p2.dob and
    p1.ssn = p2.ssn 
), hupdates as (update history set patient_id=small
    from dups
    where history.patient_id=large)

update trans set patient_id=small
from dups
where trans.patient_id=large;

/*

update history set patient_id=35097792 where patient_id=35908686;
update history set patient_id=328133 where patient_id=35924173;
update trans set patient_id=328133 where patient_id=35924173;
update history set patient_id=28525773 where patient_id=35928860;
update trans set patient_id=28525773 where patient_id=35928860;
update history set patient_id=32692492 where patient_id=36008204;
update trans set patient_id=32692492 where patient_id=36008204;

create temp table p ( small bigint, large bigint);
insert into p values
    (24504607, 36008114),
    (35142338, 36007830),
    (360102, 36008369),
    (15114652, 36009079),
    (  360565, 36007060)
     ;

update history set patient_id=p.small from p where history.patient_id=p.large;
update trans set patient_id=p.small from p where trans.patient_id=p.large;
*/

DELETE FROM patient
WHERE patient_id IN (
    SELECT patient_id
    FROM (
        SELECT patient_id, 
               ROW_NUMBER() OVER (PARTITION BY group_number, ssn, dob ORDER BY patient_id) as rn
        FROM patient
    ) t
    WHERE t.rn > 1
);
commit;

drop index patient_group_number_ssn_dob_key;
alter table patient add constraint patient_group_number_ssn_dob_key unique  (group_number, ssn, dob);
