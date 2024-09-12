<%def name="pending_trans_count()">
    select count(*)
    from trans
    where sr_mark = 'Y'
</%def>

<%def name="files_by_trans_id(offset, page_size, trans_id)">
        select state_report_file.*,
            count(distinct state_report_bill.bill_id) as bill_count,
            count(distinct state_report_entry.srid) as entry_count
        from state_report_file
        left join state_report_bill using(sr_file_id)
        join state_report_entry on state_report_entry.sr_file_id = state_report_file.sr_file_id
        where state_report_entry.trans_id = ${trans_id|e}
        group by state_report_file.sr_file_id,
                 state_report_file.status_flag,
                 state_report_file.file_name
        order by sr_file_id desc
        limit ${page_size} offset ${offset};
</%def>

<%def name="files_by_reversal_id(offset, page_size, reversal_id)">
        select state_report_file.*,
            count(distinct state_report_bill.bill_id) as bill_count,
            count(distinct state_report_entry.srid) as entry_count
        from state_report_file
        left join state_report_bill using(sr_file_id)
        join state_report_entry on state_report_entry.sr_file_id = state_report_file.sr_file_id
        where state_report_entry.reversal_id = ${reversal_id|e}
        group by state_report_file.sr_file_id,
                 state_report_file.status_flag,
                 state_report_file.file_name
        order by sr_file_id desc
        limit ${page_size} offset ${offset};
</%def>

<%def name="files(offset, page_size)">
        select state_report_file.*,
            count(distinct state_report_bill.bill_id) as bill_count,
            count(distinct state_report_entry.srid) as entry_count
        from state_report_file
        left join state_report_bill using(sr_file_id)
        left join state_report_entry on state_report_entry.sr_file_id = state_report_file.sr_file_id
        group by state_report_file.sr_file_id,
                 state_report_file.status_flag,
                 state_report_file.file_name
        order by sr_file_id desc
        limit ${page_size} offset ${offset};
</%def>

<%def name="pending_reversal_trans_count()">
    select count(*)
    from reversal
    where sr_mark = 'Y'
</%def>

<%def name="unmark_trans(trans_id)">
  update trans set sr_mark = ''
  where trans_id = ${trans_id|e};
</%def>

<%def name="pending_trans()">
    with e as (
        select trans_id, count(*) as cnt
        from state_report_entry
        where trans_id is not null
        group by trans_id)
    select trans.trans_id, patient.group_number,
           patient.first_name || ' ' || patient.last_name as patient_name,
           soj.abbr as juris,
           history.date_processed,
           now()::date - history.date_processed::date as age,
           trans.rx_number,
           trans.refill_number % 20 as refill_number,
           trans.sr_mark,
           drug.name as drug_name,
           coalesce(e.cnt, 0) as existing_report_count
    from trans
    join drug using(drug_id)
    join history using(history_id)
    join patient on history.patient_id = patient.patient_id
    join soj on patient.jurisdiction = soj.jurisdiction
    left join e on trans.trans_id = e.trans_id
    where trans.sr_mark in ('Y', 'H')
    order by history.date_processed asc
</%def>

<%def name="pending_reversals()">
    with e as (
        select reversal_id, count(*) as cnt
        from state_report_entry
        where reversal_id is not null
        group by reversal_id)
    select trans.trans_id,
           reversal.reversal_id,
           patient.group_number,
           patient.first_name || ' ' || patient.last_name as patient_name,
           soj.abbr as juris,
           reversal.reversal_date as date_processed,
           now()::date - reversal.reversal_date::date as age,
           trans.rx_number,
           trans.refill_number % 20 as refill_number,
           reversal.sr_mark,
           drug.name as drug_name,
           coalesce(e.cnt, 0) as existing_report_count
    from reversal
    join trans using(trans_id)
    join drug using(drug_id)
    join history using(history_id)
    join patient on history.patient_id = patient.patient_id
    join soj on patient.jurisdiction = soj.jurisdiction
    left join e on e.reversal_id = reversal.reversal_id
    where reversal.sr_mark in ('Y', 'H')
    order by reversal.reversal_date asc
</%def>


