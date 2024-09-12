$(document).ready(function() {
    $("INPUT.datepicker").datepicker().vdate();
    $("INPUT.numeric").numeric();
    $("INPUT[name=cost_allowed]").change(onTotalDepChange);
    $("INPUT[name=dispense_fee]").change(onTotalDepChange);
    $("INPUT[name=processing_fee]").change(onTotalDepChange);
    $("INPUT[name=sales_tax]").change(onTotalDepChange);
    $("INPUT[name=eho_network_copay]").change(onTotalDepChange);
    $("INPUT[name=total]").change(onTotalChange);
    $("INPUT[name=awp]").change(onAWPChange);
    $("INPUT[name=batch_date]").change(onInvoiceDepChange);
    $("INPUT[name=patient_id]").change(onInvoiceDepChange);
    $("INPUT.pk_lookup").click(onPKLookupClick);
    $("FORM.pk_lookup").submit(onPKFormSubmit);
    $("DIV.pk_lookup").delegate("SELECT#group_number", "change", onPKFormSubmit);
    $("DIV.pk_lookup").delegate("INPUT.use_pk", "click", onUsePKClick);
    $("FORM.add").submit(onAddFormSubmit);
    $("DIV.pk_lookup").delegate("INPUT.add_patient", 'click',
      onAddPatientClick);

    onPKLookupClick();
});

function onAddPatientClick(event) {
  event.preventDefault();
  var $btn = $(this);
  var $tr = $btn.parents("TR:first");
  var $gn = $("SELECT#group_number", $("DIV.pk_lookup"));
  var rxfill_id = $("TD.rxfill_id", $tr).text();
  var group_number = $gn.val();
  $.ajax({
    url: '/import_pk/add_patient',
    data: { rxfill_id: rxfill_id, group_number: group_number},
    type: 'POST',
    dataType: 'json',
    success: onAddPatientSuccess
  });
}

function onAddPatientSuccess(data) {
  if(data.errors.length > 0) {
    for(var i=0; i<data.errors.length; i++) {
      alert(data.errors[i]);
    }
    return;
  }
  $("FORM.pk_lookup").submit();
}

function onTotalDepChange() {
    setTotal();
    onTotalChange();
}

function onTotalChange() {
    $("INPUT[name=balance]").val($("INPUT[name=total]").val());
    setSavings();
}

function onAWPChange() {
    setSavings();
}

function setTotal() {
    var v = cost_allowed() + dispense_fee() + processing_fee() + 
            sales_tax() + eho_network_copay();
    $("INPUT[name=total]").val(v.toFixed(2));
}

function setSavings() {
    var v = awp() - total();
    $("INPUT[name=savings]").val(v.toFixed(2));
}

function cost_allowed() { return _input_float_val('cost_allowed'); }
function dispense_fee() { return _input_float_val('dispense_fee'); }
function processing_fee() { return _input_float_val('processing_fee'); }
function sales_tax() { return _input_float_val('sales_tax'); }
function eho_network_copay() { return _input_float_val('eho_network_copay'); }
function awp() { return _input_float_val('awp'); }
function total() { return _input_float_val('total'); }

function _input_float_val(name) {
    var v = parseFloat($("INPUT[name=" + name + "]").val());
    return isNaN(v) ? 0.0 : v;
}

/* Invoice ID/Line Number Assigning */

function onInvoiceDepChange() {
  $.ajax({
    url: '/import_pk/lookup_invoice_id',
    data: {
      batch_date: $("INPUT[name=batch_date]").val(),
      patient_id: $("INPUT[name=patient_id]").val()
    },
    success: onInvoiceLookupSuccess,
    dataType: 'json'
  });
}

function onInvoiceLookupSuccess(data) {
  if(data.invoice_id !== undefined) {
    $("INPUT[name=invoice_id]").val(data.invoice_id);
  }
  if(data.line_no !== undefined) {
    $("INPUT[name=line_no]").val(data.line_no);
  }
}

/* PK Trans lookup */

function onPKLookupClick() {
    $("DIV.pk_lookup").dialog({
        width: "90%",
        height: 500,
        title: "PK Lookup",
        modal: true
    });
}

function onPKFormSubmit(event) {
    event.preventDefault();

    var $form = $("FORM.pk_lookup");
    $.ajax({
        url: "/import_pk/pk_lookup",
        type: "POST",
        data: $form.serialize(),
        success: onPKLookupSuccess
    });
}

function onPKLookupSuccess(data) {
    $("DIV.pk_results").html(data);
}


function onUsePKClick(event) {
    var $tr = $(event.target).parents("TR:first");
    var rxfill_id = $("TD.rxfill_id", $tr).text();
    var group_number = $("SELECT#group_number", $("DIV.pk_lookup")).val();
    $.ajax({
        method: "POST",
        url: "/import_pk/pk_data",
        data: {rxfill_id: rxfill_id, group_number: group_number},
        success: onPKDataSuccess,
        dataType: "json"
    });
}

function onPKDataSuccess(data) {
    $("INPUT[name=shipping_cost]").val(data.shipping_price);
    $("INPUT[name=pharmacy_cost]").val(data.pharmacy_cost);
    $("INPUT[name=rxfill_id]").val(data.rxfill_id);
    $("INPUT[name=doctor_dea_number]").val(data.dea);
    $("INPUT[name=doctor_name]").val(data.doctor_name);
    $("INPUT[name=group_auth]").val(data.group_auth);
    $("SELECT[name=group_number]").val(data.group_number);
    $("INPUT[name=rx_date]").val(data.fill_date);
    $("INPUT[name=rx_number]").val(data.rx_number);
    $("INPUT[name=refill_number]").val(data.refill_number);
    $("INPUT[name=date_written]").val(data.date_written);
    $("INPUT[name=daw]").val(data.daw);
    $("INPUT[name=quantity]").val(data.quantity);
    $("INPUT[name=days_supply]").val(data.days_supply);
    $("INPUT[name=cost_allowed]").val(data.patient_price);
    $("INPUT[name=cost_submitted]").val(data.patient_price);
    $("INPUT[name=patient_id]").val(data.patient_id);
    $("INPUT[name=patient_dob]").val(data.dob);
    $("INPUT[name=patient_cardholder_nbr]").val(data.ssn);
    $("INPUT[name=referring_nabp]").val(data.referring_nabp);
    $("DIV.pk_lookup").dialog("close");
    setTotal();
    onTotalChange();
    onInvoiceDepChange();
}

function onAddFormSubmit(event) {
  event.preventDefault();
  var $form = $("FORM.add");
  $.ajax({
    url: $form.attr('action'),
    type: "POST",
    data: $form.serialize(),
    success: onAddSuccess
  });
}

function onAddSuccess(data) {
  $err = $("DIV.errors");
  $err.empty();
  if(data.errors.length > 0) {
    $.each(data.errors, function (index, value){
      $err.append($("<div class='error'></div>").text(value));
    });
    return;
  }
  var t = data.trec.trans_id;
  msg = '<div class="notice"><a href="/view_trans?trans_id=' + t + '">TX #' + t + 
        ' created. Click here to view.</a></div>';
  $("DIV.errors").after($(msg));
  $("FORM.add")[0].reset();
}
