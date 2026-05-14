import re
import string
from underthesea import sent_tokenize, word_tokenize

class VietnameseTextProcessor:
    def __init__(self, stopwords_path=None):
        self.stopwords = set()
        if stopwords_path:
            self.load_stopwords(stopwords_path)

    def load_stopwords(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.stopwords = set([line.strip().lower() for line in f if line.strip()])
        except Exception as e:
            print(f"Error loading stopwords: {e}")

    def sentence_tokenize(self, text):
        return sent_tokenize(text)

    def word_tokenize(self, text):
        return word_tokenize(text)

    def remove_urls(self, text):
        return re.sub(r'https?://\S+|www\.\S+', '', text)

    def remove_html(self, text):
         return re.sub(r'<.*?>', '', text)

    def remove_emojis(self, text):
        return re.sub(r'[^\x00-\x7F\u00A0-\u024F\u1E00-\u1EFF\s]', '', text)

    def remove_punctuation(self, text):
        return text.translate(str.maketrans('', '', string.punctuation))

    def normalize_whitespace(self, text):
        return re.sub(r'\s+', ' ', text).strip()

    def remove_stopwords(self, tokens):
        return [t for t in tokens if t.lower() not in self.stopwords]

    def preprocess(self, text):
        
        text = self.remove_html(text)
        text = self.remove_urls(text)
        text = self.remove_emojis(text)
        text = text.lower()
        text = self.remove_punctuation(text)
        text = self.normalize_whitespace(text)
        tokens = self.word_tokenize(text)
        tokens = self.remove_stopwords(tokens)
        
        return tokens

if __name__ == "__main__":
    processor = VietnameseTextProcessor(stopwords_path="stopwords.txt")

    input_text = """<p>Hello!!!</p>
I am learning NLP 😄
Visit https://abc.com now!!!"""

    print("--- Input ---")
    print(input_text)

    sentences = processor.sentence_tokenize(input_text)
    print("\n--- Sentences ---")
    print(sentences)

    tokens = processor.preprocess(input_text)
    print("\n--- Tokens ---")
    print(tokens)

    final_text = " ".join(tokens)
    print("\n--- Final Processed Text ---")
    print(final_text)