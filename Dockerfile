FROM python:3.6-slim-stretch

RUN apt-get update && apt-get install -y --no-install-recommends \
    wget=1.20 unzip=6.0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . usr/var/MapBot
RUN chmod +x usr/var/MapBot/docker-entrypoint.sh

WORKDIR /usr/var/MapBot
ENTRYPOINT ["/bin/sh","/usr/var/MapBot/docker-entrypoint.sh"]
