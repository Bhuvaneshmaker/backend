import json
from functools import lru_cache

from django.conf import settings
import firebase_admin
from firebase_admin import credentials, messaging
import requests


EXPO_PUSH_ENDPOINT = "https://exp.host/--/api/v2/push/send"


@lru_cache(maxsize=1)
def get_firebase_app():
    if firebase_admin._apps:
        return firebase_admin.get_app()

    if settings.FIREBASE_CREDENTIALS_JSON:
        cred = credentials.Certificate(json.loads(settings.FIREBASE_CREDENTIALS_JSON))
        return firebase_admin.initialize_app(
            cred,
            {"projectId": settings.FIREBASE_PROJECT_ID or None},
        )

    if not settings.FIREBASE_CREDENTIALS_PATH:
        return None

    cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
    return firebase_admin.initialize_app(
        cred,
        {"projectId": settings.FIREBASE_PROJECT_ID or None},
    )


def send_fcm_push(
    token: str,
    title: str,
    body: str,
    data: dict | None = None,
) -> str | None:
    app = get_firebase_app()
    if app is None:
        return None

    message = messaging.Message(
        token=token,
        notification=messaging.Notification(title=title, body=body),
        data={str(key): str(value) for key, value in (data or {}).items()},
    )
    return messaging.send(message, app=app)


def send_expo_push(
    token: str,
    title: str,
    body: str,
    data: dict | None = None,
) -> dict | None:
    response = requests.post(
        EXPO_PUSH_ENDPOINT,
        json={
            "to": token,
            "title": title,
            "body": body,
            "data": data or {},
        },
        headers={"Content-Type": "application/json"},
        timeout=15,
    )
    response.raise_for_status()
    return response.json()
