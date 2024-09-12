
function formatNumber ( elem_name, decimals ) {
    function numberOnly(num) {
         var vc = "-1234567890."; //strValidCharacters
         var val = "";
         var buf = "";
         for(var i=0;i<num.length;i++) {
              buf = num.substr(i, 1);
              if(vc.indexOf(buf) > -1)
                   val += buf;
         }
         if(val == "") {
            return NaN;
         } else {
             return parseFloat(val);
            }
    }

    var elem = document.getElementById(elem_name);
    var val = numberOnly(elem.value);
    if(isNaN(val)) {
        elem.value = '';
    } else {
        elem.value = val.toFixed(decimals);
    }
}
