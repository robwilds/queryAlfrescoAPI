# syntax=docker/dockerfile:1

FROM python:3.12.4-slim-bullseye

WORKDIR /python-docker

COPY . .
RUN pip3 install -r requirements.txt

RUN apt-get update && \
    apt-get install -y vim && \
    apt-get install -y iputils-ping && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

CMD [ "python3", "app.py"]