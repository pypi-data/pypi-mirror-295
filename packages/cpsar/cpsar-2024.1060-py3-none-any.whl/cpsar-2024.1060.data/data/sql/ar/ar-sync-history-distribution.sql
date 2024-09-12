begin;
create temp table dload (
    line text,
    group_number varchar(8),
    group_auth int,
    line_no int,
    account varchar(50),
    negative varchar,
    amount decimal,
    history_id bigint
);

\copy dload(line) from /server/export/bd/files/bd-distributions.txt

update dload set
    group_number = trim(substring(line from 1 for 8)),
    group_auth = substring(line from 9 for 7)::int,
    line_no = substring(line from 16 for 2)::int,
    account = trim(substring(line from 18 for 50)),
    negative = substring(line from 68 for 1),
    amount = substring(line from 69 for 9)::numeric;

update dload set amount = -amount where negative = '-';
update dload set history_id = history.history_id
from history
where dload.group_number = history.group_number
  and dload.group_auth = history.group_auth;

-- gross duplicates
with dups as (
    select group_number, group_auth, line_no, count(*)
    from dload
    group by group_number, group_auth, line_no
    having count(*) > 1)
delete from dload
using dups
    where dload.group_number = dups.group_number
      and dload.group_auth = dups.group_auth
    ;

insert into history_distribution (group_number, group_auth, line_no, account, amount, history_id)
select group_number, group_auth, line_no, account, amount, history_id from dload
on conflict (group_number, group_auth, line_no) do update set
    account = EXCLUDED.account,
    amount = EXCLUDED.amount,
    history_id = EXCLUDED.history_id;

-- select group_number, group_auth, line_no, account, negative, amount from dload order by group_number, group_auth, line_no;
commit;
