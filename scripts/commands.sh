#!/bin/sh

set -e

echo "Waiting for Postgres Database..."

# Espera até que o postgres esteja funcionando
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "Postgres is unavailable - sleeping..."
  sleep 2
done

echo "Postgres is up - continuing..."

echo "Collecting static files..."
poetry run python manage.py collectstatic --noinput

echo "Running migrations..."
poetry run python manage.py makemigrations --noinput
poetry run python manage.py migrate --noinput

echo "Starting Django server..."
poetry run python manage.py runserver 0.0.0.0:8000
