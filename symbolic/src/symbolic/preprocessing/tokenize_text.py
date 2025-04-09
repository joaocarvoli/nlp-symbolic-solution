from typing import List
from nltk import word_tokenize

def tokenize_text(text: str) -> List[str]:
    """
    Tokenizes the input text into words.
    
    Args:
        text (str): The input text to tokenize.
        
    Returns:
        List[str]: A list of tokenized words.
    """
    tokens = word_tokenize(text)
    return tokens