from datetime import datetime, timezone

from apps.common.mongo import get_collection, safe_object_id
from apps.common.utils import serialize_mongo_document


devices_collection = get_collection("devices")
slaves_collection = get_collection("slave_boards")
latest_states_collection = get_collection("latest_states")


def list_devices():
    return [serialize_mongo_document(device) for device in devices_collection.find().sort("device_id", 1)]


def create_device(payload: dict):
    now = datetime.now(timezone.utc)
    document = {**payload, "created_at": now, "updated_at": now, "last_seen": None}
    result = devices_collection.insert_one(document)
    return serialize_mongo_document(devices_collection.find_one({"_id": result.inserted_id}))


def get_device(device_pk: str):
    object_id = safe_object_id(device_pk)
    if object_id is None:
        return None
    return serialize_mongo_document(devices_collection.find_one({"_id": object_id}))


def get_device_by_numeric_id(device_id: int):
    return serialize_mongo_document(devices_collection.find_one({"device_id": device_id}))


def create_slave_board(payload: dict):
    now = datetime.now(timezone.utc)
    document = {**payload, "created_at": now, "updated_at": now}
    result = slaves_collection.insert_one(document)
    return serialize_mongo_document(slaves_collection.find_one({"_id": result.inserted_id}))


def list_slave_boards(device_pk: str | None = None):
    query = {"device_id": device_pk} if device_pk else {}
    return [serialize_mongo_document(item) for item in slaves_collection.find(query).sort("slave_id", 1)]


def get_latest_state_for_device(device_pk: str):
    states = latest_states_collection.find({"device_pk": device_pk}).sort("slave_id", 1)
    return [serialize_mongo_document(state) for state in states]


def touch_device_heartbeat(device_id: int, source_ip: str):
    now = datetime.now(timezone.utc)
    devices_collection.update_one(
        {"device_id": device_id},
        {"$set": {"last_seen": now, "status": "online", "source_ip": source_ip, "updated_at": now}},
        upsert=False,
    )
