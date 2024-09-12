/* We create invoices by finding NULL invoice id's in the trans table, creating records
 * for those.
 */

/* Invoices are created by finding all of the invoice_id's in the trans table
 * that do not have corresponding records in the invoice table */

begin;
\set ON_ERROR_STOP

-- XXX:  TESTING PURPOSES ONLY
/*
--update trans set invoice_id=null, line_no=null
--where batch_file_id = 4888;

update trans set invoice_id=null, line_no=null
where batch_file_id in (4877, 4876);
--where trans_id in (2772476, 2772477);
commit;

\a
\f ,
\o /home/jeremy/tasks/bd/19205/test-4876-4877.csv
*/
with ecm_group as (
    select '70024' as group_number
    union
    select managed_group_number
    from managed_group where group_number = '70024'
),
crs_group as (
    select '70900' as group_number
    union
    select managed_group_number
    from managed_group where group_number = '70900'

),
igroup as (
    /* Calculate the groupings key that is used to determine which transactions are on the same
     * invoice. We limit this the past year for efficency
     */
    select trans.trans_id,
    case
      -- Employeers Claim
      when trans.group_number in (select group_number from ecm_group) then
        'GRP:' || coalesce(trans.group_number, '') ||
        '|BAT:' || coalesce(trans.batch_file_id, 0) ||
        '|PCY:' || coalesce(trans.pharmacy_id, 0) ||
        '|PAT:' || coalesce(trans.patient_id, 0) ||
        '|DOC:' || coalesce(history.doctor_id, 0) ||
        '|CLM:' || coalesce(to_char(trans.doi, 'YYYYMMDD'), '')
      -- Creative Risk
      when trans.group_number in (select group_number from crs_group) then
        'GRP:' || coalesce(trans.group_number, '') ||
        '|BAT:' || coalesce(trans.batch_file_id, 0) ||
        '|PCY:' || coalesce(trans.pharmacy_id, 0) ||
        '|PAT:' || coalesce(trans.patient_id, 0) ||
        '|DOC:' || coalesce(history.doctor_id, 0) ||
        '|CLM:' || coalesce(to_char(trans.doi, 'YYYYMMDD'), '')

      -- Meadowbrook
      when trans.group_number in ('70017', '70010', '70020', '70014') then
        'GRP:' || coalesce(trans.group_number, '') ||
        '|BAT:' || coalesce(trans.batch_file_id, 0) ||
        '|PAT:' || coalesce(trans.patient_id, 0) ||
        '|CLM:' || coalesce(to_char(trans.doi, 'YYYYMMDD'), '') ||
        '|RXD:' || coalesce(to_char(trans.rx_date, 'YYYYMMDD'), '')

      -- Bridge point has invoice classes which control MCA/MSA billing
      when trans.group_number in ('70036', '70852') then
        'GRP:' || coalesce(trans.group_number, '') ||
        '|BAT:' || coalesce(trans.batch_file_id, 0) ||
        '|PAT:' || coalesce(trans.patient_id, 0) ||
        '|CLM:' || coalesce(to_char(trans.doi, 'YYYYMMDD'), '') ||
        '|RXD:' || coalesce(to_char(trans.rx_date, 'YYYYMMDD'), '') ||
        '|IVC:' || coalesce(history.inv_class, '')

      -- MPCGA wants invoice numbers to float all month
      when trans.group_number = '56500' then
        'GRP:' || coalesce(trans.group_number, '') ||
        '|BAT:' || coalesce(to_char(trans.create_date, 'YYMM'), '') ||
        '|PAT:' || coalesce(trans.patient_id, 0) ||
        '|CLM:' || coalesce(to_char(trans.doi, 'YYYYMMDD'), '')

      -- Everyone else
      else
        'GRP:' || coalesce(trans.group_number, '') ||
        '|BAT:' || coalesce(trans.batch_file_id, 0) ||
        '|PAT:' || coalesce(trans.patient_id, 0) ||
        '|DOC:' || coalesce(history.doctor_id, 0) ||
        '|CLM:' || coalesce(to_char(trans.doi, 'YYYYMMDD'), '')
      end as ikey,
      history.date_processed
    from trans
    join history using(history_id)
    where history.date_processed > CURRENT_TIMESTAMP - INTERVAL '365 DAYS'
), igroup2 as (
    /* Add the current invoice numbers and line numbers to the groupings */
    select igroup.*,
           max(invoice_id) over(partition by ikey) as invoice_id,
           max(line_no) over(partition by ikey) as line_no
    from igroup
    join trans using(trans_id)
), strans as (
    /* The transactions we need to assign invoice numbers to.
    */
    select trans.trans_id, igroup2.ikey, igroup2.date_processed
    from trans
    join igroup2 using(trans_id)
    where trans.invoice_id is null
), existing as (
    /* Create a distinct de-duped CTE with the ikey so it can be joined and not cause
     * duplicates downstream
     */
    select distinct ikey, invoice_id, line_no
    from igroup2
    where igroup2.invoice_id is not null
), continued_trans as (
    /* The existing ID's in the database that we need to continue on with those
     * same invoice numbers and line numbers.
     */

    select strans.trans_id,
           strans.ikey,
           existing.invoice_id,
--          existing.line_no as old_line_no,
--           row_number() over (partition by strans.ikey order by date_processed) as line_step,
           existing.line_no + row_number() over (partition by strans.ikey order by trans_id) as line_no
    from strans
    join existing using(ikey)
/*////////////////////////////////////////////////////////
 * Start new invoice numbers
 */
), new_invoice_id as (
    /* If we have transactions whose keys do not have an existing invoice number in
     * the trans */
    select max(invoice_id) as new_id
    from trans
    where invoice_id < 8000000
), new_trans as (
    select strans.trans_id,
           strans.ikey,
        new_id + dense_rank() over (order by strans.ikey) as invoice_id,
        row_number() over (partition by strans.ikey order by strans.trans_id) as line_no
    from (select * from strans, new_invoice_id) as strans
    left join continued_trans using(trans_id)
    where continued_trans.trans_id is null
), new_update as (
    update trans set invoice_id=new_trans.invoice_id, line_no=new_trans.line_no
      from new_trans where trans.trans_id = new_trans.trans_id)
