from typing import List
from nltk.corpus import stopwords

stops = set(stopwords.words('portuguese'))

manual_detected_stop_words = {'o', 'a', 'os', 'as', 'um', 'uma', 'uns', 'umas', 'de', 'do', 'da', 'e', 'que', 'eu', 'tu', 'ele', 'ela', 'eles', 'vós', 'nós', 'você', 'vocês', 'me', 'te', 'lhe', 'nos', 'vos', 'lhes', 'mim', 'ti', 'si'}


def remove_stop_words(words: List[str]) -> str:
    """
    Remove stop words from the given text.
    
    Args:
        text (str): The input text from which to remove stop words.
        
    Returns:
        str: The text with stop words removed.
    """
    all_stopwords = set(stops) | set(manual_detected_stop_words)
    filtered_words = [word for word in words if word.lower() not in all_stopwords]
    
    return ' '.join(filtered_words)