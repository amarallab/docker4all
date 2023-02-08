# Eighth example

[English](README.md) [Español](README.es.md)

Docker is extremely powerful, but what if you can't achieve your goals at scale with only one host computer?

Enter **Docker Swarm**.

Docker Swarm orchestrates containers across multiple hosts so that you can scale up your dockerized application at the click of a button!

To do this, I will create a dummy example (inspired by this [repo](https://github.com/saurabhindoria/celery-docker-swarm)) that can add, multiply, subtract, and divide on separate, isolated containers. Using Docker Swarm, we'll be able to assign _n_ `celery` workers per each task, and Docker Swarm will handle the load balancing and managing!

Note that this example is an improved version of the linked repo. This version allows for multiple assigned tasks per worker, avoids redundant Celery apps, and organized with less code.

## Each task

Inside `{addition, subtraction, multiplication, division}/` folder, we provide three essentials:

- Dockerfile that is needed to set up dependencies for _that_ specific container
- Tasks available for this container ONLY
- Celery worker dedicated to those tasks

## Combining them

We have a container `producer` that calls the registered tasks per `celery` worker. Even though those tasks are defined in their respective, isolated containers, we can use this `producer` container to handle any combination of tasks. This container also contains a `Flask` instance just to help with this example.

Note that we can also call any task per container using the `ClassHolder` defined in `celery_tasks/tasks.py`.

## Replicas

Because each container only handles one specific type of task, and do not depend on any other container, we can replicate any of the `{addition, subtraction, multiplication, division}` workers and Celery will just load balance any tasks in the queue.

In the `docker-compose.yaml` file, we see

      deploy:
            replicas: 2

which will duplicate these workers in this Docker compose.

## Let's scale it up!

Imagine if we wanted to replicate each worker by 100. For one single machine, we may see no increase in benefit since one single computer is limited in its concurrency and resources.

So Docker Swarm will scale this application across multiple hosts.

Docker Swarm requires a `manager` node which will load balance active containers, will restart containers if they crash, and will assign work to `worker` nodes, which do the actual heavy lifting.

To initialize a Docker Swarm, head to the host that will be your first manager host node and type:

    docker swarm init

Then, deploy the Docker containers in the swarm:

    docker stack deploy --compose-file {path-to-compose-file} {name of stack}

You'll be able to check if the microservices are running and their replicas by

    docker service ls

You can now replicate however many workers now, so trivial :)

    docker service scale {name of service in stack}={number of scale}

## Adding workers to your swarm

Now, let's add more computers to join your swarm.

Head to the computer that will be your worker and type:

    docker-machine create worker-node

You'll need a token from your manager swarm node. Get it by

    docker swarm join-token worker

This will output a command for you to use later.

And now we'll join the worker to the swarm by

    docker-machine ssh worker-node

    {type the command from earlier}

Now, you have workers to your swarm!
