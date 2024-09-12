WITH strans AS (
 SELECT *
 FROM trans
 WHERE patient_id=%(patient_id)s
),

/*/////////////////////////////////////////////////////////////////////////////
 * Reversal Balance As Of Calculation 
 */
trans_adjudication_as_of AS (
    SELECT reversal_id, SUM(amount) AS amount
    FROM trans_adjudication
    JOIN strans USING(trans_id)
    WHERE void_date IS NULL OR void_date > %(as_of)s
    GROUP BY reversal_id
),

reversal_settlement_as_of AS (
    SELECT reversal_id, SUM(amount) AS amount
    FROM reversal_settlement
    WHERE void_date IS NULL OR void_date > %(as_of)s
    GROUP BY reversal_id
),

reversal_as_of AS (
    SELECT reversal.reversal_id,
           reversal.group_number,
           reversal.group_auth,
           reversal.entry_date::date AS entry_date,
           reversal.trans_id,
           reversal.total,
           reversal.total
           - COALESCE(trans_adjudication_as_of.amount, 0)
           - COALESCE(reversal_settlement_as_of.amount, 0)
           AS balance
    FROM reversal
    JOIN strans USING(trans_id)
    LEFT JOIN trans_adjudication_as_of USING(reversal_id)
    LEFT JOIN reversal_settlement_as_of USING(reversal_id)
    WHERE reversal.entry_date <= %(as_of)s
),

/*/////////////////////////////////////////////////////////////////////////////
 * Overpayment Balance As Of Calculation 
 */

/* payments whose fund source is an overpayment. We can't limit it
 * to strans here because it's the overpayment's trans that is
 * limited, not the source of overpayment debit. */
overpayment_payment_as_of AS (
    SELECT puc_id, SUM(amount) AS amount
    FROM trans_payment
    WHERE puc_id IS NOT NULL
      AND entry_date::date <= %(as_of)s
    GROUP BY puc_id
),

overpayment_settlement_as_of AS (
    SELECT puc_id, SUM(amount) AS amount
    FROM overpayment_settlement
    WHERE void_date IS NULL OR
          void_date > %(as_of)s
    GROUP BY puc_id
),

overpayment_as_of AS (
    SELECT overpayment.puc_id,
           overpayment.amount,
           payment_type.type_name,
           overpayment.ref_no,
           overpayment.entry_date,
           overpayment.amount
           - COALESCE(overpayment_payment_as_of.amount, 0)
           - COALESCE(overpayment_settlement_as_of.amount, 0)
           AS balance,
           overpayment.trans_id,
           overpayment.note
    FROM overpayment
    JOIN payment_type USING(ptype_id)
    JOIN strans USING(trans_id)
    LEFT JOIN overpayment_payment_as_of USING(puc_id)
    LEFT JOIN overpayment_settlement_as_of USING(puc_id)
    WHERE overpayment.entry_date::date <= %(as_of)s
)

/*/////////////////////////////////////////////////////////////////////////////
 * Report
 */

SELECT 'R' || reversal_as_of.reversal_id AS credit_no,
       strans.rx_date,
       strans.invoice_id,
       strans.line_no,
       drug.name AS drug_name,
       reversal_as_of.entry_date,
       reversal_as_of.balance
FROM strans
JOIN drug USING(drug_id)
JOIN reversal_as_of USING(trans_id)
WHERE reversal_as_of.balance != 0 AND
  reversal_as_of.entry_date BETWEEN %(start_entry_date)s AND %(end_entry_date)s

UNION

SELECT 'P' || overpayment_as_of.puc_id AS credit_no,
       strans.rx_date,
       strans.invoice_id,
       strans.line_no,
       drug.name AS drug_name,
       overpayment_as_of.entry_date,
       overpayment_as_of.balance
FROM strans
JOIN drug USING(drug_id)
JOIN overpayment_as_of USING(trans_id)
WHERE overpayment_as_of.balance != 0 AND
  overpayment_as_of.entry_date BETWEEN %(start_entry_date)s AND %(end_entry_date)s
;
