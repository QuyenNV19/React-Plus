from pymongo import MongoClient
from config import settings

def get_db_client():
    """
    Creates and returns a MongoDB client.
    """
    return MongoClient(settings.MONGO_URI)

def get_database():
    """
    Returns the drug_search database instance.
    """
    client = get_db_client()
    return client[settings.DB_NAME]

def get_products_collection():
    """
    Returns the products collection instance.
    """
    db = get_database()
    return db[settings.COLLECTION_NAME]
