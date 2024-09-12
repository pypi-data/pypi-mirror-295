CREATE TEMP TABLE rebate_load (
    group_number VARCHAR(8),
    group_auth INT,
    total_amount DECIMAL(6, 2),
    client_amount DECIMAL(6, 2) DEFAULT 0,
    rebate_date DATE,
    trans_id BIGINT,
    error_msg TEXT,
    trans_balance decimal(10, 2),
    first_name varchar,
    last_name varchar,
    ssn varchar,
    claim_number varchar,
    dob date,
    drug_name varchar,
    tx_type varchar,
    rx_date date,
    invoice_date date,
    invoice_id bigint
);

CREATE INDEX rbl_idx ON rebate_load(group_number, group_auth);

INSERT INTO rebate_load (group_number, group_auth, total_amount, rebate_date)
  VALUES ${insert_values(rebates)};

delete from rebate_load where group_number not in (select group_number from group_info);

update rebate_load set
    trans_id = trans.trans_id,
    trans_balance = trans.balance,
    first_name = patient.first_name,
    last_name = patient.last_name,
    ssn = patient.ssn,
    dob = patient.dob,
    claim_number = trans.claim_number,
    drug_name = drug.name,
    tx_type = trans.tx_type,
    rx_date =  trans.rx_date,
    invoice_date = trans.invoice_date,
    invoice_id =  trans.invoice_id
    from trans, patient, drug
    where rebate_load.group_number = trans.group_number
      and rebate_load.group_auth = trans.group_auth
      and patient.patient_id = trans.patient_id
      and drug.drug_id = trans.drug_id;

update rebate_load set
    first_name = patient.first_name,
    last_name = patient.last_name,
    ssn = patient.ssn,
    dob = patient.dob,
    drug_name = drug.name
    from history, patient, drug
    where rebate_load.group_number = history.group_number
      and rebate_load.group_auth = history.group_auth
      and history.patient_id = patient.patient_id
      and drug.drug_id = history.drug_id
      and rebate_load.trans_id is null;

select * from rebate_load ORDER BY group_number, group_auth;
