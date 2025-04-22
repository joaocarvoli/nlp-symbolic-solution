from typing import List
import pandas as pd
from nltk.stem import PorterStemmer
from custom_types.strategy import WordStrategy
from preprocessing.stemming import _query_by_similarity

def get_word_categories(word: str, entries_df: pd.DataFrame, strategy: WordStrategy = WordStrategy.STEM) -> List[int]:
    exact_match = entries_df[entries_df['word'] == word]
    if not exact_match.empty:
        return exact_match.iloc[0]['category_ids']
    
    if strategy == WordStrategy.STEM:
        wildcard_entries = entries_df[entries_df['is_wildcard']]
        potential_matches = []
        for index, row in wildcard_entries.iterrows():
            wildcard_stem = row['word'][:-1]
            if word.startswith(wildcard_stem):
                potential_matches.append({'match_length': len(wildcard_stem), 'categories': row['category_ids']})

        if potential_matches:
            potential_matches.sort(key=lambda x: x['match_length'], reverse=True)
            return potential_matches[0]['categories']

    return []

def word_sentiment(word: str, entries_df: pd.DataFrame, strategy: WordStrategy = WordStrategy.STEM) -> float:
    categories = get_word_categories(word, entries_df, strategy)

    is_positive = 31 in categories
    is_negative = any(cat in categories for cat in [32, 33, 34, 35])

    if is_positive and not is_negative:
        return 1.0
    elif is_negative and not is_positive:
        return -1.0
    elif is_positive and is_negative:
        return 0.0
    else:
        return 0.0

def word_sentiment_with_stemming(word: str, entries_df: pd.DataFrame, strategy: WordStrategy = WordStrategy.STEM) -> float:
    stemmer = PorterStemmer()
    categories = get_word_categories(word, entries_df, strategy)
    if not categories:
        stem_word = stemmer.stem(word)
        if stem_word != word:
            categories = get_word_categories(stem_word, entries_df, strategy)
    if not categories:
        categories = _query_by_similarity(entries_df, word)
    is_positive = 31 in categories
    is_negative = any(cat in categories for cat in [32, 33, 34, 35])
    if is_positive and not is_negative:
        return 1.0
    elif is_negative and not is_positive:
        return -1.0
    elif is_positive and is_negative:
        return 0.0
    else:
        return 0.0

def is_quoted_phrase(tokens: List[str]) -> bool:
    if not tokens:
        return False
    return (tokens[0] == '"' and tokens[-1] == '"') or \
           (tokens[0] == "'" and tokens[-1] == "'")