<%def name="load_new_pending()">
    -- set transactions whose patients are in the jurisdiction where
    -- the client is marked with state reporting that does not already
    -- have an existing production state report entry on file
    update trans set sr_mark = 'H'
    from patient, client, history
    where history.patient_id = patient.patient_id
      and trans.group_number = client.group_number
      and trans.history_id = history.history_id
      and trans.sr_mark = ''
      and history.reverse_date is null
      and history.pharmacy_payment_date is not null
      and not exists (
        select 1
        from state_report_entry
        join state_report_file using(sr_file_id)
        where trans.trans_id = state_report_entry.trans_id
          and state_report_file.status_flag = 'P')
      and (
        (send_fl_state_reporting = true and patient.jurisdiction = '09') or
        (send_or_state_reporting = true and patient.jurisdiction = '36') or
        (send_tx_state_reporting = true and patient.jurisdiction = '42')
      );

    -- Set reversals whose transactions have previously had a state report entry
    -- whose state report entry was not a test
    update reversal set sr_mark = 'H'
    from trans, patient, client, history
    where reversal.trans_id = trans.trans_id
      and trans.history_id = history.history_id
      and history.patient_id = patient.patient_id
      and trans.group_number = client.group_number
      -- has a transaction that was sent
      and exists (
        select 1
        from state_report_entry
        join state_report_file using(sr_file_id)
        where reversal.trans_id = state_report_entry.trans_id
          and state_report_file.status_flag = 'P')
      -- not already sent
      and not exists (
        select 1
        from state_report_entry
        join state_report_file using(sr_file_id)
        where reversal.reversal_id = state_report_entry.reversal_id
          and state_report_file.status_flag = 'P')
      -- not currently marked
      and reversal.sr_mark = ''
      -- in correct jurisdiction
      and (
        (send_fl_state_reporting = true and patient.jurisdiction = '09') or
        (send_or_state_reporting = true and patient.jurisdiction = '36') or
        (send_tx_state_reporting = true and patient.jurisdiction = '42')
      );
</%def>

<%def name="reset_pending()">
    update trans set sr_mark = ''
    where sr_mark = 'Y';
    update reversal set sr_mark = ''
    where sr_mark = 'Y';
</%def>

<%def name="copy_trans_to_sre(srid, trans_id)">
  update state_report_entry set
        trans_id = trans.trans_id,
        reversal_id = NULL,
        date_of_service = trans.rx_date,
        hcpcs = drug.sr_hcpcs_code,
        hcpcs_paid = drug.sr_hcpcs_code,
        ndc = drug.ndc_number,
        drug_name = drug.name,
        days_supply = trans.days_supply,
        total = trans.cost_submitted,
        sales_tax = history.sales_tax,
        state_fee = trans.state_fee,
        insurer_paid = history_total.pharmacy,
        rx_number = trans.rx_number,
        refill_number = trans.refill_number % 20,
        quantity = trans.quantity,
        eob_review_code = '90',
        daw = trans.daw,
        entry_doctor_last_name = doctor.last_name,
        entry_doctor_first_name = doctor.first_name,
        entry_doctor_npi = history.doctor_npi_number,
        entry_doctor_state_lic_number = trans.doctor_state_lic_number

  from trans
  join drug using(drug_id)
  join history using(history_id)
  join history_total using(history_id)
  left join doctor on history.doctor_id = doctor.doctor_id
  where trans.trans_id = ${trans_id|e}
    and state_report_entry.srid = ${srid|e};
