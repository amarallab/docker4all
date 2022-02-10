# Fourth example

[English](README.en.md) [Español](README.es.md)

Before delving into different types of environments
(production, development, CI), let's focus on the
development.

It would be great if the changes we are making are
reflect directly in the execution, and we wouldn't have
to go restarting the containers.

For now, we'll remove the `gunicorn`, but leave
the `nginx`. It works the same, but we'll run
`flask` again in development mode.

For `flask` to reload the files we have
changed, it is only necessary to indicate with an environment variable that reloads: 

    flask:
      build: pythonbase
      command: python -m example.flask
      stop_signal: SIGINT
      environment:
        - FLASK_ENV=development
      env_file:
        - redis-conf.env
      volumes:
        - ./code:/app
      depends_on:
        - redis

With `workers` we can do the same, but with `celery`
you don't have this option. Therefore, we will use the
Python `watchdog` package to restart `celery`
whenever changes are detected: 

1. In the `requirements.txt` file we'll include the
    dependency `watchdog==2.1.6` 

2. We'll change the `worker` command to `watchmedo`: 

```
    worker:
      build: pythonbase
      command: watchmedo auto-restart \
               --directory=/app --pattern=*.py \
               --recursive -- celery --app example.celery \
               worker --loglevel=info
      volumes:
        - ./code:/app
      env_file:
        - redis-conf.env
      depends_on:
        - flask
        - redis
```

Ok, now you don't need to do anything to make changes, see the magic happen: 

1. Include a new `task` in `celery`. 
1. Include a new `route` in `flask`. 
1. Develop

**BONUS**

In Visual Studio Code you can install an extension to
start/stop services easily: 

![](vscode-docker-menu.png)