import math

class TFIDF:
    def __init__(self, documents, smooth_idf=True, normalize=True):
        self.documents = documents
        self.smooth_idf = smooth_idf
        self.normalize = normalize
        self.vocab = self._build_vocab()
        self.idf_scores = self._compute_idf()

    def _preprocess(self, text):
        return text.lower().strip().split()

    def _build_vocab(self):
        vocab = set()
        for doc in self.documents:
            vocab.update(self._preprocess(doc))
        return sorted(list(vocab))

    def _compute_idf(self):
        n_docs = len(self.documents)

        df_counts = {}

        for doc in self.documents:
            words_in_doc = set(self._preprocess(doc))
            for word in words_in_doc:
                df_counts[word] = df_counts.get(word, 0) + 1
        
        idf_scores = {}

        for word, df in df_counts.items():
            if self.smooth_idf:
                idf_scores[word] = math.log((1 + n_docs) / (1 + df)) + 1
            else:
                idf_scores[word] = math.log(n_docs / df)
        return idf_scores

    def _compute_tf(self, tokens):
        tf = {}
        for token in tokens:
            tf[token] = tf.get(token, 0) + 1
        
        total_tokens = len(tokens)
        for word in tf:
            if total_tokens > 0:
                tf[word] = tf[word] / total_tokens
            else:
                tf[word] = 0
        return tf

    def get_tfidf_matrix(self):
        matrix = []
        for doc in self.documents:
            tokens = self._preprocess(doc)
            tf = self._compute_tf(tokens)
            
            tfidf_vec = []
            for word in self.vocab:
                score = tf.get(word, 0) * self.idf_scores.get(word, 0)
                tfidf_vec.append(score)
            
            if self.normalize:
                norm = math.sqrt(sum(x**2 for x in tfidf_vec))
                if norm > 0:
                    tfidf_vec = [x / norm for x in tfidf_vec]
            
            matrix.append(tfidf_vec)
        return matrix

if __name__ == "__main__":
    documents = [
        "I love NLP",
        "NLP is fun",
        "I love machine learning"
    ]
    
    tfidf_engine = TFIDF(documents, smooth_idf=True, normalize=True)
    matrix = tfidf_engine.get_tfidf_matrix()
    vocabulary = tfidf_engine.vocab

    print("--- Vocabulary Mapping ---")
    vocab_mapping = {word: i for i, word in enumerate(vocabulary)}
    for word, idx in vocab_mapping.items():
        print(f"'{word}': {idx}")
    
    print("\n--- TF-IDF Matrix ---")
    header = f"{'Doc ID':<8} | " + " | ".join([f"{word:<10}" for word in vocabulary])
    print(header)
    print("-" * len(header))
    
    for i, row in enumerate(matrix):
        row_str = f"Doc {i:<4} | " + " | ".join([f"{val:<10.4f}" for val in row])
        print(row_str)
