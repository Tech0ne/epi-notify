FROM ubuntu:22.04

WORKDIR /app/

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip

RUN pip3 install requests

COPY ./login.py /app/login.py
COPY ./main.py /app/main.py

CMD [ "python3", "/app/main.py" ]