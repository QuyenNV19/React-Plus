from elasticsearch import Elasticsearch
import sys
import os

# Thêm project root vào path để import settings
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from config import settings
from data_pipeline.embedding_model import get_embedding_model

class SearchEngine:
    def __init__(self):
        self.es = Elasticsearch([settings.ES_HOST])
        self.index = settings.ES_INDEX
        self.model = get_embedding_model()

    def min_max_normalize(self, items):
        if not items:
            return items
        scores = [item["_score"] for item in items]
        min_score = min(scores)
        max_score = max(scores)
        
        if max_score == min_score:
            for item in items:
                item["normalized_score"] = 1.0
            return items
            
        for item in items:
            item["normalized_score"] = (item["_score"] - min_score) / (max_score - min_score)
        return items

    def search_by_name(self, query: str, min_hybrid_score: float = 0.7, max_results: int = 50):
        """
        Tìm kiếm Hybrid sử dụng Min-Max Normalization (0.7 BM25 + 0.3 Semantic)
        """
        if not query:
            return []

        # 1. Tạo vector cho câu truy vấn
        query_vector = self.model.get_embedding(query)
        candidates_size = 50

        # 2a. Query BM25
        bm25_query = {
            "size": candidates_size,
            "query": {
                "match": {
                    "name": query
                }
            }
        }

        # 2b. Query Semantic (KNN)
        knn_query = {
            "size": candidates_size,
            "knn": {
                "field": "content_vector",
                "query_vector": query_vector,
                "k": candidates_size,
                "num_candidates": 100
            }
        }

        try:
            # 3. Lấy kết quả và Chuẩn hóa Min-Max [0, 1]
            bm25_res = self.es.search(index=self.index, body=bm25_query)
            bm25_hits = self.min_max_normalize(bm25_res.get("hits", {}).get("hits", []))

            knn_res = self.es.search(index=self.index, body=knn_query)
            knn_hits = self.min_max_normalize(knn_res.get("hits", {}).get("hits", []))

            # 4. Gộp kết quả và lưu điểm gốc (raw score)
            combined_results = {}
            for hit in bm25_hits:
                doc_id = hit["_id"]
                combined_results[doc_id] = {
                    "_source": hit["_source"],
                    "bm25_score": hit["normalized_score"],
                    "raw_bm25_score": hit["_score"],
                    "knn_score": 0.0,
                    "raw_knn_score": 0.0
                }

            for hit in knn_hits:
                doc_id = hit["_id"]
                if doc_id in combined_results:
                    combined_results[doc_id]["knn_score"] = hit["normalized_score"]
                    combined_results[doc_id]["raw_knn_score"] = hit["_score"]
                else:
                    combined_results[doc_id] = {
                        "_source": hit["_source"],
                        "bm25_score": 0.0,
                        "raw_bm25_score": 0.0,
                        "knn_score": hit["normalized_score"],
                        "raw_knn_score": hit["_score"]
                    }

            # 5. Tính điểm Hybrid và Áp dụng Ngưỡng (Threshold)
            for doc_id, data in combined_results.items():
                if data["raw_bm25_score"] == 0.0 and data["raw_knn_score"] < 0.6:
                    data["hybrid_score"] = -1.0 # Bị loại
                else:
                    data["hybrid_score"] = 0.7 * data["bm25_score"] + 0.3 * data["knn_score"]

            # 6. Sắp xếp và Lọc theo ngưỡng min_hybrid_score thay vì cắt cứng bằng size
            sorted_docs = sorted(combined_results.values(), key=lambda x: x["hybrid_score"], reverse=True)
            
            results = []
            for doc in sorted_docs:
                if doc["hybrid_score"] < min_hybrid_score:
                    continue # Chỉ lấy những sản phẩm đạt trên ngưỡng min_hybrid_score
                
                if len(results) >= max_results:
                    break # Safety net: Không trả về quá max_results
                    
                source = doc["_source"]
                desc = source.get("description")
                summary = source.get("summary")
                desc_text = summary if summary else (desc[:200] + "..." if desc else "")

                results.append({
                    "name": source.get("name"),
                    "price": source.get("price"),
                    "rating": source.get("rating"),
                    "sold": source.get("sold"),
                    "url": source.get("url"),
                    "image_url": source.get("image_url"),
                    "description": desc_text,
                    "comments": source.get("comments"),
                    "hybrid_score": doc["hybrid_score"]
                })
            return results

        except Exception as e:
            print(f"Lỗi khi truy vấn Elasticsearch: {e}")
            return []
