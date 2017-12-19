var client_list = document.getElementById("clients");
function change_page(url, done_callback) {
    console.log("change page to: " + url);

      var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log("responseText: " + this.responseText);
            var html_start = "<body" + this.responseText.split("<body")[1];
            var body = html_start.split("</body")[0] + "</body>";
            document.body.outerHTML = body;
            console.log("done changing page to: " + url);

            if (typeof(done_callback) == "function") {
                done_callback();
            }
        }
    }
    xhttp.open("GET", url, true);
    xhttp.send();
}

function get_clients() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
	if (this.readyState == 4 && this.status == 200) {
		var data = JSON.parse(this.responseText);
        	Object.keys(data).forEach(function(key,index) {
		    	var new_elem = document.createElement("li");
		    	new_elem.id = "client-" + key + "-name";
			    new_elem.innerHTML = data[key].Name;
                var button_one = document.createElement("button");
                button_one.innerHTML = '<button id="client_' + key + '_button_one" onclick="show_documents()">Available Documents</button>';
                var button_two = document.createElement("button");
                button_two.innerHTML = '<button id="client_' + key + '_button_two" onclick="delete_user()">Delete User</button>';
                client_list.appendChild(new_elem);	
                client_list.appendChild(button_one);
                client_list.appendChild(button_two);
                button_two.onclick= function() { delete_user(data[key].Name);};
                button_one.onclick= function() {
                    change_page("client_files.html", function() {show_documents(data[key].Name);});
                };
        });
  	}
  }  
  xhttp.open("POST", "http://127.0.0.1:8000/", true);
  xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhttp.send();
}

function add_user() {
  var new_client = document.getElementById("new_client").value;
  var verify_new_client = document.getElementById("verify_new_client").value;
  if (new_client == verify_new_client && (new_client && verify_new_client != null)) {
    var user = {Name:new_client};
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var response = JSON.parse(this.response);
            console.log('response', response);
            if (response["success"] == "success"){
                alert("Success!");
            }
            else if(response["duplicate"] == "duplicate"){
                alert("Email Already In Use.");
            }
            else if(response["error"] == "error"){
                alert("Unauthorized");
            }    
        }
    }
  xhttp.open("POST", "http://127.0.0.1:8000/", true);
  xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhttp.send(JSON.stringify(user));
  }
  else if (new_client && verify_new_client == "" || new_client == "" || verify_new_client == "") {
      alert("Entry Cannot Be Blank. Try Again.");
  }
  else {
      alert("Email Addresses Do Not Match. Try Again.");
  }    
}

function delete_user(name) { 
    var name = {Name:name}
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
         if (this.readyState == 4 && this.status == 200) {
             var response = JSON.parse(this.response);
             if (response["success"] == "success"){
                 alert("Success!");
             }
             else if(response["error"] == "error"){
                 alert("Unauthorized");
             }
         }
    }
  xhttp.open("POST", "http://127.0.0.1:8000/", true);
  xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhttp.send(JSON.stringify(name));
}

function show_documents(nameparam) {
    var name = {Name:nameparam}
    document.getElementById("client_name").value = nameparam;
    document.getElementById("client").innerHTML = "Documents for " + nameparam;
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var data = JSON.parse(this.responseText);
        Object.keys(data).forEach(function(key,index) {
            var filename = data[key].filename;
            var file_id = data[key].file_id;
            console.log('filename', filename);
            console.log('file_id', file_id);
            var new_elem = document.createElement("li");
            new_elem.id = "client-file-" + key;
            new_elem.innerHTML = '<a>' + data[key].filename +'</a>';
            var delete_file_button = document.createElement("button");
            delete_file_button.innerHTML = '<button>Delete File</button>';
            var files = document.getElementById("files");
            files.appendChild(new_elem);  
            files.appendChild(delete_file_button);
            new_elem.onclick = function() {window.location.href="http://127.0.0.1:8000/" + filename + "/" + file_id;}; 
            delete_file_button.onclick = function() {window.location.href="http://127.0.0.1:8000/" + filename + "/" + file_id;};
        });
     }
  }  
  xhttp.open("POST", "http://127.0.0.1:8000/", true);
  xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhttp.send(JSON.stringify(name));
}
