import numpy as np

class BagOfWords:
    def __init__(self):
        self.vocab = {}
        self.idx_to_word = {}

    def _preprocess(self, text):
        return text.lower().strip().split()

    def fit(self, documents):
        unique_words = set()
        for doc in documents:
            tokens = self._preprocess(doc)
            unique_words.update(tokens)
        
        sorted_words = sorted(list(unique_words))
        
        for idx, word in enumerate(sorted_words):
            self.vocab[word] = idx
            self.idx_to_word[idx] = word
            
        print(f"Vocabulary: {self.vocab}\n")

    def transform(self, documents, mode="count"):
        matrix = []
        vocab_size = len(self.vocab)
        
        for doc in documents:
            tokens = self._preprocess(doc)
            vector = np.zeros(vocab_size, dtype=int)
            
            for token in tokens:
                if token in self.vocab:
                    idx = self.vocab[token]
                    if mode == "count":
                        vector[idx] += 1
                    elif mode == "binary":
                        vector[idx] = 1
            
            matrix.append(vector)
            
        return np.array(matrix)

if __name__ == "__main__":
    documents = [
        "NLP is fun",
        "I love NLP",
        "NLP NLP NLP"
    ]

    bow = BagOfWords()
    bow.fit(documents)

    print("--- Count BoW Matrix ---")
    count_matrix = bow.transform(documents, mode="count")
    print(count_matrix)
    
    print("\n--- Binary BoW Matrix (Bonus) ---")
    binary_matrix = bow.transform(documents, mode="binary")
    print(binary_matrix)
