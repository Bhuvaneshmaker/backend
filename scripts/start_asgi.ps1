$env:DJANGO_SETTINGS_MODULE = if ($env:DJANGO_SETTINGS_MODULE) { $env:DJANGO_SETTINGS_MODULE } else { "config.settings.prod" }
python -m uvicorn config.asgi:application --host 0.0.0.0 --port 8000 --workers 1

