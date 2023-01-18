FROM python:3.8
ADD ./multiplication/requirements.txt /
# ADD ./multiplication/main.py /
# ADD ./celery_tasks/ /celery_tasks/
RUN pip3 install -r requirements.txt
WORKDIR /app
ENTRYPOINT celery -A multiplication.main worker --concurrency=4 --loglevel=info -n multiplication_worker.%h