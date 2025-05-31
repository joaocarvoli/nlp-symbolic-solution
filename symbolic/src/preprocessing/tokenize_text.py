from typing import List
import re

def tokenize_text(text: str) -> List[str]:
    """
    Tokenize text into words.
    
    Args:
        text: Input text to tokenize
        
    Returns:
        List of tokens
    """
    # Simple space-based tokenization
    tokens = text.split()
    return tokens

def clean_token(token: str) -> str:
    """
    Clean a token by removing punctuation from beginning and end.
    
    Args:
        token: Input token to clean
        
    Returns:
        Cleaned token
    """
    cleaned_token = re.sub(r"^[\W_]+|[\W_]+$", "", token, flags=re.UNICODE)
    return cleaned_token if cleaned_token else token