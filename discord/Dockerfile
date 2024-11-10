FROM ubuntu:22.04

WORKDIR /app/

RUN apt-get update
RUN apt-get upgrade -y

RUN apt-get install -y python3
RUN apt-get install -y python3-pip

COPY ./discord/requirements.txt /app/requirements.txt

RUN pip3 install -r /app/requirements.txt

COPY ./shared/db.py /app/db.py
COPY ./shared/models.py /app/models.py

COPY ./discord/bot.py /app/bot.py
COPY ./discord/server.py /app/server.py

COPY ./discord/status.py /app/status.py

COPY ./discord/main.py /app/main.py

CMD [ "python3", "/app/main.py" ]