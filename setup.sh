#!/usr/bin/env bash

python3 -m venv venv || exit 1
source venv/bin/activate || exit 1
pip install twilio requests pymongo
