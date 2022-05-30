'use strict'

let home = document.getElementById("homebutton");
home.addEventListener("click", function() {
    window.location = "/";
});

let future = document.getElementById("futbutton");
future.addEventListener("click", function() {
    window.location = "/future";
});