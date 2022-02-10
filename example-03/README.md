# Third example

[English](README.md) [Español](README.es.md)

*[marks from the translator]*

The current structure is fine, but it is not very professional to execute
the `app.run` directly; this should only be done in
development. Later we will see how to have two environments:
one for production and one for development. Meanwhile:
How to use nginx and gunicorn? (it's just an example)

What is nginx and gunicorn? It's the production quality of what `flask` does for development. `flask` is meant to be used for only one person and therefore the capability for handling multiple requests is limited. Nginx is a web server that is dedicated to receiving and reading via http. Then, gunicorn is the application server that will talk to flask a.k.a Python. 

Ok, first let's install `nginx`. Add to `docker-compose.yaml`: 

    nginx:
      image: nginx:1.17-alpine
      ports:
        - 8080:80

> **Note:** Remove the redirect from port 8080 to 5000 in `web`. 

And that's it. Port 8080 now goes directly to `nginx` and
returns the static web by default. 

To serve static HTML, you just need to mount a directory
with the files in the `/usr/share/nginx/html` directory: 

    nginx:
      image: nginx:1.17-alpine
      ports:
        - 8080:80
    volumes:
      - ./nginx/static_html:/usr/share/nginx/html


To run `flask` using `gunicorn`: First of all, we update
the `requirements.txt` adding the dependency: 

    gunicorn==20.1.0

We also modified the `command` of the `web` service, to which we also
we will rename it to `flask`: 

    flask:
      build: pythonbase
      command: gunicorn example.flask:app -b 0.0.0.0:5000
      stop_signal: SIGINT

> **Note:** Images that use Python will need to be updated. For
> default, they are not built again if we modify the file
> `requirements.txt`. An easy way is to run
> `docker-compose up --build`. 

In order to redirect `request`s starting with `/api` to the service
`flask`, we will include a configuration file in the `nginx` service:

    server {
        listen 80;
        server_name localhost;

        # proxy to flask
        location /api {
            proxy_pass http://flask:5000;
        }

        # note that I put the actual files in
        # /usr/share/nginx/html/static/
        # as this is how the path combined looks like
        location / {
        root /usr/share/nginx/html;
        }
    }

> **Note:** In the `proxy_pass`, the *host* `flask` is the `flask` service! 

Now the only remaining thing is to include configuration for the `nginx` service: 

    nginx:
      image: nginx:1.17-alpine
      ports:
        - 8080:80
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d
      - ./nginx/static_html:/usr/share/nginx/html

> **Note:** Check out the code in `code/example/flask.py`, where all
> routes have been prefixed with `/api`. 

Dependencies between services are added, so that `nginx` starts a
once the `flask` service is started. 

**BONUS**

You know I hate HTML so the static page example is done
reluctantly... 
**More bonus:** I have put `scale: 3` in the `workers` service to have
three instances...because waiting takes a lot of work. 