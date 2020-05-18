FROM python:3.6-slim-stretch

RUN apt-get update && apt-get install -y --no-install-recommends \
    wget=1.18-5+deb9u3 \
    unzip=6.0-21+deb9u2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . usr/var/MapBot
RUN chmod +x usr/var/MapBot/docker-entrypoint.sh

WORKDIR /usr/var/MapBot
ENTRYPOINT ["/bin/sh","/usr/var/MapBot/docker-entrypoint.sh"]
