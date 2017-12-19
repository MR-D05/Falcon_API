var modal = document.getElementById('id01');
// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
};

var modal = document.getElementById('id02');
// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
};

document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();
    var formData = new FormData(document.getElementById('login-form'));
    var uname = formData.get("uname");
    var pword = formData.get("psw");
    var data = {username:uname, password:pword};
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var redirect = xhr.getResponseHeader("Location");
            window.location = redirect;
        }
    };
    xhr.open('POST', 'http://localhost:8080/v1/api/users', true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.withCredentials = false;
    xhr.send(JSON.stringify(data));
});

document.getElementById('registration-form').addEventListener('submit', function(event) {
    event.preventDefault();
    var formData = new FormData(document.getElementById('registration-form'));
    var email = formData.get("email");
    var uname = formData.get("uname");
    var pword = formData.get("psw");
    var data = {email_address:email, username:uname, password:pword};
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var redirect = xhr.getResponseHeader("Location");
            window.location = redirect;
        } else if (this.readyState == 4 && this.status == 409) {
            alert("Email taken. Try again.");
        } else {
            console.log("Error");
        }
    };
    xhr.open('PUT', 'http://localhost:8080/v1/api/users', true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.withCredentials = false;
    xhr.send(JSON.stringify(data));
});