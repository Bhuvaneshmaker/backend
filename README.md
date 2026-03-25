# Backend Setup

## Install

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements/base.txt
```

## Configure

Copy `.env.example` to `.env` and set MongoDB, Redis, and Firebase values.

## Run

```bash
python manage.py migrate
python manage.py ensure_default_admin
python manage.py runserver 0.0.0.0:8000
python -m workers.udp_ingest.listener
```

## Production Runtime

This project should run as an `ASGI` app in production because it uses Django Channels and WebSockets.

Recommended production server on Linux:

```bash
export DJANGO_SETTINGS_MODULE=config.settings.prod
gunicorn config.asgi:application -c gunicorn.conf.py
```

Windows local production-style testing:

```powershell
$env:DJANGO_SETTINGS_MODULE="config.settings.prod"
python -m uvicorn config.asgi:application --host 0.0.0.0 --port 8000
```

Shortcut scripts:

```powershell
.\scripts\start_asgi.ps1
```

```bash
sh ./scripts/start_asgi.sh
```

Why ASGI instead of WSGI:

- WebSockets from Django Channels need ASGI
- `runserver` is only for development
- `gunicorn + uvicorn worker` is the correct production path for this app

Default demo login:

- username: `admin`
- password: `admin123`

## API Areas

- `/api/auth/`
- `/api/sites/`
- `/api/devices/`
- `/api/telemetry/`
- `/api/alerts/`
- `/api/commissioning/`
