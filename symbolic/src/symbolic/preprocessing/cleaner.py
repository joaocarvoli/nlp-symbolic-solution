from typing import List
import pandas as pd

from preprocessing.stop_words import get_stopwords
from preprocessing.tokenize_text import clean_token, tokenize_text

def preprocess_text(text: str, remove_stopwords: bool = True) -> List[str]:
    """
    Preprocess text: tokenize, clean, lowercase, and optionally remove stopwords.
    
    Args:
        text: Input text
        remove_stopwords: Whether to remove stopwords
        
    Returns:
        List of preprocessed tokens
    """
    tokens = tokenize_text(text)
    
    tokens = [clean_token(token).lower() for token in tokens]
    
    if remove_stopwords:
        stopwords = get_stopwords(include_negations=False)
        tokens = [token for token in tokens if token not in stopwords]
    
    return tokens

def preprocess_dataframe(df: pd.DataFrame, text_column: str, output_column: str) -> pd.DataFrame:
    """
    Apply preprocessing to a dataframe column.
    
    Args:
        df: Input dataframe
        text_column: Column containing text to preprocess
        output_column: Column to store preprocessed tokens
        
    Returns:
        Processed dataframe
    """
    df = df.copy()
    df[output_column] = df[text_column].apply(preprocess_text)
    return df