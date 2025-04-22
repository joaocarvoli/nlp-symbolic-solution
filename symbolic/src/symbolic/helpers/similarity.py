from difflib import SequenceMatcher

def similar(a: str, b: str) -> float:
    """
    Calculate the similarity ratio between two strings using the SequenceMatcher.
    """
    return SequenceMatcher(None, a, b).ratio()