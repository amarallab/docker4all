# Primer ejemplo

[English](README.md) [Español](README.es.md)

En este caso, solo he creado un container `web` indicando
un directorio con un fichero `Dockerfile` para la receta
de una imagen python 3.9 ligerita (alpine, el ubuntu es
demasiado grande). También indico un `requirements.txt` con
los módulos que voy a usar. ¿Virtual environments? ¡No hace
falta, tenemos la VM (container) solo para este proyecto!

> **Nota:** Si cambias los `requirements.txt`, deberás volver
            a construir (*build*) la imagen.

En la receta de la imagen se especifica como `workdir` el
directorio `/app` y en éste se monta el directorio `code`.
Por lo tanto, para ejecutar flask, no hace falta indicar ningún
directorio extra, Tan solo con `python -m example.flask`,
python es capaz de encontrar el módulo en el directorio `/app`.

Para ejecutarlo, solo hace falta abrir una terminal:

    $ docker-compose up

> **Nota:** Verás que escribirá cosas como:
>
> `example-web-1  |  * Running on all addresses.`
>
> `example-web-1  |    WARNING: This is a development server. Do not use it in a production deployment.`
>
> `example-web-1  |  * Running on http://172.24.0.2:5000/ (Press CTRL+C to quit)`
>
> El prefijo `example` viene del fichero `.env`, donde hay una 
> variable llamada `COMPOSE_PROJECT_NAME`. Si esta variable de entorno
> no existiera, `docker-compose` utilizaría el nombre del directorio.

Bien, una vez ejecutado `docker-compose up`, ya tenemos un servidor flask
ejecutando y escuchando por el puerto `8080`. Fíjate que en el fichero
de configuración `docker-compose.yaml` se indica un tunel del puerto
`8080` al puerto `5000`, que es por donde escucha `flask`.

Abre el navegador: http://localhost:8080/welcome

Para cerrarlo hay dos formas: 

1. Ctrl+C en la terminal

1. Abre otra terminal, navega hasta este directorio y ejecuta
   `docker-compose down`

> **Nota:** El segundo ejemplo es útil cuando ejecutas el `docker-compose up`
>           con la opción `-d` (detach).