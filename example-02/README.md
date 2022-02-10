# Second example

[English](README.md) [Español](README.es.md)

*[marks from the translator]*

Flask is not enough, especially when we need to run *very expensive* tasks (in time, resources, cost). 
We are going to use **celery** with a *worker*. To connect them to the tasks and Flask, we will use **redis**. 

To instantiate a **redis** service, we include in `docker-compose.yaml`: 

    services:
      ...
      redis:
        image: redis:6-alpine

And that's it! The default configuration is enough for us. By default, all
services are connected in a virtual network and can be connected using the
Service name. Thus, from `web` you can access the service **redis**
using as *hostname* `redis`. 

Now, I'm going to define a task. To do this, I'll create another `python` file in the
`code/example` directory named `celery.py`. The important parts are: 

1. Define how the service is configured:

```
    celery = Celery(__name__)
    celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
    celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")
```

> **Note:** We're using environment variables again. We'll come back to them in a second.

2. Define a task:

```
    @celery.task(name="waiting")
    def waiting(delay):
        ...code...
```

Now let's define the *celery* workers. To do this, define a new
    service in the `docker-compose.yaml` where the command will be executed
    `celery` (installed from `requirements.txt`). The service looks like the following: 

```
    worker:
      build: pythonbase
      command: celery --app example.celery worker --loglevel=info
      volumes:
        - ./code:/app
      env_file:
        - redis-conf.env
      depends_on:
        - web
        - redis
```

Dependencies between services are also marked in `depends_on`.
This marks the start order of each service. In this case, first
the `redis` service is started (since `web` depends on `redis`), then `web`, and finally `worker` (which depends on both). 

We need to indicate how the service wll connect between *workers* and clients.
In this example, the service we use is **redis**, so we will have to define the two variables of
*CELERY_*. To do this, I'll create a file called `redis-conf.env`: 

    CELERY_BROKER_URL=redis://redis:6379/0
    CELERY_RESULT_BACKEND=redis://redis:6379/0

which takes into account that the second mention of `redis` is the *hostname* of the defined service
in `docker-compose.yaml`. That's it, everything works. 

Now we need to tell flask to execute the tasks. To do this, the `flask.py` file is modified to add a route: 

    @app.route("/run/waiting/<int:seconds>", methods=["GET"])
    def run_waiting(seconds: int):
        task_id = waiting.delay(seconds).id
        return {
            "task_id": task_id
        }

And that's it, now *flask* executes the task *waiting* on the first *worker* that becomes available. Remember that Flask is actually connecting to `Celery`, and a `worker` in `Celery` is doing the task. Flask is simply an endpoint. 

**BONUS**

To see the status of the tasks, you can make a query to the service of
*celery*: 

    @app.route("/task/list", methods=["GET"])
    def task_list():
        active_celery_tasks = celery.control.inspect().active()
        if active_celery_tasks is None:
            return {"task_list": []}
        
        result = []
        for celery_server in active_celery_tasks.values():
            for task in celery_server:
                task_result = AsyncResult(task["id"]).result
                if task_result is None:
                    continue
                task_result["task_id"] = task["id"]
                result.append(task_result)
        return {
            "task_list": result
        }

> **Final note:** Pressing Ctrl+C does not work with
> the `web` service, which worked in the previous example because it was the sole service provided (?). This is because `docker-compose` sends
> the signal `SIGTERM` and `flask` doesn't know how to interpret it, so it continues
> its execution.
> For Ctrl+C to stop the `flask` service, we indicate that
> `stop-signal` has to be sent to the `web` service with
> `stop_signal: SIGINT` in the configuration file. 
> [*Ctrl+C is actually equivalent to `docker-compose stop` which simply exits the containers while `docker-compose down` exits and removes all stopped containers.*]
