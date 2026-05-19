import time
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
import scipy.sparse as sp
from typing import Dict, Tuple


class ModelTrainer:
    def __init__(self):
        self.models = {}
        self.training_times = {}
    
    def train_logistic_regression(self, X_train: sp.csr_matrix, y_train, 
                                  max_iter: int = 100, C: float = 1.0,
                                  solver: str = 'lbfgs') -> Tuple:
        start_time = time.time()
        
        lr_model = LogisticRegression(
            max_iter=max_iter,
            C=C,
            solver=solver,
            random_state=42
        )
        lr_model.fit(X_train, y_train)
        
        training_time = time.time() - start_time
        self.models['logistic_regression'] = lr_model
        self.training_times['logistic_regression'] = training_time
        
        return lr_model, training_time
    
    def train_naive_bayes(self, X_train: sp.csr_matrix, y_train,
                          alpha: float = 1.0) -> Tuple:
        start_time = time.time()
        
        nb_model = MultinomialNB(alpha=alpha)
        nb_model.fit(X_train, y_train)
        
        training_time = time.time() - start_time
        self.models['naive_bayes'] = nb_model
        self.training_times['naive_bayes'] = training_time
        
        return nb_model, training_time
    
    def get_model(self, model_name: str):
        if model_name not in self.models:
            raise ValueError(f"Model '{model_name}' not found. Available: {list(self.models.keys())}")
        return self.models[model_name]
    
    def get_training_time(self, model_name: str) -> float:
        """Get training time for a model."""
        if model_name not in self.training_times:
            raise ValueError(f"No training time for model '{model_name}'")
        return self.training_times[model_name]
    
    def get_all_models(self) -> Dict:
        return self.models
    
    def get_all_training_times(self) -> Dict:
        return self.training_times
