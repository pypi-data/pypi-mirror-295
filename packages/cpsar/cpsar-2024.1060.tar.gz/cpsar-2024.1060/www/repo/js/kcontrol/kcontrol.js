
function browser_type () {
	if(navigator.userAgent.indexOf("Firefox")!=-1){
		var versionindex=navigator.userAgent.indexOf("Firefox")+8
		if (parseInt(navigator.userAgent.charAt(versionindex))>=1)
			//alert("You are using Firefox 1.x or above")
			return 'FIREFOX';
	}
	//Detect IE5.5+
	version=0
	if (navigator.appVersion.indexOf("MSIE")!=-1){
		temp=navigator.appVersion.split("MSIE")
		version=parseFloat(temp[1])
	}
	if (version>=5.5) //NON IE browser will return 0
		//alert("You're using IE5.5+")
		return 'INTERNET EXPLORER';
}

function toggle(elem1_id, elem2_id) {
	if(!document.getElementById(elem2_id)) {
		if(document.getElementById(elem1_id).style.display == 'none')
			document.getElementById(elem1_id).style.display = '';
		else
			document.getElementById(elem1_id).style.display = 'none';
	}
	else {
		if(document.getElementById(elem1_id))
		    document.getElementById(elem1_id).style.display = '';
		if(document.getElementById(elem2_id))
	    	document.getElementById(elem2_id).style.display = 'none';
    }
}

function input_copy(from_elem_id, to_elem_id) {
	if(!document.getElementById(to_elem_id)) return false;
	if(!document.getElementById(from_elem_id)) return false;
	getObj(to_elem_id).value = getObj(from_elem_id).value;
}
function copy_address(from_dict, to_dict, hide_elem_id) {
	if(document.getElementById(hide_elem_id))
		toggle('', hide_elem_id);
	var just_go_ahead = false;
	if(!getObj(from_dict['address']).value) {
		if(!confirm("Are you sure?  The address you are copying from appears to be blank.")) {
			return false;
		}
		just_go_ahead = true;	
	}
	if(getObj(to_dict['address']).value && just_go_ahead == false) {
		if(!confirm("Are you sure?  You will be over writting this address.")) {
			return false;
		}
	}
	input_copy(from_dict['address'], to_dict['address']);
	input_copy(from_dict['address_2'], to_dict['address_2']);
	input_copy(from_dict['state'], to_dict['state']);
	input_copy(from_dict['city'], to_dict['city']);
	input_copy(from_dict['zip_code'], to_dict['zip_code']);	
}
function dget_value(field) {
    if(document.getElementById(field))
        return document.getElementById(field).value;
    else
        return false;
}
function dget_innerHtml(field) {
    if(document.getElementById(field))
        return document.getElementById(field).innerHTML;
    else
        return false;
}
function dget_html(field) {
    if(document.getElementById(field)) {
    	if(dget_value(field))
    		return dget_value(field);
    	if(dget_innerHtml(field))
    		return dget_innerHtml(field);
    	return '';
    } else
        return '';
}
function map_it(prefix) {
    var street = dget_html(prefix + "address") + ' ';
    var box = dget_html(prefix + "address_2") + ' ';
    var city = dget_html(prefix + "city") + ' ';
    var state = dget_html(prefix + "state") + ' ';
    var zip = dget_html(prefix + "zip_code")+ ' ';
    var country = dget_html(prefix + "country");
    var mapParameter = street + box + city + state + zip + country;
    var test = mapParameter.replace(' ', '');
    if(test == '' || test == false || !test) {
    	alert("Once you provide an address, this will open a map to it for you.");
    	return false;
    } else {
    window.open('http://maps.google.com/maps?q='+mapParameter, 'goolemap', +
        'height=450,width=700,resizable=no,statusbar=no,titlebar,location=no,top=200, left=250');
        return true;
    }
 }

String.prototype.trim = function() {
    sString = this;
    while (sString.substring(0,1) == ' ') {
        sString = sString.substring(1, sString.length);
    }
    while (sString.substring(sString.length-1, sString.length) == ' ') {
        sString = sString.substring(0,sString.length-1);
    }
    return sString;
 }


String.prototype.IsNumeric = function() {
   var sText = this;
   var ValidChars = "0123456789.";
   var IsNumber=true;
   var Char;


   for (i = 0; i < sText.length && IsNumber == true; i++)
      {
      Char = sText.charAt(i);
      if (ValidChars.indexOf(Char) == -1)
         {
         IsNumber = false;
         }
      }
   return IsNumber;

}

function url_inspect(url) {
/*
    Takes the url passed in, or current url
    and returns much usefull information about
    it in a dictionary.
    The URL, by itself in 'url'.
    The entire qs after the ? in 'qs'.
    Querystring Keys and values in a dictionary 'values'.
    The bookmark in 'tag'.
    Everything bundeled up in 'all'.
*/
    if(!url) {
        var url = document.location.toString();
    }
    var u = url.split("?");
    var vals = '';
    var parts={};
    var tag = null;
    if (u.length > 1) {
         vals = u[1];
        var p = vals.split("&");
        for(var i=0;i<p.length;i++) {
            var part = p[i].split("=");
            if(i == p.length -1) {
                var temp = part[1].split("#");
                if(temp.length > 0) {
                    part[1] = temp[0];
                    tag = temp[1];
                }
            }
            parts[part[0]] = part[1];
        }
    }
    return {'url' : u[0], 'qs' : vals, 'values' : parts, 'tag' : tag, 'all' : url};
}
String.prototype.startswith = function(s) {
 return (s == this.substring(0, s.length));
};

