# syntax=docker/dockerfile:1

FROM python:latest

WORKDIR /python-docker

COPY . .

RUN pip install -r requirements.txt

RUN apt-get update && \ 
    apt-get install -y vim && \
    #apt-get install -y iputils-ping && \
    apt-get install -y curl && \
    apt install build-essential -y && \
    apt-get install manpages-dev -y && \
    pip install --upgrade pip && \
    pip install llama-cpp-python && \
    pip install llama-cpp-agent && \
    pip install huggingface-hub && \
    pip install torch && \
    pip install transformers && \
    rm -rf /var/lib/apt/lists/*


CMD [ "python3", "app.py"]