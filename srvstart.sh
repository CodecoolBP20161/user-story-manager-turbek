#!/usr/bin/env bash

sqlite3 /tmp/flaskr.db < schema.sql
export FLASK_APP=srapp.py
flask initdb
flask run