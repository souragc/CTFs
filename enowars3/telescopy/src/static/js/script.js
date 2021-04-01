function reply_click(clicked_id) {
    makeAjaxRequest();
}

function addPlanet(clicked_id) {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            alert(this.responseText)
        }
    };
    xhttp.open("GET", "../addPlanet" +
        "?name=" + document.getElementById("name").value +
        "&declination=" + document.getElementById("declination").value +
        "&rightAscension=" + document.getElementById("rightAscension").value +
        "&flag=" + document.getElementById("flag").value
        , true);
    xhttp.send();
}

function getPlanet(clicked_id) {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            alert(this.responseText)
        }
    };
    xhttp.open("GET", "../getPlanet?declination="
        + "&ticket=" + document.getElementById("ticket").value
        + "&id=" + document.getElementById("planetId").value
        , true);
    xhttp.send();
}

function makeAjaxRequest() {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("result").innerHTML = this.responseText;
        }
    };
    xhttp.open("GET", "../directTelscopeTo/" + document.getElementById("angleInput").value, true);
    xhttp.send();
}