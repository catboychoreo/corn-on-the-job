function applicationSubmitted() {
    alert("Application has been submitted!")
    window.location = "/student"
}

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

let uploadFileButton = document.getElementById("resume-upload")
let realUploadFileButton = document.getElementById("resume-file")

uploadFileButton.onclick = function () {
    realUploadFileButton.click()
}

realUploadFileButton.onchange = function () {
    uploadFileButton.innerText = "Resume uploaded!"
}