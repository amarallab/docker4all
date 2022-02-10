from celery import Celery, current_task, states

import datetime
import os 
import time

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

@celery.task(name="waiting")
def waiting(delay):
    begin = datetime.datetime.now()
    while True:
        elapsed_time = (datetime.datetime.now() - begin).total_seconds()
        if elapsed_time >= delay:
            break
        time.sleep(1)
        current_task.update_state(
            state=states.STARTED,
            meta={
                "status": "running",
                "elapsed_time": elapsed_time,
                "delay_time": delay,
                "progress": elapsed_time / delay
            }
        )
        print(f"waiting({delay}): {elapsed_time / delay}")
