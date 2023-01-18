from celery_tasks.tasks import ClassHolder
from celery_tasks.utils import create_worker_from
import celery


class Divide(celery.Task):
    name = "divide"
    def run(self, payload):
        """ actual implementation """
        num_1 = float(payload['num_1'])
        num_2 = float(payload['num_2'])
        if num_2 != 0:
            ans = num_1 / num_2
        else:
            ans = "ND"
        return ans

class FakeDivide(celery.Task):
    name = "fakedivide"
    def run(self, payload):

        return "divide"
        
tasks = ClassHolder("division", [Divide, FakeDivide])

# create celery app
app, worker = create_worker_from(tasks)

# start worker
if __name__ == '__main__':
    app.worker_main()