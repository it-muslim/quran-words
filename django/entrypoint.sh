#!/bin/sh
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -c '\q'; do
  sleep 2
done

python3 manage.py collectstatic --no-input
python3 manage.py makemigrations
python3 manage.py migrate
exec "$@"
