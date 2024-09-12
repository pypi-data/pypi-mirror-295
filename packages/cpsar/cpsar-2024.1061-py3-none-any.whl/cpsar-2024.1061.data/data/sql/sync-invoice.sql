BEGIN;

WITH orphan AS (
  SELECT DISTINCT invoice_id
  FROM trans
  WHERE NOT EXISTS (
    SELECT *
    FROM invoice
    WHERE invoice.invoice_id = trans.invoice_id)
  ),
agg AS (
  SELECT trans.invoice_id,
    SUM(adjustments) AS adjustments,
    SUM(balance) AS balance,
    SUM(total) AS total,
    COUNT(*) AS item_count,
    MAX(batch_date) AS batch_date,
    MAX(patient_id) AS patient_id,
    MAX(group_number) AS group_number,
    MAX(batch_date) + INTERVAL '15 days' AS due_date
  FROM trans
  JOIN orphan USING(invoice_id)
  GROUP BY trans.invoice_id
),
ins AS (
  INSERT INTO invoice (invoice_id, adjustments, balance,
    total, item_count, batch_date, patient_id, group_number, due_date)
  SELECT * FROM agg
  RETURNING *)

SELECT * FROM ins ORDER BY invoice_id
;

COMMIT;
