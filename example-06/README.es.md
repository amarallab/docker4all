# Sexto ejemplo

[English](README.md) [Español](README.es.md)

Al final, era más sencillo de lo que parecía el tema del WebSocket: Intenta
conectar al puerto 3000, porque es el puerto que está configurado dentro
del container. Como se hace un redirect del 8080 al 3000 usando `nginx`,
las conexiones al puerto 3000 se pierden. Para solucionarlo, tan solo
hace falta publicar el puerto 3000 del frontend (o que el frontend
escuche por el 8080):

    frontend:
      image: node:alpine
      command: npm start
      working_dir: /app
      ports:
        - 3000:3000
      volumes:
        - ./frontend:/app

Una vez aquí, se puede instalar el `material-ui` de Google para hacer una
interfaz un poco más elegante (en la app React que hicimos):

    $ npm install @material-ui/core

En este ejemplo se ha creado una serie de componentes React que hacen
consultas al `flask` para saber el estado de las tareas.

El desarrollo de todo el entorno, simplemente, funciona:

1. Puedes modificar el código de las tareas de `celery` y watchdog estará
   atento a los cambios.

2. Puedes modificar las rutas de `flask`, que hará lo mismo.

3. Puedes modificar el frontend, el navegador, usando WebSockets, reiniciará
   la interfaz nada más guardar los ficheros.

Bueno, parece que el desarrollo ya está bastante avanzado. Faltaría incluir
testings y algún ejemplo con bases de datos, pero, de momento, vamos a dejarlo
de lado.

> **Nota:** Como estamos en desarrollo, la imagen de `flask` vuelve a llamar
>           directamente a `python` y se ha quitado `gunicorn`.