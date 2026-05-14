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

**Example:**
```python
from src.dataset import DatasetManager

dm = DatasetManager()
ds = dm.load_dataset()
ds = dm.filter_by_language('en')
train_texts, train_labels, test_texts, test_labels = dm.get_train_test_data()
```

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

**Example:**
```python
from src.preprocessing import TextPreprocessor

preprocessor = TextPreprocessor(remove_stopwords=True)
clean_texts = preprocessor.preprocess_batch(raw_texts)
```

### 3. **feature_extraction.py** - `FeatureExtractor`
Converts text to BoW and TF-IDF features.

**Key Methods:**
- `fit_transform_bow()` - Generate Bag-of-Words vectors
- `fit_transform_tfidf()` - Generate TF-IDF vectors
- `get_features()` - Retrieve computed features
- `get_vocabulary_size()` - Get vocabulary stats

**Example:**
```python
from src.feature_extraction import FeatureExtractor

extractor = FeatureExtractor(max_features=None, ngram_range=(1,1))
X_train_bow, X_test_bow = extractor.fit_transform_bow(train_texts, test_texts)
X_train_tfidf, X_test_tfidf = extractor.fit_transform_tfidf()
```

### 4. **models.py** - `ModelTrainer`
Trains classification models.

**Key Methods:**
- `train_logistic_regression()` - Train LR with timing
- `train_naive_bayes()` - Train NB with timing
- `get_model()` - Retrieve trained model
- `get_all_models()` - Get all trained models

**Example:**
```python
from src.models import ModelTrainer

trainer = ModelTrainer()
lr_model, lr_time = trainer.train_logistic_regression(X_train_tfidf, train_labels)
nb_model, nb_time = trainer.train_naive_bayes(X_train_tfidf, train_labels)
```

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

**Example:**
```python
from src.evaluation import ModelEvaluator

evaluator = ModelEvaluator()
evaluator.evaluate('Logistic Regression', lr_model, X_test_tfidf, test_labels, lr_time)
evaluator.compare_models()
best_model = evaluator.get_best_model('accuracy')
```

## Running the Pipeline

### Option 1: Run Complete Pipeline
```bash
python main.py
```

This will execute the entire pipeline:
1. Load multilingual dataset
2. Filter to English texts
3. Perform EDA (generates visualization plots)
4. Preprocess texts
5. Extract BoW and TF-IDF features
6. Train Logistic Regression & Naive Bayes
7. Evaluate and compare models

**Output:**
- Console: Detailed results and comparisons
- Files: 
  - `class_distribution.png` - Class distribution visualization
  - `text_length_distribution.png` - Text length statistics

### Option 2: Use Modules Programmatically
```python
import sys
sys.path.insert(0, 'src')

from dataset import DatasetManager
from preprocessing import TextPreprocessor
from feature_extraction import FeatureExtractor
from models import ModelTrainer
from evaluation import ModelEvaluator

# Your custom pipeline here
```

## Requirements

Install dependencies:
```bash
pip install -r requirements.txt
```

**Core dependencies:**
- datasets - Hugging Face datasets
- scikit-learn - ML models and metrics
- nltk - NLP utilities
- numpy - Numerical operations
- matplotlib - Visualization

## Model Performance

The pipeline trains and compares:

1. **Logistic Regression**
   - Fast training
   - Good for linear separability
   - Configurable regularization (C parameter)

2. **Naive Bayes**
   - Very fast training
   - Probabilistic approach
   - Works well with sparse text features

## Customization

### Adjust Preprocessing
```python
preprocessor = TextPreprocessor(remove_stopwords=True, language='english')
```

### Adjust Feature Extraction
```python
extractor = FeatureExtractor(
    max_features=5000,
    ngram_range=(1, 2),  # Include bigrams
    min_df=2,
    max_df=0.95
)
```

### Adjust Model Hyperparameters
```python
trainer.train_logistic_regression(X_train_tfidf, train_labels, 
                                 max_iter=500, C=10, solver='liblinear')
trainer.train_naive_bayes(X_train_tfidf, train_labels, alpha=0.5)
```

## Notes

- Dataset is filtered to **English only** by default
- Original dataset: ~3.7M samples across 17 languages
- English subset: ~1.5M samples
- Features are in sparse matrix format (memory efficient)
- Training time varies based on dataset size and machine specs
