
begin;

create table state_report_file (
    sr_file_id bigserial primary key not null,
    create_time timestamp not null default now(),
    status_flag char(1) default '',
    file_name varchar,
    contents bytea
);


create table state_report_entry (
    srid bigserial primary key not null,
    create_time timestamp not null default now(),
    position int,
    sr_file_id bigint references state_report_file(sr_file_id)
        on update cascade
        on delete cascade,
    trans_id bigint references trans(trans_id)
        on update cascade
        on delete restrict,
    reversal_id bigint references reversal(reversal_id)
        on update cascade
        on delete restrict
);

alter table trans add column sr_mark char(1) not null default '';

alter table reversal add column sr_mark char(1) not null default '';


commit;
