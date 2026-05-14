import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "drug_search"
COLLECTION_NAME = "products"

ES_HOST = os.getenv("ES_HOST", "http://localhost:9200")
ES_INDEX = "products"

MAX_PRODUCTS = 10
CRAWL_DELAY = 1
