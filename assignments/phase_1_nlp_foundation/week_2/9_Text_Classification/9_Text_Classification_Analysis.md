# Text Classification Pipeline - Module Structure

Complete NLP pipeline for multilingual sentiment analysis with Bag-of-Words (BoW) and TF-IDF representations.

## Project Structure

```
9_Text Classification/
├── main.py                 # Main entry point - runs complete pipeline
├── requirements.txt        # Python dependencies
├── notebook/
│   └── experiment.ipynb    # Original Jupyter notebook
├── data/                   # Data files
└── src/                    # Python modules (refactored from notebook)
    ├── __init__.py         # Package initialization
    ├── dataset.py          # DatasetManager class
    ├── preprocessing.py    # TextPreprocessor class
    ├── feature_extraction.py # FeatureExtractor class
    ├── models.py           # ModelTrainer class
    └── evaluation.py       # ModelEvaluator class
```

## Modules Overview

### 1. **dataset.py** - `DatasetManager`
Handles loading and filtering multilingual sentiment dataset.

**Key Methods:**
- `load_dataset()` - Load from Hugging Face
- `filter_by_language(language)` - Filter to specific language (e.g., 'en')
- `get_train_test_data()` - Extract texts and labels

### 2. **preprocessing.py** - `TextPreprocessor`
Cleans and normalizes text data.

**Key Methods:**
- `preprocess(text)` - Preprocess single text
- `preprocess_batch(texts)` - Preprocess multiple texts

**Features:**
- Lowercase conversion
- Punctuation removal
- Whitespace normalization
- Optional stopword removal

### 3. **feature_extraction.py** - `FeatureExtractor`
Converts text to BoW and TF-IDF features.

**Key Methods:**
- `fit_transform_bow()` - Generate Bag-of-Words vectors
- `fit_transform_tfidf()` - Generate TF-IDF vectors
- `get_features()` - Retrieve computed features
- `get_vocabulary_size()` - Get vocabulary stats


### 4. **models.py** - `ModelTrainer`
Trains classification models.

**Key Methods:**
- `train_logistic_regression()` - Train LR with timing
- `train_naive_bayes()` - Train NB with timing
- `get_model()` - Retrieve trained model
- `get_all_models()` - Get all trained models

### 5. **evaluation.py** - `ModelEvaluator`
Evaluates and compares model performance.

**Key Methods:**
- `evaluate()` - Evaluate single model
- `compare_models()` - Compare all models side-by-side
- `get_best_model()` - Find best model by metric
- `print_results()` - Display formatted results

**Metrics Tracked:**
- Accuracy
- F1-Score (weighted & macro)
- Precision
- Recall
- Training Time

## Running the Pipeline

### Option 1: Run Complete Pipeline
```bash
python main.py
```

## Requirements

Install dependencies:
```bash
pip install -r requirements.txt
```
