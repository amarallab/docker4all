 # Sixth example

[English](README.md) [Español](README.es.md)

In the end, the WebSocket problem was easier to solve than it seemed: I
connected to port 3000, because that is the port that is configured within
of the container. Then, how would I do a redirect from 8080 to 3000 using 
`nginx` when connections to port 3000 are lost? To fix it, we can just publish 
the port 3000 of the frontend (or have the frontend listen for the 8080): 

    frontend:
      image: node:alpine
      command: npm start
      working_dir: /app
      ports:
        - 3000:3000
      volumes:
        - ./frontend:/app

Once here, you can install Google's `material-ui` to make a
slightly more elegant interface (in the React app we made): 

    $ npm install @material-ui/core

In this example we have created a series of React components that do
queries to the `flask` to know the status of the tasks. 

The whole development environment works simply as:

1. You can modify the code of the `celery` tasks and watchdog will be
    attentive to changes.

2. You can modify the paths of `flask`, which will do the same thing.

3. You can modify the frontend and the browser using WebSockets, which will restart
    the interface as soon as you save the files. 

Well, it seems that the development is already quite advanced. It would be necessary to include
tests and some example with databases, but for now, let's leave it
as it is. 

> **Note:** Since we're developing, the `flask` image calls back
> directly to `python` and `gunicorn` has been removed.