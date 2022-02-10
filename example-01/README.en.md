# First example

[English](README.en.md) [Español](README.es.md)

*[marks from the translator]*

In this case, I have only created a web container indicating a directory with a Dockerfile for the recipe of a lightweight python 3.9 image (alpine, ubuntu is too big). *[alpine is actually known to have some problems, see https://pythonspeed.com/articles/alpine-docker-python/ ]* I also indicate a `requirements.txt` with
the modules that I am going to use. Virtual environments? No need! We have the VM (container) just for this project!

> **Note:** If you change the `requirements.txt`, you will need to rebuild the image. 

In the image recipe, the
`/app` directory is specified as `workdir` and it is mounted to the `/code` directory. Therefore, to run flask, you don't need to specify any extra directories. With just `python -m example.flask`, python is able to find the module in the `/app` directory.

To run it, just open terminal:

    $ docker-compose up

> **Note:** Once you run this command, you'll see Docker write things such as:
>
> `example-web-1  |  * Running on all addresses.`
>
> `example-web-1  |    WARNING: This is a development server. Do not use it in a production deployment.`
>
> `example-web-1  |  * Running on http://172.24.0.2:5000/ (Press CTRL+C to quit)`
>
> The `example` prefix comes from the `.env` file, where you'll find the variable defined as `COMPOSE_PROJECT_NAME`. If this environment variable didn't exist, Docker compose would use the directory name.

Ok, so once we run `docker-compose up`, we can have the flask server running and listening on port `8080`. Note that in the `docker-compose.yaml`, we specified the configuration such that the port `8080` tunnels to port `5000`, which is where flask server is listening in the container.

Open the browser here: http://localhost:8080/welcome

There are two ways to close it: 

1. Ctrl+C in the terminal

1. Open another terminal, navigate to this directory and run
   `docker-compose down`

> **Note:** You'll have to use the second option if you run docker-compose with the `-d` option, which means `detach`. 