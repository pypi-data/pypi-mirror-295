/*/////////////////////////////////////////////////////////////////////////////
 * Master Schema File for Corporate Pharmacy Services Blue Diamond
 *                          Backend Systems
 */

CREATE TABLE eho_invoice_data (
    ebd_id BIGSERIAL,
    group_number VARCHAR(8) NOT NULL,
    group_auth INT NOT NULL,
    reversal BOOL,
    nabp VARCHAR(7) NOT NULL,
    rx_number INTEGER NOT NULL,
    refill_number INTEGER NOT NULL,
    rx_date DATE NOT NULL,
    process_date DATE NOT NULL,
    ndc VARCHAR(11) NOT NULL,
    quantity DECIMAL(10, 3) NOT NULL,
    cost_allowed DECIMAL(10, 2) NOT NULL,
    dispense_fee DECIMAL(10, 2) NOT NULL,
    sales_tax DECIMAL(10, 2) NOT NULL,
    copay DECIMAL(10, 2) NOT NULL,
    processing_fee DECIMAL(10, 2) NOT NULL,
    amount_due DECIMAL(10, 2) NOT NULL,
    batch_date DATE NOT NULL,
    file_name VARCHAR(50) NOT NULL,
    trans_id BIGINT,
    history_id BIGINT,
    UNIQUE(group_number, group_auth, reversal)
);

CREATE TABLE hcfa_1500_print_history (
    batch_date DATE,
    create_date TIMESTAMP DEFAULT NOW(),
    username VARCHAR(50)
);

CREATE TABLE bad_dea_number (
    dea_number CHAR(9) PRIMARY KEY,
    create_date TIMESTAMP DEFAULT NOW()
);

CREATE TABLE rebill (
    rebill_id BIGSERIAL PRIMARY KEY,
    trans_id BIGINT REFERENCES trans(trans_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    entry_date TIMESTAMP DEFAULT NOW(),
    total NUMERIC(10, 2),
    balance NUMERIC(10, 2),
    username VARCHAR(100)
);

CREATE TABLE rebill_credit (
    rebill_credit_id BIGSERIAL PRIMARY KEY,
    rebill_id BIGINT REFERENCES rebill(rebill_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    trans_id BIGINT REFERENCES trans(trans_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    entry_date TIMESTAMP DEFAULT NOW(),
    amount NUMERIC(10, 2),
    username VARCHAR(100)
);


CREATE TABLE history_ingredient (
    ingredient_id BIGSERIAL,
    history_id BIGINT REFERENCES history(history_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    ingredient_nbr SMALLINT,
    ndc VARCHAR(11),
    drug_id BIGINT REFERENCES drug(drug_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    qty DECIMAL,
    cost_submitted DECIMAL,
    cost_allowed DECIMAL,
    on_formulary BOOL);

CREATE INDEX history_compound_ingredient_drug_id
    ON history_ingredient(drug_id);

CREATE INDEX history_compound_history_id
    ON history_ingredient(history_id);

CREATE TABLE patient_drug_list (
    drug_list_id BIGSERIAL,
    patient_id BIGINT REFERENCES patient(patient_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    gpi_regexp VARCHAR(30) NOT NULL,
    allow_brand BOOL,
    drug_name VARCHAR(60)
);

CREATE INDEX patient_drug_list_patient_id_dx
    ON patient_drug_list(patient_id);

CREATE TABLE group_formulary (
    name VARCHAR(8),
    gpi_regexp VARCHAR(30) NOT NULL,
    source_drug_id BIGINT REFERENCES drug(drug_id),
    drug_name VARCHAR(50),
    PRIMARY KEY(name, gpi_regexp)
);
CREATE INDEX group_formulary_source_drug_id ON
    group_formulary(source_drug_id);

CREATE INDEX group_formulary_name ON group_formulary(name);

CREATE TABLE provider (
    modify_datetime VARCHAR(16),    
    doctor_key VARCHAR(8) PRIMARY KEY,
    name VARCHAR( 60),
    status VARCHAR(1),
    bac VARCHAR(1),
    bac_description VARCHAR(30),
    drug_schedule VARCHAR(15),
    expiration_date VARCHAR(8),
    address_1 VARCHAR(40),
    address_2 VARCHAR(40),
    address_3 VARCHAR(40),
    city VARCHAR(30),
    state VARCHAR(2),
    zip_code VARCHAR(10),
    phone VARCHAR(15),
    specialty VARCHAR(50),
    med_school VARCHAR(100),
    graduation_yr VARCHAR(4)

);
