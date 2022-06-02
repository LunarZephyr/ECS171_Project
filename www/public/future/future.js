'use strict'

let home = document.getElementById("homebutton");
home.addEventListener("click", function() {
    window.location = "/";
});

let curr = document.getElementById("currbutton");
curr.addEventListener("click", function() {
    window.location = "/current";
});

let height = window.innerHeight;
let headerHeight = Dimension("header");
let navheight = Dimension("nav");
let footheight = Dimension("footer");
document.getElementById("body").style.minHeight = String(height-headerHeight-navheight-footheight-100) + "px";

let contButton = document.getElementById("continueContainer");
contButton.addEventListener("click", async function() {
    var time = parseFloat(document.getElementById('time').value);
    var temp = parseFloat(document.getElementById('temp').value) + 273.15;
    var humidity = parseFloat(document.getElementById('humidity').value);
    var clouds = parseFloat(document.getElementById('clouds').value);
    var winds = parseFloat(document.getElementById('winds').value);
    let data = {
        "Time": [time],
        "Temperature": [temp],
        "Humidity": [humidity],
        "Cloud Cover": [clouds],
        "Wind Speed": [winds]
    }
    sendPostRequest('/prediction', data)
    .then(function (response) {
        let loadText = document.getElementById("mainheader");
        loadText.textContent = "Load Prediction Is: " + String(response["load"]) + " MW";
        document.getElementById("shap_bar").style.display = "inline";
        document.getElementById("shap_bar").src = "shap_nn.png?t=" + new Date().getTime();
    });
    document.getElementById("entrywrapper").style.display = "none";
    document.getElementById("body").style.display = "flex";
});

function Dimension(elmID) {
    var elmHeight, elmMargin, elm = document.getElementById(elmID);
    elmHeight = document.getElementById(elmID).offsetHeight;
    console.log(elmID, elmHeight+elmMargin)
    elmMargin = parseInt(document.defaultView.getComputedStyle(elm, '').getPropertyValue('margin-top')) + parseInt(document.defaultView.getComputedStyle(elm, '').getPropertyValue('margin-bottom'));
    return (elmHeight+elmMargin);
}