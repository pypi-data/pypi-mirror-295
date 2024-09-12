
function setup_view_client_page() {
    $("INPUT.del-markup-distribution-rule").click(onDeleteMarkupDistributionRule);
    function setup_ptype_row(row) {
        var ptype_id = row.attr("ptype_id");
        $("INPUT.delete_ptype", row).click(function() {
            $.post("/delete_payment_type", {'ptype_id': ptype_id},
                function(data) {
                    if(data.errors.length > 0) {
                        alert(data.errors);
                    } else {
                        row.remove();
                    }
                },
                'json');
        });
    }

    $("#invoice_multiplier").numeric();
    $("FORM.add_payment_type").submit(function() {
        var f = this;
        $.post("/add_payment_type", $(f).serialize(), 
            function(data) {
                if(data.errors.length > 0) {
                    alert(data.errors);
                    return;
                }
                var r = $("#payment_type_row_template").clone();
                r.removeAttr("id");
                r.attr("ptype_id", data.record.ptype_id);
                setup_ptype_row(r);
                $("SPAN.ptype_id", r).html(data.record.ptype_id);
                $(".type_name", r).html(data.record.type_name);
                $(".default_ref_no", r).html(data.record.default_ref_no);
                $(".expiration_date", r).html(data.record.expiration_date_fmt);
                $("#payment_type_table tr:last").after(r);
                r.css("display", "table-row");
                $.jGrowl("Payment Type Added Successfully");
                f.type_name.value = '';
                f.default_ref_no.value = '';
                f.expiration_date.value = '';
            }, 'json');
        return false;
    });

    $("TR.ptype_row").each(function() {
        setup_ptype_row($(this));
    });

    $("#recalc_savings").click(function() {
        var group_number = getParameterByName('group_number');
        $.please_wait();

        $.ajax({
            type: "GET",
            url: "/recalculate_savings?group_number=" + group_number,
            async: true,
            cache: false,
            success: function(data) {
                $.unplease_wait();
                var $popup = $("<div></div>");
                $popup.append(data);
                $popup.dialog({
                    modal: true,
                    title: "Recalculating Savings"
                    });

            }
        });
    });
}


function onDeleteMarkupDistributionRule() {
    var $this = $(this);
    document.location = "/markup_distributions/delete?comu_id=" + $this.attr("title");
}

