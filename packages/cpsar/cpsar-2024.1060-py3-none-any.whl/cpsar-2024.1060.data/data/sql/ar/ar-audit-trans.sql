<%def name="create_default_arg_table()">
  CREATE TEMP TABLE strans AS SELECT trans_id FROM trans;
</%def>

-- trans.writeoff_total = SUM(trans_writeoff.amount WHERE void_date IS NULL)
<%def name="check_writeoff_total(arg_table='strans')">
  WITH calc AS (
    SELECT trans_writeoff.trans_id, COALESCE(SUM(trans_writeoff.amount), 0) AS total
    FROM trans_writeoff
    JOIN ${arg_table} USING(trans_id)
    WHERE trans_writeoff.void_date IS NULL
    GROUP BY trans_writeoff.trans_id
  )
  UPDATE trans SET writeoff_total=calc.total
  FROM calc
  WHERE calc.trans_id = trans.trans_id
    AND calc.total != trans.writeoff_total
  RETURNING trans.trans_id, calc.total;
</%def>

-- rebate.client_balance = SUM(rebate_settlement.amount) +
--                         SUM(rebate_credit.amount)
<%def name="check_rebate_client_balance()">
 WITH settle AS (
   SELECT rebate_id, SUM(amount) AS total
   FROM rebate_settlement
   GROUP BY rebate_id),
 credit AS (
   SELECT rebate_id, SUM(amount) AS total
   FROM rebate_credit
   GROUP BY rebate_id),
 calc AS (
   SELECT rebate.rebate_id, rebate.client_amount
    - COALESCE(settle.total, 0)
    - COALESCE(credit.total, 0) AS client_balance
   FROM rebate
   LEFT JOIN settle USING(rebate_id)
   LEFT JOIN credit USING(rebate_id))
 UPDATE rebate SET client_balance = calc.client_balance
 FROM calc, rebate AS old_rebate
 WHERE rebate.rebate_id = calc.rebate_id
   AND rebate.client_balance != calc.client_balance
   AND rebate.rebate_id = old_rebate.rebate_id
 RETURNING rebate.rebate_id,
           rebate.client_balance,
           old_rebate.client_balance AS old_client_balance;
</%def>

-- trans.rebate_credit_total = SUM(rebate_credit.amount)
<%def name="check_rebate_credit_total(arg_table='strans')">
  WITH calc AS (
    SELECT trans.trans_id,
           COALESCE(SUM(rebate_credit.amount), 0) AS amount
    FROM trans
    JOIN ${arg_table} USING(trans_id)
    LEFT JOIN rebate_credit USING(trans_id)
    GROUP BY trans.trans_id)
  UPDATE trans SET rebate_credit_total=calc.amount
    FROM calc
    WHERE calc.trans_id = trans.trans_id AND
          trans.rebate_credit_total != calc.amount
    RETURNING trans.trans_id, trans.rebate_credit_total;
</%def>
-- trans.debit_total = SUM(trans_debit.amount)
<%def name="check_debit_total(arg_table='strans')">
  UPDATE trans SET debit_total=calc.amount
  FROM (
    SELECT trans.trans_id,
           COALESCE(SUM(trans_debit.amount), 0) AS amount
    FROM trans
    JOIN ${arg_table} USING(trans_id)
    LEFT JOIN trans_debit
    USING(trans_id)
    GROUP BY trans.trans_id) AS calc
  WHERE calc.trans_id = trans.trans_id AND
        trans.debit_total != calc.amount
  RETURNING trans.trans_id, trans.debit_total;
</%def>
/* trans.adjustments = trans.debit_total - trans.adjudication_total
 *                   - trans.writeoff_total - trans.rebill_credit_total
 */
<%def name="check_adjustments(arg_table='strans')">
  UPDATE trans SET adjustments =
     debit_total - adjudication_total - writeoff_total - rebill_credit_total
  FROM ${arg_table}
  WHERE trans.trans_id = ${arg_table}.trans_id
    AND adjustments !=
     debit_total - adjudication_total - writeoff_total - rebill_credit_total
  RETURNING trans.trans_id, adjustments;
</%def>

/* trans.rebill_credit_total = SUM(rebill_credit.amount)
 */
<%def name="check_rebill_credit_total(arg_table='strans')">
  WITH calc AS (
    SELECT rebill_credit.trans_id,
           COALESCE(SUM(rebill_credit.amount), 0) AS total
    FROM rebill_credit
    JOIN ${arg_table} USING(trans_id)
    GROUP BY rebill_credit.trans_id
  ), stored AS (
    SELECT trans.trans_id, rebill_credit_total
    FROM trans
    JOIN ${arg_table} USING(trans_id)
  )
  UPDATE trans SET rebill_credit_total=calc.total
  FROM calc, stored
  WHERE trans.trans_id = calc.trans_id
    AND trans.trans_id = stored.trans_id
    AND trans.rebill_credit_total != calc.total
  RETURNING trans.trans_id, stored.rebill_credit_total, calc.total;
