/* Clean up records */
UPDATE doi_formulary_load SET expiration_date=NULL
    WHERE expiration_date='000000' OR expiration_date='';
UPDATE doi_formulary_load SET effective_date=NULL
    WHERE effective_date='000000' OR effective_date='';
UPDATE doi_formulary_load SET dob=NULL WHERE dob='00000000';

UPDATE doi_formulary_load SET
  dob = replace(dob, ' ', '0'),
  effective_date = replace(effective_date, ' ', '0'),
  expiration_date = replace(expiration_date, ' ', '0');

/* find matching claims */
update doi_formulary_load set claim_id=claim.claim_id
  from claim, patient
  where claim.patient_id = patient.patient_id
    and patient.dob = to_date(doi_formulary_load.dob, 'YYYYMMDD')
    and patient.ssn = doi_formulary_load.ssn
    and patient.group_number = doi_formulary_load.group_number
    and claim.doi = to_date(doi_formulary_load.doi, 'YYYYMMDD');

update doi_formulary_load set error_msg = 'Claim not found'
  where claim_id is null;

/* find ids for updates*/
UPDATE doi_formulary_load SET doi_formulary_id=doi_formulary.doi_formulary_id
  FROM doi_formulary
  WHERE doi_formulary_load.claim_id = doi_formulary.claim_id AND
        doi_formulary_load.gpi_code = doi_formulary.gpi_code;

/* Perform Update */    
UPDATE doi_formulary SET
    drug_name=L.drug_name,
    invoice_class=L.invoice_class,
    effective_date=to_date(L.effective_date, 'YYYYMMDD'),
    expiration_date=to_date(L.expiration_date, 'YYYYMMDD'),
    drug_class=L.drug_class,
    brand_drug=L.brand_drug,
    fm_date=to_date(L.fm_date, 'YYYYMMDD'),
    fm_user_name=L.fm_user_name,
    mtime=NOW() 
  FROM doi_formulary_load as L
  WHERE L.error_msg IS NULL AND
      L.doi_formulary_id = doi_formulary.doi_formulary_id;

/* Perform Insert */
INSERT INTO doi_formulary (
        claim_id,
        gpi_code,
        drug_name,
        invoice_class,
        effective_date,
        expiration_date,
        drug_class,
        brand_drug,
        fm_date,
        fm_user_name)
SELECT 
        claim_id,
        gpi_code,
        drug_name,
        invoice_class,
        to_date(effective_date, 'YYYYMMDD'),
        to_date(expiration_date, 'YYYYMMDD'),
        drug_class,
        brand_drug,
        to_date(fm_date, 'YYYYMMDD'),
        fm_user_name
FROM doi_formulary_load as L
WHERE L.error_msg IS NULL AND L.doi_formulary_id IS NULL;
