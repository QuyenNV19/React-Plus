import numpy as np

class SentenceOneHotEncoder:
    def __init__(self, sentences):
        self.vocab = {"<PAD>": 0, "<UNK>": 1}
        self.idx_to_word = {0: "<PAD>", 1: "<UNK>"}
        self._build_vocab(sentences)

    def _preprocess(self, text):
        return text.lower().strip().split()

    def _build_vocab(self, sentences):
        idx = len(self.vocab)
        for sentence in sentences:
            tokens = self._preprocess(sentence)
            for token in tokens:
                if token not in self.vocab:
                    self.vocab[token] = idx
                    self.idx_to_word[idx] = token
                    idx += 1
        print(f"Vocabulary Size: {len(self.vocab)}")
        print(f"Vocabulary: {self.vocab}\n")

    def encode_word(self, word):
        vector = np.zeros(len(self.vocab), dtype=int)
        index = self.vocab.get(word.lower(), self.vocab["<UNK>"])
        vector[index] = 1
        return vector

    def encode_sentence(self, sentence, max_len=None):
        tokens = self._preprocess(sentence)

        if max_len is not None:
            tokens = tokens[:max_len]
        
        if max_len is not None:
            while len(tokens) < max_len:
                tokens.append("<PAD>")

        sequence_vectors = [self.encode_word(token) for token in tokens]
        
        return np.array(sequence_vectors)


if __name__ == "__main__":
    corpus = [
        "I love NLP",
        "NLP is fun"
    ]
    
    encoder = SentenceOneHotEncoder(corpus)
    
    input_text = "I love NLP"
    encoded_seq = encoder.encode_sentence(input_text)
    
    print(f"Input: '{input_text}'")
    print("Output (Sequence of One-Hot Vectors):")
    print(encoded_seq.tolist())
    print("-" * 30)

    test_sentence = "I love learning NLP" 
    max_seq_len = 5
    
    encoded_padded = encoder.encode_sentence(test_sentence, max_len=max_seq_len)
    
    print(f"Input: '{test_sentence}'")
    print(f"Parameters: max_len={max_seq_len}")
    print(f"Output Matrix Shape: {encoded_padded.shape}")
    print("Encoded Sequence (with <UNK> and <PAD>):")
    for i, vec in enumerate(encoded_padded):
        word = test_sentence.split()[i] if i < len(test_sentence.split()) else "<PAD>"
        print(f"  Word index {i} ({word}): {vec.tolist()}")
