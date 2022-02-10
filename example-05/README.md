# Fifth example

[English](README.md) [Español](README.es.md)

We are going to develop a frontend with React and
TypeScript.

First of all, we create the `app` using `nodejs` (if you don't have it, install from [nodejs.org](https://nodejs.org)).

    npx create-react-app frontend --template typescript

To execute it, open a terminal: 

    $ cd frontend
    $ npm start

But let's try to connect everything with `docker-compose`
so that you can connect to `flask` and run tasks in `celery`. 

For now, we will leave the example as is. Let's create the service: 

    frontend:
      image: node:alpine
      command: npm start
      working_dir: /app
      volumes:
        - ./frontend:/app

And now we will have to redirect non-`/api` requests
to this new service. We modify the `nginx.conf` file: 

    server {
        listen 80;
        server_name localhost;

        # proxy to flask
        location /api {
            proxy_pass http://flask:5000;
        }

        # proxy to frontend / npm
        location / {
            proxy_pass http://frontend:3000;
        }
    }

> **Note:** The first time the service starts, `npm` will take
> a bit of configuring (basically internet is downloading
> packages in the `node-modules` directory). 

On the other hand, we can now delete the directory of static files in
HTML since we're moving everything to React.

The `npm start` command would normally allow the browser to refresh without having to click refresh when something is changed in the code
source. This does not
works here because we are passing through `nginx`. I'm sure I
can solve this, but, in this specific example, with refreshing the
website is enough. 