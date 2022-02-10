# Quinto ejemplo

[English](README.md) [Español](README.es.md)

Vamos a meter en el desarrollo un frontend con React y
TypeScript.

Primero de todo, creamos la `app` usando `nodejs` (si no
lo tienes, instalarlo desde [nodejs.org](https://nodejs.org)).

    npx create-react-app frontend --template typescript

Para poder ejecutarlo, se suele abrir una terminal:

    $ cd frontend
    $ npm start

Pero vamos a intentar conectarlo todo con `docker-compose` y
así poder conectar con `flask` y ejecutar tareas en `celery`.

De momento, dejaremos el ejemplo tal cual. Vamos a crear el servicio:

    frontend:
      image: node:alpine
      command: npm start
      working_dir: /app
      volumes:
        - ./frontend:/app

Y ahora tendremos que redirigir las peticiones que no sean de `/api`
a este nuevo servicio. Modificamos el fichero `nginx.conf`:

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

> **Nota:** La primera vez que se inicia el servicio, `npm` tardará
>           un poco en configurar (básicamente se baja internet 
>           entero en el directorio `node-modules`).

Por otro lado, ya podemos borrar el directorio de los ficheros estáticos
HTML, lo movemos todo a react.

El comando `npm start` hace que, cuando se cambia algo en el código
fuente, el navegador se actualiza sin tener que refrescar. Esto no
funciona porque estamos pasando a través de `nginx`. Seguramente se
pueda solucionar, pero, en este ejemplo concreto, con refrescar la
página web ya es suficiente.