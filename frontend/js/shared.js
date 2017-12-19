function sign_out() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var response = JSON.parse(this.response);
            if (response["session"] == "end") {
                window.location.href = "index.html";
            } else if (response["error"] == "error") {
                alert("Unauthorized");
            }
        }
    }
    xhttp.open("GET", "https://localhost/sign_out", true);
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhttp.send();
}

function load_file(filename) {
    var xhttp = new XMLHttpRequest(filename);
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            window.location.href = "http://localhost:8000/files/" + filename;
        }
    }
    xhttp.open("GET", "http://localhost:8000/files/" + filename, true);
    xhttp.setRequestHeader("Content-Type", "application/json;charset=utf-8");
    xhttp.send();
}

var form = document.getElementById('file-form');
var uploadButton = document.getElementById('upload-button');
//var clientName = document.getElementById('client_name').value;
form.addEventListener('submit', function(event) {
    event.preventDefault();
    uploadButton.innerHTML = 'Uploading...';
    var formData = new FormData(form);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://localhost:8000/files/', true);
    xhr.send(formData);
    xhr.onload = function() {
        alert('File Uploaded.');
    }
})