String.prototype.endswith = function(val) {
    // foobar  bar   6 - 3
    if(val.length > this.length)
        return false;
    var sub = this.slice(this.length - val.length);
    return sub == val;
}
Array.prototype.find=function(val) {
    for(i=0;i<this.length;i++){
        if(this[i]==val) return i;
    }
    return -1;
}


String.prototype.normalize = function() {
    // Normalizing a string makes all of the space in the string just
    // one
    var nstr = '';
    var spacef = false;
    for(var i=0; i < this.length; i++) {
        chari = this.charAt(i);
        if(chari.match(/\s/)) {
            if(!spacef) {
                nstr = nstr + ' ';
                spacef = true;
            }
        } else {
            nstr = nstr + chari;
            spacef = false;
        }
    }
    return nstr;
}
/*
Array.prototype.find=function(val) {
    for(i=0;i<this.length;i++){
        if(this[i]==val) return i;
    }
    return -1;
}
*/
Array.prototype.ifind=function(val) {
    for(i=0;i<this.length;i++){
        if(this[i].toString().toLowerCase() == val.toString().toLowerCase())
            return i;
    }
    return -1;
}

Array.prototype.strfind=function(val) {
    for(i=0;i<this.length;i++){
        var v1 = this[i].toString().replace(/[\W]/, '').trim();
        var v2 = val.toString().replace(/[\W]/, '').trim();
        if(v1.toLowerCase() == v2.toLowerCase())
            return i;
    }
    return -1;
}

/* Adds an item on to the end of an array */
Array.prototype.append = function(item) {
    this[this.length] = item;
};


function flip_checkbox(elem) {
    elem.checked = elem.checked ? false: true;
}

function invert_disabled(elem) {
    elem.disabled = elem.disabled ? false: true;
}

function form_elem(elem) {
    // We wrap calls to make up for arrays
    if(elem.length) {
        for(i=0; i<elem.length; i++) {
            e = elem[i];
            if(e.type != 'hidden') {
                return e;
            }
        }
    } else {
        return elem;
    }
}

function popup(url, name, width, height) {
	if(!name)
		name = 'a_popup';
	name = name + new Date().getTime();
	if(!width)
		width = screen.width / 2;
	if(!height)
		height = screen.height / 2;
	var winleft = (screen.width - width) / 2;
	var winUp = (screen.height - height) / 2;
	win = window.open(url, name,
	            "height=" + height + ",width=" + width + ",status=0,resizable=1,scrollbar=1,toolbar=0,menubar=0,left=" + winleft +
			",top=" + winUp);
	//alert("self.location in popup:" + self.location);
	win.opener = self;
}

function dialog_close() {

	if(opener != null) {
		if(document.images)
			opener.location.replace(opener.location.href);
		else
			opener.location.href = opener.location.href;
	}
	window.close();
}


function trap_enter(e) {
     if (!e) e = window.event;
     if (e.keyCode == 13) {
          e.cancelBubble = true;
          if (e.returnValue) e.returnValue = false;
          if (e.stopPropagation) e.stopPropagation();
          return true;
     } else {
          return false;
     }
}
function getObj(name) {
    if (document.getElementById) {
        return document.getElementById(name);
    } else if (document.all) {
        return document.all[name];
    } else if (document.layers) {
        return getObjNN4(document,name);
    }
}
function getObjNN4(obj,name) {
    var x = obj.layers;
    var thereturn;
    for (var i=0;i<x.length;i++) {
        if (x[i].id == name)
            thereturn = x[i];
        else if (x[i].layers.length)
            var tmp = getObjNN4(x[i],name);
        if (tmp) thereturn = tmp;
    }
    return thereturn;
}


function quoteString(str) {
    rs = [
        ["%", "%25"],
        ["\\s", "%20"],
        ["'", "%27"],
        ['"', "%22"],
        ["!", "%21"],
        ["@", "%40"],
        ["#", "%23"],
        ["\\$", "%24"],
        ["\\^", "%5E"],
        ["&", "%26"],
        ["\\*", "%2A"],
        ["\\(", "%28"],
        ["\\)", "%29"],
        ["\\+", "%2B"],
        ["=", "%3D"],
        ["\\{", "%7B"],
        ["\\}", "%7D"],
        ["\\[", "%5B"],
        ["\\]", "%5D"],
        ["\\|", "%7C"],
        ["\\?", "%3F"],
        ["`", "%60"],
        ["~", "%7E"],
        ["\\\\", "%5C"]
    ]
    for(var i=0; i< rs.length; i++) {
        var reg = new RegExp(rs[i][0],"g");
        str = str.replace(reg, rs[i][1]);
    }

    return str
}
