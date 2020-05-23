#!/bin/sh

set -ex

export FLASK_APP=webapp.py
flask run --host=0.0.0.0
