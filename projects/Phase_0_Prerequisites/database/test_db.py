import os
import sys

# Đảm bảo project root nằm trong sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from database.connection import get_products_collection

def test_mongodb_data():
    """
    Kiểm tra dữ liệu trong MongoDB.
    """
    try:
        collection = get_products_collection()
        
        total_products = collection.count_documents({})
        print(f"--- KIỂM TRA MONGODB ---")
        print(f"Tổng số sản phẩm hiện có: {total_products}")
        
        if total_products == 0:
            print("Cảnh báo: Không tìm thấy dữ liệu trong collection 'products'.")
            return
        print("\n--- 2 SẢN PHẨM MẪU ---")
        samples = collection.find().limit(2)
        
        for i, p in enumerate(samples, 1):
            print(f"\nSản phẩm #{i}:")
            print(f"Tên        : {p.get('name')}")
            print(f"URL        : {p.get('url')}")
            print(f"Image      : {p.get('image_url')}")
            print(f"Giá        : {p.get('price')}")
            print(f"Rating     : {p.get('rating')}")
            print(f"Đã bán     : {p.get('sold')}")
            print(f"Mô tả      : {p.get('description')[:200] if p.get('description') else None}")

        print("\n--- KIỂM TRA HOÀN TẤT ---")

    except Exception as e:
        print(f"Lỗi khi truy vấn MongoDB: {e}")

if __name__ == "__main__":
    test_mongodb_data()