</%def>

/* trans.adjudication_total =
    SUM(trans_adjudication.amount WHERE void_date IS NULL)
 */
<%def name="check_adjudication_total(arg_table='strans')">
  WITH calc AS (
    SELECT trans_adjudication.trans_id, 
           COALESCE(SUM(trans_adjudication.amount), 0) AS total
    FROM trans_adjudication
    JOIN ${arg_table} USING(trans_id)
    WHERE void_date IS NULL
    GROUP BY trans_adjudication.trans_id
  ), stored AS (
    SELECT trans.trans_id, trans.adjudication_total
    FROM trans
    JOIN ${arg_table} USING(trans_id)
  )
  UPDATE trans SET adjudication_total = calc.total
  FROM calc, stored
  WHERE trans.trans_id = calc.trans_id
    AND trans.trans_id = stored.trans_id
    AND trans.adjudication_total != calc.total
  RETURNING trans.trans_id, stored.adjudication_total, calc.total;
</%def>

/* trans.paid_date = MAX(
        trans_payment.entry_date, 
        trans_adjudication.entry_date WHERE void_date IS NULL, 
        trans_writeoff.entry_date WHERE void_date IS NULL
        rebill_credit.entry_date WHERE void_date IS NULL
        rebate_credit.entry_date WHERE void_date IS NULL
        ) IF trans.balance = 0

  This procedure does not NULL out a paid_date once it has
  been set, but it will adjust it
 */
<%def name="check_paid_date(arg_table='strans')">
 WITH d AS (
  SELECT trans_id, entry_date::date AS entry_date
  FROM trans_payment JOIN ${arg_table} USING(trans_id)
  UNION
  SELECT trans_id, entry_date::date
  FROM trans_adjudication JOIN ${arg_table} USING(trans_id)
  WHERE void_date IS NULL
  UNION
  SELECT trans_id, entry_date::date
  FROM trans_writeoff JOIN ${arg_table} USING(trans_id)
  WHERE void_date IS NULL
  UNION
  SELECT trans_id, entry_date::date
  FROM rebill_credit JOIN ${arg_table} USING(trans_id)
  UNION
  SELECT trans_id, entry_date::date
  FROM rebate_credit JOIN ${arg_table} USING(trans_id)
  WHERE void_date IS NULL
 ), calc AS (
  SELECT trans_id, MAX(entry_date) AS entry_date
  FROM d
  GROUP BY trans_id
 )
 UPDATE trans SET paid_date=calc.entry_date
 FROM calc
 WHERE calc.trans_id=trans.trans_id
   AND trans.balance = 0
   AND trans.paid_date != calc.entry_date
 RETURNING trans.trans_id, calc.entry_date;
</%def>

<%def name="check_transfered_amount(arg_table='strans')">
  WITH calc AS (
    SELECT reversal.trans_id, SUM(group_credit.amount) AS total
    FROM ${arg_table}
    JOIN reversal USING(trans_id)
    JOIN group_credit ON reversal.reversal_id = group_credit.source_reversal_id
    GROUP BY reversal.trans_id)
  UPDATE trans SET transfered_amount=calc.total
  FROM calc
  WHERE calc.trans_id = trans.trans_id
    AND calc.total != trans.paid_amount
  RETURNING trans.trans_id, calc.total;
</%def>

<%def name="check_paid_amount(arg_table='strans')">
  WITH rebate_sum AS (
    SELECT trans_id, SUM(amount) AS amount
    FROM ${arg_table}
    JOIN rebate_credit USING(trans_id)
    WHERE void_date IS NULL
    GROUP BY trans_id),
  payment_sum AS (
    SELECT trans_id, SUM(amount) AS amount
    FROM ${arg_table}
    JOIN trans_payment USING(trans_id)
    GROUP BY trans_id),
  calc AS (
    SELECT trans_id, COALESCE(rebate_sum.amount, 0)
                   + COALESCE(payment_sum.amount, 0) AS total
    FROM ${arg_table}
    LEFT JOIN rebate_sum USING(trans_id)
    LEFT JOIN payment_sum USING(trans_id)
  )
  UPDATE trans SET paid_amount=calc.total
  FROM calc
  WHERE calc.trans_id = trans.trans_id
    AND calc.total != trans.paid_amount
  RETURNING trans.trans_id, calc.total;
</%def>

-- trans.balance = trans.total + trans.adjustments - trans.paid_amount
<%def name="check_balance(arg_table='strans')">
  UPDATE trans SET balance=total + adjustments - paid_amount
  FROM ${arg_table}
  WHERE trans.trans_id = ${arg_table}.trans_id
    AND balance != total + adjustments - paid_amount
  RETURNING trans.trans_id, total, balance
</%def>
