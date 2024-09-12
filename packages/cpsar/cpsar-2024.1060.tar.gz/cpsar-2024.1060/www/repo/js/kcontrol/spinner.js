var date = new Date();
var milliseconds =
    Date.UTC(y2k(date.getYear()),date.getMonth(),date.getDate());


function spinner_down(elem) {
    milliseconds -= 86400000;
    formatDate(elem);
}

function spinner_up(elem) {
    milliseconds += 86400000;
    formatDate(elem);
}

function formatDate(elem) {
    date = new Date(milliseconds);
    var year = date.getYear();
    var month = date.getMonth() + 1;
    var day = date.getDate();
    document.getElementByID(elem).value = ((year < 1000) ? year + 1900 : year) +
                            '-' + ((month < 10) ? '0' + month : month) +
                            '-' + ((day < 10) ? '0' + day : day);
}