</%def>
<%def name="create_send_table()">
create temp table srf as
    select 
        trans.trans_id,
        trans.group_number,
        null::bigint as reversal_id,
        trans.trans_id as record_id,
        ''::text as is_reversal,
        to_char(history.date_processed, 'YYYYMMDD') as bill_date,
        'R'::text as bill_type,
        claim.claim_number,
        trans.total::text as total,
        soj.abbr as juris,
        trans.trans_id::text as intermediary_id,
        pharmacy.nabp || '-' || trans.rx_number || '-' || trans.refill_number as bill_number,
        ''::text as unique_originator_record_id,
        coalesce(trans.sr_claim_freq_type_code, '1') as claim_freq,
        trans.sr_control_number::text as control_number,
        case when coalesce(sr_control_number, '') = '' then ''
        else
         pharmacy.nabp || '-' || trans.rx_number || '-' || trans.refill_number
        end as original_bill_number,
        client.client_name as payor_name,
        client.address_1 as payor_address_1,
        client.address_2 as payor_address_2,
        client.city as payor_city,
        client.state as payor_state,
        client.zip_code as payor_zip_code,

        to_char(history.date_processed, 'YYYYMMDD') as payor_receive_date,
        to_char(history.pharmacy_payment_date, 'YYYYMMDD') as payment_date,
        history.group_auth,
        employer.insurer_code as insurer_code_number,
        employer.tin as insurer_fein,
        client.tin as client_tin,
        patient.ssn as patient_ssn,
        patient.last_name as patient_last_name,
        patient.first_name as patient_first_name,
        to_char(patient.dob, 'YYYYMMDD') as patient_dob,
        case when patient.sex = '2' then 'F'
             when patient.sex = '1' then 'M'
             else 'U' end as patient_sex,
        case when patient.sex = '2' then '2'
             when patient.sex = '1' then '1'
             else '0' end as patient_sex_code,
        patient.address_1 as patient_address_1,
        patient.address_2 as patient_address_2,
        employer.name as insured_name,
        patient.city as patient_city,
        patient.state as patient_state,
        patient.zip_code as patient_zip_code,
        doctor.first_name as doctor_first_name,
        doctor.last_name as doctor_last_name,
        history.doctor_npi_number as doctor_npi,
        history.doctor_dea_number as doctor_dea,
        pharmacy.name as pharmacy_name,
        pharmacy.address_1 as pharmacy_address_1,
        pharmacy.address_2 as pharmacy_address_2,
        coalesce(pharmacy.address_1, '') || ' ' || coalesce(pharmacy.address_2, '') as pharmacy_address,
        'T1480'::text as principal_diagnosis_code,
        ''::text as diagnosis_code_1,
        ''::text as diagnosis_code_2,
        ''::text as diagnosis_code_3,
        ''::text as diagnosis_code_4,
        ''::text as diagnosis_code_5,
        pharmacy.city as pharmacy_city,
        pharmacy.state as pharmacy_state,
        pharmacy.zip_code as pharmacy_zip_code,
        regexp_replace(pharmacy.phone, '[^0-9]+', '', 'g') as pharmacy_phone,
        pharmacy.npi as pharmacy_npi,
        ''::text as pharmacy_state_license_number,
        pharmacy.tax_id as pharmacy_tax_id,
        to_char(claim.doi, 'YYYYMMDD') as doi,
        to_char(trans.date_written, 'YYYYMMDD') as date_written,
        pharmacy.nabp as pharmacy_nabp,
        to_char(trans.rx_date, 'YYYYMMDD') as date_of_service,
        '1'::text as line_no,
        drug.name as drug_name,
        drug.sr_hcpcs_code as hcpcs,
        drug.sr_hcpcs_code as hcpcs_paid,
        trans.quantity::int::text as quantity,
        trans.sales_tax::text as sales_tax,
        trans.state_fee::text as state_fee,
        case when trans.daw = '1' then '1'
             when trans.daw = '5' then '5'
             when trans.daw = '7' then '7'
             else '' end as no_substitution_flag,
        to_char(history_total.pharmacy, 'FM0000000.99')::text as insurer_paid,
        to_char(trans.cost_submitted, 'FM0000000.99')::text as cost_submitted,
        case when trans.compound_code = '2' then 'COMPD000000'
          else ndc_number end as ndc,
        ''::text as repackaged_ndc,
        trans.doctor_state_lic_number,
        drug.brand,
        (trans.refill_number % 20)::text as refill_number,
        trans.rx_number::text as rx_number,
        pharmacist.last_name as pharmacist_last_name,
        pharmacist.first_name as pharmacist_first_name,
        pharmacist.lic_number as pharmacist_lic_number,
        '3336C0003X'::text as pharmacist_taxonomy_code,
        coalesce(trans.daw, '0')::text as daw,
        trans.days_supply::text as days_supply,
        to_char(trans.eho_network_copay, 'FM0000000.99')::text as eho_network_copay,
        to_char(history.date_processed, 'YYYYMMDD') as date_processed,
        sr_carrier.payor_id,
        sr_carrier.carrier_fein as payor_fein,
        ''::text as date_of_admission,
        ''::text as date_of_discharge,
        doctor.last_name as entry_doctor_last_name,
        doctor.first_name as entry_doctor_first_name,
        history.doctor_npi_number as entry_doctor_npi,
        trans.doctor_state_lic_number as entry_doctor_state_lic_number,
        '90'::text as eob_review_code

    from trans
    join client using(group_number)
    join drug using(drug_id)
    join history using(history_id)
    join history_total on history.history_id = history_total.history_id
    join pharmacy on pharmacy.pharmacy_id = coalesce(history.place_of_service_id, trans.pharmacy_id)
    join patient on history.patient_id = patient.patient_id
    join claim using(claim_id)
    left join doctor on history.doctor_id = doctor.doctor_id
    left join pharmacist on history.pharmacist_id = pharmacist.pharmacist_id
    left join employer on claim.employer_tin = employer.tin
    join soj on patient.jurisdiction = soj.jurisdiction
    left join sr_carrier on patient.group_number = sr_carrier.group_number
                        and soj.abbr = sr_carrier.state
    where sr_mark = 'Y';

    insert into srf
    select 
        trans.trans_id as trans_id,
        trans.group_number,
        reversal.reversal_id as reversal_id,
        trans.trans_id as record_id,
        'Y' as is_reversal,
        to_char(reversal.reversal_date, 'YYYYMMDD') as bill_date,
        'R' as bill_type,
        claim.claim_number,
        trans.total::text as total,
        soj.abbr as juris,
        trans.trans_id::text as intermediary_id,
        pharmacy.nabp || '-' || trans.rx_number || '-' || trans.refill_number as bill_number,
        ''::text as unique_originator_record_id,
        '8' as claim_freq,
        trans.sr_control_number::text as control_number,
        case when coalesce(sr_control_number, '') = '' then ''
        else
         pharmacy.nabp || '-' || trans.rx_number || '-' || trans.refill_number
        end as original_bill_number,
        client.client_name as payor_name,
        client.address_1 as payor_address_1,
        client.address_2 as payor_address_2,
        client.city as payor_city,
        client.state as payor_state,
        client.zip_code as payor_zip_code,
        --to_char(trans.batch_date, 'YYYYMMDD') as payor_receive_date,

        to_char(reversal.reversal_date, 'YYYYMMDD') as payor_receive_date,

        to_char(history.pharmacy_payment_date, 'YYYYMMDD') as payment_date,
        history.group_auth,
        employer.insurer_code as insurer_code_number,
        employer.tin as insurer_fein,
        client.tin as client_tin,
        patient.ssn as patient_ssn,
        patient.last_name as patient_last_name,
        patient.first_name as patient_first_name,
        to_char(patient.dob, 'YYYYMMDD') as patient_dob,
        case when patient.sex = '2' then 'F'
             when patient.sex = '1' then 'M'
             else 'U' end as patient_sex,
        case when patient.sex = '2' then '2'
             when patient.sex = '1' then '1'
             else '0' end as patient_sex_code,
        patient.address_1 as patient_address_1,
        patient.address_2 as patient_address_2,
        employer.name as insured_name,
        patient.city as patient_city,
        patient.state as patient_state,
        patient.zip_code as patient_zip_code,
        doctor.first_name as doctor_first_name,
        doctor.last_name as doctor_last_name,
        history.doctor_npi_number as doctor_npi,
        history.doctor_dea_number as doctor_dea,
        pharmacy.name as pharmacy_name,
        pharmacy.address_1 as pharmacy_address_1,
        pharmacy.address_2 as pharmacy_address_2,
        coalesce(pharmacy.address_1, '') || ' ' || coalesce(pharmacy.address_2, '') as pharmacy_address,
        'T1480'::text as principal_diagnosis_code,
        ''::text as diagnosis_code_1,
        ''::text as diagnosis_code_2,
        ''::text as diagnosis_code_3,
        ''::text as diagnosis_code_4,
        ''::text as diagnosis_code_5,
        pharmacy.city as pharmacy_city,
        pharmacy.state as pharmacy_state,
        pharmacy.zip_code as pharmacy_zip_code,
        regexp_replace(pharmacy.phone, '[^0-9]+', '', 'g') as pharmacy_phone,
        pharmacy.npi as pharmacy_npi,
        ''::text as pharmacy_state_license_number,
        pharmacy.tax_id as pharmacy_tax_id,
        to_char(claim.doi, 'YYYYMMDD') as doi,
        to_char(trans.date_written, 'YYYYMMDD') as date_written,
        pharmacy.nabp as pharmacy_nabp,
        to_char(trans.rx_date, 'YYYYMMDD') as date_of_service,
        '1'::text as line_no,
        drug.name as drug_name,
        drug.sr_hcpcs_code as hcpcs,
        drug.sr_hcpcs_code as hcpcs_paid,
        trans.quantity::int::text as quantity,
        trans.sales_tax::text as sales_tax,
        trans.state_fee::text as state_fee,
        case when trans.daw = '1' then '1'
             when trans.daw = '7' then '7'
             else '' end as no_substitution_flag,
        to_char(history_total.pharmacy, 'FM0000000.99')::text as insurer_paid,
        to_char(trans.cost_submitted, 'FM0000000.99')::text as cost_submitted,
        case when trans.compound_code = '2' then 'COMPD000000'
             else drug.ndc_number end as ndc,
        ''::text as repackaged_ndc,
        trans.doctor_state_lic_number,
        drug.brand,
        (trans.refill_number % 20)::text as refill_number,
        trans.rx_number::text as rx_number,
        pharmacist.last_name as pharmacist_last_name,
        pharmacist.first_name as pharmacist_first_name,
        pharmacist.lic_number as pharmacist_lic_number,
        '3336C0003X'::text as pharmacist_taxonomy_code,
        coalesce(trans.daw, '0')::text as daw,
        trans.days_supply::text as days_supply,
        to_char(trans.eho_network_copay, 'FM0000000.99')::text as eho_network_copay,
        to_char(history.date_processed, 'YYYYMMDD') as date_processed,
        sr_carrier.payor_id,
        sr_carrier.carrier_fein as payor_fein,
        '90'::text as eob_review_code
    from reversal
    join client using(group_number)
    join trans using(trans_id)
    join drug using(drug_id)
    join history using(history_id)
    join history_total on history.history_id = history_total.history_id
    join pharmacy on pharmacy.pharmacy_id = coalesce(history.place_of_service_id, trans.pharmacy_id)
    join patient on history.patient_id = patient.patient_id
    join claim using(claim_id)
    left join doctor on history.doctor_id = doctor.doctor_id
    left join pharmacist on history.pharmacist_id = pharmacist.pharmacist_id
    join soj on patient.jurisdiction = soj.jurisdiction
    left join employer on claim.employer_tin = employer.tin
    left join sr_carrier on patient.group_number = sr_carrier.group_number
                        and soj.abbr = sr_carrier.state
    where reversal.sr_mark = 'Y';

    -- pull most recent pharmacy state license number. Issue 27595
    with m as (
        select pharmacy_npi, pharmacy_state, max(bill_id) as bill_id
        from state_report_bill
        group by pharmacy_npi, pharmacy_state
    ), m1 as (
        select state_report_bill.pharmacy_npi,
               state_report_bill.pharmacy_state,
               state_report_bill.pharmacy_state_license_number
        from state_report_bill
        join m using(bill_id)
    )
    update srf set pharmacy_state_license_number=m1.pharmacy_state_license_number
    from m1
    where srf.pharmacy_state = m1.pharmacy_state and srf.pharmacy_npi = m1.pharmacy_npi;

