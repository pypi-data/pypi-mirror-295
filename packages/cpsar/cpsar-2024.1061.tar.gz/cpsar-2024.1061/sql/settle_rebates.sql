
<%def name="available_rebates(group_number, rebate_date)">
  SELECT rebate.rebate_id, rebate.trans_id, drug.name AS drug_name,
      patient.first_name, patient.last_name, rebate.client_amount,
      rebate.client_balance
  FROM rebate
  JOIN trans USING(trans_id)
  JOIN patient USING(patient_id)
  JOIN drug USING(drug_id)
  WHERE rebate.rebate_date = ${rebate_date |e}
    AND trans.group_number = ${group_number |e}
    AND rebate.client_balance != 0
  ORDER BY rebate.rebate_id;
</%def>

<%def name='apply_rebate_settlements(values)'>
/* Create settlements for the given rebates with the given check numbers
*/
CREATE TEMP TABLE load (
    rebate_id BIGINT,
    check_number VARCHAR(30),
    apply_amount DECIMAL(10, 2),
    settle_date DATE NOT NULL,
    username VARCHAR(100) NOT NULL,
    error_msg TEXT
);
INSERT INTO load (rebate_id, check_number, apply_amount, settle_date, username)
  VALUES ${insert_values(values)};

/* Apply amount comes in as int of pennies. Turn to deciaml */
UPDATE load SET apply_amount = apply_amount / 100;

/* Be sure the amount is in bounds */
UPDATE load SET
  error_msg = 'rebate ' || load.rebate_id || ' only has ' ||
              client_balance || ' to apply'
  FROM rebate
  WHERE load.rebate_id = rebate.rebate_id
    AND load.error_msg IS NULL
    AND load.apply_amount > rebate.client_balance;

INSERT INTO rebate_settlement (rebate_id, check_number, settle_date, amount,
                               username)
  SELECT load.rebate_id, load.check_number, load.settle_date,
         load.apply_amount, load.username
  FROM load
  JOIN rebate USING(rebate_id)
  WHERE load.error_msg IS NULL;

UPDATE rebate SET client_balance = client_balance - apply_amount
  FROM load
  WHERE rebate.rebate_id = load.rebate_id
    AND load.error_msg IS NULL;

SELECT *
  FROM load
  WHERE error_msg IS NOT NULL;
</%def>
