for (let i = 0; i < 10; i++){
    document.getElementById("lots-of-postings").appendChild(
        document.getElementsByClassName("postings")[0].cloneNode(true)
            )
}
