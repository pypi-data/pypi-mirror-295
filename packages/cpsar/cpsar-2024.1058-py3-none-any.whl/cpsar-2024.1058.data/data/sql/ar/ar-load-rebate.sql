CREATE TEMP TABLE rebate_load (
    group_number VARCHAR(8),
    group_auth INT,
    total_amount DECIMAL(6, 2),
    client_amount DECIMAL(6, 2) DEFAULT 0,
    rebate_date DATE,
    trans_id BIGINT,
    error_msg TEXT);

CREATE INDEX rbl_idx ON rebate_load(group_number, group_auth);

INSERT INTO rebate_load (group_number, group_auth, total_amount,
                         rebate_date)
 VALUES ${insert_values(rebates)};

UPDATE rebate_load SET trans_id=trans.trans_id
  FROM trans
  WHERE rebate_load.group_number = trans.group_number
    AND rebate_load.group_auth = trans.group_auth;

UPDATE rebate_load SET error_msg='TX not found'
  WHERE trans_id IS NULL;

UPDATE rebate_load SET client_amount = client.trans_rebate_amount
  FROM client
  WHERE rebate_load.group_number = client.group_number
   AND client.trans_rebate_amount IS NOT NULL;

UPDATE rebate_load SET client_amount = total_amount *
    (client.trans_rebate_percent / 100)
  FROM client
  WHERE rebate_load.group_number = client.group_number
   AND client.trans_rebate_percent IS NOT NULL;

UPDATE rebate_load SET error_msg = 'Ignoring Duplicate'
  FROM (
    SELECT trans.trans_id, trans.group_number, trans.group_auth
    FROM trans JOIN rebate USING(trans_id)
  ) as r
  WHERE rebate_load.group_number = r.group_number AND rebate_load.group_auth = r.group_auth;

INSERT INTO rebate (trans_id, total_amount, client_amount, client_balance,
    rebate_date)
 SELECT trans_id, total_amount, client_amount, client_amount, rebate_date
 FROM rebate_load
 WHERE error_msg IS NULL;

SELECT * FROM rebate_load
  WHERE error_msg IS NOT NULL
  ORDER BY group_number, group_auth;
