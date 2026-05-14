import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from dataset import DatasetManager
from preprocessing import TextPreprocessor
from feature_extraction import FeatureExtractor
from models import ModelTrainer
from evaluation import ModelEvaluator
from config import *


def example_1_basic_pipeline():
    print("\n" + "=" * 60)
    print("EXAMPLE 1: Basic Complete Pipeline")
    print("=" * 60)
    
    dm = DatasetManager()
    dm.load_dataset()
    dm.filter_by_language(LANGUAGE)
    train_texts, train_labels, test_texts, test_labels = dm.get_train_test_data()
    
    preprocessor = TextPreprocessor(remove_stopwords=REMOVE_STOPWORDS)
    train_texts = preprocessor.preprocess_batch(train_texts)
    test_texts = preprocessor.preprocess_batch(test_texts)
    
    extractor = FeatureExtractor(max_features=MAX_FEATURES, ngram_range=NGRAM_RANGE)
    X_train_tfidf, X_test_tfidf = extractor.fit_transform_tfidf()
    
    trainer = ModelTrainer()
    trainer.train_logistic_regression(X_train_tfidf, train_labels)
    trainer.train_naive_bayes(X_train_tfidf, train_labels)
    
    evaluator = ModelEvaluator()
    models = trainer.get_all_models()
    for name, model in models.items():
        time = trainer.get_training_time(name)
        evaluator.evaluate(name, model, X_test_tfidf, test_labels, time)
    
    evaluator.compare_models()


def example_2_with_stopwords():
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Pipeline with Stopword Removal")
    print("=" * 60)
    
    dm = DatasetManager()
    dm.load_dataset()
    dm.filter_by_language(LANGUAGE)
    train_texts, train_labels, test_texts, test_labels = dm.get_train_test_data()
    
    # Preprocess WITH stopword removal
    preprocessor = TextPreprocessor(remove_stopwords=True)
    train_texts = preprocessor.preprocess_batch(train_texts)
    test_texts = preprocessor.preprocess_batch(test_texts)
    
    # Extract features
    extractor = FeatureExtractor(max_features=5000, ngram_range=(1, 1))
    X_train_bow, X_test_bow = extractor.fit_transform_bow(train_texts, test_texts)
    X_train_tfidf, X_test_tfidf = extractor.fit_transform_tfidf()
    
    # Train and evaluate
    trainer = ModelTrainer()
    lr_model, lr_time = trainer.train_logistic_regression(X_train_tfidf, train_labels, max_iter=500)
    
    evaluator = ModelEvaluator()
    evaluator.evaluate('Logistic Regression (with stopwords removed)', 
                      lr_model, X_test_tfidf, test_labels, lr_time)
    evaluator.print_results('Logistic Regression (with stopwords removed)')


def example_3_ngrams():
    """Example 3: Using bigrams for better context."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Pipeline with N-grams (1,2)")
    print("=" * 60)
    
    dm = DatasetManager()
    dm.load_dataset()
    dm.filter_by_language(LANGUAGE)
    train_texts, train_labels, test_texts, test_labels = dm.get_train_test_data()
    
    # Preprocess
    preprocessor = TextPreprocessor(remove_stopwords=False)
    train_texts = preprocessor.preprocess_batch(train_texts)
    test_texts = preprocessor.preprocess_batch(test_texts)
    
    # Extract features with bigrams
    extractor = FeatureExtractor(max_features=5000, ngram_range=(1, 2))
    X_train_tfidf, X_test_tfidf = extractor.fit_transform_tfidf()
    print(f"Vocabulary size with bigrams: {extractor.get_vocabulary_size()}")
    
    # Train models
    trainer = ModelTrainer()
    lr_model, lr_time = trainer.train_logistic_regression(X_train_tfidf, train_labels)
    
    evaluator = ModelEvaluator()
    evaluator.evaluate('LR with Bigrams', lr_model, X_test_tfidf, test_labels, lr_time)
    evaluator.print_results('LR with Bigrams')


def example_4_hyperparameter_tuning():
    """Example 4: Compare different hyperparameter settings."""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Hyperparameter Comparison")
    print("=" * 60)
    
    dm = DatasetManager()
    dm.load_dataset()
    dm.filter_by_language(LANGUAGE)
    train_texts, train_labels, test_texts, test_labels = dm.get_train_test_data()
    
    # Preprocess
    preprocessor = TextPreprocessor(remove_stopwords=False)
    train_texts = preprocessor.preprocess_batch(train_texts)
    test_texts = preprocessor.preprocess_batch(test_texts)
    
    # Extract features
    extractor = FeatureExtractor(max_features=MAX_FEATURES)
    X_train_tfidf, X_test_tfidf = extractor.fit_transform_tfidf()
    
    # Try different C values for Logistic Regression
    C_values = [0.1, 1.0, 10.0]
    evaluator = ModelEvaluator()
    
    for C in C_values:
        trainer = ModelTrainer()
        model, train_time = trainer.train_logistic_regression(
            X_train_tfidf, train_labels, max_iter=1000, C=C
        )
        model_name = f'LR (C={C})'
        evaluator.evaluate(model_name, model, X_test_tfidf, test_labels, train_time)
    
    evaluator.compare_models()
    best = evaluator.get_best_model('accuracy')
    print(f"\nBest configuration: {best}")


def example_5_feature_comparison():
    """Example 5: Compare BoW vs TF-IDF."""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: BoW vs TF-IDF Comparison")
    print("=" * 60)
    
    dm = DatasetManager()
    dm.load_dataset()
    dm.filter_by_language(LANGUAGE)
    train_texts, train_labels, test_texts, test_labels = dm.get_train_test_data()
    
    # Preprocess
    preprocessor = TextPreprocessor(remove_stopwords=False)
    train_texts = preprocessor.preprocess_batch(train_texts)
    test_texts = preprocessor.preprocess_batch(test_texts)
    
    extractor = FeatureExtractor(max_features=MAX_FEATURES)
    X_train_bow, X_test_bow = extractor.fit_transform_bow(train_texts, test_texts)
    X_train_tfidf, X_test_tfidf = extractor.fit_transform_tfidf()
    
    trainer_bow = ModelTrainer()
    model_bow, time_bow = trainer_bow.train_logistic_regression(X_train_bow, train_labels)
    
    trainer_tfidf = ModelTrainer()
    model_tfidf, time_tfidf = trainer_tfidf.train_logistic_regression(X_train_tfidf, train_labels)
    
    evaluator = ModelEvaluator()
    evaluator.evaluate('LR with BoW', model_bow, X_test_bow, test_labels, time_bow)
    evaluator.evaluate('LR with TF-IDF', model_tfidf, X_test_tfidf, test_labels, time_tfidf)
    evaluator.compare_models()


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("TEXT CLASSIFICATION - USAGE EXAMPLES")
    print("=" * 60)
    print("\nRunning multiple examples to demonstrate module usage...")
    print("Note: Examples use real Hugging Face dataset - may take time")
    
    try:
        example_1_basic_pipeline()
        
        print("\n" + "=" * 60)
        print("Examples completed successfully!")
        print("=" * 60)
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()
