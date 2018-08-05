function alertImage(result){
    if (result.target.responseText === "No Image Found") {
        let elt = document.getElementById("loader-wrapper"); 
        elt.setAttribute("class", "hidden");
        alert("Not a Valid Image"); 
    }
    else {
        window.location.href="/select_image"; 
    }
}


function upload(evt){
    evt.preventDefault();

    let form = $('#imageuploadform')[0]

    let file = $('#userimage')[0].files[0];

    let data = new FormData(form);
    data.append(file.name, file);

    let request = new XMLHttpRequest();
    request.open("POST", "/submit_image");
    request.onload = alertImage;
    request.send(data);
}

$("#imageuploadform").on("submit", upload)