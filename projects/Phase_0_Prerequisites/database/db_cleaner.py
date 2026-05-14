import sys
import os
from pymongo import MongoClient
from elasticsearch import Elasticsearch

# Thêm thư mục gốc vào path để import settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import settings

def clean_mongodb():
    print("--- DỌN DẸP MONGODB ---")
    try:
        client = MongoClient(settings.MONGO_URI)
        db = client[settings.DB_NAME]
        collection = db[settings.COLLECTION_NAME]
        
        count = collection.count_documents({})
        if count > 0:
            result = collection.delete_many({})
            print(f"Thành công: Đã xóa {result.deleted_count} sản phẩm khỏi MongoDB.")
        else:
            print("MongoDB đã sạch, không có dữ liệu để xóa.")
        client.close()
    except Exception as e:
        print(f"Lỗi khi dọn dẹp MongoDB: {e}")

def clean_elasticsearch():
    print("\n--- DỌN DẸP ELASTICSEARCH ---")
    try:
        es = Elasticsearch(settings.ES_HOST)
        if es.indices.exists(index=settings.ES_INDEX):
            es.indices.delete(index=settings.ES_INDEX)
            print(f"Thành công: Đã xóa Index '{settings.ES_INDEX}' khỏi Elasticsearch.")
        else:
            print(f"Index '{settings.ES_INDEX}' không tồn tại trong Elasticsearch.")
    except Exception as e:
        print(f"Lỗi khi dọn dẹp Elasticsearch: {e}")

if __name__ == "__main__":
    print("\n==========================================")
    print("       DATABASE CLEANER TOOL")
    print("==========================================\n")
    
    confirm = input("CẢNH BÁO: Hành động này sẽ xóa TOÀN BỘ dữ liệu trong MongoDB và Elasticsearch.\nBạn có chắc chắn muốn thực hiện không? (y/n): ")
    
    if confirm.lower() == 'y':
        clean_mongodb()
        clean_elasticsearch()
        print("\nHoàn tất! Database hiện đã trống hoàn toàn.")
    else:
        print("\nĐã hủy thao tác. Không có dữ liệu nào bị xóa.")
