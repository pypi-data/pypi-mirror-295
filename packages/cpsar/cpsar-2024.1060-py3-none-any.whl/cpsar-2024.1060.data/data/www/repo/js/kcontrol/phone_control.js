
function removeNonNumeric(num) {
     var vc = "1234567890"; //strValidCharacters
     var val = "";
     var buf = "";
     for(var i=0;i<num.length;i++) {
          buf = num.substr(i, 1);
          if(vc.indexOf(buf) > -1)
               val += buf;
     }
     return val;
}
function setPhone(elem_id) {
    elem = document.getElementById(elem_id);
    var num = removeNonNumeric(elem.value);
    if(num.length > 10) {
        elem.value = '(' + num.substring(0,3) + ') ' + num.substring(3,6) + '-' + num.substring(6,10) + ' ext. ' + num.substring(10,num.length);
    }
    /*
    else if(num.length == 11) {
        elem.value = num.substring(0,1) + '-(' + num.substring(1,4) + ') ' + num.substring(4,7) + '-' + num.substring(7,11);
    }
    */
    else if(num.length == 10) {
        elem.value = '(' + num.substring(0,3) + ') ' + num.substring(3,6) + '-' + num.substring(6,10);
    }
    else if(num.length == 7) {
        elem.value = num.substring(0,3) + '-' + num.substring(3,7);
    }
}
