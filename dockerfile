# syntax=docker/dockerfile:1

FROM python:3.12.4
#FROM nvidia/cuda:12.6.3-cudnn-devel-ubuntu24.04
#FROM ubuntu:24.04
#FROM ubuntu/python:3.12-24.04_stable

WORKDIR /python-docker

#COPY requirements.txt requirements.txt #uncomment if not installing reqs in CMD

#RUN apt update && apt install python3 python3-pip -y

#RUN pip3 install -r requirements.txt --no-cache-dir --break-system-packages #uncomment if not installing reqs in CMD

COPY . .

#RUN rm -rf /var/lib/apt/lists/*


#CMD ["python3", "app.py"]
CMD pip3 install -r requirements.txt --no-cache-dir --break-system-packages; python3 app.py
