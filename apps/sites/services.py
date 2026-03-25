from datetime import datetime, timezone

from apps.common.mongo import get_collection, safe_object_id
from apps.common.utils import serialize_mongo_document


sites_collection = get_collection("sites")
blocks_collection = get_collection("blocks")


def list_sites():
    return [serialize_mongo_document(site) for site in sites_collection.find().sort("name", 1)]


def create_site(payload: dict):
    now = datetime.now(timezone.utc)
    document = {**payload, "created_at": now, "updated_at": now}
    result = sites_collection.insert_one(document)
    return serialize_mongo_document(sites_collection.find_one({"_id": result.inserted_id}))


def list_blocks():
    return [serialize_mongo_document(block) for block in blocks_collection.find().sort("name", 1)]


def create_block(payload: dict):
    now = datetime.now(timezone.utc)
    document = {**payload, "created_at": now, "updated_at": now}
    result = blocks_collection.insert_one(document)
    return serialize_mongo_document(blocks_collection.find_one({"_id": result.inserted_id}))


def get_block(block_id: str):
    object_id = safe_object_id(block_id)
    if object_id is None:
        return None
    return serialize_mongo_document(blocks_collection.find_one({"_id": object_id}))


def update_block(block_id: str, payload: dict):
    object_id = safe_object_id(block_id)
    if object_id is None:
        return None

    payload["updated_at"] = datetime.now(timezone.utc)
    blocks_collection.update_one({"_id": object_id}, {"$set": payload})
    return get_block(block_id)
