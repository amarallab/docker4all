from celery_tasks.tasks import ClassHolder
from celery_tasks.utils import create_worker_from
import celery

class Multiply(celery.Task):
    name = "multiply"
    def run(self, payload):
        """ actual implementation """
        num_1 = float(payload['num_1'])
        num_2 = float(payload['num_2'])
        ans = num_1 * num_2
        return ans

class FakeMultiply(celery.Task):
    name = "fakemultiply"
    def run(self, payload):

        return "multiply"
        
tasks = ClassHolder("multiplication", [Multiply, FakeMultiply])
# create celery app
app, worker = create_worker_from(tasks)

# start worker
if __name__ == '__main__':
    app.worker_main()