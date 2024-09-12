
/* Clean up records */

delete from drug_feed where blue_diamond_mark != 'Y';

update drug_feed set dea_class = null where dea_class = '';
update drug_feed set daily_dosage = null where daily_dosage = '';

update drug_feed set error_msg='Invalid NDC #'
  where ndc_nbr !~ E'^[0-9]{11}$';

/* Discard duplicate update/inserts for the same drug */
delete from drug_feed where drug_feed_id not in (
  select max(drug_feed_id) as drug_feed_id
  from drug_feed
  group by ndc_nbr);

/* Lookup drug_id */
update drug_feed set drug_id=drug.drug_id
  from drug
  where drug_feed.error_msg is null
    and drug_feed.ndc_nbr = drug.ndc_number;

/* assigned controlled flag */
update drug_feed set controlled=true
  where error_msg is null and dea_class is not null;

/* assign brand */
update drug_feed set brand=
  case when generic_code='Y' then 'G'
       when eho_generic='Y' then 'G'
       else 'B' end
  where error_msg is null;

/* Perform Update */    
update drug set
    ndc_number=L.ndc_nbr,
    name=L.drug_name,
    brand=L.brand,
    gpi_code=L.gpi_code,
    multisource=L.multi_source,
    class=L.dea_class,
    dpc_code=L.dpc_code,
    daily_dosage=to_numeric(L.daily_dosage),
    n_drug_status=L.wc_n_drug_status,
    mtime=NOW()
  from drug_feed as L
  where L.error_msg is null and
      L.drug_id = drug.drug_id;

/* Perform Insert */
insert into drug (ndc_number, name, brand, gpi_code, multisource,
                  class, dpc_code, daily_dosage, n_drug_status)
  select ndc_nbr, drug_name, brand, gpi_code, multi_source,
         dea_class, dpc_code, to_number(daily_dosage, '999'),
         wc_n_drug_status
  from drug_feed
  where error_msg is null
    and drug_id is null;

delete from drug_feed where error_msg is null;
