let homeButton = document.getElementById("home")

homeButton.onclick = function () {
    window.location = "/student"
}

let myApplicationsButton = document.getElementById("my-applications")

myApplicationsButton.onclick = function () {
    window.location = "/student/myapplications"
}

let logOutButton = document.getElementById("logout")

logOutButton.onclick = function () {
    window.location = "/logout"
}