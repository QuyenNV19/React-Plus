import sys
import os
import warnings
import multiprocessing
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np

warnings.filterwarnings("ignore")
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
try:
    import datasets
    datasets.logging.set_verbosity_error()
    datasets.utils.logging.disable_progress_bar()
except ImportError:
    pass

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from dataset import DatasetManager
from preprocessing import TextPreprocessor
from feature_extraction import FeatureExtractor
from models import ModelTrainer
from evaluation import ModelEvaluator


def main():
    print("=" * 70)
    print("                  TEXT CLASSIFICATION PIPELINE")
    print("=" * 70)
    
    # ========== STEP 1: LOAD & FILTER DATASET ==========
    print("[1/5] Loading and filtering dataset (clapAI/MultiLingualSentiment)...", end="", flush=True)
    dataset_manager = DatasetManager()
    ds = dataset_manager.load_dataset()
    ds = dataset_manager.filter_by_language('en')
    train_texts_raw, train_labels, test_texts_raw, test_labels = dataset_manager.get_train_test_data()
    print(f" Done. (Train: {len(train_texts_raw):,} | Test: {len(test_texts_raw):,})")
    
    # ========== STEP 2: TEXT PREPROCESSING ==========
    print("[2/5] Preprocessing text...", end="", flush=True)
    preprocessor = TextPreprocessor(remove_stopwords=True) 
    train_texts = preprocessor.preprocess_batch(train_texts_raw)
    test_texts = preprocessor.preprocess_batch(test_texts_raw)
    print(f" Done. (Cleaned: {len(train_texts):,} train / {len(test_texts):,} test samples)")
    
    # ========== STEP 3: FEATURE EXTRACTION ==========
    print("[3/5] Extracting features (BoW & TF-IDF)...", end="", flush=True)
    extractor = FeatureExtractor(max_features=None, ngram_range=(1, 1))
    X_train_bow, X_test_bow = extractor.fit_transform_bow(train_texts, test_texts)
    X_train_tfidf, X_test_tfidf = extractor.fit_transform_tfidf()
    print(f" Done. (Vocabulary size: {extractor.get_vocabulary_size():,})")
    
    # ========== STEP 4: MODEL TRAINING ==========
    print("[4/5] Training models on TF-IDF features...", end="", flush=True)
    trainer = ModelTrainer()
    lr_model, lr_time = trainer.train_logistic_regression(X_train_tfidf, train_labels, max_iter=100)
    nb_model, nb_time = trainer.train_naive_bayes(X_train_tfidf, train_labels)
    print(f" Done. (Logistic Regression: {lr_time:.2f}s | Naive Bayes: {nb_time:.2f}s)")
    
    # ========== STEP 5: MODEL EVALUATION ==========
    print("[5/5] Evaluating models...", end="", flush=True)
    evaluator = ModelEvaluator()
    evaluator.evaluate('Logistic Regression', lr_model, X_test_tfidf, test_labels, lr_time)
    evaluator.evaluate('Naive Bayes', nb_model, X_test_tfidf, test_labels, nb_time)
    print(" Done.")
    
    # ========== RESULTS COMPARISON ==========
    print("\n" + "=" * 70)
    print("                            EVALUATION SUMMARY")
    print("=" * 70)
    
    results = evaluator.get_results()
    print(f"{'Model Name':<25} | {'Accuracy':<10} | {'F1 (Weighted)':<13} | {'Training Time':<13}")
    print("-" * 70)
    for model_name, res in results.items():
        time_str = f"{res['training_time']:.4f}s" if res['training_time'] is not None else "N/A"
        print(f"{model_name:<25} | {res['accuracy']:<10.4f} | {res['f1_weighted']:<13.4f} | {time_str:<13}")
    print("-" * 70)
    
    best_model_name = evaluator.get_best_model('accuracy')
    best_res = results[best_model_name]
    print(f"🏆 Best Model: {best_model_name} (Accuracy: {best_res['accuracy']:.4f} | F1: {best_res['f1_weighted']:.4f})")
    print("=" * 70 + "\n")


if __name__ == '__main__' and multiprocessing.current_process().name == 'MainProcess':
    main()
