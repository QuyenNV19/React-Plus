import json
import os
import sys

# Đảm bảo có thể import các module từ project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from database.repository import insert_product

def load_processed_data_to_mongo(json_file_path):
    """
    Đọc dữ liệu từ file JSON đã xử lý và lưu vào MongoDB.
    """
    if not os.path.exists(json_file_path):
        print(f"Lỗi: Không tìm thấy file tại {json_file_path}")
        return

    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            products = json.load(f)
        
        print(f"Đang bắt đầu lưu {len(products)} sản phẩm vào MongoDB...")
        
        success_count = 0
        for product in products:
            try:
                insert_product(product)
                success_count += 1
                if success_count % 100 == 0:
                    print(f"Tiến độ: {success_count}/{len(products)}...")
            except Exception as e:
                print(f"Lỗi khi lưu sản phẩm {product.get('url')}: {e}")
                
        print(f"Hoàn thành! Đã lưu/cập nhật thành công {success_count} sản phẩm.")
        
    except Exception as e:
        print(f"Lỗi khi xử lý file JSON: {e}")

if __name__ == "__main__":
    # Mặc định tìm file data_processed.json trong thư mục data_pipeline
    default_path = os.path.join(project_root, "data_pipeline", "data_processed.json")
    
    print("--- TRÌNH NẠP DỮ LIỆU MONGODB ---")
    load_processed_data_to_mongo(default_path)
