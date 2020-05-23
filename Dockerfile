FROM python:3.6-slim-stretch

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . usr/var/MapBot
RUN chmod +x usr/var/MapBot/docker-entrypoint.sh

WORKDIR /usr/var/MapBot
ENTRYPOINT ["/bin/sh","/usr/var/MapBot/docker-entrypoint.sh"]
