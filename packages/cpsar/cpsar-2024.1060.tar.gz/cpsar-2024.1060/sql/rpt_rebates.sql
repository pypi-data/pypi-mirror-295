CREATE TEMP TABLE report AS
    SELECT rebate.*,
           trans.group_number,
           trans.group_auth as "claim_reference_number",
           trans.balance AS trans_balance,
           trans.rx_date,
           trans.quantity,
           patient.first_name,
           patient.last_name,
           patient.ssn,
           patient.dob,
           trans.claim_number,
           drug.name AS drug_name,
           drug.ndc_number,
           trans.tx_type,
           trans.awp,
           pharmacy.nabp,
           pharmacy.name as pharmacy_name
    FROM rebate
    JOIN trans USING(trans_id)
    JOIN patient USING(patient_id)
    jOIN drug USING(drug_id)
    JOIN pharmacy using(pharmacy_id)
    WHERE rebate.rebate_date BETWEEN ${start_date} AND ${end_date}
      AND trans.group_number ${gn_frag};
% if has_client_amount:
  DELETE FROM report
  WHERE client_amount IS NULL OR client_amount = 0;
% endif
% if has_client_balance:
  DELETE FROM report
  WHERE client_balance IS NULL OR client_balance = 0;
% endif

SELECT * FROM report
  ORDER BY rebate_id;
