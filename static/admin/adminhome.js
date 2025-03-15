function confirmDeletion(){
    return confirm("Are you sure you want to delete this job listing? This is irreversible.")
}

let homeButton = document.getElementById("home")

homeButton.onclick = function () {
    window.location = "/admin"
}

let reviewButton = document.getElementById("review")

reviewButton.onclick = function () {
    window.location = "/admin/review"
}

let logOutButton = document.getElementById("admin-logout")

logOutButton.onclick = function () {
    window.location = "/signin"
}
