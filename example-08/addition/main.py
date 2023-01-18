from celery_tasks.tasks import ClassHolder
from celery_tasks.utils import create_worker_from
import celery

class Add(celery.Task):
    name = "add"
    def run(self, payload):
        """ actual implementation """
        num_1 = float(payload['num_1'])
        num_2 = float(payload['num_2'])
        ans = num_1 + num_2
        return ans

class FakeAdd(celery.Task):
    name = "fakeadd"
    def run(self, payload):

        return "add"
        
tasks = ClassHolder("addition", [Add, FakeAdd])


# create celery app
app, worker = create_worker_from(tasks)

# start worker
if __name__ == '__main__':
    app.worker_main()