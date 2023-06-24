from pymongo import MongoClient, ASCENDING
from .config import settings


client = MongoClient(settings.db_url)
db = client[settings.db_name]


user_collection = db["users"]
user_collection.create_index([('email', ASCENDING)])


organisation_collection = db["organisation"]
organisation_collection.create_index([('name', ASCENDING)])

permissions_collection = db["permissions"]
permissions_collection.create_index([('organisation_id', ASCENDING)])
