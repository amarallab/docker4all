# Cuarto ejemplo

[English](README.md) [Español](README.es.md)

Antes de profundizar en diferentes tipos de entornos
(producción, desarrollo, CI), vamos a centrarnos en el
desarrollo.

Estaría genial que los cambios que vamos haciendo se
reflejen directamente en la ejecución, y así no tener
que ir reiniciando los contenedores.

De momento, quitamos de nuevo el `gunicorn`, pero dejamos
el `nginx`. Funciona igual, pero volvemos a ejecutar
`flask` en modo de desarrollo.

Para que `flask` recargue los ficheros que hemos
cambiado, tan solo hace falta indicar con una variable
de entorno que recargue:

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

Con los `workers` podemos hacer lo mismo, pero `celery`
no tiene una opción para hacerlo. Utilizaremos el
paquete `watchdog` de Python para reiniciar `celery`
cada vez que se detecten cambios:

1. En el fichero `requirements.txt` incluimos la
   dependencia `watchdog==2.1.6`

2. Cambiamos el comando del `worker` por el `watchmedo`:

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

Bien, ahora no hace falta hacer nada para hacer cambios, como:

1. Incluir una nueva `task` en `celery`. 
1. Incluir una nueva `route` en `flask`.
1. Desarrollo

**BONUS**

En Visual Studio Code se puede instalar una extensión para
iniciar/parar los servicios fácilmente:

![](vscode-docker-menu.png)