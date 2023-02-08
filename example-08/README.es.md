# Octavo ejemplo

[English](README.md) [Español](README.es.md)

Docker es bastante potente, pero, ¿y si no pudieses lograr todos tus objetivos con un solo ordenador?

Bienvenido a **Docker Swarm**.

Docker Swarm orquesta varios contenedores en varios hosts, por lo que ¡puedes escalar tu aplicación docker con un click de ratón!

Para hacerlo, crearemos un ejemplo sencillo (inspirado en este [repositorio](https://github.com/saurabhindoria/celery-docker-swarm)) para sumar, multiplicar, restar y dividir en contenedores separados. Usando Docker Swarm, podremos asignar _n_ `workers` de `celery` para cada tarea y Docker Swarm controlará el balanceo de la carga.

Debemos tener en cuenta que este ejemplo es una versión mejorada del repositorio vinculado. Esta versión permite múltiples tareas asignadas por `worker`, evita aplicaciones de `celery` redundantes y se organiza con menos código.

## Cada tarea

Dentro del directorio `{addition, subtraction, multiplication, division}/`, proporcionamos tres elementos esenciales:

- Dockerfile que se necesita para configurar dependencias para _ese_ contenedor específico
- Tareas disponibles para este contenedor SOLAMENTE
- `worker` de `celery` dedicado a esas tareas

## Combinándolos

Tenemos un contenedor `producer` que llama a las tareas registradas por cada `worker` de `celery`. Aunque estas tareas están definidas en sus respectivos contenedores aislados, podemos usar este contenedor `producer` para manejar cualquier combinación de tareas. Este contenedor también contiene una instancia de `Flask` solo para ayudar en el ejemplo.

También hay que tener en cuenta que podemos llamar a cualquier tarea por contenedor usando `ClassHolder` que está definido en `celery_tasks/tasks.py`.

## Réplicas

Debido a que cada contenedor solo maneja un tipo específico de tarea y no depende de ningún otro contenedor, podemos replicar cualquiera de los `workers` de `{addition, subtraction, multiplication, division}` y `celery` simplemente equilibrará la carga de cualquier tarea en la cola.

En el archivo `docker-compose.yaml`, podemos cambiar:

    deploy:
        replicas: 2

que duplicará estos `workers` en este Docker compose.

## ¡Vamos a ampliarlo!

Imaginemos que quisiéramos replicar cada `worker` por 100. Para un solo ordenador es posible que no veamos un aumento en el beneficio ya que uno solo está limitado en su concurrencia y recursos.

Si usamos Docker Swarm, podremos escalar esta aplicación en varios ordenadores.

Docker Swarm requiere un nodo `manager` que equilibre la carga de los contenedores activos, reiniciar los contenedores si fallan y asignar tareas a los nodos `workers`, que son los que realmente hacen el trabajo pesado.

Para inicializar un Docker Swarm, escribe en el host que sea el primer nodo de administrador:

    docker swarm init

A partir de ahora, haz `deploy` de los contenedores Docker en el *swarm*:

    docker stack deployment --compose-file {ruta-al-composer-file} {nombre del stack}

Para verificar si los microservicios y sus réplicas se están ejecutando:

    docker service ls

Por último, ya se pueden replicar tantos `workers` como se quieran:

    docker service scale {nombre del servicio en el stack}={número de escala}

## Añadiendo odenadores a tu *swarm*

Vamos a añadir más ordenadores al *swarm*. Escribe en el ordenador que quieres añadir:

    docker-machine create worker-node

Para ello, se necesitará un token del `manager` del *swarm*. Para obtenerlo:

    docker swarm join-token worker

Este comando generará una salida en la terminal que se tendrá que copiar y pegar más en el siguiente paso.

Para unir el node al *swarm*:

    docker-machine ssh worker-node
    {pegar el comando anterior}

¡Ahora ya tenemos los ordenadores en el *swarm*!