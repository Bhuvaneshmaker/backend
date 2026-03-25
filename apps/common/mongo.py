from functools import lru_cache

from bson import ObjectId
from bson.errors import InvalidId
from django.conf import settings
from pymongo import MongoClient


@lru_cache(maxsize=1)
def get_mongo_client() -> MongoClient:
    return MongoClient(settings.MONGODB_URI)


def get_database():
    return get_mongo_client()[settings.MONGODB_NAME]


def get_collection(name: str):
    return get_database()[name]


def safe_object_id(value: str):
    try:
        return ObjectId(value)
    except (InvalidId, TypeError):
        return None
