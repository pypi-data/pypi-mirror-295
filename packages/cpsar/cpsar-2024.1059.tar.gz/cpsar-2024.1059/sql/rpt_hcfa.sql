with
-- Common fields to both compounds and non compounds
com as (
    select client.billing_name || '|'
            || client.address_1 || '|'
            || client.city || ' '
            || client.state || ' '
            || client.zip_code as client_address,
            patient.ssn as patient_ssn,
            patient.last_name || ', ' || patient.first_name as patient_name,
            to_char(patient.dob, 'MM/DD/YYYY') as patient_dob,
            case when patient.sex = '1' then 'M'
                 when patient.sex = '2' then 'F'
                 else 'U' end as patient_sex,
            patient.address_1 as patient_address,
            patient.city as patient_city,
            patient.state as patient_state,
            patient.zip_code as patient_zip_code,
            patient.phone as patient_phone,
            claim.claim_number as claim_number,
            client.billing_name as client_billing_name,
            to_char(claim.doi, 'MM/DD/YYYY') as claim_doi,
            doctor.name as doctor_name,
            history.doctor_dea_number as doctor_dea_number,
            history.doctor_npi_number as doctor_npi_number,
            to_char(trans.rx_date, 'MM/DD/YYYY') as rx_date,
            trans.compound_code,
            trans.total as trans_total,
            history.history_id,
            trans.drug_id,
            trans.days_supply,
            trans.quantity,
            trans.trans_id,
            trans.invoice_id,
            pharmacy.npi as pharmacy_npi,
            pharmacy.name || '|' ||
                coalesce(pharmacy.address_1, '') || '|' ||
                coalesce(pharmacy.address_2, '') || '|' ||
                coalesce(pharmacy.city, '') || ' ' ||
                coalesce(pharmacy.state, '') || ' ' ||
                coalesce(pharmacy.zip_code, '') as pharmacy_address
    from trans
    join client using(group_number)
    join patient using(patient_id)
    join pharmacy using(pharmacy_id)
    join history using(history_id)
    join claim using(claim_id)
    left join doctor on history.doctor_id = doctor.doctor_id
    where trans.batch_date between ${start_date} and ${end_date}
      and trans.group_number ${gn_frag}
      % if not zero_balance_trans:
      and trans.balance != 0
      % endif
      % if first_name:
      and patient.first_name ilike ${first_name}
      % endif
      % if last_name:
      and patient.last_name ilike ${last_name}
      % endif

-- Records for both compounds and non compounds
), agg as (
    select com.*,
        'N4' || drug.ndc_number || ' UN' || quantity || ' ' || drug.name as drug_desc,
        '' as ingredient_indicator,
        trans_total::text as cost,
        quantity::int::text as form_quantity,
        0 as ingredient_id
    from com
    join drug on com.drug_id = drug.drug_id
    where com.compound_code != '2'
    union all
    select com.*,
        'N4' || drug.ndc_number || ' UN' || history_ingredient.qty || ' ' || drug.name || ' ' || com.days_supply || ' DS' as drug_desc,
        'J3490' as ingredient_indicator,
        history_ingredient.cost::text as cost,
        history_ingredient.qty::text as form_quantity,
        history_ingredient.ingredient_id
    from com
    join history_ingredient using(history_id)
    join drug on history_ingredient.drug_id = drug.drug_id
    where com.compound_code = '2'
)

