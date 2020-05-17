#!/bin/sh

set -ex

if [ ! -d ./stanford-corenlp-full-2018-10-05 ]; then
    wget http://nlp.stanford.edu/software/stanford-corenlp-full-2018-10-05.zip -nc -c
fi

if [ -f stanford-corenlp-full-2018-10-05.zip ]; then
    unzip -n stanford-corenlp-full-2018-10-05.zip
    rm stanford-corenlp-full-2018-10-05.zip
fi

export FLASK_APP=webapp.py
flask run --host=0.0.0.0
