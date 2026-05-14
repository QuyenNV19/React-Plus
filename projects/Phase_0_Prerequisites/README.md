# 🛒 Product Search Engine System

Dự án này là một hệ thống tìm kiếm sản phẩm hoàn chỉnh, từ bước thu thập dữ liệu (Crawling), xử lý làm sạch (Processing) đến cung cấp dịch vụ tìm kiếm qua Elasticsearch. Hệ thống được tối ưu hóa để chạy mượt mà trên Docker với cơ chế tự động nạp dữ liệu và chống trùng lặp.

---

## 🛠 Công nghệ sử dụng

- **Backend**: Python 3.10+, FastAPI, Uvicorn
- **Crawler**: BeautifulSoup4, urllib
- **Database**: MongoDB (Lưu trữ dữ liệu gốc)
- **Search Engine**: Elasticsearch 8.x 
- **DevOps**: Docker, Docker Compose

---

## 📂 Cấu trúc dự án

```text
├── config/              # Cấu hình kết nối (MongoDB, ES, Settings)
├── crawler/             # Module thu thập dữ liệu từ chiaki.vn
├── data_pipeline/       # Xử lý dữ liệu & Đồng bộ Elasticsearch
├── database/            # Quản lý kết nối & nạp dữ liệu vào MongoDB
├── search_service/      # Dịch vụ FastAPI cung cấp API tìm kiếm
├── entrypoint.sh        # Kịch bản tự động hóa khi khởi chạy Docker
├── Dockerfile           # Đóng gói API Service
└── docker-compose.yml   # Quản lý toàn bộ hệ thống (Mongo, ES, API)
```

---

## 🚀 Hướng dẫn khởi chạy nhanh (Quick Start)

Dự án đã có sẵn dữ liệu sạch (`data_processed.json`). Bạn có thể chạy hệ thống chỉ với **1 lệnh duy nhất**:

### 1. Khởi động toàn bộ hệ thống
Mở Terminal tại thư mục gốc dự án và chạy:
```powershell
docker-compose up --build
```

**Hệ thống sẽ tự động thực hiện:**
- Bật MongoDB & Elasticsearch.
- Đợi Elasticsearch sẵn sàng (khoảng 30 giây).
- **Tự động nạp dữ liệu** từ file JSON vào Elasticsearch.
- Khởi động Search API tại cổng `8000`.

### 2. Kiểm tra kết quả
Sau khi log hiện `Application startup complete`, hãy truy cập:
- **Tài liệu API tương tác**: [http://localhost:8000/docs](http://localhost:8000/docs)


### 🔄 Quy trình làm mới dữ liệu (Tùy chọn)
Nếu muốn tự thu thập dữ liệu mới:
1. `python crawler/main.py` -> Thu thập dữ liệu thô.
2. `python data_pipeline/processor.py` -> Làm sạch và chuẩn hóa.
3. `python database/data_loader.py` -> Lưu trữ vào MongoDB.
4. `python data_pipeline/indexer.py` -> Đồng bộ lên Elasticsearch.

---

