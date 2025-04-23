from typing import Set
from nltk.corpus import stopwords

def get_stopwords(include_negations: bool = False) -> Set[str]:
    nltk_stops = set(stopwords.words('portuguese'))
    
    manual_stops = {
        'o', 'a', 'os', 'as', 'um', 'uma', 'uns', 'umas', 'de', 'do', 'da', 'e', 
        'que', 'eu', 'tu', 'ele', 'ela', 'eles', 'vós', 'nós', 'você', 'vocês', 
        'me', 'te', 'lhe', 'nos', 'vos', 'lhes', 'mim', 'ti', 'si'
    }
    
    all_stopwords = nltk_stops | manual_stops
    
    if not include_negations:
        negations = {'não', 'nunca', 'jamais', 'nem', 'sem'}
        for word in negations:
            all_stopwords.discard(word)
            
    return all_stopwords