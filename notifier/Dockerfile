FROM ubuntu:22.04

WORKDIR /app/

RUN apt-get update
RUN apt-get upgrade -y

RUN apt-get install -y python3
RUN apt-get install -y python3-pip

COPY ./notifier/requirements.txt /app/requirements.txt

RUN pip3 install -r /app/requirements.txt

COPY ./notifier/login.py /app/login.py
COPY ./notifier/main.py /app/main.py

CMD [ "python3", "/app/main.py" ]