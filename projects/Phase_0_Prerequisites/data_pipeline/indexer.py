import sys
import os
import json
from elasticsearch import Elasticsearch, helpers

# Thêm project root vào path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from database.connection import get_products_collection
from config import settings
from data_pipeline.embedding_model import get_embedding_model

def create_index_if_not_exists(es):
    """Tạo index với mapping chuẩn cho Hybrid Search nếu chưa tồn tại."""
    if not es.indices.exists(index=settings.ES_INDEX):
        mapping = {
            "mappings": {
                "properties": {
                    "name": {"type": "text", "analyzer": "standard"},
                    "description": {"type": "text"},
                    "summary": {"type": "text"},
                    "url": {"type": "keyword"},
                    "price": {"type": "integer"},
                    "rating": {"type": "float"},
                    "sold": {"type": "integer"},
                    "content_vector": {
                        "type": "dense_vector",
                        "dims": 384,
                        "index": True,
                        "similarity": "cosine"
                    }
                }
            }
        }
        es.indices.create(index=settings.ES_INDEX, body=mapping)
        print(f"Đã tạo index '{settings.ES_INDEX}' với mapping chuẩn.")

def index_data():
    """
    Đọc dữ liệu từ file JSON (ưu tiên) hoặc MongoDB và đẩy vào Elasticsearch.
    Sử dụng URL làm _id để tránh trùng lặp dữ liệu.
    """
    es = Elasticsearch([settings.ES_HOST])
    
    # 1. Khởi tạo Mapping
    create_index_if_not_exists(es)
    
    # 2. Khởi tạo Model Embedding
    model = get_embedding_model()
    
    # 3. Đọc dữ liệu
    json_path = os.path.join(project_root, "data_pipeline", "data_processed.json")
    products = []
    
    if os.path.exists(json_path):
        print(f"Đang đọc dữ liệu từ file: {json_path}")
        with open(json_path, 'r', encoding='utf-8') as f:
            products = json.load(f)
    else:
        print("Không thấy file JSON, đang thử lấy dữ liệu từ MongoDB...")
        collection = get_products_collection()
        products = list(collection.find({}))

    if not products:
        print("Không có dữ liệu để index.")
        return

    print(f"Đang chuẩn bị tạo Vector và index {len(products)} sản phẩm...")
    
    actions = []
    for i, product in enumerate(products):
        doc_id = product.get("url")
        
        # Tạo chuỗi văn bản kết hợp name + summary để lấy ngữ nghĩa sâu
        name = product.get("name", "")
        summary = product.get("summary", "")
        combined_text = f"{name}. {summary}"
        
        # Tạo Vector
        vector = model.get_embedding(combined_text)
        
        source_data = product.copy()
        if "_id" in source_data:
            source_data.pop("_id")
        
        # Lưu vector vào trường content_vector
        source_data["content_vector"] = vector
            
        actions.append({
            "_index": settings.ES_INDEX,
            "_id": doc_id,
            "_source": source_data
        })
        
        if (i + 1) % 50 == 0:
            print(f"Đã xử lý {i + 1}/{len(products)} sản phẩm...")
    
    try:
        success, failed = helpers.bulk(es, actions)
        print(f"Hoàn thành! Thành công: {success}, Thất bại: {failed}")
    except Exception as e:
        print(f"Lỗi khi index dữ liệu vào Elasticsearch: {e}")

if __name__ == "__main__":
    print("--- ELASTICSEARCH HYBRID INDEXER ---")
    index_data()
