from datetime import datetime



def serialize_mongo_document(document):
    if not document:
        return None

    serialized = {}
    for key, value in document.items():
        if key == "_id":
            serialized["id"] = str(value)
        elif isinstance(value, datetime):
            serialized[key] = value.isoformat()
        else:
            serialized[key] = value
    return serialized
