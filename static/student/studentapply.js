function applicationSubmitted() {
    alert("Application has been submitted!")
    window.location = "/student"
}

let homeButton = document.getElementById("home")

homeButton.onclick = function () {
    window.location = "/student"
}

let logOutButton = document.getElementById("student-logout")

logOutButton.onclick = function () {
    window.location = "/signin"
}

let uploadFileButton = document.getElementById("resume-upload")
let realUploadFileButton = document.getElementById("resume-file")

uploadFileButton.onclick = function () {
    realUploadFileButton.click()
}

realUploadFileButton.onchange = function () {
    uploadFileButton.innerText = "Resume uploaded!"
}