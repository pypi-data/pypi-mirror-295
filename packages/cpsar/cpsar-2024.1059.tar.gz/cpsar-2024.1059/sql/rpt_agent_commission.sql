
CREATE TEMP TABLE sdistribution AS
WITH sgroup AS (
   SELECT client.group_number, client.client_name
   FROM distribution_rule
   JOIN client USING(group_number)
   WHERE distribution_account = %(account)s
     AND client.inactive = false
   UNION
   SELECT client.group_number, client.client_name
   FROM distribution
   JOIN trans using(trans_id)
   JOIN client USING(group_number)
   WHERE distribution.distribution_date
      BETWEEN %(start_date)s AND %(end_date)s AND
     distribution.distribution_account = %(account)s
     and client.inactive = false
 ), sdistribution AS (
    SELECT distribution.*, trans.tx_type, trans.group_number
    FROM distribution
    JOIN trans USING(trans_id)
    WHERE distribution.distribution_date
      BETWEEN %(start_date)s AND %(end_date)s AND
     distribution.distribution_account = %(account)s
 )
  SELECT sdistribution.amount, sdistribution.tx_type, sdistribution.trans_id, sgroup.*
  FROM sgroup
  LEFT JOIN sdistribution USING(group_number);

CREATE TEMP TABLE report AS
  SELECT
         group_number,
         client_name,
         -- Mail Order Brand
         COUNT(DISTINCT CASE WHEN tx_type = 'MB' AND amount > 0 THEN trans_id ELSE NULL END) AS mb_count,
         SUM(CASE WHEN tx_type = 'MB' AND amount > 0 THEN amount ELSE 0 END)  AS mb_commission,

         -- Mail Order Generic
         COUNT(DISTINCT CASE WHEN tx_type = 'MG' AND amount > 0 THEN trans_id ELSE NULL END) AS mg_count,
         SUM(CASE WHEN tx_type = 'MG' AND amount > 0 THEN amount ELSE 0 END)  AS mg_commission,

         -- Retail Brand
         COUNT(DISTINCT CASE WHEN tx_type ~ '[RPWV]B' AND amount > 0 THEN trans_id ELSE NULL END) AS rb_count,
         SUM(CASE WHEN tx_type ~ '[RPWV]B' AND amount > 0 THEN amount ELSE 0 END)  AS rb_commission,

         -- Retail Generic
         COUNT(DISTINCT CASE WHEN tx_type ~ '[RPWV]G' AND amount > 0 THEN trans_id ELSE NULL END) AS rg_count,
         SUM(CASE WHEN tx_type ~ '[RPWV]G' AND amount > 0 THEN amount ELSE 0 END)  AS rg_commission,

         -- Mail Order Compounds
         COUNT(DISTINCT CASE WHEN tx_type !~ '[RPWVM][BG]' AND amount > 0 THEN trans_id ELSE NULL END) AS mo_count,
         SUM(CASE WHEN tx_type !~ '[RPWVM][BG]'  AND amount > 0 THEN amount ELSE 0 END)  AS mo_commission,

         COUNT(DISTINCT trans_id) AS trans_count,
         SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) AS commission_subtotal,

         SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END) AS reversals_and_writeoffs,
         COALESCE(SUM(amount), 0) AS commission_total
  FROM sdistribution
  GROUP BY group_number, client_name;

CREATE TEMP TABLE total AS
  SELECT
         '' as group_number, '' as client_name,
         -- Mail Order Brand
         COUNT(DISTINCT CASE WHEN tx_type = 'MB' AND amount > 0 THEN trans_id ELSE NULL END) AS mb_count,
         SUM(CASE WHEN tx_type = 'MB' AND amount > 0 THEN amount ELSE 0 END)  AS mb_commission,

         -- Mail Order Generic
         COUNT(DISTINCT CASE WHEN tx_type = 'MG' AND amount > 0 THEN trans_id ELSE NULL END) AS mg_count,
         SUM(CASE WHEN tx_type = 'MG' AND amount > 0 THEN amount ELSE 0 END)  AS mg_commission,

         -- Retail Brand
         COUNT(DISTINCT CASE WHEN tx_type ~ '[RPWV]B' AND amount > 0 THEN trans_id ELSE NULL END) AS rb_count,
         SUM(CASE WHEN tx_type ~ '[RPWV]B' AND amount > 0 THEN amount ELSE 0 END)  AS rb_commission,

         -- Retail Generic
         COUNT(DISTINCT CASE WHEN tx_type ~ '[RPWV]G' AND amount > 0 THEN trans_id ELSE NULL END) AS rg_count,
         SUM(CASE WHEN tx_type ~ '[RPWV]G' AND amount > 0 THEN amount ELSE 0 END)  AS rg_commission,

         -- Mail Order Compounds
         COUNT(DISTINCT CASE WHEN tx_type !~ '[RPWVM][BG]' AND amount > 0 THEN trans_id ELSE NULL END) AS mo_count,
         SUM(CASE WHEN tx_type !~ '[RPWVM][BG]'  AND amount > 0 THEN amount ELSE 0 END)  AS mo_commission,

         COUNT(DISTINCT trans_id) AS trans_count,
         SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) AS commission_subtotal,

         SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END) AS reversals_and_writeoffs,
         COALESCE(SUM(amount), 0) AS commission_total
  FROM sdistribution;
