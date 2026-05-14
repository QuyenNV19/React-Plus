"""
Text Classification Package
Multilingual sentiment analysis with BoW and TF-IDF representations.
"""

from .dataset import DatasetManager
from .preprocessing import TextPreprocessor
from .feature_extraction import FeatureExtractor
from .models import ModelTrainer
from .evaluation import ModelEvaluator

__all__ = [
    'DatasetManager',
    'TextPreprocessor',
    'FeatureExtractor',
    'ModelTrainer',
    'ModelEvaluator'
]

assignments\phase_1_nlp_foundation\week_2\9_Text Classification