update trans set invoice_id=continued_trans.invoice_id, line_no=continued_trans.line_no
      from continued_trans
      where trans.trans_id = continued_trans.trans_id;


--- start old logic

INSERT INTO invoice (invoice_id, group_number, batch_date, patient_id, memo,
                     due_date, total, balance, adjustments, item_count)
  SELECT 
           trans.invoice_id,
           trans.group_number,
           trans.batch_date,
           trans.patient_id,
           client.memo,
           trans.create_date + INTERVAL '1 day' * client.due_date_days as due_date,
           SUM(trans.total),
           SUM(trans.balance),
           SUM(trans.adjustments),
           COUNT(trans.trans_id)
    FROM trans
    JOIN client ON
         client.group_number = trans.group_number
    LEFT JOIN invoice ON
         trans.invoice_id = invoice.invoice_id
    WHERE invoice.invoice_id IS NULL AND
          trans.invoice_id IS NOT NULL
    GROUP BY trans.invoice_id, trans.group_number, trans.batch_date,
             trans.patient_id, client.memo, client.due_date_days,
             trans.create_date;

/* Setting invoice memos from pharmacy memos */
UPDATE invoice SET memo = pharmacy.invoice_memo
    FROM pharmacy, trans
    WHERE invoice.memo IS NULL
      AND invoice.invoice_id = trans.invoice_id
      AND trans.pharmacy_id = pharmacy.pharmacy_id
      AND pharmacy.invoice_memo IS NOT NULL;


commit;
