from sentence_transformers import SentenceTransformer
import torch

class EmbeddingModel:
    def __init__(self, model_name='paraphrase-multilingual-MiniLM-L12-v2'):
        """
        Khởi tạo model embedding. 
        Model này hỗ trợ tiếng Việt và có kích thước vector là 384.
        """
        print(f"Đang tải model Embedding: {model_name}...")
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = SentenceTransformer(model_name, device=self.device)
        print(f"Model đã sẵn sàng trên thiết bị: {self.device}")

    def get_embedding(self, text):
        """Chuyển đổi văn bản thành vector."""
        if not text:
            return None
        return self.model.encode(text).tolist()

# Khởi tạo một instance dùng chung để tránh load model nhiều lần
_instance = None

def get_embedding_model():
    global _instance
    if _instance is None:
        _instance = EmbeddingModel()
    return _instance
