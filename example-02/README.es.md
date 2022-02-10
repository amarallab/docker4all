# Segundo ejemplo

[English](README.md) [Español](README.es.md)

Flask no es suficiente, necesitamos ejecutar tareas *muy costosas* en un sistema
de tareas. Vamos a usar **celery**, de momento, con un *worker* y, para conectarlo
todo, usaremos **redis**.

Para instanciar un servicio de **redis**, incluimos en `docker-compose.yaml`:

    services:
      ...
      redis:
        image: redis:6-alpine

¡Y ya está! La configuración por defecto ya es correcta. Por defecto, todos los
servicios están conectados en una red virtual y se pueden conectar usando el 
nombre del servicio. Así, desde `web` se puede acceder al servicio **redis**
usando como *hostname* `redis`.

Ahora, voy a definir una tarea. Para ello, creo otro fichero de `python` en el
directorio `code/example` llamado `celery.py`. Las partes importantes son:

1. Definir cómo se configura el servicio:

```
    celery = Celery(__name__)
    celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
    celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")
```

> **Nota:** Usamos otra vez variables de entorno, las vemos en un momento.

2. Definir una tarea:

```
    @celery.task(name="waiting")
    def waiting(delay):
        ...code...
```

Ahora vamos a definir los *workers* de *celery*. Para ello, se define un nuevo
   servicio en el `docker-compose.yaml` donde se ejecutará el comando
   `celery` (instalado a partir del `requirements.txt`). El servicio:

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

Por otro lado, también se marcan las dependencias entre los servicios.
Esto marca el orden de inicio de cada servicio. En este caso, primero
se inicia el servicio `redis`, después `web` y, por último, `worker`.

Necesitamos indicar el servicio para conectar entre *workers* y los clientes. En
este ejemplo usamos **redis**, así que tendremos que definir las dos variables de
*CELERY_*. Para ello, creo un fichero llamado `redis-conf.env`:

    CELERY_BROKER_URL=redis://redis:6379/0
    CELERY_RESULT_BACKEND=redis://redis:6379/0

Teniendo en cuenta que el segundo `redis` es el *hostname* del servicio definido
en `docker-compose.yaml`. Ya está, todo funciona.

Ahora falta ejecutar las tareas, para ello, se modifica el fichero `flask.py` y se
le añade una ruta:

    @app.route("/run/waiting/<int:seconds>", methods=["GET"])
    def run_waiting(seconds: int):
        task_id = waiting.delay(seconds).id
        return {
            "task_id": task_id
        }

Y ya está, ahora *flask* ejecuta la tarea *waiting* en el primer *worker* que 
esté libre.

**BONUS**

Para ver el estado de las tareas, se puede hacer una consulta al servicio de
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

> **Nota final:** Para cancelar los servicios, presionar Ctrl+C no funciona con
>                 el servicio `web`. Esto es debido a que `docker-compose` envia
>                 el signal `SIGTERM` y `flask` no lo interpreta, así que sigue
>                 su ejecución.
>                 Para que Ctrl+C pare el servicio de `flask`, se indica que
>                 `stop-signal` se tiene que enviar al servicio `web` con
>                 `stop_signal: SIGINT`.
