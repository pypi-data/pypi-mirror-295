$(document).ready(function() {
    var trans = trans_data();
    new Collapsable();
    new StateFeeLink();
    new EditCostAllowedLink();
    new UpdateTotalLink();
    new PharmacistOverrideButton();
    new TempStateReportNDCLink();

    new AddPaymentButton();
    new AddOverPaymentButton();
    new AdjudicateOtherTransactionButton();

    new ReverseTransButton();
    new ReverseBatchButton();

    new AddAdjudicationButton();
    var form = new AddAdjudicationForm(trans.adj_candidates);
    form.populateReversalSelect();

    new AddWriteOffButton();
    new PaymentTypeSelect();

    new AddDebitButton();
    new AddRebateCreditButton();
    new AddRebateCreditSelect();

    new VoidAdjudicationButton();
    new VoidWriteoffButton();

    new ChangeTxTypeForm();

    $("INPUT.datepicker").datepicker();

    new IngredientCostUpdateForm();

    new DoctorStateLicNumberBox();

    new RecalculateDistributionButton();

    new EditInvoiceFormButton();
});

function Collapsable() {
    var $nodes = $(".collapse");
    $nodes.click(function() {
        var body = $("TBODY", $(this).parents('TABLE'));
        var body = $("TR", body);

        if(body.css('display') === 'table-row') {
            body.css('display', 'none');
        } else {
            body.css('display', 'table-row');
        }
    });

    $nodes.click();
}

function StateFeeLink() {
    var $link = $("#state_fee_link");
    var $form = $("#state_fee_form");

    $link.click(function() {
        $form.toggle();
        return false;
    });
}


function RecalculateDistributionButton() {
  var $button = $("BUTTON.recalc");
  var trans_id = $("#trans_id").val();

  function onSuccess(html) {
    $(html).dialog({
      title: "Reprice Calculation",
      width: "90%"
    });
  }

  $button.click(function() {
    $.get("/reprice_trans?trans_id=" + trans_id, onSuccess);
  });
}

function VoidAdjudicationButton() {
    var $buttons = $("A.voida");
    var $dialog = $("#void_adjudication_form");
    var $form = $("FORM", $dialog);
    var $adjudication_id = $("INPUT.adjudication_id", $form);

    $buttons.click(function() {
        var $button = $(this);
        $adjudication_id.val($button.data("adjudication_id"));
        $dialog.dialog({
            title: "Void Adjudication",
            modal: true
        });
        return false;
    });
}

function EditInvoiceFormButton() {
    var $buttons = $(".edit-invoice");
    var $dialog = $("#edit_invoice_form");
    var $form = $("FORM", $dialog);

    $buttons.click(function() {
        var $button = $(this);
        $dialog.dialog({
            title: "Edit Invoice Number",
            modal: true
        });
        return false;
    });
}

function VoidWriteoffButton() {
    var $buttons = $("A.voidw");
    var $dialog = $("#void_writeoff_form");
    var $form = $("FORM", $dialog);
    var $writeoff_id = $("INPUT.writeoff_id", $form);

    $buttons.click(function() {
        var $button = $(this);
        $writeoff_id.val($button.data("writeoff_id"));
        $dialog.dialog({
            title: "Void Writeoff",
            modal: true
        });
        return false;
    });
}

function PharmacistOverrideButton() {
    var $link = $("#override_pharmacist_button");
    var $form = $("#override_pharmacist_form");

    $link.click(function() {
        $form.css("display", "block");
        return false;
    });
}

function TempStateReportNDCLink() {
    var $link = $("#temp_sr_ndc_override_link");
    var $form = $("#temp_sr_ndc_override_form");

    $link.click(function() {
        $link.css("display", "none");
        $form.css("display", "block");
        return false;
    });
}

function EditCostAllowedLink() {
    var $link = $("#edit_cost_allowed");
    var $form = $("#cost_allowed_form");
    $link.click(function() {
        $form.toggle();
        return false;
    });
}

function ReverseBatchButton() {
    var $link = $("A.reverse_batch");
    var $form = $("#reversal_batch_form");
    $link.click(function(e) {
        e.preventDefault();
        $form.dialog({
                modal: true,
                title: 'Add Reversal to Batch',
                width: 500
        });
    });

}


function UpdateTotalLink() {
    var $link = $("A.update_total");
    var $form = $("#total_update_form");
    $link.click(function(e) {
        e.preventDefault();
        $form.dialog({
                modal: true,
                title: 'Update total'
        });
    });
}


function ReverseTransButton() {
    var $btn = $("#reverse_trans");
    var $form = $("#reverse_trans_form");
    $btn.click(function() {
        $form.toggle();
        return false;
    });
}

function AddPaymentButton() {
    var $btn = $("#add_payment_button");
    var $form = $("#add_payment");
    $btn.click(function() {
        $form.toggle();
        return false;
    });
}

function AddOverPaymentButton() {
    var $btn = $("#add_overpayment_button");
    var $form = $("#add_overpayment");
    $btn.click(function() {
        $form.toggle();
        return false;
    });
}

