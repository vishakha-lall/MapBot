FROM python:3.6

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/var/MapBot
WORKDIR /usr/var/MapBot

ENTRYPOINT ["/bin/sh","./docker-entrypoint.sh"]
