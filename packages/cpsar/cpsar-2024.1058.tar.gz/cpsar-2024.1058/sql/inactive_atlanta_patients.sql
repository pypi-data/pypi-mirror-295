/* Provide a list of patients who have not had refills on prescriptions
 * recently
 */

WITH active_patient AS (
 SELECT DISTINCT patient.*, claim.status AS claim_status,
    user_info.email AS adjuster_email
 FROM patient
 LEFT JOIN claim USING(patient_id)
 LEFT JOIN user_info ON claim.email1 = user_info.email
 WHERE patient.group_number = '58400' AND patient.status='A' AND claim.status IS NULL
), most_recent_rx AS (
 SELECT active_patient.patient_id, MAX(history.rx_date) AS rx_date
 FROM history
 JOIN active_patient USING(patient_id)
 GROUP BY active_patient.patient_id
)

SELECT active_patient.first_name,
       active_patient.last_name,
       active_patient.dob,
       active_patient.ssn AS id,
       most_recent_rx.rx_date AS last_rx_date,
       NOW() - rx_date AS days_since_rx,
       adjuster_email
FROM active_patient
LEFT JOIN most_recent_rx USING(patient_id)
WHERE most_recent_rx.rx_date IS NULL OR
      NOW() - most_recent_rx.rx_date > '45 DAYS'::interval
ORDER BY first_name;

