# Backend Setup

## Install

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements/base.txt
```

## Configure

Copy `.env.example` to `.env` and set MongoDB, Redis, and Firebase values.

For Render, this project expects:

- `MONGODB_URI` from MongoDB Atlas or another hosted MongoDB
- `DJANGO_SETTINGS_MODULE=config.settings.prod`
- `CORS_ALLOWED_ORIGINS=https://mobileems.vercel.app`
- `CSRF_TRUSTED_ORIGINS=https://mobileems.vercel.app`

For a MongoDB-only prototype deployment:

- leave `DATABASE_URL` empty so Django falls back to local SQLite
- leave `REDIS_URL` empty so Channels falls back to in-memory sockets
- keep `MONGODB_URI` pointed at MongoDB Atlas

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

## Render Deployment

This repository includes [render.yaml](/D:/Android/render.yaml) so you can deploy with a Render Blueprint.

Recommended Render setup:

1. Push this repository to GitHub.
2. In Render, create a new Blueprint and select the repository.
3. Let Render create:
   - one web service for Django ASGI
4. In the service environment, fill the required secret values:
   - `MONGODB_URI`
   - `FIREBASE_PROJECT_ID`
   - `FIREBASE_CREDENTIALS_JSON` with the full Firebase service-account JSON for Render
   - `FIREBASE_CREDENTIALS_PATH` only if you are mounting a credentials file yourself
   - leave `DATABASE_URL` empty for the MongoDB-only prototype flow
   - leave `REDIS_URL` empty unless you later add Render Key Value
5. Deploy and verify:
   - `/health/`
   - `/api/health/`

Important:

- This backend should run as `ASGI`, not `WSGI`, because it uses Django Channels and WebSockets.
- Render Web Services are the right place for the HTTP and WebSocket API.
- `REDIS_URL` is only the Redis server connection string for shared websocket/pubsub state. It is optional in this prototype because the backend falls back to Django's in-memory channel layer when `REDIS_URL` is blank.
- `DATABASE_URL` is only for Django's SQL database layer. In this prototype it can stay blank, and the app will use SQLite locally on the Render instance.
- The raw UDP ingest listener should stay outside Render or behind another gateway/service that accepts UDP, then forward parsed data into this backend.

## API Areas

- `/api/auth/`
- `/api/sites/`
- `/api/devices/`
- `/api/telemetry/`
- `/api/alerts/`
- `/api/commissioning/`
