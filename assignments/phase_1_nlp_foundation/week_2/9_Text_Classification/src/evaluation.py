from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report
import numpy as np
from typing import Dict, List


class ModelEvaluator:
    def __init__(self):
        self.results = {}
    
    def evaluate(self, model_name: str, model, X_test, y_test,
                 training_time: float = None) -> Dict:
        y_pred = model.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        f1_weighted = f1_score(y_test, y_pred, average='weighted')
        f1_macro = f1_score(y_test, y_pred, average='macro')
        precision = precision_score(y_test, y_pred, average='weighted')
        recall = recall_score(y_test, y_pred, average='weighted')
        
        result = {
            'model': model_name,
            'accuracy': accuracy,
            'f1_weighted': f1_weighted,
            'f1_macro': f1_macro,
            'precision': precision,
            'recall': recall,
            'training_time': training_time
        }
        
        self.results[model_name] = result
        return result
    
    # def print_results(self, model_name: str):
    #     """Print evaluation results for a model."""
    #     if model_name not in self.results:
    #         print(f"No results for model '{model_name}'")
    #         return
        
    #     result = self.results[model_name]
    #     print(f"\n{'=' * 50}")
    #     print(f"Model: {model_name.replace('_', ' ').title()}")
    #     print(f"{'=' * 50}")
    #     print(f"  Accuracy:        {result['accuracy']:.4f}")
    #     print(f"  F1-Score (weighted): {result['f1_weighted']:.4f}")
    #     print(f"  F1-Score (macro):    {result['f1_macro']:.4f}")
    #     print(f"  Precision:       {result['precision']:.4f}")
    #     print(f"  Recall:          {result['recall']:.4f}")
    #     if result['training_time'] is not None:
    #         print(f"  Training Time:   {result['training_time']:.4f} seconds")
    #     print()
    
    # def print_all_results(self):
    #     for model_name in self.results:
    #         self.print_results(model_name)
    
    # def compare_models(self) -> Dict:
    #     if not self.results:
    #         print("No models evaluated yet.")
    #         return {}
        
    #     print("\n" + "=" * 80)
    #     print("MODEL COMPARISON")
    #     print("=" * 80)
    #     print(f"{'Model':<25} {'Accuracy':<12} {'F1 (weighted)':<15} {'Training Time':<15}")
    #     print("-" * 80)
        
    #     for model_name, result in self.results.items():
    #         time_str = f"{result['training_time']:.4f}s" if result['training_time'] else "N/A"
    #         print(f"{model_name:<25} {result['accuracy']:<12.4f} {result['f1_weighted']:<15.4f} {time_str:<15}")
        
    #     print("=" * 80 + "\n")
    #     return self.results
    
    def get_best_model(self, metric: str = 'accuracy') -> str:
        if not self.results:
            raise ValueError("No models evaluated yet.")
        
        if metric not in ['accuracy', 'f1_weighted', 'f1_macro', 'precision', 'recall']:
            raise ValueError(f"Unknown metric: {metric}")
        
        best_model = max(self.results.items(), key=lambda x: x[1][metric])
        return best_model[0]
    
    def get_results(self) -> Dict:
        return self.results
