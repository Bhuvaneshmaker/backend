#!/usr/bin/env bash
set -o errexit

python manage.py migrate --noinput
python manage.py ensure_default_admin
gunicorn config.asgi:application -c gunicorn.conf.py
