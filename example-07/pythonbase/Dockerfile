FROM python:3.9-alpine
RUN apk add --update --no-cache \
    build-base \
    mariadb-connector-c-dev \
    freetype-dev \
    fribidi-dev \
    harfbuzz-dev \
    jpeg-dev \
    lcms2-dev \
    libffi-dev \
    openjpeg-dev \
    tcl-dev \
    tiff-dev \
    tk-dev \
    zlib-dev
ENV PYTHONPATH=/usr/lib/python3.9/site-packages


ENV PYTHONPATH=/usr/lib/python3.9/site-packages

COPY requirements.txt /
RUN pip install -r /requirements.txt
RUN rm /requirements.txt

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1