</%def>

<%def name="create_state_report_records(username, status_flag, file_name)">
with f as (
    insert into state_report_file (username, status_flag, file_name, send_time)
    values (${username|e}, ${status_flag|e}, ${file_name|e}, now())
    returning sr_file_id, status_flag, file_name
), i as (
    insert into state_report_entry (sr_file_id, trans_id, claim_freq_type_code, control_number)
    select f.sr_file_id, srf.trans_id, srf.claim_freq, srf.control_number
    from srf, f
    where srf.trans_id != 0
    returning trans_id, srid
), iu as (
    update srf set unique_originator_record_id = i.srid::text
    from i
    where i.trans_id = srf.trans_id
), r as (
    insert into state_report_entry (sr_file_id, reversal_id, claim_freq_type_code, control_number)
    select f.sr_file_id, srf.reversal_id, srf.claim_freq, srf.control_number
    from srf, f
    where srf.reversal_id != 0
    returning reversal_id, srid
), ru as (
    update srf set unique_originator_record_id = r.srid
    from r
    where r.reversal_id = srf.reversal_id
)
select sr_file_id from f;
</%def>

<%def name="trans()">
    select * from srf order by trans_id
</%def>

<%def name="send_record_count()">
    select count(*) from srf;
</%def>
<%def name="clear_sr_mark()">
    update trans set sr_mark = '', sr_control_number=NULL, sr_claim_freq_type_code=NULL
    from srf
    where srf.trans_id = trans.trans_id;

    update reversal set sr_mark = ''
    from srf
    where srf.reversal_id = reversal.reversal_id;
