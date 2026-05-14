#!/bin/bash
export PYTHONIOENCODING=utf-8

wait_for_elasticsearch() {
  echo "Đang đợi Elasticsearch tại $ES_HOST sẵn sàng..."
  until curl -s "$ES_HOST" > /dev/null; do
    echo "Elasticsearch chưa sẵn sàng, đang thử lại sau 5 giây..."
    sleep 5
  done
  echo "Elasticsearch đã sẵn sàng!"
}

# 1. Đợi DB sẵn sàng
wait_for_elasticsearch

# 2. Nạp dữ liệu từ JSON vào Database (vì dữ liệu đã có sẵn)
echo "--- BẮT ĐẦU NẠP DỮ LIỆU VÀO DATABASE ---"
python data_pipeline/indexer.py
echo "--- NẠP DỮ LIỆU HOÀN TẤT ---"

# 3. Khởi động Search API
echo "Khởi động Search API..."
uvicorn search_service.main:app --host 0.0.0.0 --port 8000
