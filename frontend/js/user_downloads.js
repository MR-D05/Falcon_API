var client_list = document.getElementById("files");
function retrieve_files() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var response = JSON.parse(this.response);
        var data = JSON.parse(this.responseText);
            Object.keys(data).forEach(function(key,index) {
                var new_elem = document.createElement("a");
                new_elem.id = "client-" + key + "-file";
                new_elem.setAttribute('href', ' ' +
                new_elem.innerHTML = data[key].filename;
                var button_one = document.createElement("button");
                button_one.innerHTML = '<button id="client_' + key + '_button_one" onclick="show_documents()">Available Documents</button>';
                var button_two = document.createElement("button");
                button_two.innerHTML = '<button id="client_' + key + '_button_two" onclick="delete_user()">Delete User</button>';
                client_list.appendChild(new_elem);  
                client_list.appendChild(button_one);
                client_list.appendChild(button_two);
                button_two.onclick= function() { delete_user(data[key].Name);};
        });
    }
  }  
  xhttp.open("GET", "http://127.0.0.1:8000/v1/api/files", true);
  xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhttp.send();
}

