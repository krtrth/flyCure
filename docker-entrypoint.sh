#!/bin/sh
set -e

if [ -n "${MYSQL_HOST:-}" ]; then
    python - <<'PY'
import os
import time

import MySQLdb

host = os.environ["MYSQL_HOST"]
port = int(os.environ.get("MYSQL_PORT", "3306"))
user = os.environ.get("MYSQL_USER", "flycure")
password = os.environ.get("MYSQL_PASSWORD", "flycure")
name = os.environ.get("MYSQL_DATABASE", "flycure")

for attempt in range(60):
    try:
        conn = MySQLdb.connect(
            host=host,
            port=port,
            user=user,
            passwd=password,
            db=name,
        )
        conn.close()
        print("MySQL is ready.")
        break
    except MySQLdb.Error:
        if attempt == 59:
            raise SystemExit("MySQL did not become ready after 120 seconds.")
        print(f"Waiting for MySQL ({attempt + 1}/60).")
        time.sleep(2)
PY
elif [ -n "${DATABASE_URL:-}" ]; then
    python - <<'PY'
import os
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from django.db import connections
from django.db.utils import InterfaceError, OperationalError

for attempt in range(60):
    try:
        connections["default"].ensure_connection()
        print("Database is ready.")
        break
    except (InterfaceError, OperationalError):
        if attempt == 59:
            raise SystemExit("Database did not become ready after 120 seconds.")
        print(f"Waiting for database ({attempt + 1}/60).")
        time.sleep(2)
PY
fi

python manage.py migrate --noinput
python manage.py collectstatic --noinput
if [ "$(python -c 'from config.settings import DEBUG; print(DEBUG)')" = "True" ]; then
    # Safe to re-run locally: skips hospitals/doctors if the catalog already has rows.
    python manage.py seed_marketplace
else
    echo "Skipping sample marketplace data because DEBUG is disabled."
fi

if [ -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]; then
    python - <<'PY'
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")
password = os.environ["DJANGO_SUPERUSER_PASSWORD"]

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Created superuser '{username}'.")
else:
    print(f"Superuser '{username}' already exists.")
PY
fi

if [ "$(python -c 'from config.settings import DEBUG; print(DEBUG)')" = "True" ]; then
    exec python manage.py runserver 0.0.0.0:8000
fi

exec gunicorn config.wsgi:application \
    --bind "0.0.0.0:${PORT:-8000}" \
    --workers "${WEB_CONCURRENCY:-1}" \
    --threads "${GUNICORN_THREADS:-2}" \
    --access-logfile - \
    --error-logfile -
