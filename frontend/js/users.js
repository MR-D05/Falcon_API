function on_load() {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var data = JSON.parse(this.responseText);
            var username = data;
            document.getElementById('user').value = username;
            document.getElementById('user').innerHTML = 'Your Documents';
            update_page(function () {show_documents(username);});
        }
    };
    xhr.open('GET', 'http://localhost:8080/v1/api/users', true);
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    xhr.send();
}

function update_page(callback) {
    if (typeof(callback) == 'function') {
                callback();
    }
}

function show_documents(username) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var data = JSON.parse(this.responseText);
            Object.keys(data).forEach(function(key, index) {
                var uuidname = data[key].uuidname;
                var filename = data[key].filename;
                var new_elem = document.createElement('li');
                new_elem.id = 'user-file-' + key;
                new_elem.innerHTML = '<a>' + data[key].filename + '</a>';
                var documents = document.getElementById('documents');
                documents.appendChild(new_elem);
                new_elem.onclick = function() { window.location.href = 'http://localhost:8080/v1/api/files/' + uuidname; };
            });
        }
    };
    xhr.open('GET', 'http://localhost:8080/v1/api/' + username + '/' + 'files', true);
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    xhr.send();
}

document.getElementById('file-form').addEventListener('submit', function(event) {
    event.preventDefault();
    document.getElementById('upload-button').innerHTML = 'Uploading...';
    var username = document.getElementById('user').value;
    var formData = new FormData(document.getElementById('file-form'));
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 201) {
            location.reload();
        }
    };
    xhr.open('POST', 'http://localhost:8080/v1/api/' + username + '/' + 'files', true);
    xhr.send(formData);
    xhr.onload = function() {
        alert('File Uploaded.');
    };
});