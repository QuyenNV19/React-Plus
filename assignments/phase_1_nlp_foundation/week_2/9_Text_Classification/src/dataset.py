from datasets import load_dataset, DatasetDict
from typing import Dict, List, Tuple


class DatasetManager: 
    def __init__(self, dataset_name: str = "clapAI/MultiLingualSentiment"):
        self.dataset_name = dataset_name
        self.ds = None
        
    def load_dataset(self) -> DatasetDict:
        self.ds = load_dataset(self.dataset_name)
        return self.ds
    
    def filter_by_language(self, language: str = 'en') -> DatasetDict:
        if self.ds is None:
            raise ValueError("Dataset not loaded. Call load_dataset() first.")
        
        def filter_func(x):
            lang_field = x.get('language') or x.get('lang')
            return lang_field == language
        
        ds_train_filtered = self.ds['train'].filter(filter_func)
        ds_test_filtered = self.ds['test'].filter(filter_func)
        
        self.ds = DatasetDict({
            'train': ds_train_filtered,
            'test': ds_test_filtered
        })
        return self.ds
    
    def get_train_test_data(self) -> Tuple[List[str], List[int], List[str], List[int]]:
        if self.ds is None:
            raise ValueError("Dataset not loaded or filtered. Call load_dataset() first.")
        
        train_texts = [item['text'] for item in self.ds['train']]
        train_labels = [item['label'] for item in self.ds['train']]
        test_texts = [item['text'] for item in self.ds['test']]
        test_labels = [item['label'] for item in self.ds['test']]
        
        return train_texts, train_labels, test_texts, test_labels
    
    def get_dataset(self) -> DatasetDict:
        return self.ds