</%def>

<%def name="set_file_contents(sr_file_id, contents)">
    update state_report_file set contents = ${contents|e}
    where sr_file_id = ${sr_file_id|e};
</%def>

<%def name="drop_send_table()">
    drop table srf;
</%def>


<%def name="save_on_own_bill(sr_file_id, username)">
    ${create_send_table()}
    with
    sr_bill as (
        insert into state_report_bill (
            sr_file_id,
            trans_id,
            intermediary_id,
            bill_date,
            bill_number,
            claim_number,
            juris,
            claim_freq,
            control_number,
            insurer_code_number,
            insurer_fein,
            payor_name,
            payor_id,
            payor_fein,
            payor_address_1,
            payor_address_2,
            payor_city,
            payor_state,
            payor_zip_code,
            payor_receive_date,
            payment_date,
            patient_last_name,
            patient_first_name,
            patient_ssn,
            patient_dob,
            patient_sex,
            patient_address_1,
            patient_address_2,
            patient_city,
            patient_state,
            patient_zip_code,
            doi,
            principal_diagnosis_code,
            insured_name,
            doctor_last_name,
            doctor_first_name,
            doctor_npi,
            doctor_state_lic_number,
            pharmacist_last_name,
            pharmacist_first_name,
            pharmacist_lic_number,
            pharmacy_name,
            pharmacy_npi,
            pharmacy_nabp,
            pharmacy_address_1,
            pharmacy_address_2,
            pharmacy_city,
            pharmacy_state,
            pharmacy_zip_code,
            pharmacy_state_license_number
        )
        select
            ${sr_file_id|e},
            trans_id,
            trans_id,
            to_date(bill_date, 'YYYYMMDD'),
            bill_number,
            claim_number,
            juris,
            claim_freq,
            control_number,
            insurer_code_number,
            insurer_fein,
            payor_name,
            payor_id,
            payor_fein,
            payor_address_1,
            payor_address_2,
            payor_city,
            payor_state,
            payor_zip_code,
            to_date(payor_receive_date, 'YYYYMMDD'),
            to_date(payment_date, 'YYYYMMDD'),
            patient_last_name,
            patient_first_name,
            patient_ssn,
            to_date(patient_dob, 'YYYYMMDD'),
            patient_sex,
            patient_address_1,
            patient_address_2,
            patient_city,
            patient_state,
            patient_zip_code,
            to_date(doi, 'YYYYMMDD'),
            'T1480',
            insured_name,
            doctor_last_name,
            doctor_first_name,
            doctor_npi,
            doctor_state_lic_number,
            pharmacist_last_name,
            pharmacist_first_name,
            pharmacist_lic_number,
            pharmacy_name,
            pharmacy_npi,
            pharmacy_nabp,
            pharmacy_address_1,
            pharmacy_address_2,
            pharmacy_city,
            pharmacy_state,
            pharmacy_zip_code,
            pharmacy_state_license_number
        from srf
        returning *
    ),
    sr_entry as (
        insert into state_report_entry (
            sr_file_id,
            bill_id,
            trans_id,
            reversal_id,
            date_of_service,
            hcpcs,
            hcpcs_paid,
            ndc,
            drug_name,
            days_supply,
            total,
            sales_tax,
            state_fee,
            insurer_paid,
            rx_number,
            refill_number,
            quantity,
            eob_review_code,
            daw,
            entry_doctor_last_name,
            entry_doctor_first_name,
            entry_doctor_state_lic_number,
            entry_doctor_npi
        )
        select
            ${sr_file_id|e},
            sr_bill.bill_id,
            srf.trans_id,
            srf.reversal_id,
            to_date(srf.date_of_service, 'YYYYMMDD'),
            srf.hcpcs,
            srf.hcpcs,
            srf.ndc,
            srf.drug_name,
            srf.days_supply,
            srf.cost_submitted::numeric,
            srf.sales_tax::numeric,
            srf.state_fee::numeric,
            srf.insurer_paid::numeric,
            srf.rx_number,
            srf.refill_number,
            srf.quantity,
            srf.eob_review_code,
            srf.daw,
            srf.entry_doctor_last_name,
            srf.entry_doctor_first_name,
            srf.entry_doctor_state_lic_number,
            srf.entry_doctor_npi
        from srf
        join sr_bill on srf.trans_id = sr_bill.trans_id
        order by srf.group_auth
    ), tupdate as (
        update trans set sr_mark = ''
        from srf
        where trans.trans_id = srf.trans_id
    ), rupdate as (
        update reversal set sr_mark = ''
        from srf
        where reversal.reversal_id = srf.reversal_id
    )
    select * from sr_bill;
