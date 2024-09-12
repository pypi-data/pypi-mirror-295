$(document).ready(function() {
    // stops [] from being put on multivalue form submissions
    $.ajaxSettings.traditional = true;

    /*Set default date for the post date field on initial load.*/
    $("#entry_date").val(default_US_Date());

    /*/////////////////////////////////////////////////////////////////////////
     * Payment Information Field Events 
     */
    $("#ptype_id").change(function() {
        /* When a payment type is selected we either show the check # entry
         * box or we show the payment value on the option to the user
         */
        var $ptype_id = $("#ptype_id");
        var $ref_no = $("#ref_no");
        var $opt = $("OPTION:selected", $ptype_id);
        var default_ref_no = $opt.attr("title");
        var group_number = $opt.data("group-number");
        if(default_ref_no.length > 0) {
          $ref_no.val(default_ref_no);
        }
        if(group_number !== null) {
          $("#group_number").val(group_number);
        }
        check_payment_add_button();
    });

    $("#payment_amount").change(function() {
        check_payment_add_button();
    });

    /* When ENTER is pressed on any of the payment information fields, add 
     * the payment
     */
    $('#ref_no, #payment_amount').keypress(
      function(e) {
       var code = (e.keyCode ? e.keyCode : e.which);
       if(code == 13) { //Enter keycode
           if(check_payment_add_button()) {
               $(this).change();
               $("#add_payment_button").click();
           } else {
                var tb = $("INPUT");
                var next = tb[tb.index(this) + 1];
                if(next !== null) {
                    next.focus();
                    next.select();
                    return false;
                }
           }
       }
    });

   $("#payment_amount").currency();

    $("#add_payment_button").click(function() {
      /* When the user clicks the Add button under the payment info form, a new
       * option is added to the payment drop down at the top which can then be
       * used to apply funds. */
      var amount = get_currency_amount($("#payment_amount"));
      var $ptype_id = $("#ptype_id");

      var type_name = $("#ptype_id OPTION:selected").data("type-name");
      var ptype_id = $ptype_id.val();
      var ref_no = $("#ref_no").val();
      var caption = type_name + ": " + ref_no;

      /* Add new option to the post payment list box */
      var opt = $("<option></option>");
      opt.attr("amount", amount);
      opt.attr("total_applied", "0");
      opt.attr("value", ptype_id);
      opt.attr("type", type_name);
      opt.attr("ref_no", ref_no);
      opt.text(caption);
      $("#payment_select").append(opt);

      /* Reset payment info form */
      $ptype_id[0].selectedIndex = 0;
      $("#ref_no").val("");
      clear_currency_amount($("#payment_amount"));

      /* Select new option added */
      var len = $("#payment_select>option").length - 1;
      $("#payment_select")[0].selectedIndex = len;
      $("#payment_select").change();

      $("#invoice_id").focus();

      /* Update the last check entered display */
      var previous_trans = $("TD.previous_trans");
      var $check_display = $("<span class='ck_display'></span>");
      $check_display.text(caption + " " + format_currency(opt.attr("amount")));

      /* Limit the number of last checks displayed to 5 */
      if ($('TD.previous_trans > SPAN').length >= 5) {
          $('TD.previous_trans SPAN:first').remove();
      }
      opt.data("check_display", $check_display);
      $(previous_trans).append($check_display);
    });

    /*/////////////////////////////////////////////////////////////////////////
     * Search Parameters Field Events 
     */
    /* Only numbers allowed */
    $('#invoice_id, #invoice_line_no, #trans_group_auth').numeric();

     /* When the user is entering a hbs order number, it's always GROUPH */
    $("#hbs_order_number").numeric();
    $("#hbs_order_number").change(function() {
        $("#group_number").val("GROUPH");

    });

    /* When ENTER is pressed on any of the search fields, do the 
     * search
     */

   $('#invoice_id, #invoice_line_no, ' +
     '#patient_last_name, #patient_first_name, #trans_group_auth, ' +
     '#trans_report_code, #batch_date, #invoice_date, #rx_number, ' +
     '#payer_code, #hbs_order_number').keypress(function(e) {
       var code = (e.keyCode ? e.keyCode : e.which);
       if(code == 13) { //Enter keycode
           $(this).change();
           $("#search_button").click();
       }
   });

   /* When clicked, populate the right pane with all transactions matching
    * the criteria.
    */


   $("#search_button").click(function() {
       var args = {
            group_number: $("#group_number").val(),
            invoice_id: $("#invoice_id").val(),
            invoice_line_no: $("#invoice_line_no").val(),
            group_auth: $("#trans_group_auth").val(),
            rx_number: $("#rx_number").val(),
            payer_code: $("#payer_code").val(),
            report_code: $("#trans_report_code").val(),
            batch_date: $("#batch_date").val(),
            invoice_date: $("#invoice_date").val(),
            patient_last_name: $("#patient_last_name").val(),
            patient_first_name: $("#patient_first_name").val(),
            hbs_order_number: $("#hbs_order_number").val()
        };

        $.please_wait();
        $.get("/ppayment/trans_search", args, function(data) {
            if($("#group_number").val().length === 0 &&
               $("#invoice_id").val().length > 0 &&
               data.transactions.length > 0) {
               $("#group_number").val(data.transactions[0].group_number).change();
            }

            var post_table = $("#post_table").remove();
            /* Remove rows that don't have any monies applied to them from the
             * transaction list to make room for the search results
             */
            $("TBODY TR.transdata", post_table).each(function() {
                var elem = $(this);
                if(!(elem.data("applied") > 0)) {
                    elem.remove();
                }
            });
            /* Add all the search results to the transaction table */
            for(var x = 0; x < data.transactions.length; x++) {
                build_tx_row(post_table, data.transactions[x]);
            }

            $("#transaction_container").prepend(post_table);

            /* Focus on the first amount entry box */
            var tb = $("INPUT.amount");
            var next = tb[1];
            if(next !== undefined) {
                next.focus();
                next.select();
            }

            $.unplease_wait();
        }, 'json');

        $.get("/ppayment/unapplied_cash_search", args, function(data) {
            /* Removed unused unapplied cash records */
            $("#payment_select > OPTION").each(function() {
                var e = $(this);
                if(get_currency_amount(e, 'total_applied') === 0 &&
                   e.attr('type') === 'UC') {
                    e.remove();
                }
            });

            /* Add new unapplied cash records from search */
            var options = Array();
            for(var i = 0; i < data.records.length; i++) {
                var rec = data.records[i];
                var opt = $("<option></option>");
                opt.attr("amount", rec.balance);
                opt.attr("total_applied", "0");
                opt.attr("value", rec.ptype_id);
                opt.attr("ref_no", rec.ref_no);
                opt.attr("puc_id", rec.puc_id);
                opt.attr("type", rec.type_name);
                opt.attr("reversal_id", rec.reversal_id);
                switch(rec.type_name) {
                case "GROUPC":
                  opt.text("Group Credit: " + rec.group_number);
                  break;
                case "REV":
                  opt.text("Reversal: "
                      + rec.first_name + " " + rec.last_name
                      + " " + rec.ref_no);
                  break;
                default:
                  opt.text(rec.group_number + " - "
                      + rec.first_name + " " + rec.last_name
                      + " " + rec.type_name + ": " + rec.ref_no);
                }
                options.push(opt);
            }

            var selectBox = document.getElementById("payment_select");
            options.sort(function(a, b) {
              return a.text().localeCompare(b.text());
            });
            //selectBox.innerHTML = "";
            options.forEach(function(o) {
              selectBox.add(o[0]);
            });

        }, 'json');

   });

    /*/////////////////////////////////////////////////////////////////////////
     * Payment Management Controls
     */
    $("#payment_select").change(function() {
        var opt = $('#payment_select>option:selected');
        var amount = get_currency_amount(opt, "amount");
        var total_applied = get_currency_amount(opt, "total_applied");
        var left_to_apply = amount - total_applied;

        set_currency_amount($("#current_amount"), amount);
        set_currency_amount($("#current_total_applied"), total_applied);
        set_currency_amount($("#current_left_to_apply"), left_to_apply);

        check_remove_payment_button();
    });

    $("#remove_payment_button").click(function() {
        var $check_display = $('#payment_select>option:selected').data(
                                "check_display");
        if($check_display !== undefined) {
          $check_display.remove();
        }
        $('#payment_select>option:selected').remove();
        set_currency_amount($("#current_amount"), 0);
        set_currency_amount($("#current_left_to_apply"), 0);
        check_remove_payment_button();
    });

    $("#use_payment_button").click(function() {
        /* Go through each transaction applying monies until there is none
         * left.
         */
        $("TBODY TR.transdata").each(function() {
            if(get_currency_amount($("#current_left_to_apply")) === 0) {
                return;
            }
            var applied = $(this).data("applied");
            var elem = $("INPUT.amount", $(this));
            var balance = get_currency_amount($(".balance", $(this)));
            if(applied !== balance) {
                set_currency_amount(elem, balance);
                elem.change();
            }
        });
    });
    $("#remove_payment_button").disable();

   /*/////////////////////////////////////////////////////////////////////////
    * Top Payment Bar Events & Setup
    */

   $("#current_amount").currency();
   $("#current_amount").readonly(true);

   $("#current_left_to_apply").currency();
   $("#current_left_to_apply").readonly(true);
   set_currency_amount($("#current_left_to_apply"), 
                       get_currency_amount($("#payment_amount")));
   $("#current_total_applied").currency();
   $("#current_total_applied").readonly(true);
   set_currency_amount($("#current_total_applied"), 0);

   $("#reset_button").click(function()
   {
        $("#ref_no").val("");
        $("#ptype_id")[0].selectedIndex = 0;

        clear_currency_amount($("#payment_amount"));

        $("#hbs_order_number").val("");
        $("#group_number").val("");
        $("#group_number").readonly(false);
        $("#patient_last_name").val("");
        $("#patient_first_name").val("");
        $("#invoice_id").val("");
        $("#invoice_line_no").val("");
        $("#trans_group_auth").val("");
        $("#rx_number").val("");
        $("#payer_code").val("");

        clear_currency_amount($("#current_amount"));
        clear_currency_amount($("#current_left_to_apply"));
        clear_currency_amount($("#current_total_applied"));
        $("TABLE.payment TBODY").empty();

        $("#payment_select > OPTION").each(function() {
            if($(this).attr("amount") !== undefined) {
                $(this).remove();
            }
        });
   });

   $("#post_button").click(function() {
        var form = {
            ptype_id: [],     // ptype_id
            ref_no: [],         
            trans_id: [],     // transaction payment applied to
            entry_date: [],   // when to post the payment for
            amount: [],       // how much to post the payment for
            overpayment: [],  // Is this an overpayment or a payment?
            puc_id: [],       // source of funds if it is a previous overpayment
            reversal_id: [],  // source of funds if it is a reversal
            type: []          // The type of funds that it is
        };

        /* Build a review box */
        var doc = $("<div class='or'><h3>Please Review</h3>" 
            + "<div class='review'><table class='review'></table></div>" 
            + "<center><input class='post' id='send_post_button' type='button' value='POST' />" 
            + "</center></div>");

        /* Build up all the payment transactions, adding to the form and
         * creating UI elements
         */
        $("TBODY TR.payment_line").each(function() {
            var $payment_row = $(this);
            
            /* Data stored on the transaction row located above the payment
             * row */
            var $trans_node = $payment_row.data('trans_node');
            var patient_id = $trans_node.attr('patient_id');
            var first_name = $(".patient_first_name", $trans_node).text();
            var last_name = $(".patient_last_name", $trans_node).text();
            var invoice_ref = $(".invoice_ref", $trans_node).text();
            var trans_id = $trans_node.attr("trans_id");
            var balance = get_currency_amount($("span.balance", $trans_node));

            /* Data stored on the payment option from #payment_select */
            var $payment_opt = $payment_row.data("payment_option");
            var ptype_id = $payment_opt.attr("value");
            var caption = $payment_opt.text();
            var type = $payment_opt.attr("type");
            var ref_no = $payment_opt.attr("ref_no") || "";
            var puc_id = $payment_opt.attr("puc_id") || "";
            var reversal_id = $payment_opt.attr("reversal_id") || "";

            console.log($payment_opt, ref_no);

            /* Data stored on the payment row itself */
            var amt = get_currency_amount($payment_row);  
            var entry_date = $payment_row.data("entry_date");

            var overpayment_amount = amt - balance;
            var applied_amt;

            if (amt <= balance ) {
                applied_amt = amt;
            } else {
                applied_amt = balance;
            }

            var applied_amt_fmt = format_currency(applied_amt);
            var review_row_html = "<tr><td>" + caption + "</td><td>"
              + applied_amt_fmt + "</td><td>" + first_name + " " + last_name
              + "</td><td>" + "inv #" + invoice_ref + "</td><td>" + entry_date
              + "</td></tr>";

            append(form.ptype_id, ptype_id);
            append(form.ref_no, ref_no);
            append(form.trans_id, trans_id);
            append(form.entry_date, entry_date);
            append(form.amount, applied_amt);
            append(form.overpayment, "N");
            append(form.puc_id, puc_id);
            append(form.reversal_id, reversal_id);
            append(form.type, type);

            /* Adding an overpayment checking logic. The puc_id check is
             * because you can't post an overpayment from a previous overpayment
            */ 
            if (amt > balance && puc_id === '' && reversal_id === '') {
                var op_fmt = format_currency(overpayment_amount);
                var op_caption = caption + " Over Payment";
                review_row_html +=
                    "<tr><td>" + op_caption + "</td><td>" 
                    + op_fmt + "</td><td>" + first_name + " " 
                    + last_name + "</td><td>" + "inv #" + invoice_ref 
                    + "</td><td>" + entry_date + "</td></tr>";

                append(form.ptype_id, ptype_id);
                append(form.ref_no, ref_no);
                append(form.trans_id, trans_id);
                append(form.entry_date, entry_date);
                append(form.amount, overpayment_amount);
                append(form.overpayment, "Y");
                append(form.puc_id, "");
                append(form.reversal_id, "");
                append(form.type, "OP");
            }
            $("table", doc).append(review_row_html);
        });


        $(".post", doc).click(function() {
            $.post("/ppayment/post", form, function(data) {
                if(data.errors.length) {
                    jQuery.facebox(data.errors + "");
                } else {
                    jQuery(document).trigger('close.facebox')
                    $("#reset_button").click();
                    $("#ref_no").focus();
                }
            }, 'json');
        });
        jQuery.facebox(doc);
        $("#send_post_button").focus();
   });

   check_payment_add_button();

   $("#ref_no").focus();

   /* If we have some search parameter then go ahead and search */
   if($("#invoice_id").val().length > 0 ||
      $("#group_number").val().length > 0 ||
      $("#patient_last_name").val().length > 0 ||
      $("#patient_first_name").val().length > 0 ||
      $("#rx_number").val().length > 0 ||
      $("#payer_code").val().length > 0 ||
      $("#trans_group_auth").val().length > 0) {
        $("#search_button").click();
   }

});

