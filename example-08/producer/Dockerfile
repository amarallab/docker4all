FROM python:3.8
ADD ./producer/requirements.txt /
# ADD ./producer/main.py /
# ADD ./celery_tasks/ /celery_tasks/
RUN pip3 install -r requirements.txt
WORKDIR /app
ENTRYPOINT python3 producer/main.py