select
invoice_id,
client_address as "0",                                  -- A	0	Sponsor Name and Address
'7' as "1_CHK",                                         -- B	1_CHK	Should always be "7"
patient_ssn as "1A",                                    -- C	1A	Patient ID
patient_name as "2",                                    -- D	2	Patient Name (Last Name, First Name)
patient_dob as "3_DATE",                                -- E	3_DATE	Patient DOB
patient_sex as "3_SEX",                                 -- F	3_SEX	Patient Gender
patient_name as "4",                                    -- G	4	Patient Name (Last Name, First Name)
patient_address as "5_ADDRESS",                         -- H	5_ADDRESS	Patient Address
patient_city as "5_CITY",                               -- I	5_CITY	Patient City
patient_state as "5_STATE",                             -- J	5_STATE	Patient State
patient_zip_code as "5_ZIP",                            -- K	5_ZIP	Patient Zip Code
patient_phone as "5_PHONE",                             -- L	5_PHONE	Patient Phone #
'SELF' as "6_RELATIONSHIP",                             -- M	6_RELATIONSHIP	Should always be "SELF"
patient_address as "7_ADDRESS",                         -- N	7_ADDRESS	Patient Address
patient_city as "7_CITY",                               -- O	7_CITY	Patient City
patient_state as "7_STATE",                             -- P	7_STATE	Patient State
patient_zip_code as "7_ZIP",                            -- Q	7_ZIP	Patient Zip Code
patient_phone as "7_PHONE",                             -- R	7_PHONE	Patient Phone #
'' as "9_NAME",                                         -- S	9_NAME	Leave Blank
'' as "9_A",                                            -- T	9_A	Leave Blank
'' as "9_D",                                            -- U	9_D	Leave Blank
'' as "10_CONDITION",                                   -- V	10_CONDITION	Leave Blank
'' as "10_A",                                           -- W	10_A	Leave Blank
'' as "10_B",                                           -- X	10_B	Leave Blank
'' as "10_C",                                           -- Y	10_C	Leave Blank
'' as "10_STATE",                                       -- Z	10_STATE	Leave Blank
'' as "10_D",                                           -- AA	10_D	Leave Blank
claim_number as "11",                                   -- AB	11	Patient Claim #
patient_dob as "11_A_DATE",                             -- AC	11_A_DATE	Patient DOB
patient_sex as "11_A_SEX",                              -- AD	11_A_SEX	Patient Gender
'' as "11_B_PRE",                                       -- AE	11_B_PRE	Leave Blank
'' as "11_B",                                           -- AF	11_B	Leave Blank
client_billing_name as "11_C",                          -- AG	11_C	Sponsor Name
'NO' as "11_D",                                         -- AH	11_D	Should always be "NO"
'' as "12_SIGNED",                                      -- AI	12_SIGNED	Leave Blank
'' as "12_DATE",                                        -- AJ	12_DATE	Leave Blank
'' as "13_SIGNED",                                      -- AK	13_SIGNED	Leave Blank
claim_doi as "14_DATE",                                 -- AL	14_DATE	Patient DOI
'' as "14_QUAL",                                        -- AM	14_QUAL	Leave Blank
'' as "15_QUAL",                                        -- AN	15_QUAL	Leave Blank
'' as "15_DATE",                                        -- AO	15_DATE	Leave Blank
'' as "16_DATE_FROM",                                   -- AP	16_DATE_FROM	Leave Blank
'' as "16_DATE_TO",                                     -- AQ	16_DATE_TO	Leave Blank
'DK' as "17_PRE",                                       -- AR	17_PRE	Should always be "DK"
doctor_name as "17",                                    -- AS	17	Prescribing Doctor Name (Last Name, First Name)
'' as "17_A",                                           -- AT	17_A	Leave Blank
doctor_dea_number as "17A_ADDITIONAL",                  -- AU	17A_ADDITIONAL	Prescribing Doctor DEA
doctor_npi_number as "17B_ADDITIONAL",                  -- AV	17B_ADDITIONAL	Prescribing Doctor NPI
'' as "18_DATE_FROM",                                   -- AW	18_DATE_FROM	Leave Blank
'' as "18_DATE_TO",                                     -- AX	18_DATE_TO	Leave Blank
'' as "19",                                             -- AY	19	Leave Blank
'' as "20",                                             -- AZ	20_CHK	Leave Blank
'' as "20_CHARGES",                                     -- BA	20_CHARGES	Leave Blank
'0' as "21_ICD",                                        -- BB	21_ICD	Should always be "0"
'T14.80' as "21_A",                                     -- BC	21_A	Should always be "T14.80"
'' as "21_B",                                           -- BD	21_B	Leave Blank
'' as "21_C",                                           -- BE	21_C	Leave Blank
'' as "21_D",                                           -- BF	21_D	Leave Blank
'' as "21_E",                                           -- BG	21_E	Leave Blank
'' as "21_F",                                           -- BH	21_F	Leave Blank
'' as "21_G",                                           -- BI	21_G	Leave Blank
'' as "21_H",                                           -- BJ	21_H	Leave Blank
'' as "21_I",                                           -- BK	21_I	Leave Blank
'' as "21_J",                                           -- BL	21_J	Leave Blank
'' as "21_K",                                           -- BM	21_K	Leave Blank
'' as "21_L",                                           -- BN	21_L	Leave Blank
'' as "22_CODE",                                        -- BO	22_CODE	Leave Blank
'' as "22_REF",                                         -- BP	22_REF	Leave Blank
'' as "23",                                             -- BQ	23	Leave Blank
drug_desc as "24A_1",                                   -- BR	24A_1	"Qualifier(Always N4 for NDC), NDC, Qty and Drug following format: N443386035701 UN40 HYDROCO/APAP TAB 7.5-325
rx_date as "24A_DATE_FROM",                             -- BS	24A_DATE_FROM	Date filled in MM/DD/YYYY format
rx_date as "24A_DATE_TO",                               -- BT	24A_DATE_TO	Date filled in MM/DD/YYYY format
'1' as "24_B",                                          -- BU	24_B	Should always be "1"
'' as "24_C",                                           -- BV	24_C	Leave Blank
ingredient_indicator as "24_D",                         -- BW	24_D	Leave Blank unless it's a compound ingredient, then always report "J3490"
'' as "24_MOD1",                                        -- BX	24_MOD1	Leave Blank
'' as "24_MOD2",                                        -- BY	24_MOD2	Leave Blank
'' as "24_MOD3",                                        -- BZ	24_MOD3	Leave Blank
'' as "24_MOD4",                                        -- CA	24_MOD4	Leave Blank
'' as "24_E",                                           -- CB	24_E	Leave Blank
cost as "24_F",                                         -- CC	24_F	Drug Price to Sponsor
form_quantity as "24_G",                                -- CD	24_G	Qty (No Decimals)
'' as "24_H",                                           -- CE	24_H	Leave Blank
'' as "24_I",                                           -- CF	24_I	Leave Blank
'' as "24_J",                                           -- CG	24_J	Leave Blank
pharmacy_npi as "24_J",                                 -- CH	24_J	Filling Pharmacy NPI
'631040950' as "25_TIN",                                -- CI	25_TIN	Should always be "631040950"
'' as "26",                                             -- CJ	26	Leave Blank
'YES' as "27",                                          -- CK	27	Should always be "YES"
'' as "29",                                             -- CL	29	Leave Blank
'SIG' as "31",                                          -- CM	31	Should always be "SIG"
'' as "31_DATE",                                        -- CN	31_DATE	Leave Blank
pharmacy_address as "32",                               -- CO	32	Filling Pharmacy Name and Address with each line separated by a "|"
pharmacy_npi as "32A",                                  -- CP	32A	Filling Pharmacy NPI
'' as "32B",                                            -- CQ	32B	Leave Blank
'CORPORATE PHARMACY SERVICES|P.O. BOX 1950|GADSDEN, AL 35902' as "33",
                                                        -- CR	33	Should always be "CORPORATE PHARMACY SERVICES|P.O. BOX 1950|GADSDEN, AL 35902"
'800-568-3784' as "33_PHONE",                           -- CS	33_PHONE	Should always be "800-568-3784"
'1437194933' as "33_A",                                 -- CT	33_A	Should always be "1437194933"
'' as "33_B"                                            -- CU	33_B	Leave Blank
from agg
order by trans_id, ingredient_id;
