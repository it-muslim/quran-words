#!/bin/sh
python3 manage.py collectstatic --no-input
python3 manage.py makemigrations
python3 manage.py migrate
exec "$@"
