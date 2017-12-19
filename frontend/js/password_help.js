var modal = document.getElementById('id01');
// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
};

document.getElementById('email-form').addEventListener('submit', function(event) {
    event.preventDefault();
    var formData = new FormData(document.getElementById('email-form'));
    var email = formData.get("email");
    var data = {user_email:email};
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/v1/api/password-reset-request', true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.withCredentials = false;
    xhr.send(JSON.stringify(data));
});

document.getElementById('hidden-form').addEventListener('submit', function(event) {
    event.preventDefault();
    var emailformData = new FormData(document.getElementById('email-form'));
    var formData = new FormData(document.getElementById('hidden-form'));
    var email = emailformData.get("email");
    var rstkn = formData.get("password-reset-token");
    var data = {user_email:email, reset_token:rstkn};
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var redirect = xhr.getResponseHeader("Location");
            window.location = redirect;
        }
    };
    xhr.open('POST', '/v1/api/password-reset', true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.withCredentials = false;
    xhr.send(JSON.stringify(data));
});

document.getElementById('hidden-form-cancel').addEventListener('click', function(event) {
    var x = document.getElementById("hidden-form");
    if (x.style.display === "block") {
        x.style.display = "none";
    }
});

document.getElementById('email-form-cancel').addEventListener('click', function(event) {
    var x = document.getElementById("id01");
    var y = document.getElementById("hidden-form");
    x.style.display = "none";
    y.style.display = "none";
});

document.getElementById('email-button').addEventListener('click', function(event) {
    var x = document.getElementById("hidden-form");
    var y = document.getElementById("email").value;
    if (y === "") {
        alert("You must enter an email first.");
    }
    else if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "block";
    }
});