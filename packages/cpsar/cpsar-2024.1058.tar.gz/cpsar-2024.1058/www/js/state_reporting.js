function stateReportingSetup() {
  $("BUTTON.load_new_pending").click(onLoadNewPending);
  $("BUTTON.reset_pending").click(onResetPending);
  $("INPUT.hold").change(onHoldChange);
  $("BUTTON.unmark").click(onUnmarkClick);
}

function onResetPending() {
  document.location = "/state_reporting/reset_pending";
}

function onLoadNewPending() {
  document.location = "/state_reporting/load_new_pending";

}

function onHoldChange() {
  var $e = $(this);
  $.ajax({
    url: '/state_reporting/set_hold',
    data: {
      trans_id: $e.attr('trans'),
      reversal_id: $e.attr('reversal'),
      hold: $e.is(':checked') ? '1': '0'
    },
    type: 'POST',
    dataType: 'text'
  });
}

function onUnmarkClick() {
  var $e = $(this);
  $e.attr('trans');
  $.please_wait();
  $.ajax({
    url: '/state_reporting/unmark',
    data: {
      trans_id: $e.attr('trans'),
      hold: $e.is(':checked') ? '1': '0'
    },
    type: 'POST',
    dataType: 'text',
    success: onUnmarkSuccess.bind(this)
  });
}

function onUnmarkSuccess() {
  $.unplease_wait();
  $(this).parents("TR:first").remove();
  var $p = $("#pending_trans_count");
  $p.text(parseInt($p.text()) - 1);
}

/* Manual Bill/Entry Functionality */
function setupBillForm() {
  new CopyFromTransButton();
  new CopyFromSRIDButton();
  new DeleteLineLineItemButton();
}

function DeleteLineLineItemButton() {
    var $button = $("INPUT.delete-state-report-entry");
    console.log("HERE", $button);
    $button.click(function() {
        var $button = $(this);
        var srid = $button.attr("srid");
        document.location = "/sr_manual/delete_entry?srid=" + srid;
    });
}

function CopyFromTransButton() {
    var $button = $("INPUT.copy-from-trans");
    var $dialog = $("#copy-from-trans-dialog");
    var $sridInput = $("INPUT.srid", $dialog);

    $button.click(function() {
        var $button = $(this);
        var srid = $button.attr("srid");
        $sridInput.val(srid);
        $dialog.dialog({
            title: "Copy From Transaction",
            modal: true
        });
        return false;
    });
}

function CopyFromSRIDButton() {
    var $buttons = $("INPUT.copy-from-srid");
    var $dialog = $("#copy-from-srid-dialog");
    var $sridInput = $("INPUT.srid", $dialog);

    $buttons.click(function() {
        var $button = $(this);
        var srid = $button.attr("srid");
        console.log($button, srid);
        $sridInput.val(srid);
        $dialog.dialog({
            title: "Copy From State Report Entry",
            modal: true
        });
        return false;
    });
}


