SELECT trans.trans_id,
       trans.rx_date,
       trans.group_number,
       trans.group_auth,
       patient.first_name,
       patient.last_name,
       drug.ndc_number,
       drug.name as drug_name,
       trans.quantity,
       trans.days_supply
FROM trans
JOIN patient USING(patient_id)
JOIN drug USING(drug_id)
JOIN history USING(history_id)
WHERE history.reverse_date IS NULL
  AND history.date_processed BETWEEN ${start_date} AND ${end_date}
  AND drug.brand = 'B'
  AND trans.group_number ${gn_frag}
  AND trans_id NOT IN (
    SELECT trans_id
    FROM rebate)
  AND trans.group_number NOT IN (
    'GROUPH',
    'GROUPMJO',
    'GROUPSPL',
    'GROUPSUN',
    'HELIOS')
ORDER BY trans.trans_id;
