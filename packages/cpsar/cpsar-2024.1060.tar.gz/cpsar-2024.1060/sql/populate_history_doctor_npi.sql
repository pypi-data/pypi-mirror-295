begin;

with d as (
    select doctor_id, doc_key as npi
    from doctor_key
    where length(doc_key) = 10
)

update history set doctor_npi_number = d.npi
from d
where (history.doctor_npi_number is null or history.doctor_npi_number = '')
  and d.doctor_id = history.doctor_id;


with d as (
    select doctor_id, doc_key as dea
    from doctor_key
    where length(doc_key) = 9
)

update history set doctor_dea_number = d.dea
from d
where (history.doctor_dea_number is null or history.doctor_dea_number = '')
  and d.doctor_id = history.doctor_id;

commit;
