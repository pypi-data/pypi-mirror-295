DELETE FROM trans WHERE batch_date = '2011-07-23' AND group_number = '59000'
    AND invoice_id NOT IN (318825, 318826);

/* IN 318825 */
UPDATE trans SET
    balance=total,
    paid=FALSE,
    claim_number = '11C27B936039'
WHERE invoice_id = 318825;

UPDATE patient SET
    ssn = '100100061',
    dob = '1964-02-27',
    first_name = 'OMA',
    last_name = 'LANDE',
    sex = '1',
    address_1 = '3936 W. 69TH PLACE',
    address_2 = 'Suite 1A',
    city = 'CHICAGO',
    state = 'IL',
    zip_code = '60629',
    jurisdiction = '12'
WHERE patient_id=14380;

UPDATE claim SET
   doi = '2011-09-08',
   claim_number = '11C27B936039',
   effective_date = '2011-09-09',
   expiration_date = NULL
WHERE claim_id=47670;

UPDATE adjuster SET first_name='TEST', last_name='ADJUSTER'
WHERE adjuster_id = 75;

/* IN 318826 */
UPDATE trans SET
    balance = total,
    paid = FALSE,
    claim_number = '11C27B884049'
WHERE invoice_id = 318826;
UPDATE patient SET
    ssn = '100100079',
    dob = '1964-01-24',
    first_name = 'MAR',
    last_name = 'LINDE',
    sex = '2',
    jurisdiction = '48',
    address_1 = 'W6873 S SHORE DR',
    address_2 = '',
    city = 'DELAVAN',
    state = 'WI',
    zip_code = '53115'

WHERE patient_id=13023;

UPDATE claim SET
    doi = '2011-07-12',
    claim_number = '11C27B884049',
    effective_date = '2011-07-13',
    expiration_date = NULL
WHERE claim_id=47726;

UPDATE adjuster SET first_name='TEST', last_name='ADJUSTER'
WHERE adjuster_id = 78;

UPDATE client SET
    client_name = 'CCMSI',
    billing_name = 'CCMSI',
    contact_name = 'John Grubbs',
    address_1='111 Test Rd',
    address_2 = '',
    city = 'Belton',
    state = 'TX',
    zip_code = '76502'
WHERE group_number = '59000';
