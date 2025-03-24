function submitPost() {
    console.log("hiiii?")
    return alert("Post submitted! It will be reviewed and upon approval will be made public for applicants.")
}

let homeButton = document.getElementById("home")

homeButton.onclick = function () {
    window.location = "/employer"
}

let logOutButton = document.getElementById("logout")

logOutButton.onclick = function () {
    window.location = "/signin"
}

let uploadFileButton = document.getElementById("logo-upload")
let realUploadFileButton = document.getElementById("logo-file")
let previewImage = document.getElementById("preview-img")
let placeholderText = document.getElementById("instructions")

uploadFileButton.onclick = function () {
    realUploadFileButton.click()
}

realUploadFileButton.onchange = function () {
    let file = realUploadFileButton.files[0]
    if (file) {
        placeholderText.style.display = "none";
        previewImage.style.display = "block";
        previewImage.src = URL.createObjectURL(file)
    }
}