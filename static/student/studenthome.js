let homeButton = document.getElementById("home")

homeButton.onclick = function () {
    window.location = "/student"
}

let logOutButton = document.getElementById("student-logout")

logOutButton.onclick = function () {
    window.location = "/signin"
}
