import json
import os
from strategies import BFSDeepCrawlStrategy
from config import CrawlerRunConfig
from crawler import WebCrawler

def save_to_json(data, target_path):
    # Tạo thư mục nếu chưa tồn tại
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    
    with open(target_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"\n--- Đã lưu {len(data)} sản phẩm vào: {target_path} ---")

if __name__ == "__main__":
    entry_url = "https://chiaki.vn/"
    # Lấy thư mục gốc của project (cha của thư mục crawler)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(project_root, "data_pipeline")
    output_file = os.path.join(output_dir, "data_raw.json")

    bfs_strategy = BFSDeepCrawlStrategy()
    
    # Chạy thử với 5 mẫu theo yêu cầu của bạn
    config = CrawlerRunConfig(
        deep_crawl_strategy=bfs_strategy,
        max_depth=5,
        max_pages=1000,
        same_domain_only=True
    )

    crawler = WebCrawler()

    print(f"\n--- ĐANG CRAWL {config.max_pages} SẢN PHẨM ---\n")

    results = crawler.run(entry_url, config)

    if results:
        # Lưu file
        save_to_json(results, output_file)
        
        # Hiển thị đầy đủ thông tin ra terminal
        for i, p in enumerate(results, 1):
            print(f"\n[{i}] ------------------------")
            print(f"Tên        : {p.get('name')}")
            print(f"URL        : {p.get('url')}")
            print(f"Image      : {p.get('image_url')}")
            print(f"Giá        : {p.get('price')}")
            print(f"Rating     : {p.get('rating')}")
            print(f"Đã bán     : {p.get('sold')}")
            print(f"Mô tả      : {p.get('description')[:5000] if p.get('description') else None}...")
            print(f" Bình luận  : {p.get('comments')[:5000] if p.get('comments') else 'Không có bình luận'}...")
    else:
        print("Không tìm thấy sản phẩm nào hoặc có lỗi xảy ra.")
