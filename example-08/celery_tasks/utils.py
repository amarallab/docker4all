import celery


def create_worker_from(ClassHolder, celery_config='celery_tasks.celery_config'):
    """
    Create worker instance given WorkerClass
    :param WorkerClass: WorkerClass to perform task
    :type WorkerClass: subclass of celery.Task
    :param celery_config: celery config module, default 'celery_tasks.celery_config'. This depends on
                            project path
    :type celery_config: str
    :return: celery app instance and worker task instance
    :rtype: tuple of (app, worker_task)
    """
    app = celery.Celery()
    app.config_from_object(celery_config)
    app.conf.update(task_default_queue=ClassHolder.name)  # update worker queue

    worker_tasks = {}
    for task in ClassHolder.tasks:

        assert issubclass(task, celery.Task)
        worker_task = app.register_task(task())
        worker_tasks[task.name] = worker_task

    return app, worker_tasks
