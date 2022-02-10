# Tercer ejemplo

[English](README.md) [Español](README.es.md)

La estructura está bien, pero no es muy profesional ejecutar
el `app.run` directamente, cuando esto solo debe hacerse en
desarrollo. Más adelante veremos cómo tener dos entornos:
uno para producción y otro de desarrollo. Mientras, tanto:
¿Cómo usar nginx y gunicorn? (es solo un ejemplo)

Bien, primero instalemos `nginx`. Añadir a `docker-compose.yaml`:

    nginx:
      image: nginx:1.17-alpine
      ports:
        - 8080:80

> **Nota:** Quita el redirect del port 8080 al 5000 en `web`.

Y ya está. El puerto 8080 ahora va directamente a `nginx` y
retorna la web estática por defecto.

Para servir HTML estático, tan solo hace falta montar un directorio
con los ficheros en el directorio `/usr/share/nginx/html`:

    nginx:
      image: nginx:1.17-alpine
      ports:
        - 8080:80
    volumes:
      - ./nginx/static_html:/usr/share/nginx/html


Para ejecutar `flask` usando `gunicorn`: primero de todo, actualizamos
el `requirements.txt` añadiendo la dependencia:

    gunicorn==20.1.0

También modificamos el `command` del servicio de `web`, al que tambien
le cambiaremos el nombre por `flask`:

    flask:
      build: pythonbase
      command: gunicorn example.flask:app -b 0.0.0.0:5000
      stop_signal: SIGINT

> **Nota:** Las imágenes que usar Python tendrán que actualizarse. Por
>           defecto, no se construyen de nuevo si modificamos el fichero
>           `requirements.txt`. Una forma sencilla es ejecutar
>           `docker-compose up --build`.

Para poder redirigir las `request` que comiencen por `/api` al servicio
`flask`, incluiremos un fichero de configuración en el servicio `nginx`:

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

> **Nota:** en el `proxy_pass`, el *host* `flask` es el servicio `flask`!

Ahora solo queda incluir el fichero de configuración en el servicio `nginx`:

    nginx:
      image: nginx:1.17-alpine
      ports:
        - 8080:80
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d
      - ./nginx/static_html:/usr/share/nginx/html

> **Nota:** Revisa el código de `code/example/flask.py`, donde a todas
>           las rutas se les ha añadido un prefijo `/api`.

Se añaden dependencias entre servicios, para que `nginx` comience una
vez el servicio `flask` esté iniciado.

**BONUS**

Sabes que odio HTML, así que el ejemplo de la página estática está hecho
a mala gana...

**Otro bonus:** he puesto `scale: 3` en el servicio de `workers` para tener
tres instancias... porque esperar requiere mucho trabajo.