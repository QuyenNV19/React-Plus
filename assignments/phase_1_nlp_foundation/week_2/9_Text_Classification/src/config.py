

# Dataset Configuration
DATASET_NAME = "clapAI/MultiLingualSentiment"
LANGUAGE = 'en' 

# Preprocessing Configuration
REMOVE_STOPWORDS = False  
STOPWORDS_LANGUAGE = 'english'

# Feature Extraction Configuration
MAX_FEATURES = None  
NGRAM_RANGE = (1, 1)  
MIN_DF = 1  
MAX_DF = 1.0  
# Model Training Configuration
LR_MAX_ITER = 1000  
LR_C = 1.0  
LR_SOLVER = 'lbfgs'  

NB_ALPHA = 1.0  

# Evaluation Configuration
EVAL_METRIC = 'accuracy'  

# Output Configuration
SAVE_PLOTS = True
PLOT_DPI = 100
PLOT_DIR = '.'  

RANDOM_SEED = 42
