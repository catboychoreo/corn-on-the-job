let uploadFileButton = document.getElementById("resume-upload");
let realUploadFileButton = document.getElementById("resume-file");

uploadFileButton.onclick = function () {
  realUploadFileButton.click();
};

realUploadFileButton.onchange = function () {
  uploadFileButton.innerText = "Resume uploaded!";
};
