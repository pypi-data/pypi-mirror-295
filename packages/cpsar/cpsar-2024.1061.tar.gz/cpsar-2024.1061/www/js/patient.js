
function patient_uc_load() {
    $(".revoke_uc").click(revoke_uc_click);

    $("#payment_amount").numeric();
    $(".add_uc").submit(add_uc_submit);
}

/*////////////////////////////////////////////////////////////////////////////
 * Called when the user clicks a revoke button beside an unapplied cash 
 * entry.
 */
function revoke_uc_click() {
    var row = $(this).parents("TR:first");
    var pid = $(".puc_id", row).text();
    $.ajax({
        url: '/patient/revoke_uc',
        data: {puc_id: pid},
        dataType: 'json',
        type: 'POST',
        error: function(req, stat, err) {
            $.jGrowl("An error occured contacting the server: " + stat + err);
        },
        success: function(data, stat, req) {
            if(data.errors.length > 0) {
                for(var i=0; i < data.errors.length; i++) {
                    $.jGrowl(data.errors[i]);
                }
            } else {
                row.remove();
            }
        }
    });
}

function add_uc_submit() {
    var args = {
        check_no: $("#check_no").val(),
        amount: $("#payment_amount").val(),
        patient_id: $("#patient_id").val()
    }
    $.ajax({
        url: '/patient/add_uc',
        data: args,
        dataType: 'json',
        type: 'POST',
        error: function(req, stat, err) {
            $.jGrowl("An error occured contacting the server: " + stat + err);
        },
        success: function(data, stat, req) {
            if(data.errors.length > 0) {
                for(var i=0; i < data.errors.length; i++) {
                    $.jGrowl(data.errors[i]);
                }
            } else {
                window.location.reload();
            }
        }
    });
    return false;
}
