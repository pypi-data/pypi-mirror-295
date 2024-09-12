
$(document).ready(function() {
    $("INPUT.numeric").numeric();
    $(".collapse").click(function() {
        var body = $("TBODY", $(this).parents('TABLE:first'));
        var body = $("TR", body);

        if(body.css('display') === 'table-row') {
            body.css('display', 'none');
        } else {
            body.css('display', 'table-row');
        }
    });

    $(".collapse").click();

    $(".iprint_all").click(function() {
        $(".iprint").each(function() {
            var $this = $(this);
            if($this.attr("checked")) {
                $this.removeAttr("checked");
            } else {
                $this.attr("checked", "checked");
            }
        });
    });

    $(".iprint_form").submit(function() {
        var form = $(this);
        $(".trans_id", form).remove();
        $(".iprint").each(function() {
            if($(this).attr("checked")) {
                form.append($("<input type='hidden' class='trans_id' " +
                    "name='trans_id' value='" +
                    + $(this).attr("title") + "' />"));
            }
        });
        return true;
    });


    $(".print_hcfa_form").submit(function() {
        var form = $(this);
        $(".trans_id", form).remove();
        $(".iprint").each(function() {
            if($(this).attr("checked")) {
                form.append($("<input type='hidden' class='trans_id' " +
                    "name='trans_id' value='" +
                    + $(this).attr("title") + "' />"));
            }
        });
        return true;
    });

    $("INPUT.mark_for_rebill").click(function() {
        var data = [];
        $("INPUT.iprint:checked").each(function() {
            data[data.length] = $(this).val();
        });
        $.ajax({
            url: "/ac_flip_rebill",
            dataType: 'json',
            type: 'post',
            data: {trans_id: data},
            success: function(data, stat, req) {
                $.jGrowl("Rebill Flag Updated");
            }
        });
    });

    $("INPUT.mark_for_state_reporting").click(function() {
        var data = [];
        $("INPUT.iprint:checked").each(function() {
            data[data.length] = $(this).val();
        });
        $.ajax({
            url: "/ac_mark_sr_flag",
            dataType: 'json',
            type: 'post',
            data: {trans_id: data},
            success: function(data, stat, req) {
                $.jGrowl("Marked for State Reporting");
            }
        });
    });
});
