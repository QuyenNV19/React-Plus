import sys
import os
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from dataset import DatasetManager
from preprocessing import TextPreprocessor
from feature_extraction import FeatureExtractor
from models import ModelTrainer
from evaluation import ModelEvaluator


def main():
    """Main pipeline execution."""
    print("\n" + "=" * 60)
    print("TEXT CLASSIFICATION PIPELINE")
    print("Multilingual Sentiment Analysis with BoW & TF-IDF")
    print("=" * 60)
    
    # ========== STEP 1: LOAD & FILTER DATASET ==========
    print("\n[STEP 1] Loading and filtering dataset...")
    dataset_manager = DatasetManager()
    ds = dataset_manager.load_dataset()
    ds = dataset_manager.filter_by_language('en')
    train_texts_raw, train_labels, test_texts_raw, test_labels = dataset_manager.get_train_test_data()
    
    # ========== STEP 2: TEXT PREPROCESSING ==========
    print("\n[STEP 2] Preprocessing texts...")
    preprocessor = TextPreprocessor(remove_stopwords=False)  # Set to True to remove stopwords
    train_texts = preprocessor.preprocess_batch(train_texts_raw)
    test_texts = preprocessor.preprocess_batch(test_texts_raw)
    print(f"Preprocessed {len(train_texts)} training samples and {len(test_texts)} test samples")
    
    # ========== STEP 3: FEATURE EXTRACTION ==========
    print("\n[STEP 3] Extracting features (BoW & TF-IDF)...")
    extractor = FeatureExtractor(max_features=None, ngram_range=(1, 1))
    X_train_bow, X_test_bow = extractor.fit_transform_bow(train_texts, test_texts)
    X_train_tfidf, X_test_tfidf = extractor.fit_transform_tfidf()
    print(f"Vocabulary size: {extractor.get_vocabulary_size()}")
    
    # ========== STEP 4: MODEL TRAINING ==========
    print("\n[STEP 4] Training models with TF-IDF features...")
    trainer = ModelTrainer()
    lr_model, lr_time = trainer.train_logistic_regression(X_train_tfidf, train_labels, max_iter=100)
    nb_model, nb_time = trainer.train_naive_bayes(X_train_tfidf, train_labels)
    
    # ========== STEP 5: MODEL EVALUATION ==========
    print("\n[STEP 5] Evaluating models...")
    evaluator = ModelEvaluator()
    evaluator.evaluate('Logistic Regression', lr_model, X_test_tfidf, test_labels, lr_time)
    evaluator.evaluate('Naive Bayes', nb_model, X_test_tfidf, test_labels, nb_time)
    
    # ========== RESULTS ==========
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    evaluator.print_all_results()
    evaluator.compare_models()
    
    print("=" * 60)
    best_model_name = evaluator.get_best_model('accuracy')
    best_result = evaluator.get_results()[best_model_name]
    print(f"Best Model (by Accuracy): {best_model_name}")
    print(f"Accuracy: {best_result['accuracy']:.4f}")
    print(f"F1-Score (weighted): {best_result['f1_weighted']:.4f}")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()
