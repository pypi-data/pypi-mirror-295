function showErrors(errors) {
    for(var i=0; i < errors.length; i++) {
        $.jGrowl(errors[i]);
    }
}

function getParameterByName(name)
{
  name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
  var regexS = "[\\?&]" + name + "=([^&#]*)";
  var regex = new RegExp(regexS);
  var results = regex.exec(window.location.href);
  if(results == null)
    return "";
  else
    return decodeURIComponent(results[1].replace(/\+/g, " "));
}

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


if (top.location != location) {
    top.location.href = document.location.href ;
}
