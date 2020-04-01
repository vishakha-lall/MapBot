#!/usr/bin/env bash

if [ ! -d MapBot ]; then
    git clone https://github.com/vishakha-lall/MapBot.git -b gssoc-master
fi

export GCLOUD_API_KEY=<YOUR_API_KEY_HERE>

docker-compose -f ./MapBot/docker-compose.yml up -d && docker attach mapbot_bot
