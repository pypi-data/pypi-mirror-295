begin;
with c as (
    delete from nabp_tt_prefix
    where chain_code is not null
    returning chain_code, group_number, prefix
), d as (select distinct * from c)

insert into nabp_tt_prefix (nabp, group_number, prefix, chain_code)
select distinct pharmacy.nabp,
    d.group_number,
    d.prefix,
    pharmacy.chain_code
from pharmacy
join d using(chain_code)
where pharmacy.nabp is not null;

commit;