</%def>

<%def name="create_sr_file(file_name, status_flag, username)">
    insert into state_report_file (file_name, status_flag, username)
    values ( ${file_name |e},  ${status_flag |e}, ${username |e} )
    returning *
</%def>

<%def name="save_on_one_bill(sr_file_id, username)">
    ${create_send_table()}
    with
    sr_bill as (
        insert into state_report_bill (
            sr_file_id,
            trans_id,
            intermediary_id,
            bill_date,
            bill_number,
            claim_number,
            juris,
            claim_freq,
            control_number,
            insurer_code_number,
            insurer_fein,
            payor_name,
            payor_id,
            payor_fein,
            payor_address_1,
            payor_address_2,
            payor_city,
            payor_state,
            payor_zip_code,
            payor_receive_date,
            payment_date,
            patient_last_name,
            patient_first_name,
            patient_ssn,
            patient_dob,
            patient_sex,
            patient_address_1,
            patient_address_2,
            patient_city,
            patient_state,
            patient_zip_code,
            doi,
            principal_diagnosis_code,
            insured_name,
            doctor_last_name,
            doctor_first_name,
            doctor_npi,
            doctor_state_lic_number,
            pharmacist_last_name,
            pharmacist_first_name,
            pharmacist_lic_number,
            pharmacy_name,
            pharmacy_npi,
            pharmacy_nabp,
            pharmacy_address_1,
            pharmacy_address_2,
            pharmacy_city,
            pharmacy_state,
            pharmacy_zip_code,
            pharmacy_state_license_number
        )
        select
            ${sr_file_id|e},
            trans_id,
            trans_id,
            to_date(bill_date, 'YYYYMMDD'),
            '',
            claim_number,
            juris,
            claim_freq,
            control_number,
            insurer_code_number,
            insurer_fein,
            payor_name,
            payor_id,
            payor_fein,
            payor_address_1,
            payor_address_2,
            payor_city,
            payor_state,
            payor_zip_code,
            to_date(payor_receive_date, 'YYYYMMDD'),
            to_date(payment_date, 'YYYYMMDD'),
            patient_last_name,
            patient_first_name,
            patient_ssn,
            to_date(patient_dob, 'YYYYMMDD'),
            patient_sex,
            patient_address_1,
            patient_address_2,
            patient_city,
            patient_state,
            patient_zip_code,
            to_date(doi, 'YYYYMMDD'),
            'T1480',
            insured_name,
            doctor_last_name,
            doctor_first_name,
            doctor_npi,
            doctor_state_lic_number,
            pharmacist_last_name,
            pharmacist_first_name,
            pharmacist_lic_number,
            pharmacy_name,
            pharmacy_npi,
            pharmacy_nabp,
            pharmacy_address_1,
            pharmacy_address_2,
            pharmacy_city,
            pharmacy_state,
            pharmacy_zip_code,
            pharmacy_state_license_number
        from srf
        order by trans_id
        limit 1
        returning *
    ),
    sr_entry as (
        insert into state_report_entry (
            sr_file_id,
            bill_id,
            trans_id,
            reversal_id,
            date_of_service,
            hcpcs,
            hcpcs_paid,
            ndc,
            drug_name,
            days_supply,
            total,
            sales_tax,
            state_fee,
            insurer_paid,
            rx_number,
            refill_number,
            quantity,
            eob_review_code,
            daw,
            entry_doctor_last_name,
            entry_doctor_first_name,
            entry_doctor_state_lic_number,
            entry_doctor_npi
        )
        select
            ${sr_file_id|e},
            sr_bill.bill_id,
            srf.trans_id,
            srf.reversal_id,
            to_date(srf.date_of_service, 'YYYYMMDD'),
            srf.hcpcs,
            srf.hcpcs,
            srf.ndc,
            srf.drug_name,
            srf.days_supply,
            srf.cost_submitted::numeric,
            srf.sales_tax::numeric,
            srf.state_fee::numeric,
            srf.insurer_paid::numeric,
            srf.rx_number,
            srf.refill_number,
            srf.quantity,
            srf.eob_review_code,
            srf.daw,
            srf.entry_doctor_last_name,
            srf.entry_doctor_first_name,
            srf.entry_doctor_state_lic_number,
            srf.entry_doctor_npi
        from srf, sr_bill
        order by srf.group_auth
    ), tupdate as (
        update trans set sr_mark = ''
        from srf
        where trans.trans_id = srf.trans_id
    ), rupdate as (
        update reversal set sr_mark = ''
        from srf
        where reversal.reversal_id = srf.reversal_id
    )
    select * from sr_bill;
