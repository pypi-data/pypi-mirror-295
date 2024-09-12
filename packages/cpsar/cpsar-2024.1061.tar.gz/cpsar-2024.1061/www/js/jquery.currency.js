(function(factory){
  if(typeof define === 'function' && define.amd){
    define(['jquery'], factory);
  } else {
        factory(window.jQuery);
  }
}(function($) {

$.fn.currency = function(options) {
    var vc = "1234567890."; //strValidCharacters
    return this.each(function() {
        var elem = $(this);
        elem.change(function() {
            var num = elem.val();
            var val = "";
            var buf = "";
            for(var i=0; i<num.length; i++) {
                  buf = num.substr(i, 1);
                  if(vc.indexOf(buf) > -1)
                       val += buf;
             }
             val = parseFloat(val);
             if(isNaN(val)) {
                display = '';
                amount = 0;
            } else {
                display = "$" + val.toFixed(2);
                amount = parseInt((val * 100).toFixed(0));
            }
            elem.val(display);
            elem.data("currency.amount", amount);
        });
        elem.change();
    })
}

$.fn.amount = function() {
  if(arguments.length === 0) {
    return $(this).data("currency.amount");
  }
  var amt = arguments[0];
  if(amt) {
    $(this).data('currency.amount', amt);
    this.val("$" + (amt/100).toFixed(2));
  } else {
    $(this).data('currency.amount', 0);
    this.val("");
  }
}

}));

