function isDigit(c) {
    return ((c=='0')||(c=='1')||(c=='2')||(c=='3')||(c=='4')||(c=='5')||(c=='6')||(c=='7')||(c=='8')||(c=='9'))
}
function isNumeric(n) {
    num = parseInt(n,10);
    return !isNaN(num);
}
function padZero(n) {
    v="";
    if (n<10)
        return ('0'+n);
    else
        return n;
}
function handle_time_blur(elem) {
    var val = elem.value;
    if(val == '')
        return;
    if(val == '00:00')
        return '12:00 am';
    validateTimePicker(elem);
}

function validateTimePicker(ctl) {
    t=ctl.value.toLowerCase();
    t=t.replace(" ","");
    t=t.replace(".",":");
    t=t.replace("-","");
    var pre_mode = null;
    if(t.endswith('am') == true)
        pre_mode = 'am';
    if(t.endswith('pm') == true)
        pre_mode = 'pm';
    t=t.replace("am","");
    t=t.replace("pm","");
    if ((isNumeric(t))&&(t.length==4)) {
        t=t.charAt(0)+t.charAt(1)+":"+t.charAt(2)+t.charAt(3);
    }
    var t=new String(t);
    tl=t.length;
    if (tl==1 ) {
        if (isDigit(t)) {
            if(t==0) t=12;
            ctl.value=t+":00 " + (pre_mode != null ? pre_mode : "am");
        } else
            return false;
    }
    else if (tl==2) {
        if (isNumeric(t)) {
            if (parseInt(t,10)<13){
                if (t.charAt(1)!=":"){
                    if(t == 12) {
                        ctl.value = t + ':00 ' + (pre_mode != null ? pre_mode : 'pm');
                    }
                    else{
                        if (t==24 || t==0) {
                            t=12;
                            mode="am";
                        }
                        ctl.value= t + ':00 ' + (pre_mode != null ? pre_mode : 'am');
                    }
                }
                else
                    ctl.value= t + '00 ' + (pre_mode != null ? pre_mode : 'am');
            }

            else if (parseInt(t,10)==24) {
                ctl.value= "12:00 " + (pre_mode != null ? pre_mode : 'am');
            }
            else if (parseInt(t,10)<24) {
                if (t.charAt(1)!=":")
                    ctl.value= (t-12) + ':00 ' + (pre_mode != null ? pre_mode : 'pm');
                else
                    ctl.value= (t-12) + '00 ' + (pre_mode != null ? pre_mode : 'pm');
            }
            else if (parseInt(t,10)<=59) {

                ctl.value= '12:'+padZero(t)+' ' + (pre_mode != null ? pre_mode : 'am');
            }
            else {
                ctl.value= '1:'+padZero(t%60)+' ' + (pre_mode != null ? pre_mode : 'am');
                }
            }
            else
               {
                if ((t.charAt(0)==":")&&(isDigit(t.charAt(1))))
                ctl.value = "12:" + padZero(parseInt(t.charAt(1),10)) + " " + (pre_mode != null ? pre_mode : 'am');
            else
                return false;
        }
    }
    else if (tl>=3) {
        var arr = t.split(":");
        if (t.indexOf(":") > 0)
        {
            hr=parseInt(arr[0],10);

            if(arr[0].length == 2) {
                mn=parseInt(arr[1],10);
            }
            else {
                mn=parseInt(arr[2],10);
            }
            mn=(+mn);
            if (t.indexOf("pm")>0)
                mode="pm";
            else
                mode="am";

            if (isNaN(hr))
                hr=0;
            else {
                if (hr>24)
                    return false;
                else if (hr==24) {
                    mode="am";
                    hr=0;
                } else if (hr>12) {
                    mode="pm";
                    hr-=12;
                }
            }
            mn = (+mn);
            if (isNaN(mn))
                mn=0;
            else {
                if (mn>60) {
                    mn=mn%60;
                    hr+=1;
                }
            }
        } else {
            var temp=parseInt(arr[0],10);
            temp = String(temp);
            hr=temp.charAt(0);
            mn = temp.slice(1,3);
            hr = (+hr);
            mn = (+mn);
            if (isNaN(hr))
                hr=0;
            else {
                mode = "am";
                if (hr>24) {
                    return false;
                } else if (hr==24) {
                    mode="am";
                    hr=0;
                } else if (hr>12) {
                    mode="pm";
                    hr-=12;
                }
            }
        }

        if (hr==24 || hr==0) {
            hr=12;
            mode="am";
        }
        if(pre_mode)
            mode = pre_mode;
        ctl.value=hr+":"+padZero(mn)+" "+mode;
    }
}

function time_help(elem, event) {
    var help_text = "Do not enter any letters except 'am' or 'pm'.\\n  Example: '1:42 pm' or '1342'.";
    if(event.keyCode == 191 && event.ctrlKey == true) {
        alert(help_text);
        event.returnValue = false;
        return false;
    } else {
        return true;
    }
}
