import sys
import os

project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

from search_service.search_engine import SearchEngine

def print_results(title, hits, min_score=None):
    print(f"\n{title}")
    print("-" * 80)
    
    valid_hits = []
    for hit in hits:
        score = hit.get('_score', 0)
        if min_score is not None and score < min_score:
            continue
        valid_hits.append(hit)
        
    if not valid_hits:
        print("Không tìm thấy kết quả.")
        return
    
    for i, hit in enumerate(valid_hits):
        score = hit.get('_score', 0)
        source = hit.get('_source', {})
        name = source.get('name', 'N/A')
        # Truncate name for display
        if len(name) > 60:
            name = name[:57] + "..."
        print(f"{i+1}. [Score: {score:.4f}] {name}")

def main():
    engine = SearchEngine()
    
    query = "Thuốc canxi tăng cường chắc khỏe xương" # Thay đổi query ở đây để test
    print("=" * 80)
    print(f"  SO SÁNH KẾT QUẢ TÌM KIẾM: '{query}'")
    print("=" * 80)

    # 1. Tạo vector cho câu truy vấn
    query_vector = engine.model.get_embedding(query)
    
    # Lấy nhiều kết quả thô sau đó cắt bằng ngưỡng (Threshold) thay vì cắt cứng bằng size
    fetch_size = 50 
    
    # Định nghĩa các ngưỡng (Thresholds)
    BM25_THRESHOLD = 5.0      # Điểm BM25 thô thường > 5.0 là có từ khóa khớp tốt
    SEMANTIC_THRESHOLD = 0.7  # Cosine Similarity >= 0.7 là tương đồng ngữ nghĩa tốt

    # ---------------------------------------------------------
    # 1. BM25 Only (Text Search)
    # ---------------------------------------------------------
    bm25_query = {
        "size": fetch_size,
        "query": {
            "match": {
                "name": {
                    "query": query
                }
            }
        }
    }
    
    try:
        bm25_res = engine.es.search(index=engine.index, body=bm25_query)
        print_results(f"1. KẾT QUẢ BM25 (NGƯỠNG: >= {BM25_THRESHOLD})", bm25_res.get("hits", {}).get("hits", []), min_score=BM25_THRESHOLD)
    except Exception as e:
        print(f"Lỗi BM25: {e}")

    # ---------------------------------------------------------
    # 2. Semantic Search Only (KNN Vector)
    # ---------------------------------------------------------
    semantic_query = {
        "size": fetch_size,
        "knn": {
            "field": "content_vector",
            "query_vector": query_vector,
            "k": fetch_size,
            "num_candidates": 100
        }
    }
    
    try:
        semantic_res = engine.es.search(index=engine.index, body=semantic_query)
        print_results(f"2. KẾT QUẢ SEMANTIC (NGƯỠNG: >= {SEMANTIC_THRESHOLD})", semantic_res.get("hits", {}).get("hits", []), min_score=SEMANTIC_THRESHOLD)
    except Exception as e:
        print(f"Lỗi Semantic: {e}")

    # ---------------------------------------------------------
    # 3. Hybrid Search (Min-Max Normalization: 0.7 BM25 + 0.3 Semantic)
    # ---------------------------------------------------------
    try:
        # Gọi engine.search_by_name với ngưỡng Hybrid
        HYBRID_THRESHOLD = 0.7
        hybrid_results = engine.search_by_name(query, min_hybrid_score=HYBRID_THRESHOLD)
        print(f"\n3. KẾT QUẢ HYBRID (NGƯỠNG MIN-MAX HYBRID: >= {HYBRID_THRESHOLD})")
        print("-" * 80)
        if not hybrid_results:
            print("Không tìm thấy kết quả.")
        else:
            for i, res in enumerate(hybrid_results):
                name = res.get('name', 'N/A')
                score = res.get('hybrid_score', 0)
                if len(name) > 60:
                    name = name[:57] + "..."
                print(f"{i+1}. [Score: {score:.4f}] {name}")
    except Exception as e:
        print(f"Lỗi Hybrid: {e}")

    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
