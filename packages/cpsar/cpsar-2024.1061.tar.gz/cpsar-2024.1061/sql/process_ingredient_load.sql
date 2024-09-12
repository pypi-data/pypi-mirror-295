ALTER TABLE ingredient_load ADD COLUMN history_id BIGINT;
ALTER TABLE ingredient_load ADD COLUMN drug_id BIGINT;
ALTER TABLE ingredient_load ADD COLUMN ingredient_id BIGINT;
ALTER TABLE ingredient_load ADD COLUMN error_msg TEXT;

UPDATE ingredient_load SET history_id=history.history_id
  FROM history
  WHERE history.group_number = ingredient_load.group_number
    AND history.group_auth = ingredient_load.group_auth::int;

UPDATE ingredient_load
  SET error_msg = 'No history record for ' || group_number || ':' || group_auth
  WHERE history_id IS NULL;

UPDATE ingredient_load
  SET ingredient_id=history_ingredient.ingredient_id
  FROM history_ingredient
  WHERE history_ingredient.history_id = ingredient_load.history_id
    AND history_ingredient.ingredient_nbr = ingredient_load.ingredient_nbr::int;

UPDATE ingredient_load
  SET drug_id=drug.drug_id
  FROM drug
  WHERE ingredient_load.ndc = drug.ndc_number;

/* Set the drug_id to generic compound ingredient id when we don't have
 * a matching NDC #. Also the AWP is totally messed up on these.
 */
UPDATE ingredient_load
  SET drug_id=drug.drug_id, awp=cost_submitted
  FROM drug
  WHERE ingredient_load.drug_id IS NULL
    AND drug.ndc_number = '00000000002';

UPDATE ingredient_load SET error_msg='Could not find matching drug record'
  WHERE drug_id IS NULL;

INSERT INTO history_ingredient (
  history_id, drug_id, qty, cost_submitted, ingredient_nbr,
  cost_allowed, awp, ndc)
  SELECT history_id, drug_id, qty::numeric, cost_submitted::numeric,
      ingredient_nbr::int, cost_allowed::numeric, awp::numeric, ndc
  FROM ingredient_load
  WHERE error_msg IS NULL AND ingredient_id IS NULL;

UPDATE history_ingredient SET
    qty=I.qty::numeric,
    cost_submitted=I.cost_submitted::numeric,
    cost_allowed=I.cost_allowed::numeric,
    awp=I.awp::numeric,
    ndc=I.ndc
  FROM ingredient_load as I
  WHERE I.error_msg IS NULL
    AND I.ingredient_id = history_ingredient.ingredient_id;


/* the AWP's on the history table are wrong, we calculate them as the sum of the
 * ingredients
 */

WITH agg AS (SELECT history_id, SUM(awp) AS s FROM history_ingredient GROUP BY history_id)
UPDATE history SET awp=agg.s
FROM agg WHERE agg.history_id = history.history_id AND history.compound_code = '2';


WITH agg AS (SELECT history_id, SUM(awp) AS s FROM history_ingredient GROUP BY history_id)
UPDATE trans SET awp=agg.s
FROM agg WHERE agg.history_id = trans.history_id AND trans.compound_code = '2';
