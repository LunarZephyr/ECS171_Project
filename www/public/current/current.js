'use strict'

let home = document.getElementById("homebutton");
home.addEventListener("click", function() {
    window.location = "/";
});

let future = document.getElementById("futbutton");
future.addEventListener("click", function() {
    window.location = "/future";
});

sendGetRequest('/prediction/current')
.then(function (data) {
    let price = data["price"];
    let priceText = document.getElementById("mainheader");
    priceText.textContent = "Current Price Forecast: €" + String(Math.round(price * 100) / 100) + " per MWh";
    document.getElementById("loadtext").style.display = "none";
    document.getElementById("shap_bar").style.display = "inline";
    document.getElementById("shap_bar").src = "shap_bar.png?t=" + new Date().getTime();
});