#!/bin/sh
set -e

python - <<'PY'
import os
import time

import MySQLdb

host = os.environ.get("MYSQL_HOST", "db")
port = int(os.environ.get("MYSQL_PORT", "3306"))
user = os.environ.get("MYSQL_USER", "flycure")
password = os.environ.get("MYSQL_PASSWORD", "flycure")
name = os.environ.get("MYSQL_DATABASE", "flycure")

last_error = None
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
    except Exception as exc:
        last_error = exc
        print(f"Waiting for MySQL ({attempt + 1}/60): {exc}")
        time.sleep(2)
else:
    raise SystemExit(f"MySQL did not become ready: {last_error}")
PY

python manage.py migrate --noinput
# Safe to re-run: skips hospitals/doctors if the catalog already has rows.
python manage.py seed_marketplace

python - <<'PY'
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@flycure.local")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Created superuser '{username}'.")
else:
    print(f"Superuser '{username}' already exists.")
PY

exec python manage.py runserver 0.0.0.0:8000
