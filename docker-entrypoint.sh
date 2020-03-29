set -ex

git pull

if [ ! -d ./stanford-corenlp-full-2018-10-05 ]; then
    wget http://nlp.stanford.edu/software/stanford-corenlp-full-2018-10-05.zip -nc -c
fi

if [ -f stanford-corenlp-full-2018-10-05.zip ]; then
    unzip -n stanford-corenlp-full-2018-10-05.zip
    rm stanford-corenlp-full-2018-10-05.zip
fi

python init.py
