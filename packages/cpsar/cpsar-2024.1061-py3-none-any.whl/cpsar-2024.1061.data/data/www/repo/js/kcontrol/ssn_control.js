
// SSN Control Javascript
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
function setSSN(elem_id) {
    elem = document.getElementById(elem_id);
    var num = removeNonNumeric(elem.value);
    if(num.length == 10) {
        elem.value =  num.substring(0,1) + '-' + num.substring(1,3) + '- ' + num.substring(3,6) + '-' + num.substring(6,10);
    }
    else if(num.length == 9) {
        elem.value = num.substring(0,3) + '-' + num.substring(3,5) + '-' + num.substring(5,9);
    }
}
function SSNsyncFromHidden(elem_id) {
    var num = removeNonNumeric(document.getElementById(elem_id).value);
    document.getElementById(elem_id + '_1').value = num.substring(0,3);
    document.getElementById(elem_id + '_2').value = num.substring(3,5);
    document.getElementById(elem_id + '_3').value = num.substring(5,9);
}
function SSNsyncToHidden(elem_id) {
    var num = document.getElementById(elem_id + '_1').value + 
              document.getElementById(elem_id + '_2').value + 
              document.getElementById(elem_id + '_3').value;
    document.getElementById(elem_id).value = num.substring(0,3) + 
        '-' + num.substring(3,5) + 
        '-' + num.substring(5,9);
}
function autojump(fieldName,nextFieldName,fakeMaxLength) {
    var current_field = document.getElementById(fieldName);
    current_field.nextField = document.getElementById(nextFieldName);
    current_field.maxLength=fakeMaxLength;
    current_field.onkeyup=autojumpKeyUp;

}
function autojumpKeyUp() {
    if(this.value.length > this.maxLength) {
        var buf = '';
        for(var i=0;i<this.value.length;i++)
            buf = this.value[i];
        this.value = buf;
    }
    if(this.value.length == this.maxLength)
        this.nextField.focus();
}
