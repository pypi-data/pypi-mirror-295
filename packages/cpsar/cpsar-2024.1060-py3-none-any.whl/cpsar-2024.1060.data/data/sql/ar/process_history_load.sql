
/* Clean up data fields */
UPDATE history_load SET doi=NULL WHERE doi='000000';
UPDATE history_load SET reverse_date = NULL WHERE reverse_date = '000000';
UPDATE history_load SET pharmacy_payment_date = NULL WHERE pharmacy_payment_date = '000000';
UPDATE history_load SET cost_allowed=0 WHERE cost_allowed=NULL;
UPDATE history_load SET dispense_fee=0 WHERE dispense_fee=NULL;
UPDATE history_load SET sales_tax=0 WHERE sales_tax=NULL;
UPDATE history_load SET eho_network_copay=0 WHERE eho_network_copay=NULL;
UPDATE history_load SET processing_fee=0 WHERE processing_fee=NULL;
UPDATE history_load SET cost_submitted=0 WHERE cost_submitted=NULL;
UPDATE history_load SET usual_customary=0 WHERE usual_customary=NULL;
UPDATE history_load SET state_fee=0 WHERE state_fee=NULL;
UPDATE history_load SET awp=0 WHERE awp=NULL;
UPDATE history_load SET generic_price=0 WHERE generic_price=NULL;
UPDATE history_load SET pbm_copay_2=0 WHERE pbm_cost_2=NULL;
UPDATE history_load SET pbm_fee_2=0 WHERE pbm_fee_2=NULL;
UPDATE history_load SET pbm_sales_tax_2=0 WHERE pbm_sales_tax_2=NULL;
UPDATE history_load SET pbm_copay_2=0 WHERE pbm_copay_2=NULL;
UPDATE history_load SET pharmacy_cost_allowed=0 WHERE pharmacy_cost_allowed=NULL;
UPDATE history_load SET pharmacy_dispense_fee=0 WHERE pharmacy_dispense_fee=NULL;

/* Fix DOI */
UPDATE history_load SET fixed_doi = to_date_safe(history_load.doi, 'YYMMDD')
  WHERE doi IS NOT NULL;

UPDATE history_load SET fixed_doi = fixed_doi - '100 years'::interval
  WHERE fixed_doi > NOW();

/* Populate Foreign Key Fields */
UPDATE history_load SET patient_id=P.patient_id
FROM patient as P
WHERE history_load.patient_cardholder_nbr = P.ssn AND
    history_load.group_number = P.group_number AND
    (to_date_safe(history_load.patient_dob, 'YYYYMMDD') = P.dob OR
     (history_load.patient_dob IS NULL AND P.dob IS NULL));

UPDATE history_load SET pharmacy_id=pharmacy.pharmacy_id
FROM pharmacy
WHERE history_load.pharmacy_nabp = pharmacy.nabp;

UPDATE history_load SET drug_id=drug.drug_id
FROM drug
WHERE history_load.drug_ndc_number = drug.ndc_number;

UPDATE history_load SET doctor_id=doctor_key.doctor_id
FROM doctor_key
WHERE history_load.doctor_npi_number=doctor_key.doc_key;

UPDATE history_load SET doctor_id=doctor_key.doctor_id
FROM doctor_key
WHERE history_load.doctor_dea_number=doctor_key.doc_key;

UPDATE history_load SET claim_id=claim.claim_id
FROM claim
WHERE history_load.patient_id=claim.patient_id AND
    history_load.fixed_doi = claim.doi;

UPDATE history_load SET pharmacist_id=pharmacist.pharmacist_id
FROM pharmacist
WHERE history_load.lic_number = pharmacist.lic_number AND
      history_load.lic_state = pharmacist.lic_state;

/* Mark dirty records */
UPDATE history_load SET error_msg = 'Patient not on file'
  WHERE patient_id IS NULL;

UPDATE history_load SET error_msg = 'Pharmacy NABP ' || pharmacy_nabp || ' not on file'
  WHERE pharmacy_id IS NULL;

UPDATE history_load SET error_msg = 'Drug not on file'
  WHERE drug_id IS NULL;

UPDATE history_load SET error_msg = 'Client not on file'
  WHERE group_number IS NULL;