</%def>

<%def name="create_bsr_search(terms)">

</%def>

<%def name="create_bsr_search(terms)">
  create temp table bsr_search as
  select *,
         null::text as file_name,
         null::text as patient_first_name,
         null::text as patient_last_name
  from bishop_bsr where false;

% if terms.get('ctime'):
  insert into bsr_search
  select bishop_bsr.*, load_file.name
  from bishop_bsr
  left join load_file using(file_id)
  where
    bishop_bsr.ctime between ${'%s 00:00:00' % terms['ctime']|e} and ${'%s 23:59:59' % terms['ctime']|e};
% endif

% if terms.get('trans_id'):
  insert into bsr_search
  select bishop_bsr.*,
         load_file.name,
         state_report_bill.patient_first_name,
         state_report_bill.patient_last_name
  from bishop_bsr
  left join load_file using(file_id)
  left join state_report_bill using(bill_id)
  where bishop_bsr.trans_id = ${terms['trans_id']|e};
% endif

% if terms.get('bishop_number'):
  insert into bsr_search
  select bishop_bsr.*,
         load_file.name,
         state_report_bill.patient_first_name,
         state_report_bill.patient_last_name
  from bishop_bsr
  left join load_file using(file_id)
  left join state_report_bill using(bill_id)
  where bishop_number = ${terms['bishop_number']|e};
