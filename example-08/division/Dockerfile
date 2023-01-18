FROM python:3.8
ADD ./division/requirements.txt /
# ADD ./division/main.py /
# ADD ./celery_tasks/ /celery_tasks/
RUN pip3 install -r requirements.txt
WORKDIR /app
ENTRYPOINT celery -A division.main worker --concurrency=4 --loglevel=info -n division_worker.%h