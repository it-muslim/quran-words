#!/bin/sh
python3 manage.py collectstatic --no-input
python3 manage.py makemigrations
python3 manage.py migrate
gunicorn config.wsgi -b 0.0.0.0:8000 --workers 3 --timeout 600
