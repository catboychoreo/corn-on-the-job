let homeButton = document.getElementById("home")

homeButton.onclick = function(){
    window.location = "../student%20home/studenthome.html"
}

let uploadFileButton = document.getElementById("resume-upload")
let realUploadFileButton = document.getElementById("resume-file")

uploadFileButton.onclick = function(){
    realUploadFileButton.click()
    console.log("Hi")
}