/*/////////////////////////////////////////////////////////////////////////////
 * Name Control Javascript Library
 */

function NameCtrl(elem, format, title, first, middle, last, suffix) {
	this.format = format;
  	this.elem = document.getElementById(elem);
  	this.elem.name_ctrl = this;
 	this.form = this.elem.form;
 	this.title = this.form[title];
 	this.first = this.form[first];
 	this.middle = this.form[middle];
 	this.last = this.form[last];
 	this.suffix = this.form[suffix];
 
   	this.titles = ['Dr.', 'Miss', 'Mr.', 'Mrs.', 'Ms.', 'Prof.'];
  	this.suffixes = ['I', 'II', 'III', 'Jr.', 'Sr.'];
  	
 	this.popup = function() {
 		//alert('pop' + this.middle + ' ' + this.suffix);
 	}
  
  	this.elemSync = function() {
  		// Synronize the hidden controls with the input box
		this.resetHidden();
  		value = this.elem.value.trim();
  		if(!value)
  			return;
  		var vals = value.split(" ");
  		var nvals = new Array();
  		for(var i=0; i < vals.length;) {
  			var comma_pos = vals[i].indexOf(',');
  			if(comma_pos == vals[i].length-1) {
  				// Found a comma at the end. This is the
  				// last name, followed by the first name
  				
  				// Are there at least two things after us?
  				if(i + 2 <= vals.length - 1) {
  					// We have last,first middle
  					nvals.append(vals[i+1]);
  					nvals.append(vals[i+2]);
  					nvals.append(vals[i].substr(0, vals[i].length-1));
  					i += 3;
  				} else if(i != vals.length - 1) {	// Is there something after us?
					// We have last, first
  					nvals.append(vals[i+1]);
  					nvals.append(vals[i].substr(0, vals[i].length-1));
  					i += 2;
  				} else {
  					// A comma was found on the last element. Who cares?
  					nvals.append(vals[i]);
  					i++;
  				}
  			} else if(comma_pos == 0) {
  				// We found a comma at the beginning, this is the 
  				// first name, but we have already appended the last
  				// name.
  				
  				// Is there something after us?
  				if(i != vals.length - 1) {
  					// Yes, we assume middle name "last ,first middle"
	  				nvals.splice(nvals.length-1, 0, 
	  					vals[i].substr(1, vals[i].length),
	  					vals[i+1]);
	  				i += 2;
  				} else {
	  				nvals.splice(nvals.length-1, 0,
	  					vals[i].substr(1, vals[i].length));
  					i++;
  				}
  			} else if(comma_pos != -1) {
  				// We found a comma in the middle of a word. The user
  				// did not put a space before or after the comma
  				var tnames = vals[i].split(',');
  				// Is there something after us?
  				if(i != vals.length - 1) {
  					// Yes, we assume middle name "last,first middle"
	  				nvals.append(tnames[1]);
	  				nvals.append(vals[i+1]);
	  				nvals.append(tnames[0]);
	  				i += 2;
	  			} else {
	  				nvals.append(tnames[1]);
	  				nvals.append(tnames[0]);
	  				i++;
	  			}
  			} else {
  				// We did not find a comma, so just tack it on
  				nvals.append(vals[i]);
  				i++
  			}
  		}
  		vals = nvals;

  		if((match = this.matchTitle(vals[0])) != -1) {
  			// title given
  			this.title.value = this.titles[match];
  			vals = vals.slice(1);
  		}
  		if((match = this.matchSuffix(vals[vals.length-1])) != -1) {
  			this.suffix.value = this.suffixes[match];
  			vals = vals.slice(0, vals.length-1);
  		}
  		
  		if(vals.length >= 3) {
  			// we have a middle, first and last
  			this.first.value = vals[0];
  			this.middle.value = vals[1];
  			this.last.value = vals[2];
  		} else if(vals.length == 2) {
  			this.first.value = vals[0];
  			this.last.value = vals[1];
  		} else if(vals.length == 1) {
			if(this.title.value)
				this.last.value = vals[0];
			else
  				this.first.value = vals[0];
  		}
  		this.hiddenToElem();
  	}

	this.hiddenToElem = function() {
		var value = this.format;
		var map = {
	 		 '%T' : this.title.value, 
			 '%F' : this.first.value, 
			 '%M' : this.middle.value, 
			 '%L' : this.last.value, 
			 '%S' : this.suffix.value
		};
		var good = false;
		for(find in map) {
			if(map[find])
				good = true;
		}
		if(!good) {
			this.elem.value = '';
			return;
		}
		for(find in map) {
			value = value.replace(find, map[find]);
		}
		this.elem.value = value.normalize().trim();
	}
	
	this.resetHidden = function() {
		this.title.value = '';
		this.first.value = '';
		this.middle.value = '';
		this.last.value = '';
		this.suffix.value = '';
	}
	
  	this.matchTitle = function(val) {
  		return this.titles.strfind(val);
  	}
  	
  	this.matchSuffix = function(val) {
  		return this.suffixes.strfind(val);
  	
  	}
 }; 