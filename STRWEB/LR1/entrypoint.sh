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
python manage.py collectstatic --noinput

echo "Creating superuser (if not exists)..."
python manage.py bootstrap_superuser || true

if python manage.py shell -c "from apps.catalog.models import Product; raise SystemExit(0 if Product.objects.exists() else 1)"; then
  echo "Seed data already exists; skipping seed."
else
  python manage.py seed_data
fi

echo "Starting Gunicorn..."
exec gunicorn zooshop.wsgi:application \
  --bind 0.0.0.0:${PORT:-8000} \
  --workers 3 \
  --timeout 30