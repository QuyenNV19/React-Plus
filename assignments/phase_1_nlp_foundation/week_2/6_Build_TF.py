class TF:
    def __init__(self,sentences):
        self.sentences = sentences

    def _preprocess(self,text):
        return text.lower().strip().split()

    def compute_tf(self):
        tokens = self._preprocess(self.sentences)
        total_words = len(tokens)

        word_counts = {}
        
        for token in tokens:
            word_counts[token] = word_counts.get(token, 0) + 1
        
        tf_scores = {}
        for word, count in word_counts.items():
            tf_scores[word] = count / total_words
        return word_counts,tf_scores

if __name__ == "__main__":
    input_text = "NLP NLP is fun"
    tf = TF(input_text)
    raw_counts, normalized_tf = tf.compute_tf()
    
    print(f"Input Sentence: '{input_text}'")
    print(f"Total Terms: {sum(raw_counts.values())}\n")
    
    print(f"{'Word':<10} | {'Raw Count':<10} | {'Normalized TF':<15}")
    print("-" * 40)
    
    for word in raw_counts:
        count = raw_counts[word]
        tf = normalized_tf[word]
        print(f"{word:<10} | {count:<10} | {tf:<15.2f}")

    print("\nExpected Dictionary Format:")
    print(normalized_tf)

    

    