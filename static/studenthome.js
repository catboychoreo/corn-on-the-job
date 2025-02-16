// creates 10 different job postings
for (let i = 0; i < 10; i++){
    document.getElementById("lots-of-postings").appendChild(
        document.getElementsByClassName("postings")[0].cloneNode(true)
            )
}

let applyButton = document.getElementById("apply")

applyButton.onclick = function() {
    window.location = "/apply"
}

let homeButton = document.getElementById("home")

homeButton.onclick = function(){
    window.location = "/"
}

let logOutButton = document.getElementById("student-logout")

logOutButton.onclick = function(){
    window.location = "/signin"
}
