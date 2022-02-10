# Seventh exammple

[English](README.en.md) [Español](README.es.md)

I got curious about WebSockets, so let's work it into the service. 
Since I don't want to change the example we have with
`celery`, I'm going to create another `flask` service that responds
to `WebSockets` requests and an application with `Xcode`
to act as a client. 

To do this, I will end up mounting the `nginx` service again and
all requests to `localhost:8080/ws/` will go to a
new service `flask_ws`. 

In the meantime, I'll first make the `flask_ws` service which
listens to everything and later I will integrate. Although, in this
`commit`, you will only see the final work. 

## Nginx

The server has to forward requests for `socket.io`
to the `flask_ws` server, so:

    location /socket.io {
        proxy_http_version 1.1;
        proxy_buffering off;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_pass http://flask_ws_upstream/socket.io;
    }

But be careful! I put `flask_ws_upstream`, not `flask_ws`.
I don't know exactly what the upstream does, but the
`websockets` didn't work without it, so upstream is defined at startup
from the `nginx` configuration file: 

    upstream flask_ws_upstream {
        server flask_ws:5000;
    }


> **Note:** In order not to have problems with the domain, I have edited
> the `/etc/hosts` file and added the name `heltenachat.com`
> and assigned to `127.0.0.1`: 
>
>        127.0.0.1 heltenachat.com
>
> &nbsp;

## MariaDB

Now yes, I'm going to save the chat messages on a server
Database. To do this, I defined a new service in
`docker-compose` with the `mariadb` image. I'll mount the
`mariadb-data` volume in `/var/lib/mysql` so I don't lose
the data from the database. 

The connection data is included in the file
`mariadb.env`. 

## Flask WebServer

In order to work with `websockets`, this service must work with `gunicorn`. To be able to restart it when
a file changes, I include in the `watchmedo` command. 

I also include as a dependency of `mariadb` that the condition should be *healthy*, not just running: 

    depends_on:
      mariadb:
        condition: service_healthy

How to define that a service is "*healthy*"? We can indicate this
with the `healthcheck` field: 

    healthcheck:
      test: "mysql -u $${MARIADB_USER} -p$${MARIADB_PASSWORD} -e \"USE $${MARIADB_DATABASE}\""
      interval: 2s
      timeout: 20s
      retries: 10

In this case, the service will be "*healthy*" when it can be
connected to the database with a valid username and password. 

> **Note:** Double dollar (`$${MARIADB_USER}`) is used because
> you have to use the value of the variable **inside**
> from the service, not when creating the image from `docker` .

## BONUS: Xcode

If you have `macOS` and `Xcode`, you can run the app
chat on an `iOS` device with this project.

The last five chat messages will appear on the web page,
so I have also changed the code of `react`. 