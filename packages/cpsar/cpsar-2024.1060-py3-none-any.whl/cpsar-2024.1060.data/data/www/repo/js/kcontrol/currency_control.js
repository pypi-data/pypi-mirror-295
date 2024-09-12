function formatCurrency(elem) {
    function numberOnly(num) {
         var vc = "-1234567890."; //strValidCharacters
         var val = "";
         var buf = "";
         for(var i=0;i<num.length;i++) {
              buf = num.substr(i, 1);
              if(vc.indexOf(buf) > -1)
                   val += buf;
         }
         val = parseFloat(val);
         if(isNaN(val)) {
            return '';
        } else {
            return val.toFixed(2);
        }
    }

    elem.value = numberOnly(elem.value);
}

