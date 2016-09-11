#!/usr/bin/env bash

export FLASK_APP=srapp.py
flask initdb
flask run