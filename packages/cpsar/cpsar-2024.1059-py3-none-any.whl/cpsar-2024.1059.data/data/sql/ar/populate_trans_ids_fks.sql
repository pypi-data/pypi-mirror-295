/* Populate all of the trans_id columns across the database that need to be
 * updated when new transactions are made. */

/* Link reversals to to transactions */
UPDATE reversal SET
    trans_id=trans.trans_id, total=trans.total, balance=trans.total
  FROM trans
  WHERE reversal.trans_id IS NULL
    AND reversal.group_number = trans.group_number
    AND reversal.group_auth = trans.group_auth;

/* Link transactions to the EHO invoice data records */
UPDATE eho_invoice_data SET trans_id=trans.trans_id
  FROM trans
  WHERE eho_invoice_data.trans_id IS NULL AND
        eho_invoice_data.group_number = trans.group_number AND
        eho_invoice_data.group_auth = trans.group_auth;

