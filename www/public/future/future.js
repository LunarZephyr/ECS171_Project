'use strict'

let home = document.getElementById("homebutton");
home.addEventListener("click", function() {
    window.location = "/";
});

let curr = document.getElementById("currbutton");
curr.addEventListener("click", function() {
    window.location = "/current";
});