/* Update existing history records */
UPDATE history SET
    patient_id=L.patient_id,
    pharmacy_id=L.pharmacy_id,
    doctor_id=L.doctor_id,
    drug_id=L.drug_id,
    doi=L.doi,
    rx_date=to_date_safe(L.rx_date, 'YYMMDD'),
    rx_number=L.rx_number::bigint,
    date_written=to_date_safe(L.date_written, 'YYMMDD'),
    daw=L.daw,
    quantity=L.quantity::numeric,
    days_supply=L.days_supply::int,
    compound_code=L.compound_code,
    refill_number=L.refill_number::int,
    cost_submitted=L.cost_submitted::numeric,
    cost_allowed=L.cost_allowed::numeric,
    dispense_fee=L.dispense_fee::numeric,
    sales_tax=L.sales_tax::numeric,
    eho_network_copay=L.eho_network_copay::numeric,
    pbm_cost_2=L.pbm_cost_2::numeric,
    pbm_fee_2=L.pbm_fee_2::numeric,
    pbm_sales_tax_2=L.pbm_sales_tax_2::numeric,
    pbm_copay_2=L.pbm_copay_2::numeric,
    processing_fee=L.processing_fee::numeric,
    usual_customary=L.usual_customary::numeric,
    state_fee=L.state_fee::numeric,
    awp=L.awp::numeric,
    date_processed=L.date_processed::timestamp,
    reverse_date=to_date_safe(L.reverse_date, 'YYMMDD'),
    pharmacy_payment_date=to_date_safe(L.pharmacy_payment_date, 'YYMMDD'),
    claim_id=L.claim_id,
    generic_price=L.generic_price::numeric,
    doctor_dea_number=L.doctor_dea_number,
    doctor_npi_number=L.doctor_npi_number,
    lic_number=L.lic_number,
    lic_state=L.lic_state,
    pharmacist_id=L.pharmacist_id,
    inv_class=L.inv_class,
    level_of_effort=L.level_of_effort,
    sponsor_cost_allowed=L.sponsor_cost_allowed::numeric,
    sponsor_dispense_fee=L.sponsor_dispense_fee::numeric,
    pharmacy_cost_allowed=L.pharmacy_cost_allowed::numeric,
    pharmacy_dispense_fee=L.pharmacy_dispense_fee::numeric,
    hit_id=L.hit_id::int,
    soj=L.soj
FROM history_load AS L
WHERE history.group_number = L.group_number
  AND history.group_auth = L.group_auth::int
  AND L.error_msg IS NULL;

/* put back pharmacist id overrides */
UPDATE history
SET pharmacist_id=pharmacist.pharmacist_id
FROM pharmacist
WHERE history.cps_lic_number = pharmacist.lic_number
  AND history.cps_lic_state = pharmacist.lic_state;

 -- Create new history records
INSERT INTO history(
    group_number, group_auth, patient_id, pharmacy_id, doctor_id,
    drug_id, doi, rx_date, rx_number, date_written, daw, quantity,
    days_supply, compound_code, refill_number, cost_submitted,
    cost_allowed, dispense_fee, sales_tax, eho_network_copay,
    pbm_cost_2, pbm_fee_2, pbm_sales_tax_2, pbm_copay_2,
    processing_fee, usual_customary, state_fee, awp, date_processed,
    reverse_date, pharmacy_payment_date, claim_id, generic_price, doctor_dea_number,
    doctor_npi_number, lic_number, lic_state, pharmacist_id, inv_class,
    level_of_effort,sponsor_cost_allowed, sponsor_dispense_fee,
    pharmacy_cost_allowed, pharmacy_dispense_fee,
    hit_id,soj
)
SELECT 
    L.group_number, L.group_auth::int, L.patient_id, L.pharmacy_id,
    L.doctor_id, L.drug_id, L.doi,
    to_date_safe(L.rx_date, 'YYMMDD') AS rx_date,
    L.rx_number::bigint AS rx_number,
    to_date_safe(L.date_written, 'YYMMDD') AS date_written,
    L.daw, L.quantity::numeric AS quantity,
    L.days_supply::int AS days_supply,
    L.compound_code, L.refill_number::int AS refill_number,
    L.cost_submitted::numeric AS cost_submitted,
    L.cost_allowed::numeric AS cost_allowed,
    L.dispense_fee::numeric AS dispense_fee,
    L.sales_tax::numeric AS sales_tax,
    L.eho_network_copay::numeric AS eho_network_copay,
    L.pbm_cost_2::numeric as pbm_cost_2,
    L.pbm_fee_2::numeric as pbm_fee_2,
    L.pbm_sales_tax_2::numeric as pbm_sales_tax_2,
    L.pbm_copay_2::numeric as pbm_copay_2,
    L.processing_fee::numeric AS processing_fee,
    L.usual_customary::numeric AS usual_customary,
    L.state_fee::numeric AS state_fee,
    L.awp::numeric AS awp,
    L.date_processed::timestamp AS date_processed,
    to_date_safe(L.reverse_date, 'YYMMDD') AS reverse_date,
    to_date_safe(L.pharmacy_payment_date, 'YYMMDD')
        AS pharmacy_payment_date,
    L.claim_id,
    L.generic_price::numeric AS generic_price,
    L.doctor_dea_number,
    L.doctor_npi_number,
    L.lic_number,
    L.lic_state,
    L.pharmacist_id,
    L.inv_class,
    L.level_of_effort,
    L.sponsor_cost_allowed::numeric,
    L.sponsor_dispense_fee::numeric,
    L.pharmacy_cost_allowed::numeric,
    L.pharmacy_dispense_fee::numeric,
    L.hit_id::int,
    L.soj
FROM history_load as L
WHERE NOT EXISTS (
    SELECT *
    FROM history
    WHERE 
        history.group_number = L.group_number AND
        history.group_auth = L.group_auth::int)
  AND error_msg IS NULL;

/* Clean out all of the records that we have loaded */
DELETE FROM history_load WHERE error_msg IS NULL;

