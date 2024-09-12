/* Master script which links records across different tables relationally using
 * foreign keys. A lot of source data from COBOL has foreign keys, but the data
 * is not structured in a way to easily allow joins in SQL. Inside the COBOL
 * data there is a lot of conditional foreign key logic based on multiple
 * fields.
 */

/* Link transactions to the EHO invoice data records */
UPDATE eho_invoice_data SET trans_id=trans.trans_id
FROM trans
WHERE eho_invoice_data.trans_id IS NULL AND
      eho_invoice_data.group_number = trans.group_number AND
      eho_invoice_data.group_auth = trans.group_auth;

/* Set invoice.patient_id based on the patient_id on the trans */
UPDATE invoice SET patient_id=X.patient_id
FROM (
    SELECT DISTINCT invoice.invoice_id, trans.patient_id
    FROM invoice
    JOIN trans ON
         trans.invoice_id = invoice.invoice_id AND
         invoice.patient_id IS NULL
) AS X
WHERE invoice.invoice_id=X.invoice_id;


