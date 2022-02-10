from celery.result import AsyncResult
from flask import Flask, request
from example.celery import celery, waiting

app = Flask(__name__)

@app.route("/api/welcome", methods=["GET"])
def action_list():
    return "Hello from flask!"

@app.route("/api/run/waiting/<int:seconds>", methods=["GET"])
def run_waiting(seconds: int):
    task_id = waiting.delay(seconds).id
    return {
        "task_id": task_id
    }

@app.route("/api/task/info/<task_id>", methods=["GET"])
def task_info(task_id):
    task = AsyncResult(task_id)
    if task.ready():
        return {
            "task_id": task_id,
            "progress": 1
        }
    if task.result is None:
        return {
            "task_id": task_id,
            "progress": 0
        }
    
    task_result = task.result
    task_result["task_id"] = task_id
    return task_result

@app.route("/api/task/list", methods=["GET"])
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