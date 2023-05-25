FROM ubuntu:20.04
FROM python:3.9
LABEL authors="EndEden"

WORKDIR /usr/src/app

ARG DEBIAN_FRONTEND=noninteractive

ENV TZ="Europe/Chisinau"


RUN apt-get update && apt-get install -y software-properties-common mc \
 python3-pip \
 pandoc libpq-dev

RUN apt-get update -y \
  && apt-get -y install \
    xvfb

RUN apt-get install -y python3-tk

COPY . .

RUN pip install --upgrade pip && pip3 install -r requirements.txt
RUN pip3 install gunicorn

RUN python3 manage.py migrate
RUN python3 manage.py collectstatic --no-input

CMD [ "/usr/local/bin/gunicorn", "--access-logfile", "-", "--workers", "3", "--log-level", "debug", "--bind", "0.0.0.0:8000", "CA_Python.wsgi:application" ]