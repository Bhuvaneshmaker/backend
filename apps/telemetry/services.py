from datetime import datetime, timezone

from apps.common.mongo import get_collection, safe_object_id
from apps.common.utils import serialize_mongo_document
from apps.devices.services import get_device_by_numeric_id, touch_device_heartbeat
from workers.udp_ingest.publisher import publish_telemetry_update


packets_collection = get_collection("telemetry_packets")
latest_states_collection = get_collection("latest_states")
history_collection = get_collection("elevator_state_history")
slaves_collection = get_collection("slave_boards")


def save_packet(parsed_frame: dict, source_ip: str):
    now = datetime.now(timezone.utc)
    document = {**parsed_frame, "source_ip": source_ip, "received_at": now}
    result = packets_collection.insert_one(document)
    return serialize_mongo_document(packets_collection.find_one({"_id": result.inserted_id}))


def save_elevator_states(parsed_frame: dict, source_ip: str):
    device = get_device_by_numeric_id(parsed_frame["device_id"])
    device_pk = device["id"] if device else None
    block_id = device.get("block_id") if device else None
    touch_device_heartbeat(parsed_frame["device_id"], source_ip)

    saved_states = []
    now = datetime.now(timezone.utc)
    for elevator in parsed_frame["elevators"]:
        slave_board = slaves_collection.find_one({"device_id": device_pk, "slave_id": elevator["slave_id"]}) if device_pk else None
        elevator_id = str(slave_board["_id"]) if slave_board else None
        state = {
            "device_id": parsed_frame["device_id"],
            "device_pk": device_pk,
            "block_id": block_id,
            "elevator_id": elevator_id,
            "slave_id": elevator["slave_id"],
            "source_ip": source_ip,
            **elevator,
            "updated_at": now,
        }
        latest_states_collection.update_one(
            {"device_id": state["device_id"], "slave_id": state["slave_id"]},
            {"$set": state},
            upsert=True,
        )
        history_collection.insert_one(state)
        serializable = serialize_mongo_document(
            latest_states_collection.find_one({"device_id": state["device_id"], "slave_id": state["slave_id"]})
        )
        publish_telemetry_update(serializable)
        from apps.alerts.services import evaluate_state_alerts

        evaluate_state_alerts(serializable)
        saved_states.append(serializable)
    return saved_states


def get_latest_states():
    return [serialize_mongo_document(item) for item in latest_states_collection.find().sort([("device_id", 1), ("slave_id", 1)])]


def list_packets(limit: int = 50):
    return [serialize_mongo_document(item) for item in packets_collection.find().sort("received_at", -1).limit(limit)]


def get_packet(packet_id: str):
    object_id = safe_object_id(packet_id)
    if object_id is None:
        return None
    return serialize_mongo_document(packets_collection.find_one({"_id": object_id}))


def get_elevator_history(elevator_id: str, limit: int = 100):
    return [
        serialize_mongo_document(item)
        for item in history_collection.find({"elevator_id": elevator_id}).sort("updated_at", -1).limit(limit)
    ]
