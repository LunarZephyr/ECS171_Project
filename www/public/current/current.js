'use strict'

let home = document.getElementById("homebutton");
home.addEventListener("click", function() {
    window.location = "/";
});

let future = document.getElementById("futbutton");
future.addEventListener("click", function() {
    window.location = "/future";
});

let height = window.innerHeight;
let headerHeight = Dimension("header");
let navheight = Dimension("nav");
let footheight = Dimension("footer");
document.getElementById("body").style.minHeight = String(height-headerHeight-navheight-footheight-90) + "px";

sendGetRequest('/prediction/current')
.then(function (data) {
    let price = data["price"];
    let priceText = document.getElementById("mainheader");
    priceText.textContent = "Current Price Forecast: €" + String(Math.round(price * 100) / 100) + " per MWh";
    document.getElementById("loadtext").style.display = "none";
    document.getElementById("shap_bar").style.display = "inline";
    document.getElementById("shap_bar").src = "shap_bar.png?t=" + new Date().getTime();
});

function Dimension(elmID) {
    var elmHeight, elmMargin, elm = document.getElementById(elmID);
    elmHeight = document.getElementById(elmID).offsetHeight;
    elmMargin = parseInt(document.defaultView.getComputedStyle(elm, '').getPropertyValue('margin-top')) + parseInt(document.defaultView.getComputedStyle(elm, '').getPropertyValue('margin-bottom'));
    console.log(elmID, elmHeight+elmMargin)
    return (elmHeight+elmMargin);
}