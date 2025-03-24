let homeButton = document.getElementById("home")

homeButton.onclick = function () {
    window.location = "/employer"
}

let postButton = document.getElementById("post")

postButton.onclick = function () {
    window.location = "/employer/post"
}

let logOutButton = document.getElementById("logout")

logOutButton.onclick = function () {
    window.location = "/signin"
}