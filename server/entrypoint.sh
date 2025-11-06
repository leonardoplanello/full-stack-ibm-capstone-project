#!/bin/sh

# Make migrations and migrate the database.
echo "Making migrations and migrating the database. "
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Collect static files (ignore errors for missing directories)
python manage.py collectstatic --noinput --clear || echo "Warning: collectstatic had errors, continuing..."

# Use PORT environment variable if provided, otherwise default to 8000
PORT=${PORT:-8000}
exec gunicorn djangoproj.wsgi --bind 0.0.0.0:$PORT --workers 3

