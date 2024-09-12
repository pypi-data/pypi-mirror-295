DELETE FROM drug_load WHERE ndc_number IS NULL;

UPDATE drug_load SET daily_dosage = NULL WHERE daily_dosage = '';
UPDATE drug_load SET mfg_name = '' WHERE mfg_name IS NULL;
UPDATE drug_load SET duplicate_class = NULL WHERE duplicate_class= '';
UPDATE drug_load SET generic_ndc = NULL WHERE generic_ndc = '00000000000';

INSERT INTO drug (
    ndc_number, name, brand, gpi_code, brand_ndc, generic_ndc, multisource,
    class, daily_dosage, duplicate_class, n_drug_status, mfg_name, y_drug_status)
SELECT ndc_number, name, brand, gpi_code, brand_ndc,
    generic_ndc, multisource, class, to_number(daily_dosage, '999'),
    duplicate_class, n_drug_status, mfg_name, y_drug_status
FROM drug_load AS L
ON CONFLICT (ndc_number) DO UPDATE SET
    name=EXCLUDED.name,
    brand_ndc=EXCLUDED.brand_ndc,
    generic_ndc=EXCLUDED.generic_ndc,
    multisource=EXCLUDED.multisource,
    class=EXCLUDED.class,
    daily_dosage=EXCLUDED.daily_dosage,
    duplicate_class=EXCLUDED.duplicate_class,
    n_drug_status=EXCLUDED.n_drug_status,
    mfg_name=EXCLUDED.mfg_name,
    y_drug_status=EXCLUDED.y_drug_status;