% endif

% if terms.get('source_ref'):
  insert into bsr_search
  select bishop_bsr.*, load_file.name,
         state_report_bill.patient_first_name,
         state_report_bill.patient_last_name
  from bishop_bsr
  left join load_file using(file_id)
  left join state_report_bill using(bill_id)
  where source_ref = ${terms['source_ref']|e};
% endif

% if terms.get('patient_last_name'):
  insert into bsr_search
  select bishop_bsr.*, load_file.name,
         state_report_bill.patient_first_name,
         state_report_bill.patient_last_name
  from bishop_bsr
  left join load_file using(file_id)
  join state_report_bill using(bill_id)
  where state_report_bill.patient_last_name ilike ${terms['patient_last_name']|e};

  insert into bsr_search
  select bishop_bsr.*, load_file.name, patient.first_name, patient.last_name
  from bishop_bsr
  left join load_file using(file_id)
  join trans using(trans_id)
  join patient on trans.patient_id = patient.patient_id
  where patient.last_name ilike ${terms['patient_last_name']|e};
% endif

% if terms.get('patient_first_name'):
  insert into bsr_search
  select bishop_bsr.*, load_file.name,
         state_report_bill.patient_first_name,
         state_report_bill.patient_last_name
  from bishop_bsr
  left join load_file using(file_id)
  join state_report_bill using(bill_id)
  where state_report_bill.patient_first_name ilike ${terms['patient_first_name']|e};

  insert into bsr_search
  select bishop_bsr.*, load_file.name, patient.first_name, patient.last_name
  from bishop_bsr
  left join load_file using(file_id)
  join trans using(trans_id)
  join patient on trans.patient_id = patient.patient_id
  where patient.first_name ilike ${terms['patient_first_name']|e};
% endif

% if terms.get('claim_number'):
  insert into bsr_search
  select bishop_bsr.*, load_file.name, 
         state_report_bill.patient_first_name,
         state_report_bill.patient_last_name
  from bishop_bsr
  left join load_file using(file_id)
  join state_report_bill using(bill_id)
  where state_report_bill.claim_number like ${terms['claim_number']|e};

  insert into bsr_search
  select bishop_bsr.*, load_file.name,
         patient.first_name,
         patient.last_name
  from bishop_bsr
  left join load_file using(file_id)
  join trans using(trans_id)
  join patient using(patient_id)
  join history using(history_id)
  join claim using(claim_id)
  where claim.claim_number like ${terms['claim_number']|e};
% endif

</%def>

