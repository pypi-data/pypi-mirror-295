<%include file='ar-audit-trans.sql' />
<%def name="available_rebate()">
    SELECT rebate.rebate_id, rebate.client_balance, trans.patient_id
    FROM rebate
    JOIN trans USING(trans_id)
    JOIN client USING(group_number)
    WHERE rebate.client_balance != 0
      AND client.auto_apply_trans_rebate = TRUE;
</%def>
<%def name="candidate_trans(batch_date)">
    SELECT trans.trans_id, trans.balance, trans.patient_id
    FROM trans
    JOIN client USING(group_number)
    WHERE batch_date = ${batch_date|e}
      AND client.auto_apply_trans_rebate = TRUE
    ORDER BY trans_id DESC;
</%def>
<%def name='apply_rebate_credits(values)'>
/* Create credits on the given transactions from the provided rebates
*/
CREATE TEMP TABLE load (
    trans_id BIGINT, 
    rebate_id BIGINT,
    amount DECIMAL(10, 2) NOT NULL,
    entry_date DATE NOT NULL,
    username VARCHAR(100) NOT NULL,
    error_msg TEXT
);

INSERT INTO load (trans_id, rebate_id, amount, entry_date, username)
  VALUES ${insert_values(values)};

/* Be sure the rebate has enough monies */
UPDATE load SET
  error_msg = 'rebate only has a balance of ' || rebate.client_balance 
            || '. Cannot apply ' || load.amount
  FROM rebate
  WHERE rebate.rebate_id = load.rebate_id
    AND rebate.client_balance < load.amount
    AND load.error_msg IS NULL;

/* Be sure the target transaction has a big enough balance to not go negative */
WITH tsum AS (
    SELECT trans_id, SUM(amount) AS amount
    FROM load
    GROUP BY trans_id),
  terr AS (
    SELECT trans.trans_id, tsum.amount AS load_amount, trans.balance
    FROM tsum
    JOIN trans USING(trans_id)
    WHERE tsum.amount > trans.balance
  )
  UPDATE load SET
  error_msg = 'trans ' || load.trans_id || ' only has a balance of '
           ||  terr.balance || '. Cannot apply ' || terr.load_amount
  FROM terr
  WHERE load.trans_id = terr.trans_id
    AND load.error_msg IS NULL;

/* Be sure the source rebate and the target trans have the same patient */
UPDATE load SET
  error_msg = 'rebate patient ' || source_trans.patient_id
    || ' not the same as target trans patient ' || target_trans.patient_id
  FROM rebate, trans AS source_trans, trans AS target_trans
  WHERE load.rebate_id = rebate.rebate_id
    AND rebate.trans_id = source_trans.trans_id
    AND load.trans_id = target_trans.trans_id
    AND source_trans.patient_id != target_trans.patient_id
    AND load.error_msg IS NULL;

/* Do insert */
INSERT INTO rebate_credit (entry_date, rebate_id, trans_id, amount, username)
  SELECT entry_date, rebate_id, trans_id, amount, username
  FROM load
  WHERE error_msg IS NULL;

/* Update the balance on the rebate */
UPDATE rebate SET client_balance = client_balance - load.amount
  FROM load
  WHERE load.rebate_id = rebate.rebate_id
    AND load.error_msg IS NULL;

/* Update the balance on the trans. You can't do this with a simple
 * FROM because it can match more than one trans */
WITH rct AS (
   SELECT trans_id, SUM(amount) AS amount
   FROM load
   WHERE load.error_msg IS NULL
   GROUP BY trans_id)
UPDATE trans SET balance = balance - rct.amount,
                 rebate_credit_total=rebate_credit_total + rct.amount,
                 paid_amount=paid_amount + rct.amount
  FROM rct
  WHERE trans.trans_id = rct.trans_id;

/* Log the activity on the trans */
INSERT INTO trans_log (trans_id, message, username)
  SELECT trans_id, 'Applied rebate credit of ' || amount, username
  FROM load
  WHERE error_msg IS NULL;
      
/* Update the paid_date on the trans if it's balanced. Only updates the same 
 * trans once. */
UPDATE trans SET paid_date = load.entry_date
  FROM load
  WHERE load.trans_id = trans.trans_id
    AND trans.balance = 0
    AND load.error_msg IS NULL;

/* Update the balance on the invoice */
WITH ivs AS (
  SELECT DISTINCT trans.invoice_id
  FROM trans
  JOIN load USING(trans_id)
), b AS (
  SELECT trans.invoice_id, SUM(trans.balance) AS balance
  FROM trans
  WHERE invoice_id IN (SELECT invoice_id FROM ivs)
  GROUP BY trans.invoice_id)
UPDATE invoice SET balance = b.balance
  FROM b
  WHERE b.invoice_id = invoice.invoice_id;

SELECT * FROM load WHERE error_msg IS NOT NULL;
</%def>
<%def name="_recalc_trans_amounts()">
 /* Recalculate the transaction balance. This function needs to be
  * evaluated using a WITH expression called args with a single column trans_id
  */
 , t AS (
    SELECT args.trans_id, SUM(rebate_credit.amount) AS amount
    FROM args
    JOIN rebate_credit USING(trans_id))
 , u1 AS (
    UPDATE trans SET rebate_credit_total=t.amount
    FROM t WHERE t.trans_id=trans.trans_id)
 , u2 AS (
    UPDATE trans SET adjustments=debit_total - adjudication_total
      - writeoff_total - rebill_credit_total - rebate_credit_total
    FROM t WHERE t.trans_id=trans.trans_id)
 , u3 AS (
    UPDATE trans SET balance=total + adjustments - paid_amount
    FROM t WHERE t.trans_id=trans.trans_id)
 /* paid_date calculation */
 SELECT trans_payment.trans_id, MAX(entry_date) AS entry_date
 FROM trans_payment
 JOIN args USING(trans_id)

 SELECT trans_payment.trans_id, MAX(entry_date) AS entry_date
 FROM trans_payment
 JOIN args USING(trans_id)


 GROUP BY trans_payment.trans_id
</%def>
<%def name='cleanup()'>
DROP TABLE load;
</%def>

WITH args AS (SELECT DISTINCT trans_id FROM load)
  ${self._recalc_trans_amounts()};

