from datetime import datetime, timezone

from apps.common.firebase import send_expo_push, send_fcm_push
from apps.common.mongo import get_collection, safe_object_id
from apps.common.utils import serialize_mongo_document
from workers.udp_ingest.publisher import publish_alert_event


alerts_collection = get_collection("alerts")
push_tokens_collection = get_collection("push_tokens")


def list_alerts():
    return [serialize_mongo_document(alert) for alert in alerts_collection.find().sort("created_at", -1)]


def create_alert(payload: dict):
    existing = alerts_collection.find_one(
        {
            "device_id": payload["device_id"],
            "slave_id": payload.get("slave_id"),
            "code": payload["code"],
            "resolved_at": None,
        }
    )
    if existing:
        return serialize_mongo_document(existing)

    now = datetime.now(timezone.utc)
    document = {**payload, "acknowledged": False, "created_at": now, "resolved_at": None}
    result = alerts_collection.insert_one(document)
    alert = serialize_mongo_document(alerts_collection.find_one({"_id": result.inserted_id}))
    publish_alert_event(alert)
    notify_alert(alert)
    return alert


def acknowledge_alert(alert_id: str, username: str):
    object_id = safe_object_id(alert_id)
    if object_id is None:
        return None

    now = datetime.now(timezone.utc)
    alerts_collection.update_one(
        {"_id": object_id},
        {"$set": {"acknowledged": True, "acknowledged_by": username, "resolved_at": now}},
    )
    return serialize_mongo_document(alerts_collection.find_one({"_id": object_id}))


def notify_alert(alert: dict):
    tokens = push_tokens_collection.find({})
    for item in tokens:
        token = item.get("token")
        provider = item.get("provider", "fcm")
        if not token:
            continue

        try:
            if provider == "expo":
                send_expo_push(token, alert["title"], alert["message"], {"alert_id": alert["id"]})
            else:
                send_fcm_push(token, alert["title"], alert["message"], {"alert_id": alert["id"]})
        except Exception:
            continue


def evaluate_state_alerts(state: dict):
    if state.get("connection_status") == "Disconnected":
        create_alert(
            {
                "device_id": state["device_id"],
                "slave_id": state["slave_id"],
                "severity": "high",
                "code": "LIFT_DISCONNECTED",
                "title": "Lift disconnected",
                "message": f"Lift {state['slave_id']} on device {state['device_id']} is disconnected.",
            }
        )
    elif state.get("malfunction"):
        create_alert(
            {
                "device_id": state["device_id"],
                "slave_id": state["slave_id"],
                "severity": "critical",
                "code": "LIFT_MALFUNCTION",
                "title": "Lift malfunction",
                "message": f"Lift {state['slave_id']} on device {state['device_id']} reported a malfunction.",
            }
        )
