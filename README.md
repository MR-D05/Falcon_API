A RESTful SaaS File Storage Application Implementing the Falcon Framework
====================


Read Falcon's documention here:

[https://github.com/falconry/falcon](https://github.com/falconry/falcon)
[http://falcon.readthedocs.org/en/latest/](http://falcon.readthedocs.org/en/latest/)


Running Outside of Docker
====================


The following tutorial will get this application up and runnning on a Debian-based system. Note that you will have to modify the following commands to reflect the most up-to-date packages.

Ensure that you have [nginx](https://nginx.org/en/docs/) as well as [PostgreSQL](https://www.postgresql.org/) installed on your system.

Download [Flyway](http://flywaydb.org/) and install it to your /opt directory, make it executable, and export to PATH. 

```
sudo wget https://repo1.maven.org/maven2/org/flywaydb/flyway-commandline/5.0.2/flyway-commandline-5.0.2-linux-x64.tar.gz && sudo tar -xf flyway-commandline-5.0.2-linux-x64.tar.gz -C /opt && sudo chmod a+x /opt/flyway-5.0.2/flyway
```

```
PATH=$PATH:/opt/flyway-5.0.2
````

I recommend using [pipenv](https://docs.pipenv.org/) to create and manage a virtualenv for an instance of this applicaiton running outside of Docker. Go ahead and install [pipenv](https://docs.pipenv.org/). After spawning an environment shell with:

```
pipenv shell
```

Install the application's dependencies with:

```
pipenv install
```

When dependencies are finished installing, you should be able to run the application successfully with:

```
pipenv run DATABASE_URL='postgresql://localhost:5432/databasename?user=yourusername&password=yourpassword' APP_STORAGE_PATH=./file_storage gunicorn --reload 'falconapi.app:get_app()'
```

You want to make sure the PostgreSQL connection URL contains your specific database name, username, and password.

Also, go ahead and amend your PostgreSQL pg_hba.conf file so flyway can connect via JDBC. The JDBC driver connects to PostgreSQL via TCP. Though not advised as a permanent configuration, to get started, alter the pg_hba.conf file to reflect the 'trust' method for IPv4 connections. You can find this file in this working directory:

```
/etc/postgresql/9.4/main
```

From here, with proper configuration of [nginx](https://nginx.org/en/docs/), you should be able to begin feeling out the functionality of the application by navigating to [localhost](http://localhost:8080).

You want your [nginx.conf](https://www.nginx.com/resources/wiki/start/topics/examples/full/) file to point to the frontend directory for this application such that when you point the browser to localhost:8080 it will serve up your frontend files. You also want to adjust the configuration in such a way that when the browser hits any url with the prefix '/v1' it will hit the application backend at a different port of the same domain. Something like this:

```
    server {
        listen       8080;
        server_name  localhost;

        location /v1 {
            proxy_pass http://127.0.0.1:8000;
        }
        
        location / {
            root   /path/to/falconapi/frontend;
            index  index.html index.htm;
        }
```

Now, restart [nginx](https://nginx.org/en/docs/) "nginx -s reload", and point your browswer to localhost:8080. 

Environment Variables?
====================


`DATABASE_URL` - Connection URL for the PostgreSQL database.


Migrations
====================


This application uses [Flyway](http://flywaydb.org/) to manage database migrations with [PostgreSQL](https://www.postgresql.org/).


Testing
====================


```
docker-compose run web nosetests -v --with-coverage --cover-package=app --cover-xml --cover-html
```


API Endpoints
====================


### Verify existing user

**POST:**
```
/v1/api/users
```

**Body:**
```JSON
{
    "email": "email",
    "password": "password"
}
```

**Response:**
```JSON
{
    "token": "token"
}
```

**Status Codes:**
* `200` Success
* `400` Bad Request


### Create a new user

**PUT:**
```
/v1/api/users
```

**Body:**
```JSON
{
    "email": "email",
    "username": "username",
    "password": "password"
}
```

**Response:**
```JSON
{
    "token": "token"
}
```

**Status Codes:**
* `201` Success
* `400` Bad Request
* `409` Bad Request (Email taken)


### Retrieve users

**GET:**
```
/v1/api/users
```

**Body:**
```JSON
{
    "email": "email",
    "password": "password"
}
```


### Retrieve an existing user's files

**GET:**
```
/v1/api/files
```

**Body:**
```JSON
{
    "username": "username",
    "password": "password"
}
```

**Response:**
```JSON
{
    "token": "token"
}
```

**Status Codes:**
* `200` Success
* `500` Internal Server Error


### Insert a new file for existing user 

**POST:**
```
v1/api/{username}/files
```

**Body:**
```JSON
{
    "username": "username",
    "password": "password"
}
```

**Response:**
```JSON
{
    "token": "token"
}
```

**Status Codes:**
* `200` Success
* `400` Bad Request


### Delete a file

**DELETE:**
```
/v1/api/files/{filename}
```


**Status Codes:**
* `200` Success
* `500` Internal Server Error


### Download a file

**GET:**
```
/v1/api/files/{filename}
```


**Status Codes:**
* `200` Success
* `500` Internal Server Error
