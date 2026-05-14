import sys
import os

# Thêm project root vào path để có thể import các module khác
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from fastapi import FastAPI, Query, HTTPException
from search_service.search_engine import SearchEngine
import uvicorn

app = FastAPI(
    title="Product Search API",
    description="API tìm kiếm sản phẩm sử dụng FastAPI và Elasticsearch",
    version="1.0.0"
)

# Khởi tạo search engine
try:
    search_engine = SearchEngine()
except Exception as e:
    print(f"Không thể kết nối tới Elasticsearch: {e}")
    search_engine = None

@app.get("/search")
async def search(q: str = Query(None, description="Từ khóa tìm kiếm sản phẩm")):
    """
    Endpoint tìm kiếm sản phẩm theo tên.
    """
    if not q or q.strip() == "":
        return {"results": [], "message": "Vui lòng nhập từ khóa tìm kiếm."}
    
    if not search_engine:
        raise HTTPException(status_code=503, detail="Dịch vụ tìm kiếm hiện không khả dụng.")
    
    try:
        results = search_engine.search_by_name(q.strip())
        return {
            "query": q,
            "total_results": len(results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Chào mừng bạn đến với Product Search API. Truy cập /docs để xem tài liệu."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

