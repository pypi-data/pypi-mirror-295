$(document).ready(function() {
    new Collapsable();
});

function Collapsable() {
    var $nodes = $(".collapse");
    $nodes.click(function() {
        var body = $(this).next('DIV');

        if(body.css('display') === 'block') {
            body.css('display', 'none');
        } else {
            body.css('display', 'block');
        }
    });

    $nodes.click();
}
