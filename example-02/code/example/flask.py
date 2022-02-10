from celery.result import AsyncResult
from flask import Flask, request
from example.celery import celery, waiting

app = Flask(__name__)

@app.route("/welcome", methods=["GET"])
def action_list():
    return "Hello!"

@app.route("/run/waiting/<int:seconds>", methods=["GET"])
def run_waiting(seconds: int):
    task_id = waiting.delay(seconds).id
    return {
        "task_id": task_id
    }

@app.route("/task/list", methods=["GET"])
def task_list():
    active_celery_tasks = celery.control.inspect().active()
    if active_celery_tasks is None:
        return {"task_list": []}
    
    result = []
    for celery_server in active_celery_tasks.values():
        for task in celery_server:
            task_result = AsyncResult(task["id"]).result
            if task_result is None:
                continue
            task_result["task_id"] = task["id"]
            result.append(task_result)
    return {
        "task_list": result
    }

if __name__ == "__main__":
    app.run("0.0.0.0", 5000)