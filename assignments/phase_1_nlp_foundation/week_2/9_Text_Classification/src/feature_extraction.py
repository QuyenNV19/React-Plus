
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from typing import List, Tuple
import scipy.sparse as sp


class FeatureExtractor:    
    def __init__(self, max_features: int = None, ngram_range: Tuple[int, int] = (1, 1),
                 min_df: int = 1, max_df: float = 1.0):
        self.max_features = max_features
        self.ngram_range = ngram_range
        self.min_df = min_df
        self.max_df = max_df
        
        self.vectorizer = CountVectorizer(
            max_features=max_features,
            ngram_range=ngram_range,
            min_df=min_df,
            max_df=max_df
        )
        self.tfidf_transformer = TfidfTransformer()
        
        self.X_train_bow = None
        self.X_test_bow = None
        self.X_train_tfidf = None
        self.X_test_tfidf = None
    
    def fit_transform_bow(self, train_texts: List[str], test_texts: List[str]) -> Tuple:
        self.X_train_bow = self.vectorizer.fit_transform(train_texts)
        self.X_test_bow = self.vectorizer.transform(test_texts)
        
        print(f"BoW shape: {self.X_train_bow.shape}")
        return self.X_train_bow, self.X_test_bow
    
    def fit_transform_tfidf(self) -> Tuple:
        if self.X_train_bow is None or self.X_test_bow is None:
            raise ValueError("BoW features not computed. Call fit_transform_bow() first.")
        
        self.X_train_tfidf = self.tfidf_transformer.fit_transform(self.X_train_bow)
        self.X_test_tfidf = self.tfidf_transformer.transform(self.X_test_bow)
        
        print(f"TF-IDF shape: {self.X_train_tfidf.shape}")
        return self.X_train_tfidf, self.X_test_tfidf
    
    def get_features(self, feature_type: str = 'tfidf') -> Tuple:
        if feature_type == 'bow':
            if self.X_train_bow is None:
                raise ValueError("BoW features not computed.")
            return self.X_train_bow, self.X_test_bow
        elif feature_type == 'tfidf':
            if self.X_train_tfidf is None:
                raise ValueError("TF-IDF features not computed.")
            return self.X_train_tfidf, self.X_test_tfidf
        else:
            raise ValueError(f"Unknown feature type: {feature_type}")
    
    def get_vocabulary_size(self) -> int:
        return len(self.vectorizer.vocabulary_)
