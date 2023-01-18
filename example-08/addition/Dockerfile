FROM python:3.8
ADD ./addition/requirements.txt /
# ADD ./addition/main.py /
# ADD ./celery_tasks/ /celery_tasks/
RUN pip3 install -r requirements.txt
WORKDIR /app
ENTRYPOINT celery -A addition.main worker --concurrency=4 --loglevel=info -n addition_worker.%h