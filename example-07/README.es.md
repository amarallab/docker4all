# Séptimo ejemplo

[English](README.md) [Español](README.es.md)

Me ha salido la curiosidad de los WebSockets, así que vamos a
ello. Como no quiero cambiar el ejemplo que tenemos con
`celery`, voy a crear otro servicio `flask` que responda
a peticiones de `WebSockets` y una aplicación con `Xcode`
que haga de cliente.

Para ello, acabaré montando otra vez el servicio `nginx` y
todas las peticiones a `localhost:8080/ws/` irán a un
nuevo servicio `flask_ws`.

Mientras tanto, primero haré el servicio `flask_ws` que
escuche todo y ya después integraré, aunque, en este
`commit`, solo vas a ver el trabajo final.

## Nginx

El servidor tiene que reenviar las peticiones de `socket.io`
al servidor de `flask_ws`, así que:

    location /socket.io {
        proxy_http_version 1.1;
        proxy_buffering off;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_pass http://flask_ws_upstream/socket.io;
    }

Pero, ¡cuidado!, que no he puesto `flask_ws`, sino `flask_ws_upstream`.
No sé exactamente qué hace el upstream, pero no funcionan los
`websockets` sin ello, así que se define el upstream al inicio
del fichero de configuración de `nginx`:

    upstream flask_ws_upstream {
        server flask_ws:5000;
    }


> **Nota:** Para no tener problemas con el dominio, he editado
>           el fichero `/etc/hosts` y he añadido el nombre `heltenachat.com`
>           y asignado a `127.0.0.1`:
>
>        127.0.0.1 heltenachat.com
>
> &nbsp;

## MariaDB

Ahora sí, voy a guardar los mensajes del chat en un servidor
de base de datos. Para ello, defino un nuevo servicio en 
`docker-compose` con la imagen de `mariadb`. Montaré el
volumen `mariadb-data` en `/var/lib/mysql` y así no perderé
los datos de la base de datos.

Los datos de la conexión se incluyen en el fichero
`mariadb.env`.

## Flask WebServer

Para poder trabajar con `websockets`, este servicio debe
de trabajar con `gunicorn`. Para poder reiniciarlo cuando
un fichero cambia, incluyo en el comando `watchmedo`.

También incluyo como dependencia de `mariadb` no solo que
esté arriba, sigo que esté "*healthy*":

    depends_on:
      mariadb:
        condition: service_healthy

¿Cómo defino que un servicio está "*helathy*"? Indicándolo
con el campo `healthcheck`:

    healthcheck:
      test: "mysql -u $${MARIADB_USER} -p$${MARIADB_PASSWORD} -e \"USE $${MARIADB_DATABASE}\""
      interval: 2s
      timeout: 20s
      retries: 10

En este caso, el servicio estará "*healthy*" cuando se pueda
conectar a la base de datos con usuario y contraseña válidos.

> **Nota:** Se usa doble dólar (`$${MARIADB_USER}`) porque se
>           tiene que usar el valor de la variable **dentro**
>           del servicio, no al crear la imagen desde `docker`.

## BONUS: Xcode

Si tienes `macOS` y `Xcode`, puedes ejecutar la aplicación
de chat en un dispotivo `iOS` con este proyecto.

Los cinco últimos mensajes del chat aparecerán en la página web, 
así que también he cambiado el código de `react`.