/*/////////////////////////////////////////////////////////////////////////
 * New Element Building Procedures
 */
function build_tx_row(post_table, data) {
    var row = $("#trans_row_tmpl", post_table).clone();
    var tbody = $("TBODY", post_table);
    row.removeAttr("id");
    row.attr("trans_id", data.trans_id);
    row.attr("patient_id", data.patient_id);
    $(".rx_date", row).text(data.rx_date);
    $(".batch_date", row).text(data.batch_date);
    $(".invoice_ref", row).text(data.invoice_id + "-" + data.line_no);
    $(".rx_number", row).text(data.rx_number);
    $(".payer_code", row).text(data.payer_code);
    $(".group_ref", row).text(data.group_number + "-" + data.group_auth);
    $(".patient_first_name", row).text(data.patient_first_name);
    $(".patient_last_name", row).text(data.patient_last_name);
    $(".drug_name", row).text(data.drug_name);
    $(".balance", row).text((data.balance/100).toFixed(2));
    $(".balance", row).attr("amount", data.balance);
    $(".applied", row).readonly(true);
    $(".applied", row).currency();

    $(".amount", row).focus(function() {
        $(this).select();
    });

    $(".patient_first_name, .patient_last_name, .drug_name", row).click(
        function() {
         window.open("/view_trans?trans_id=" + data.trans_id);
        });

    row.css("display", "table-row");
    $(".blue_button", row).css("display", "none");
    tbody.append(row);

    $(".amount", row).currency();
    $(".amount", row).keypress(function(e) {
       var code = (e.keyCode ? e.keyCode : e.which);
       if(code == 13 || code == 9) { //Enter or tab keycode
            var tb = $("INPUT.amount");
            var next = tb[tb.index(this) + 1];
            if(next !== undefined) {
                next.focus();
                next.select();
                return false;
            }
       }
    });

    $(".round_button", row).click(function() {
        var bal = get_currency_amount($(".balance", row));
        var applied = get_currency_amount($(".applied", row));
        var outstanding = 0;
        if (applied === 0){
            outstanding = bal;
        }
        var amt_node = $(".amount", row);
        set_currency_amount(amt_node, outstanding);
        amt_node.change();
    });

    $(".amount", row).change(function() {
        var elem = $(this);
        var row = $(this).parents("TR");
        var opt = $('#payment_select>option:selected');
        var $entry_date = $('#entry_date').val();

        /*set date value for payment lines */
        if ($entry_date === "" || $entry_date === null 
            || $entry_date === undefined) {
            $entry_date = default_US_Date();
        }   

        /* Remove any pre-existing payment line for this particular
         * payment because we are going to replace it (or leave it
         * deleted)
         */
        var checks = row.nextAll("TR");
        var previously_applied = 0;
        for(var i=0; i < checks.length; i++) {
            var e = $(checks[i]);
            if(!e.hasClass('payment_line')) {
                break;
            }
            var payment_opt = e.data('payment_option');
            if(payment_opt.get(0) === opt.get(0)) {
                e.remove();
                previously_applied = get_currency_amount(e);
                break;
            }
        }

        var total_applied = get_currency_amount(
               $("#current_total_applied"));
        total_applied -= previously_applied;
        var left_to_apply = get_currency_amount(
               $("#current_left_to_apply"));
        left_to_apply += previously_applied;

        /* Figure out how much has been applied to see the maximum amount
         * that can be set on the payment
         */
        var ta_node = $("INPUT.applied", row);
        var trans_applied = get_currency_amount(ta_node);
        trans_applied -= previously_applied;

        var balance = data.balance - trans_applied;

        /* when an amount is entered in, be sure we have the money left */
        var amt = get_currency_amount(elem);
        if(amt > left_to_apply) {
            amt = left_to_apply;
        }

        /* Don't allow type UC (unapplied cash) to post overpayments */
        type = opt.attr('type');
        if (type === "UC") {
            if (amt > data.balance){
                amt = data.balance;
            }

        }

        /* update the transaction applied amount display */
        trans_applied += amt;
        set_currency_amount(ta_node, trans_applied);

        /* reset the entry box to take a new number */
        clear_currency_amount(elem);

        /* Make a new row below to store the payment, storing a reference to
         * the currently selected option.
         */
        if(amt > 0) {
            pay_row = $("<tr class='payment_line'></tr>");
            pay_cell = $("<td colspan='8' class='payment_line'></td>");
            pay_cell.text($entry_date + " " + opt.text());
            pay_row.append(pay_cell);

            pay_cell = $("<td class='payment_line'></td>");
            pay_cell.text(format_currency(amt));
            pay_row.append(pay_cell);

            pay_cell = $("<td class='payment_line'></td>");
            pay_row.append(pay_cell);

            pay_row.data('payment_option', opt);
            pay_row.attr("amount", amt);
            pay_row.data('trans_node', row);
            pay_row.data('entry_date', $entry_date);
            row.after(pay_row);
        }

        if(trans_applied >= data.balance) {
            $(".blue_button", row).css("display", "inline");
            $(".red_button", row).css("display", "none");
        } else {
            $(".blue_button", row).css("display", "none");
            $(".red_button", row).css("display", "inline");
        }

        /* Add information to the row to make it easy for the seach handler
         * to know whether we should remove the row or not
         */
        row.data('applied', trans_applied);

        /* Update the total controls across the top */
        total_applied += amt;
        left_to_apply -= amt;
        set_currency_amount($("#current_total_applied"), total_applied);
        var opt = $('#payment_select>option:selected');
        opt.attr('total_applied', total_applied);
        set_currency_amount($("#current_left_to_apply"), left_to_apply);

        check_remove_payment_button();
    });
}


