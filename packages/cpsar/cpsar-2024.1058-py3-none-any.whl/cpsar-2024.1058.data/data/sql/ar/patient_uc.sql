DROP TABLE patient_unapplied_cash;

CREATE TABLE patient_unapplied_cash (
  puc_id BIGSERIAL PRIMARY KEY,
  patient_id BIGINT REFERENCES patient(patient_id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  username varchar(255),
  amount NUMERIC(10, 2),
  type VARCHAR(5),
  ref VARCHAR(255),
  entry_date TIMESTAMP DEFAULT NOW()
);
