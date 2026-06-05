#!/bin/sh

set -e

python manage.py migrate --noinput

python manage.py createsuperuser --no-input || echo "Superuser already exists. Skipping creation."

python manage.py seed

exec "$@"