/*/////////////////////////////////////////////////////////////////////////
 * Consistency Checking Procedures
 */

function recalc_apply_totals() {
    /* Recalculate Total Applied and Left to Apply */

    var total_payment = get_currency_amount($("#current_amount"));
    var total_applied = 0;

    var opt = $('#payment_select>option:selected');

    $("TBODY TR.payment_line").each(function() {
        var payment_opt = $(this).data("payment_option");
        if(payment_opt.get(0) === opt.get(0)) {
            total_applied += get_currency_amount($(this));
        }
    });
    
    set_currency_amount($("#current_total_applied"), total_applied);
    set_currency_amount($("#current_left_to_apply"),
                        total_payment - total_applied);

    set_currency_amount($("#current_left_to_apply"),
                        total_payment - total_applied);


    var opt = $('#payment_select>option:selected');
    opt.attr('total_applied', total_applied);

}

function check_payment_add_button() {
  if(is_payment_amount_entered()) {
    $("#add_payment_button").enable();
  } else {
    $("#add_payment_button").disable();
  }
}

function is_payment_amount_entered() {
  if($("#payment_amount").val().length === 0) {
    return false;
  } else {
    return true;
  }
}

function check_remove_payment_button() {
    /* We only let a payment be removed if none of the payment has been
     * applied.
     */

    var opt = $('#payment_select>option:selected');
    var total_applied = get_currency_amount(opt, "total_applied");
    if(total_applied === 0 && opt.text() !== 'Payment' ) {
        $("#remove_payment_button").enable();
    } else {
        $("#remove_payment_button").disable();
    }

}

