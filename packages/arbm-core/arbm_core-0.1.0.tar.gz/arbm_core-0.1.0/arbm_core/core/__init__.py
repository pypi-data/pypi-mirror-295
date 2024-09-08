from pymongo import MongoClient  # type: ignore

MONGO_ATLAS_URI = "mongodb://atlas-sql-669056bca4d6f730260f6ff5-u4q29.a.query.mongodb.net/sample_mflix?ssl=true&authSource=admin"
MONGO_ATLAS_DB_NAME = "sample_mflix"

__all__ = ["MongoDb"]

_mongodb_client = MongoClient(MONGO_ATLAS_URI, uuidRepresentation="standard")
MongoDb = _mongodb_client[MONGO_ATLAS_DB_NAME]
