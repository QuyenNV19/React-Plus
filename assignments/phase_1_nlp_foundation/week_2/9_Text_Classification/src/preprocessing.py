
import re
import nltk
from nltk.corpus import stopwords
from typing import List
import warnings

warnings.filterwarnings('ignore')


class TextPreprocessor:
    
    def __init__(self, remove_stopwords: bool = True, language: str = 'english'):
        self.remove_stopwords = remove_stopwords
        self.language = language
        self.stop_words = set()
        
        if self.remove_stopwords:
            try:
                nltk.download('stopwords', quiet=True)
                self.stop_words = set(stopwords.words(language))
            except Exception as e:
                print(f"Warning: Could not load stopwords: {e}")
    
    def preprocess(self, text: str) -> str:
        text = text.lower()
        
        text = re.sub(r'[^\w\s]', '', text)
        
        text = re.sub(r'\s+', ' ', text).strip()
        
        if self.remove_stopwords and self.stop_words:
            words = text.split()
            words = [word for word in words if word not in self.stop_words]
            text = " ".join(words)
        
        return text
    
    def preprocess_batch(self, texts: List[str]) -> List[str]:
        return [self.preprocess(text) for text in texts]
