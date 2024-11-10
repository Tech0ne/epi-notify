FROM ubuntu:22.04

WORKDIR /app/

RUN apt-get update
RUN apt-get upgrade -y

RUN apt-get install -y python3
RUN apt-get install -y python3-pip

COPY ./hooks/requirements.txt /app/requirements.txt

RUN pip3 install -r /app/requirements.txt

COPY ./shared/db.py /app/db.py
COPY ./shared/models.py /app/models.py

COPY ./hooks/remove_expired_links.py /app/remove_expired_links.py

COPY ./hooks/login.py /app/login.py

COPY ./hooks/main.py /app/main.py

CMD [ "python3", "/app/main.py" ]