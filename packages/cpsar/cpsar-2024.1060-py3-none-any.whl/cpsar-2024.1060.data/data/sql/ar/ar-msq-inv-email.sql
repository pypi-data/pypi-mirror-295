
/* Creates invoice tokens for all msqs invoices that do not have them
 * and returns those tokens
 */
set search_path=msq,public;

with unsent as (
  -- all invoices that have not been had emails sent
  select distinct
    trans.invoice_id,
    trans.group_number,
    trans_file.invoice_date,
    case when group_info.direct_invoice_email is null
         then trans.adjuster1_email
         else group_info.direct_invoice_email
    end as adjuster1_email,
    case when group_info.direct_invoice_email is null
         then trans.adjuster2_email
         else ''
    end as adjuster2_email
  from trans
  join trans_file using(trans_file_id)
  join group_info on trans.group_number = group_info.group_number
  left join invoice_token on trans.invoice_id = invoice_token.invoice_id
  where invoice_token.token is null
    and group_info.email_adjuster_direct_invoice_flag = True
--    and trans.group_number not in ('87019', '87030', '87028', '87037')
), by_email as (
  -- flattening the emails into a single column with a fallback email for
  -- those without
    select adjuster1_email as email, invoice_id, invoice_date, group_number
    from unsent
    where coalesce(adjuster1_email, '') != ''
    union
    select adjuster2_email, invoice_id, invoice_date, group_number
    from unsent
    where coalesce(adjuster2_email, '') != ''
    union
    select 'rx@medicalservicequotes.com',
           invoice_id, invoice_date, group_number
    from unsent
    where coalesce(adjuster1_email, '') = ''
      and coalesce(adjuster2_email, '') = ''
), secret as (
  -- invoice tokens to be emailed, one per invoice date and email
    select
        email,
        invoice_date,
        substring(sha1(random()::text) for 17) as token,
        group_number,
        now() + '30 days'::interval as expires
    from (select distinct email, invoice_date, group_number from by_email) t
)
, token as (
    insert into invoice_token (token, email, invoice_date, invoice_id)
        select secret.token, secret.email, secret.invoice_date, by_email.invoice_id
        from secret
        join by_email on secret.email = by_email.email
              and secret.invoice_date = by_email.invoice_date
              and secret.group_number = by_email.group_number
        returning *)
select * from secret order by email, invoice_date, group_number;

