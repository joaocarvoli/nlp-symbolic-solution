from typing import Dict, List, Set

def apply_negation_rule(tokens: List[str], token_sentiments: List[float], negations: Set[str]) -> float:
    """
    Apply negation rule: invert sentiment in a window after negation words.
    
    Args:
        tokens: List of tokens
        token_sentiments: List of sentiment scores for each token
        negations: Set of negation words
        
    Returns:
        Adjustment to sentiment score
    """
    adjustment = 0.0
    window_size = 4
    
    for i, token in enumerate(tokens):
        if token.lower() in negations:
            for j in range(i + 1, min(i + 1 + window_size, len(tokens))):
                if token_sentiments[j] != 0:
                    adjustment -= 2 * token_sentiments[j]
    
    return adjustment

def apply_intensifier_rule(tokens: List[str], token_sentiments: List[float], 
                          intensifiers: Dict[str, float]) -> float:
    """
    Apply intensifier rule: amplify sentiment of words following intensifiers.
    
    Args:
        tokens: List of tokens
        token_sentiments: List of sentiment scores for each token
        intensifiers: Dictionary mapping intensifier words to multipliers
        
    Returns:
        Adjustment to sentiment score
    """
    adjustment = 0.0
    
    for i, token in enumerate(tokens):
        if token.lower() in intensifiers:
            multiplier = intensifiers[token.lower()]
            if i + 1 < len(tokens) and token_sentiments[i + 1] != 0:
                adjustment += (multiplier - 1) * token_sentiments[i + 1]
    
    return adjustment

def apply_punctuation_rule(tokens: List[str]) -> float:
    """
    Apply punctuation rule: amplify sentiment based on punctuation and letter repetition.
    
    Args:
        tokens: List of tokens
        
    Returns:
        Multiplier for sentiment score
    """
    multiplier = 1.0
    
    for token in tokens:
        if "!" in token:
            count_ex = token.count("!")
            multiplier += 0.1 * count_ex
        
        for char in set(token):
            if token.count(char) > 2 and char.isalpha():
                multiplier += 0.05
    
    return multiplier