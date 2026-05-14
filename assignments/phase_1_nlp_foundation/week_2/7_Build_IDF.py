import math

class IDF:
    def __init__(self, documents):
        self.documents = documents
        self.n_docs = len(documents)

    def _preprocess(self, text):
        return set(text.lower().strip().split())

    def compute_df(self):
        df_counts = {}
        for doc in self.documents:
            unique_words = self._preprocess(doc)
            for word in unique_words:
                df_counts[word] = df_counts.get(word, 0) + 1
        return df_counts

    def compute_idf(self):
        df_counts = self.compute_df()
        idf_scores = {}
        
        for word, df in df_counts.items():
            idf_scores[word] = math.log(self.n_docs / df)
            
        return idf_scores

if __name__ == "__main__":
    corpus = [
        "NLP is fun",
        "NLP is powerful",
        "I love learning NLP",
        "Python is great for NLP"
    ]
    
    idf_calculator = IDF(corpus)
    df_counts = idf_calculator.compute_df()
    idf_scores = idf_calculator.compute_idf()
    
    print(f"Total Documents (N): {len(corpus)}\n")
    print(f"{'Word':<10} | {'DF':<5} | {'IDF Score':<10}")
    print("-" * 32)

    for word in sorted(idf_scores.keys()):
        df = df_counts[word]
        score = idf_scores[word]
        print(f"{word:<10} | {df:<5} | {score:.4f}")
