from datetime import datetime, timezone

from apps.common.mongo import get_collection
from apps.common.utils import serialize_mongo_document


jobs_collection = get_collection("commissioning_jobs")


def create_job(action: str, target_device: str, payload: dict, requested_by: str):
    now = datetime.now(timezone.utc)
    document = {
        "action": action,
        "target_device": target_device,
        "payload": payload,
        "status": "queued",
        "requested_by": requested_by,
        "created_at": now,
        "completed_at": None,
    }
    result = jobs_collection.insert_one(document)
    return serialize_mongo_document(jobs_collection.find_one({"_id": result.inserted_id}))
