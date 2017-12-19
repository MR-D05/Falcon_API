var modal = document.getElementById('id01');
// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
};

document.getElementById('password-form').addEventListener('submit', function(event) {
    event.preventDefault();
    var formData = new FormData(document.getElementById('password-form'));
    var uname = formData.get("uname");
    var oldpsw = formData.get("oldpsw");
    var pword = formData.get("psw");
    var data = {username:uname, old_password:oldpsw, new_password:pword};
    var xhr = new XMLHttpRequest();
    xhr.open('PUT', '/v1/api/password-reset', true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.withCredentials = false;
    xhr.send(JSON.stringify(data));
});

document.getElementById('password-form-cancel').addEventListener('click', function(event) {
    var x = document.getElementById("password-form");
    if (x.style.display === "block") {
        x.style.display = "none";
    }
});