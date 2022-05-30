'use strict'

let curr = document.getElementById("currbutton");
curr.addEventListener("click", function() {
    window.location = "./current";
});

let future = document.getElementById("futbutton");
future.addEventListener("click", function() {
    window.location = "./future";
});