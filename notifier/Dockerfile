FROM ubuntu:22.04

WORKDIR /app/

RUN apt-get update
RUN apt-get upgrade -y

RUN apt-get install -y python3
RUN apt-get install -y python3-pip

COPY ./requirements.txt /app/requirements.txt

RUN pip3 install -r /app/requirements.txt

COPY ./login.py /app/login.py
COPY ./main.py /app/main.py

COPY ./add_user.py /usr/bin/add_user
RUN chmod +x /usr/bin/add_user

CMD [ "python3", "/app/main.py" ]