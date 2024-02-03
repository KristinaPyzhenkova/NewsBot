FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    git \
    python3-pip \
    libssl-dev \
    libc++1


RUN pip install git+https://github.com/pylakey/aiotdlib@268dc082cf05461a112536ecc944e95b682f3c50

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y python3 python3-pip netcat

RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir
