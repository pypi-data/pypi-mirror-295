import logging
import sys

import cpsar.runtime as R
from cpsar import pg

CURRENT_VERSION = 23

SCHEMAS = [
    'bd',
    'mjoseph',
    'msq',
    'sunrise'
]

def migrate():
    while db_version() < CURRENT_VERSION:
        upgrade()

def db_version():
    query = """
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'dbversion'
        )
        """
    cursor = R.db.cursor()
    cursor.execute(query)
    if not cursor.fetchone()[0]:
        cursor.execute("""
            create table public.dbversion (version int default 0, updated timestamp default now());
            insert into public.dbversion values(0, now());
            """)
        R.db.commit()

    cursor.execute("""
        select version from public.dbversion
        """)
    return cursor.fetchone()[0]

def upgrade():
    next_version = db_version() + 1
    handler = version_registry[next_version]
    cursor = R.db.cursor()
    handler(cursor)
    cursor.execute("update dbversion set version=%s, updated=now()", (next_version,))
    R.db.commit()

version_registry = {}

def reg(version):
    def inner(func):
        version_registry[version] = func
        return func
    return inner

def next_version(number, sql, exclude=[]):
    @reg(number)
    def inner(cursor):
        for s in SCHEMAS:
            if s in exclude:
                continue
            logging.debug(sql.format(s=s))
            cursor.execute(sql.format(s=s))

@reg(1)
def version1(cursor):
    # BD Issue 33524
    cursor.execute("alter table bd.state_report_bill add column icd_code char(3)")

@reg(2)
def version2(cursor):
    # BD Issue 33524
    cursor.execute("alter table bd.state_report_bill alter column icd_code set default '0'")

@reg(3)
def version3(cursor):
    # BD Issue 33524
    cursor.execute("update bd.state_report_bill set icd_code = '0' where icd_code = null")

@reg(4)
def version4(cursor):
    # BD Issue 33313. Add preview to load files.
    for s in SCHEMAS:
        cursor.execute(f"alter table {s}.load_profile add column preview_module varchar(100) default null")
    pg.execute_mako(cursor, "bd/views/profile_status.sql")

@reg(5)
def version5(cursor):
    """ BD Issue 33313. New custom EDI file format uploaded by Lindsay so we
    have to add some fields to the EDI file table to make it more flexible to
    support different kinds of files.
    """
    cursor.execute("alter table bd.user_edi_file add column source_file bytea")
    cursor.execute("alter table bd.user_edi_file add column source_file_name text")
    cursor.execute("alter table bd.user_edi_file add column source_definition jsonb")

@reg(6)
def version6(cursor):
    for s in SCHEMAS:
        cursor.execute(f"alter table {s}.sftp_account add column label text")

@reg(7)
def version7(cursor):
    for s in SCHEMAS:
        cursor.execute(f"alter table {s}.group_info add column backend_fields json")

@reg(8)
def version8(cursor):
    cursor.execute("""
        create table claim_backend_value (
            claim_id bigint references claim(claim_id) on delete cascade on update cascade,
            group_number varchar(8),
            ssn varchar(11),
            dob date,
            name varchar(30),
            doi date,
            value text,
            PRIMARY KEY(group_number, ssn, dob, doi, name)
        );
        create index claim_backend_value_claim_idx on claim_backend_value(group_number, ssn, dob, doi);
        """)

@reg(9)
def version9(cursor):
    for s in SCHEMAS:
        cursor.execute(f"alter table {s}.group_info add column claim_auth_formulary_flag bool")

@reg(10)
def version10(cursor):
    for s in SCHEMAS:
        cursor.execute(f"alter table {s}.auth_action add column pa_list bool not null default false")

@reg(11)
def version11(cursor):
    for s in SCHEMAS:
        cursor.execute(f"""
            create table {s}.assigned_auth_action (
                aa_group_id serial primary key,
                group_number varchar(15) references {s}.group_info(group_number)
                    on delete cascade on update cascade,
                aa_id int references auth_action(aa_id)
                    on delete cascade on update cascade,
                order_number int not null default 1
                );
            create unique index assigned_auth_action_gaa_idx on {s}.assigned_auth_action(group_number, aa_id);

        """)
        cursor.execute("""
            insert into assigned_auth_action (group_number, aa_id)
            select group_number, aa_id from auth_action
            where group_number is not null
            on conflict (group_number, aa_id) do nothing;
            """)

next_version(12, "alter table {s}.auth_action rename column field_list to selector_list")
next_version(13, "alter table {s}.auth_action add column field_list text[] not null default '{{}}'")
next_version(14, "alter table {s}.auth_action add column commentary text")
next_version(15, "alter table {s}.group_info add column manage_auth_drug_list bool not null default false")
next_version(16, "alter table {s}.group_info rename column manage_auth_drug_list to manage_auth_drug_list_flag")
next_version(17, """
--    drop index {s}.assigned_auth_action_group_number_fkey;
    alter table {s}.assigned_auth_action drop constraint if exists assigned_auth_action_group_number_fkey;
    alter table {s}.assigned_auth_action add constraint assigned_auth_action_group_number_fkey
        foreign key (group_number) references {s}.group_info(group_number)
            on update cascade
            on delete cascade;
""")
next_version(18, """
    alter table {s}.auth_action add column formulary_policy_list text[] not null default '{{}}'
""")
next_version(19, """
    alter table {s}.assigned_auth_action drop constraint if exists assigned_auth_action_aa_id_fkey;
    alter table {s}.assigned_auth_action add constraint assigned_auth_action_aa_id_fkey
        foreign key (aa_id) references {s}.auth_action(aa_id)
            on update cascade
            on delete cascade;
""")
next_version(20, """
    alter table {s}.group_info add column patient_express_expire_days int default 5;
""")
next_version(21, """
    alter table {s}.user_info add column express_enroll_menuitem_flag bool default false;
""", exclude=["bd", "mjoseph", "sunrise"])

@reg(22)
def version22(cursor):
    cursor.execute("alter table hit alter column pat_special_id type varchar(15)")
    cursor.execute("alter table hit add column alternate_id varchar(20)")

next_version(23, "alter table {s}.auth_action add column legacy_manage_drug_list bool not null default false")

if __name__ == '__main__': 
    if "-v" in sys.argv:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)
    R.db.setup()
    migrate()