function AdjudicateOtherTransactionButton() {
    var $btn = $("#adj_other_tx_button");
    var $form = $("#adj_tx");
    $btn.click(function() {
        $form.toggle();
        return false;
    });
}

function AddAdjudicationButton() {
    var $btn = $("#add_adjudication_button");
    var $form = $("#add_adjudication");
    $btn.click(function() {
        $form.toggle();
        return false;
    });
}

function AddWriteOffButton() {
    var $btn = $("#add_write_off_button");
    var $form = $("#add_writeoff");
    $btn.click(function() {
        $form.toggle();
        return false;
    });
}

function IngredientCostUpdateForm() {

    function onButtonClick(event) {
        var $row = $(this).parents("TR:first");
        var cost = $row.find("INPUT.cost").val();
        var ingredient_id = $row.find("INPUT.ingredient_id").val();
        var args = {cost: cost, ingredient_id: ingredient_id};
        $.post("/update_ingredient_cost", args, onSuccess, 'json');
    }

    function onSuccess(data) {
        if(data.errors && data.errors.length > 0) {
            showErrors(data.errors);
            return;
        }
        $.jGrowl("Cost Updated");
    }

    $("BUTTON.ingredient").click(onButtonClick);
}

function DoctorStateLicNumberBox() {
    var $box = $("#doctor_state_lic_number");
    var trans_id = $("#trans_id").val();
    function onChange(event) {
        args = {trans_id: trans_id, lic_number: $box.val()};
        $.post("/update_doctor_state_lic_number", args, onSuccess, 'json');
    }

    function onSuccess(data) {
        if(data.errors && data.errors.length > 0) {
            showErrors(data.errors);
            return;
        }
        $.jGrowl("Doctor State License Number Updated");
    }

    $box.change(onChange);
}


function AddAdjudicationForm(adj_candidates) {
    var $container = $("#add_adjudication");
    var $reversal_select = $("#adjudication_reversal_id");
    var $trans_id = $("#adjudication_trans_id");
    var $balance = $("#adjudication_balance");
    var $reversal_date = $("#adjudication_reversal_date");
    var $trans_link = $("#adjudication_trans_link");

    $reversal_select.change(function() {
        var $opt = $("OPTION:selected", $reversal_select);
        var adj = $opt.data("candidate")
        if(adj === undefined) {
            resetForm();
            return;
        }
        $trans_id.val(adj.trans_id);
        $balance.val(adj.balance.toFixed(2));
        $reversal_date.val(adj.reversal_date);

        $link = $("<a target='_blank'>View</a>");
        $link.attr("href", "/view_trans?trans_id=" + adj.trans_id);
        $trans_link.empty().append($link);
    });

    this.populateReversalSelect = function() {
        for(var i=0; i < adj_candidates.length; i++) {
            var cand = adj_candidates[i];
            var $opt = $("<option></option>");
            $opt.text(cand.trans_id);
            $opt.attr("value", cand.reversal_id);
            $opt.data("candidate", cand);
            $reversal_select.append($opt);
        }
    }

    function resetForm() {
        $trans_id.val('');
        $balance.val('');
        $reversal_date.val('');
        $trans_link.empty();
    }
}

function PaymentTypeSelect() {
    var $select = $("#add_payment_ptype_id");
    var $textbox = $("#add_payment_ref_no");
    $select.change(function() {
        var $opt = $("OPTION:selected", $select);
        $textbox.val($opt.attr("title"));
    });
}

function AddDebitButton() {
    var $btn = $("#add_debit_button");
    var $form = $("#" + $btn.attr("href"));
    $btn.click(function() {
        $form.toggle();
        return false;
    });
}

function AddRebateCreditButton() {
    var $btn = $("#add_rebate_credit");
    var $form = $("#" + $btn.attr("href"));
    $btn.click(function() {
        $form.toggle();
        return false;
    });
}

function AddRebateCreditSelect() {
    var $select = $("#add_rebate_credit_select");
    var $amount = $("#add_rebate_credit_amount");
    function onSelectChange(event) {
        var tamt = $("OPTION:selected", $select).data("amount");
        $amount.val(tamt);
    }
    $select.change(onSelectChange);
}

function ChangeTxTypeForm() {
    var $form = $("#change_tx_type");
    $form.submit(onSubmit);

    function onSubmit(event) {
        event.preventDefault();
        $.ajax({
            url: $form.attr("action"),
            type: $form.attr("method"),
            data: $form.serialize(),
            success: onSuccess,
            dataType: 'json'
        });
    }

    function onSuccess(data) {
        $("DIV.message").remove();
        $("DIV.error").remove();
        if(data.errors.length > 0) {
            $(data.errors).each(function(idx, err) {
                var $node = $("<div class='error'></div>").html(err);
                $("DIV.page_header").after($node);
            });

        } else {
            var $node = $("<div class='message'>Tx Type Changed to " + data.tx_type + "</div>");
            $("DIV.page_header").after($node);
            $("SPAN.tx_type").text(data.tx_type);
        }
    }
}