/*/////////////////////////////////////////////////////////////////////////
 * Utility
 */
function get_currency_amount(elem, attr) {
    if(attr === undefined) {
        attr = 'amount';
    }
    var amt = elem.attr(attr);
    if(amt === undefined) {
        return 0;
    } else {
        return parseInt(amt);
    }
}

function set_currency_amount(elem, amt) {
    elem.attr('amount', amt);
    elem.val("$" + (amt/100).toFixed(2));
}

function format_currency(amt) {
    return "$" + (amt/100).toFixed(2);
}

function clear_currency_amount(elem) {
    elem.removeAttr('amount');
    elem.val('');
}

function append(l, o) { l[l.length] = o; }

/*Making the date pretty US format for us*/
function default_US_Date() { 
    return (new Date()).print("%m/%d/%Y");
}   

/* jQuery extensions */
jQuery.please_wait = function() {
    $.blockUI({ css: { 
        border: 'none', 
        padding: '15px', 
        backgroundColor: '#000', 
        '-webkit-border-radius': '10px', 
        '-moz-border-radius': '10px', 
        opacity: .5, 
        color: '#fff' 
    }});
}

jQuery.unplease_wait = function() {
    $.unblockUI();
}

$.fn.enable = function(options) {
    return this.each(function() {
        $(this).removeAttr('disabled');
    });
}

$.fn.disable = function(options) {
    return this.each(function() {
        $(this).attr('disabled', 'disabled');
    });
}


$.fn.readonly = function(options) {
    var vc = "1234567890."; //strValidCharacters
    return this.each(function() {
        var elem = $(this);
        elem.keypress(function() {
            return false;
        });
    });
}

$.fn.currency = function(options) {
    var vc = "1234567890."; //strValidCharacters
    return this.each(function() {
        var elem = $(this);
        elem.change(function() {
            var num = elem.val();
            var val = "";
            var buf = "";
            for(var i=0; i<num.length; i++) {
                  buf = num.substr(i, 1);
                  if(vc.indexOf(buf) > -1)
                       val += buf;
             }
             val = parseFloat(val);
             if(isNaN(val)) {
                display = '';
                amount = 0;
            } else {
                display = "$" + val.toFixed(2);
                amount = parseInt((val * 100).toFixed(0));
            }
            elem.val(display);
            elem.attr("amount", amount);
        });
        elem.change();
    })
}
