import random

import sys
sys.path.append('')

# from celery_tasks.tasks import AdditionCeleryTask, SubtractionCeleryTask, MultiplicationCeleryTask, DivisionCeleryTask
# from division.main import tasks as divisiontask
from division.main import worker as division_worker
from multiplication.main import worker as multiplication_worker
from addition.main import worker as addition_worker
from subtraction.main import worker as subtraction_worker

from flask import Flask

flask_app = Flask(__name__)

# create worker
# _, addition_worker = create_worker_from(additiontask)
# _, subtraction_worker = create_worker_from(subtractiontask)
# _, multiplication_worker = create_worker_from(multiplicationtask)
# _, division_worker = create_worker_from(divisiontask)


@flask_app.route('/create_tasks/<count>', methods=["GET"])
def create_tasks(count):
    count = int(count)
    for i in range(count):
        num_1 = random.randint(1, 1000)
        num_2 = random.randint(1, 1000)
        payload = {
            'num_1': num_1,
            'num_2': num_2
        }
        addition_worker['fakeadd'].apply_async(args=[payload, ])
        subtraction_worker['fakesubtract'].apply_async(args=[payload, ])
        multiplication_worker['fakemultiply'].apply_async(args=[payload, ])
        division_worker['fakedivide'].apply_async(args=[payload, ])
    return "Done " + str(count)


if __name__ == '__main__':
    flask_app.run(host = "0.0.0.0", port=5000, debug=True)
