
CREATE TABLE dbo.bd_adjudication_detail (
    adjudication_id INT,
    trans_id INT,
    invoice_id INT,
    invoice_date INT,
    group_number VARCHAR(8),
    patient_first_name VARCHAR(12),
    patient_last_name VARCHAR(15),
    rx_number INT,
    drug_name VARCHAR(40),
    rx_date INT,
    adjudication_date INT,
    username VARCHAR(50),
    source_trans_id INT,
    source_invoice_id INT,
    amount DECIMAL(10, 2)
);

CREATE TABLE dbo.bd_rx_reg (
   reg_id VARCHAR(20) PRIMARY KEY NOT NULL,
   batch_date INT NULL,
   nabp VARCHAR(7) NOT NULL,
   group_number VARCHAR(8) NOT NULL,
   rx_date INT NOT NULL,
   process_date INT NOT NULL,
   first_name VARCHAR(12),
   last_name VARCHAR(15),
   group_auth INT NOT NULL,
   claim_number VARCHAR(50),
   rx_number INT NOT NULL,
   refill_number INT NOT NULL,
   ndc VARCHAR(15) NOT NULL,
   drug_name VARCHAR(100),
   cost_allowed DECIMAL(10, 2) NOT NULL,
   dispense_fee DECIMAL(10, 2) NOT NULL,
   sales_tax DECIMAL(10, 2) NOT NULL,
   copay DECIMAL(10, 2) NOT NULL,
   processing_fee DECIMAL(10, 2) NOT NULL,
   amount_due DECIMAL(10, 2) NOT NULL,
   trans_id BIGINT,
   history_id BIGINT
);

CREATE TABLE dbo.bd_eho_invoice_data (
   ebd_id BIGINT PRIMARY KEY NOT NULL,
   batch_date INT NOT NULL,
   nabp VARCHAR(7) NOT NULL,
   group_number VARCHAR(8) NOT NULL,
   rx_date INT NOT NULL,
   process_date INT NOT NULL,
   first_name VARCHAR(12),
   last_name VARCHAR(15),
   group_auth INT NOT NULL,
   claim_number VARCHAR(50),
   rx_number INT NOT NULL,
   refill_number INT NOT NULL,
   ndc VARCHAR(15) NOT NULL,
   drug_name VARCHAR(100),
   cost_allowed DECIMAL(10, 2) NOT NULL,
   dispense_fee DECIMAL(10, 2) NOT NULL,
   sales_tax DECIMAL(10, 2) NOT NULL,
   copay DECIMAL(10, 2) NOT NULL,
   processing_fee DECIMAL(10, 2) NOT NULL,
   amount_due DECIMAL(10, 2) NOT NULL,
   trans_id BIGINT,
   history_id BIGINT
);

CREATE TABLE billed_tx (
  "trans_id" INT PRIMARY KEY, 
  "batch_date" DATE NOT NULL,
  "group_number" VARCHAR(8) NOT NULL, 
  "group_auth" BIGINT, 
  "invoice_id" BIGINT, 
  "line_no" BIGINT, 
  "rx_date" DATE NOT NULL, 
  "pharmacy_nabp" VARCHAR(255) NOT NULL,
  "refill_number" INT NOT NULL,
  "rx_number" INT NOT NULL,
  "date_written" DATE, 
  "cost_allowed" NUMERIC(10,2) NOT NULL, 
  "dispense_fee" NUMERIC(11,2) NOT NULL, 
  "sales_tax" NUMERIC(11,2) NOT NULL, 
  "copay" NUMERIC(11,2) NOT NULL, 
  "processing_fee" NUMERIC(11,2) NOT NULL
);

CREATE TABLE dbo.bd_receipt(
	payment_id int NOT NULL,
    trans_id int NOT NULL,
	entry_date datetime NOT NULL,
    amount numeric(10, 2) not null,
    note text,
    username VARCHAR(50) NOT NULL,
    check_no VARCHAR(40) NULL,
    card_type VARCHAR(20) NULL,
    card_number VARCHAR(30) NULL,
    expiration_date DATETIME NULL,
    direct_deposit BIT NOT NULL,
    unapplied_cash BIT NOT NULL,

    PRIMARY KEY (payment_id)
);

CREATE TABLE dbo.bd_real_receipt(
	receipt_id VARCHAR(15) NOT NULL,
    payment_id int,
    puc_id int,
	entry_date datetime NOT NULL,
    trans_id int NOT NULL,
    amount numeric(10, 2) not null,
    note text,
    username VARCHAR(50) NOT NULL,
    check_no VARCHAR(40) NULL,
    card_type VARCHAR(20) NULL,
    card_number VARCHAR(30) NULL,
    expiration_date DATETIME NULL,
    direct_deposit BIT NOT NULL,
    pharmacy_nabp VARCHAR(7) NOT NULL,
    group_number VARCHAR(8) NOT NULL,
    PRIMARY KEY (receipt_id)
);

CREATE TABLE dbo.bd_reversal (
     reversal_id int NOT NULL,
     trans_id int NOT NULL,
     reversal_date DATETIME NOT NULL,
     entry_date DATETIME NOT NULL,

	 PRIMARY KEY (reversal_id)
);

CREATE TABLE dbo.bd_reversal_credit (
    credit_id VARCHAR(11) NOT NULL,
	adj_id int,
    settlement_id int,
    reversal_id int NOT NULL,
    trans_id int NOT NULL,
    invoice_id int,
    entry_date DATETIME NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    note text,
    username VARCHAR(50) NOT NULL,
    pharmacy_nabp VARCHAR(8),

    PRIMARY KEY (credit_id)
);

CREATE TABLE dbo.bd_adjudication (
    wo_id int NOT NULL,
    trans_id int NOT NULL,
    entry_date DATETIME NOT NULL,
    amount numeric(10, 2),
    note text,
    username VARCHAR(50) NOT NULL,

    PRIMARY KEY (wo_id)
);

CREATE TABLE dbo.bd_patient_unapplied_cash (
    group_number VARCHAR(8) NOT NULL,
    patient_first_name VARCHAR(12) NOT NULL,
    patient_last_name VARCHAR(15) NOT NULL,
    puc_id BIGINT,
    reversal_id BIGINT,
    amount numeric(10, 2) NOT NULL,
    balance numeric(10, 2) NOT NULL,
    type VARCHAR(5),
    trans_id BIGINT,
    claim_number VARCHAR(100),
    invoice_id BIGINT,
    drug_ndc_number CHAR(11),
    drug_name VARCHAR(30),
    rx_date int,
    reversal_date int,
    batch_date int,
    create_date int,
    entry_date int,
    entry_time int

);
