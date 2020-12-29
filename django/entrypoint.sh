#!/bin/sh
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 5
done

python3 manage.py collectstatic --no-input
python3 manage.py makemigrations
python3 manage.py migrate
exec "$@"
