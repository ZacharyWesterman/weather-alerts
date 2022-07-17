#!/usr/bin/env bash

cd "$(dirname "${BASH_SOURCE[0]}")" || exit 1
venv/bin/python main.py
