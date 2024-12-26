# syntax=docker/dockerfile:1

#FROM python:3.12.4
#FROM nvidia/cuda:12.6.3-cudnn-devel-ubuntu24.04
FROM ubuntu:24.04

WORKDIR /python-docker

COPY . .

RUN apt update && apt install python3 python3-pip -y
#python3 -m venv llama_env && source llama_env/bin/activate

RUN pip3 install -r requirements.txt --break-system-packages

RUN \
  #apt-get update && \
  apt-get install -y vim && \
  #apt-get install -y iputils-ping && \
  #apt-get install -y curl && \
  #apt install build-essential -y && \
  #apt-get install manpages-dev -y && \
  #pip3 install --upgrade pip && \
  #pip3 install llama-cpp-python --break-system-packages && \
  #pip3 install llama-cpp-agent --break-system-packages && \
  #pip3 install huggingface-hub --break-system-packages && \
  #pip3 install torch==2.5.1 torchvision===0.20.1 --break-system-packages && \
  #pip3 install transformers --break-system-packages && \
  #pip3 install openai einops timm accelerate opencv-python --break-system-packages && \
  rm -rf /var/lib/apt/lists/*


CMD [ "python3", "app.py"]
