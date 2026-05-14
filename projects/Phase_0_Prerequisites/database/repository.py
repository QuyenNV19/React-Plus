from database.connection import get_products_collection
from datetime import datetime

def insert_product(product_data):
    """
    Inserts or updates a product in the MongoDB collection.
    Uses the product URL as a unique identifier.
    """
    collection = get_products_collection()
    
    if "created_at" not in product_data:
        product_data["created_at"] = datetime.utcnow()
        
    return collection.update_one(
        {"url": product_data["url"]},
        {"$set": product_data},
        upsert=True
    )

def get_all_products():
    """
    Retrieves all product documents from the collection.
    """
    collection = get_products_collection()
    return list(collection.find({}))
