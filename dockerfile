# syntax=docker/dockerfile:1

FROM python:slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN apt-get update && \
    apt-get install -y vim

CMD [ "python3", "app.py"]