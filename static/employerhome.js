let homeButton = document.getElementById("home")

homeButton.onclick = function(){
    window.location = "/employer"
}

let logOutButton = document.getElementById("employer-logout")

logOutButton.onclick = function(){
    window.location = "/signin"
}