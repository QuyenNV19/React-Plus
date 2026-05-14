import json
import os
import re
from transformers import pipeline

print("Đang tải model tóm tắt... Vui lòng đợi.")
try:
    summarizer = pipeline("summarization", model="VietAI/vit5-base-vietnews-summarization")
except Exception as e:
    print(f"Không thể tải model transformers: {e}")
    summarizer = None

def load_data(file_path):
    """Loads raw JSON data from the specified file path."""
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

def summarize_text(text):
    """Tóm tắt văn bản sử dụng Transformers."""
    if not summarizer or not text or len(text) < 100:
        return text[:200] + "..." if text else ""
    
    try:
        input_text = text[:1024]
        summary = summarizer(input_text, max_length=150, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        print(f"Lỗi khi tóm tắt: {e}")
        return text[:200] + "..."

def clean_product(product):
    """Cleans and validates individual product data."""
    def to_int(val, default=0):
        try:
            return int(val) if val is not None else default
        except (ValueError, TypeError):
            return default

    def to_float(val, default=0.0):
        try:
            return float(val) if val is not None else default
        except (ValueError, TypeError):
            return default

    def clean_str(val, default=""):
        return str(val).strip() if val is not None else default

    desc = clean_str(product.get("description"))
    
    cleaned = {
        "name": clean_str(product.get("name")),
        "url": product.get("url"),
        "image_url": product.get("image_url"),
        "price": to_int(product.get("price")),
        "rating": to_float(product.get("rating")),
        "sold": to_int(product.get("sold")),
        "description": desc,
        "comments": clean_str(product.get("comments")),
        "summary": summarize_text(desc) # Thêm phần tóm tắt
    }
    
    return cleaned

def transform_data(raw_data):
    """Transforms a list of raw products into cleaned products."""
    print(f"Bắt đầu xử lý và tóm tắt {len(raw_data)} sản phẩm...")
    processed_data = []
    for i, item in enumerate(raw_data):
        print(f"Processing item {i+1}/{len(raw_data)}...")
        processed_data.append(clean_product(item))
    print("Xử lý hoàn tất.")
    return processed_data

def save_data(data, output_path):
    """Saves the processed data to a JSON file."""
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Successfully saved {len(data)} items to {output_path}")
    except Exception as e:
        print(f"Error saving data: {e}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_dir, "data_raw.json")
    output_file = os.path.join(base_dir, "data_processed.json")
    
    print("--- PIPELINE XỬ LÝ VÀ TÓM TẮT DỮ LIỆU ---")
    
    raw_products = load_data(input_file)
    if raw_products:
        processed_products = transform_data(raw_products)
        save_data(processed_products, output_file)
    else:
        print("Không có dữ liệu để xử lý.")
