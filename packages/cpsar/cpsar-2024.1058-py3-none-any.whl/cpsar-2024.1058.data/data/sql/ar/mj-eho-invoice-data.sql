insert into mjoseph.eho_invoice_data
  select
    substring(data from 1 for 8) as group_number,
    to_number(substring(data from 9 for 7), '9999999') as group_auth,
    substring(data from 16 for 1) as reversal_flag,
    substring(data from 17 for 7) as nabp_nbr,
    to_number(substring(data from 24 for 7), '9999999') as rx_nbr,
    to_number(substring(data from 31 for 2), '99') AS refill_nbr,
    to_date(substring(data from 33 for 6), 'YYMMDD') AS date_filled,
    to_date(substring(data from 39 for 6), 'YYMMDD') AS date_processed,
    substring(data from 45 for 11) as ndc_nbr,
    to_number(substring(data from 56 for 9), '99999.999') AS qty,
    to_number(substring(data from 65 for 10), '9999999.99') as cost,
    to_number(substring(data from 75 for 10), '9999999.99') as fee,
    to_number(substring(data from 85 for 10), '9999999.99') as sales_tax,
    to_number(substring(data from 95 for 10), '9999999.99') as copay,
    to_number(substring(data from 105 for 10), '9999999.99') as processing_fee,
    to_number(substring(data from 115 for 10), '9999999.99') as due,
    fname,
    to_date(right(fname, 6), 'YYMMDD') as batch_date
  from staging;
