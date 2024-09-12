
$(document).ready(function() {
  function onGroupNumberChange() {
    var gn = $(this).val();
    if(gn.length === 0) { return; }
    $.post("/ac_adjuster_search",
           {group_number: gn},
           onAdjusterSearchSuccess,
           'json');
    $("#report_code").val('');
  }

  function onReportCodeChange() {
    var rc = $(this).val();
    if(rc.length === 0) { return; }
    $.post("/ac_adjuster_search",
           {report_code: rc},
           onAdjusterSearchSuccess,
           'json');
    $("#group_number").val('');
  }

  function onAdjusterSearchSuccess(data) {
    $("#adjuster_email").empty();
    $("#adjuster_email").append("<option></option>");
    $(data).each(appendAdjusterOption);
  }

  function appendAdjusterOption() {
    var label = this.first_name + " " + this.last_name + " - " + this.email;
    var $opt = $("<option></option>");
    $opt.attr("value", this.email);
    $opt.text(label);
    $("#adjuster_email").append($opt);
  }

  $("#group_number").change(onGroupNumberChange).change();
  $("#report_code").change(onReportCodeChange);
});
