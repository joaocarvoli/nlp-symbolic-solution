from enum import Enum
 
class WordStrategy(Enum):
    EXACT = 'exact'
    STEM = 'stem'
     
# This will be populated at runtime to avoid circular imports
WORD_STRATEGY = {}
 
def register_word_sentiment_functions(exact_func, stem_func):
    """Register the word sentiment functions to avoid circular imports"""
    global WORD_STRATEGY
    WORD_STRATEGY[WordStrategy.EXACT] = exact_func
    WORD_STRATEGY[WordStrategy.STEM] = stem_func