function view_invoice(invoice_id) {
    document.location = '/invoice/' + invoice_id + '/view';
}
function view_claim(claim_id) {
    document.location = '/claim/' + claim_id;
}

function view_claim_popup(claim_id) {
    window.open('/claim/' + claim_id);
}

function view_doctor(id) {
    document.location = '/doctor/' + id + '/view';
}

function view_patient(id) {
    document.location = '/patient/' + id + '/view';
}

function view_pharmacy(id) {
    document.location = '/pharmacy/' + id + '/view';
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
function basic_search(keyword, type) {
	document.location = '/search?__keyword__=' + quoteString(keyword) + '&__search_type__=' + type;
}

function show_hide(id) {
    var elem = document.getElementById(id);
    if(elem.style.display == "none") {
        elem.style.display = "block";
    } else {
        elem.style.display = "none";
    }
}
