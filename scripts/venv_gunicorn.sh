#!/bin/sh

source /root/FlaskProject/venv/bin/activate
cd /root/FlaskProject
gunicorn -w 5 run:app --daemon
