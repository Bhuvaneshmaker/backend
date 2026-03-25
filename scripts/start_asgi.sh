#!/usr/bin/env sh
export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-config.settings.prod}"
exec gunicorn config.asgi:application -c gunicorn.conf.py

