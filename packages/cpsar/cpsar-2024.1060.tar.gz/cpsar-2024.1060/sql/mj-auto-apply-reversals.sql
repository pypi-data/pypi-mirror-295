<%def name='pending_reversals()'>
    select reversal.balance,
           reversal.reversal_id,
           trans.invoice_date,
           trans.group_number,
           trans.patient_id,
           trans.rx_number,
           trans.invoice_id,
           trans.line_no
    from reversal
    join trans using(trans_id)
    join group_info on trans.group_number = group_info.group_number
    where reversal.balance != 0
      and group_info.auto_apply_reversals_flag = True;
</%def>

<%def name='pending_overpayments()'>
    select overpayment.balance,
           overpayment.overpayment_id,
           overpayment.ref_no,
           trans.invoice_date,
           trans.group_number,
           trans.patient_id,
           trans.rx_number,
           trans.invoice_id,
           trans.line_no
    from overpayment
    join trans using(trans_id)
    join group_info on trans.group_number = group_info.group_number
    where overpayment.balance != 0
      and group_info.auto_apply_overpayments_flag = true;
</%def>

<%def name='candidate_trans_for(patient_id, invoice_date)'>
  select trans.trans_id, 
         trans.balance,
         trans.patient_id,
         trans.rx_number,
         trans.group_number,
         trans.invoice_date,
         trans.invoice_id,
         trans.line_no
  from trans
  where balance != 0 and patient_id=${patient_id|e}
    and invoice_date = ${invoice_date|e}
  order by trans.trans_id
</%def>
