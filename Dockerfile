FROM python:3.6-slim-stretch

RUN apt-get update && apt-get install -y git wget unzip

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

WORKDIR /usr/var/MapBot
ENTRYPOINT ["/bin/sh","/usr/local/bin/docker-entrypoint.sh"]
