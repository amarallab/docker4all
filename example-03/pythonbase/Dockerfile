FROM python:3.9-alpine
RUN apk add --update --no-cache
ENV PYTHONPATH=/usr/lib/python3.9/site-packages

COPY requirements.txt /
RUN pip install -r /requirements.txt
RUN rm /requirements.txt

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1