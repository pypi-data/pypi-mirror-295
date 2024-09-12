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
    $("INPUT.rx_lookup").click(onRxLookupClick);
    $("FORM.rx_lookup").submit(onPKFormSubmit);
    $("DIV.rx_lookup").delegate("INPUT.load_rx", "click", onLoadRxClick);
    $("FORM.add").submit(onAddFormSubmit);
    $("DIV.rx_lookup").delegate("INPUT.add_patient", 'click',
      onAddPatientClick);
    $("DIV.rx_lookup").delegate("INPUT.add_drug", 'click',
      onAddDrugClick);

//    onRxLookupClick();
});

function onAddPatientClick(event) {
  event.preventDefault();
  var $btn = $(this);
  var $tr = $btn.parents("TR:first");
  var script_id = $("TD.script_id", $tr).text();
  $.ajax({
    url: '/import_liberty/add_script_patient',
    data: {script_id: script_id},
    type: 'POST',
    dataType: 'json',
    success: onAddPatientSuccess
  });
}

function onAddDrugClick(event) {
  event.preventDefault();
  var $btn = $(this);
  var $tr = $btn.parents("TR:first");
  var script_id = $("TD.script_id", $tr).text();
  var brand = $("SELECT.add_brand_generic", $tr).val();
  $.ajax({
    url: '/import_liberty/add_script_drug',
    data: {script_id: script_id, brand: brand},
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
  $("FORM.rx_lookup").submit();
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

function onRxLookupClick() {
    $("DIV.rx_lookup").dialog({
        width: "90%",
        height: 500,
        title: "Liberty Rx Lookup",
        modal: true
    });
}

function onPKFormSubmit(event) {
    event.preventDefault();
    var $form = $("FORM.rx_lookup");
    $.ajax({
        url: "/import_liberty/rx_lookup",
        type: "POST",
        data: $form.serialize(),
        success: onPKLookupSuccess
    });
}

function onPKLookupSuccess(data) {
    $("DIV.pk_results").html(data);
}


function onLoadRxClick(event) {
    var $tr = $(event.target).parents("TR:first");
    var script_id = $("TD.script_id", $tr).text();
    $.ajax({
        method: "POST",
        url: "/import_liberty/load_rx",
        data: {script_id: script_id},
        success: onPKDataSuccess,
        dataType: "json"
    });
}

function floatToMoney(f) {
  if(f === undefined) {
    return "0.00";
  }
  return f.toFixed(2);
}

function onPKDataSuccess(data) {
// Bill Fields
    $("INPUT[name=cost_allowed]").val(floatToMoney(data.cost_allowed));
    $("INPUT[name=dispense_fee]").val(floatToMoney(data.dispense_fee));
    $("INPUT[name=processing_fee]").val(floatToMoney(data.processing_fee));
    $("INPUT[name=sales_tax]").val(floatToMoney(data.sales_tax));
    $("INPUT[name=copay]").val(floatToMoney(data.copay));
    $("INPUT[name=awp]").val(floatToMoney(data.awp));
    $("INPUT[name=state_fee]").val(floatToMoney(data.state_fee));
// Rx/Trans Fields
    $("INPUT[name=doctor_dea_number]").val(data.dea);
    $("INPUT[name=doctor_name]").val(data.doctor_name);
    $("SELECT[name=group_number]").val(data.group_number);
    $("INPUT[name=rx_date]").val(data.rx_date);
    $("INPUT[name=rx_number]").val(data.rx_number);
    $("INPUT[name=refill_number]").val(data.refill_number);
    $("INPUT[name=date_written]").val(data.date_written);
    $("INPUT[name=daw]").val(data.daw);
    $("INPUT[name=quantity]").val(data.quantity);
    $("INPUT[name=drug_ndc_number]").val(data.ndc);
    $("SELECT[name=drug_id]").append($('<option>').val(data.drug_id).text(data.drug_id));
    $("SELECT[name=drug_id]").val(data.drug_id);
    $("INPUT[name=drug_name]").val(data.drug_name);
    $("SELECT[name=compound_code]").val(data.compound_code);

    $("DIV.tx_type").text(data.tx_type);
    $("INPUT[name=days_supply]").val(data.days_supply);
    $("INPUT[name=client_price]").val(floatToMoney(data.client_price));
    $("INPUT[name=patient_id]").val(data.patient_id);
    $("INPUT[name=patient_dob]").val(data.dob);
    $("INPUT[name=patient_cardholder_nbr]").val(data.cardholder_number);
    $("INPUT[name=referring_nabp]").val(data.referring_nabp);
    $("DIV.rx_lookup").dialog("close");

    setTotal();
    onTotalChange();
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
