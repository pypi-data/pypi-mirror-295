
SELECT
 /* 1. Prescription / Service Reference Number Mandatory Reference number
  * assigned by the provider for the dispensed drug/product and/or service
  * provided (a.k.s. Rx Number).  Must be unique to a claim. */
  trans.rx_number,
  
 /* 2. New / Refill Code   Mandatory The code indicating whether the
  * prescription is an original or a refill. (00 = Original fill, 01-99 = Actual
  * fill number) */
  (trans.refill_number %% 20)::text,

  /* 3 Transaction Reference Number    Situational A reference number assigned
   * by the claim provider's practice management system to each of the records
   * in the batch. This number facilitates the process of matching the claim
   * response. This number should be submitted if available. */
  trans.trans_id::text,

  /* 4.  Prescription Type   Mandatory   Identifies the prescription as a
   * new/refill, adjusted, or reversed. Blank = Not Specified, '1' = New/Refill,
   * '0' = Adjusted, '1-' = Reversed */
  '1',

 /* 5.  Transaction Type    Mandatory   01 = Payment, 02 = Adjustment, 03 =
  * Rejection, 04 = Pass-thru, 05 = Capture, 06 = Out-of-Cycle Reversal, 07 =
  * In-Cycle Reversal, 08 = Pending Payment, 09 = Partial Claim Payment, 10 =
  * Partial Claim Adjustment */
  '01',

 /* 6.  Date of Service Mandatory   Date the prescription was filled */
  to_char(trans.rx_date, 'YYYYMMDD'),

 /* 7.   Patient ID Qualifier    Situational Code qualifying the "Patient ID".
  * Blank = Not Specified, 01 = Social Security Number, 02 = Driver's License
  * Number, 03 = US Military ID, 99 = Other */
 '',

 /* 8.   Patient ID  Situational ID assigned to the patient. Used to uniquely
  * identify the patient for purposes other than billing. */
 '',

 /* 9.   Person Code Situational Code assigned to a specific person within a
  * family. This code is used in conjunction with the member ID to uniquely
  * identify the family members. 001 = Cardholder, 002 = Spouse, 003-999 = Other */
 '',

 /* 10. Patient Relationship Code   Mandatory   Code indicating relationship of
  * patient to cardholder. 0 = Not specified, 1 = Cardholder, 2 = Spouse, 3 =
  * Child, 4 = Other */
 '1',

 /* 11. Patient Last Name   Situational Individual's Last Name */
 '',

 /* 12.  Patient First Name  Situational Individual's First Name */
 '',

 /* 13.  Date of Birth   Situational Date of Birth for patient */
 '',

 /* 14.  Hierarchy Level ID1 Mandatory   ID assigned by the processor to the
  * primary benefit level of grouping for the cardholder */
 trans.group_number,

 /* 15.  Product/ Service ID Mandatory   NDC Number of the drug dispensed. */
 drug.ndc_number,

 /* 16.  Drug Type   Situational Code to indicate the type of drug dispensed. 0
  * = Not Specified, 1 = Single Source Brand, 2 = Branded Generic, 3 = Generic,
  * 4 = OTC (Over The Counter) */
 '',

 /* 17.  Day's Supply    Mandatory   Estimated number of days the prescription
  * will last */
 trans.days_supply,

 /* 18.  Metric Quantity Dispensed   Mandatory   Total quantity dispensed in
  * this prescription */
 trans.quantity,

 /* 19.  Patient Pay Amount  Mandatory   Total amount paid by the patient */
 trans.eho_network_copay,

 /* 20.  Amount Billed   Mandatory   The submitted amount billed for each
  * prescription */
 trans.total,

 /* 21.  Dispense As Written (DAW) / Product Selection Code  Mandatory   Code
  * indicating whether or not the prescriber's instructions regarding generic
  * substitution were followed. 0 = No Product Selection Indicated - this is
  * the field default value that is appropriately used for prescriptions for
  * single source brand, co-branded/co-licensed, or generic products, 1 =
  * Substitution Not Allowed By Prescriber, 2 = Substitution Allowed - Patient
  * Requested Product Dispensed, 3 = Substitution Allowed - Pharmacist Selected
  * Product Dispensed, 4 = Substitution Allowed - Generic Drug Not In Stock, 5
  * = Substitution Allowed - Brand Drug Dispensed As A Generic, 6 = Override, 7
  * = Substitution Not Allowed - Brand Drug Mandated By Law, 8 = Substitution
  * Allowed - Generic Drug Not Available In Marketplace, 9 = Substitution
  * Allowed By Prescriber, But Plan Requests Brand - patient's plan requested
  * brand product to be dispensed */
 trans.daw,

 /* 22.  Prescriber ID Qualifier Mandatory   Code qualifying the "Prescriber
  * ID". 01 = National Provider ID (NPI), 02 = Blue Cross, 03 = Blue Shield, 04
  * = Medicare, 05 = Medicaid, 06 = UPIN, 07 = NCPDP Provider ID, 08 = State
  * License, 09 = Champus, 10 = Health Industry Number (HIN), 11 = Federal Tax
  * ID, 12 = Drug Enforcement Administration (DEA) Number, 13 = State Issued,
  * 14 = Plan Specific, 99 = Other */
 CASE WHEN history.doctor_npi_number IS NOT NULL THEN
        '01'
      WHEN history.doctor_dea_number IS NOT NULL THEN
        '12'
     ELSE
        ''
 END,

 /* 23.  Prescriber ID   Mandatory   ID assigned to the prescriber */
 COALESCE(history.doctor_npi_number, history.doctor_dea_number, ''),

 /* 24.  Prescriber Last Name    Optional    Prescriber Last Name */
 '',

 /* 25.  Prior Authorization Type Code   Situational Code clarifying the "Prior
  * Authorization Number Submitted" or benefit plan exemption. 0 = Not
  * Specified, 1 = Medical Certification, 2 = EPSDT (Early Periodic Screening
  * Diagnosis Treatment), 3 = Exemption form Co-Pay, 4 = Exemption from Co-Pay
  * and/or co-insurance, 5 = Family planning indicator, 6 = TANF (Temporary
  * Assistance for Needy Families), 7 = Payer defined exemption (Note: Formerly
  * known as AFDC - Aid to Families with Dependent Children), 9 = Emergency
  * Preparedness */
  '0',

 /* 26.  Prior Authorization Number  Situational Number assigned by the
  * processor to identify an authorized transaction */
  '',

 /* 27.  Compound Code   Mandatory   1 = Not a Compound, 2 = Compound
 */
  '1',

 /* 28. Pharmacy NABP field addition*/
  pharmacy.nabp,

 /* 29. Identifies the transaction as POS or Mail Order */
  CASE WHEN pharmacy.nabp = '0123682' THEN 'M'
       ELSE 'R' END,

 /* 30. Pharmacy NPI Number */
  pharmacy.npi,

 /* 31. Pharmacy Name */
  pharmacy.name

FROM trans
JOIN drug USING(drug_id)
JOIN history USING(history_id)
JOIN pharmacy ON history.pharmacy_id = pharmacy.pharmacy_id
LEFT JOIN doctor ON history.doctor_id = doctor.doctor_id
WHERE batch_date BETWEEN %(from_date)s AND %(to_date)s
    AND history.reverse_date IS NULL
    AND trans.compound_code = '1'
ORDER BY trans.group_number, trans.group_auth;
