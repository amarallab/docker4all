from celery_tasks.tasks import ClassHolder
from celery_tasks.utils import create_worker_from
import celery

class Subtract(celery.Task):
    name = "subtract"
    def run(self, payload):
        """ actual implementation """
        num_1 = float(payload['num_1'])
        num_2 = float(payload['num_2'])
        ans = num_1 - num_2
        return ans

class FakeSubtract(celery.Task):
    name = "fakesubtract"
    def run(self, payload):

        return "subtract"
        
tasks = ClassHolder("subtraction", [Subtract, FakeSubtract])
# create celery app
app, worker = create_worker_from(tasks)

# start worker
if __name__ == '__main__':
    app.worker_main()