#!/bin/bash
set -e

cd /app

# Ожидаем БД
echo "Waiting for PostgreSQL..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 1
done
echo "PostgreSQL is ready!"

# Запускаем миграции
echo "Running migrations..."
python manage.py migrate --noinput

echo "Creating superuser (if not exists)..."
python manage.py bootstrap_superuser || true

python manage.py clear_db
python manage.py seed_data

echo "Starting Gunicorn..."
exec gunicorn zooshop.wsgi:application \
  --bind 0.0.0.0:${PORT:-8000} \
  --workers 3 \
  --timeout 30