from typing import List
from nltk.stem import PorterStemmer
from pandas import DataFrame
from helpers.similarity import similar


def _query_by_similarity(entry_df: DataFrame, word: str) -> List[int]:
    """
    Finds the most similar entry in a DataFrame based on a given word and returns its category ID.

    This function filters the DataFrame to include only entries marked as "wildcards" (`is_wildcard`).
    It then calculates similarity scores between the given word and the wildcard words in the DataFrame.
    The entry with the highest similarity score is selected, and its associated category ID is returned.

    Args:
        entry_df (DataFrame): A DataFrame containing entries with columns such as "is_wildcard", "word", and "category_ids".
        word (str): The input word to compare against the wildcard entries in the DataFrame.

    Returns:
        List[int]: A list containing the category ID(s) of the most similar entry.
    """
    wildcard_df = entry_df[entry_df["is_wildcard"]].copy()

    if wildcard_df.empty:
        return []

    wildcard_df["similarity"] = wildcard_df["word"].apply(lambda w: similar(w, word))
    top_match = wildcard_df.loc[wildcard_df["similarity"].idxmax()]

    return top_match["category_ids"]


def stemming_words(words: List[str], entry_df: DataFrame, porter_steamer: PorterStemmer) -> List[str]:
    words_steamed = []

    for word in words:
        if entry_df["word"].isin([word]).any():
            words_steamed.append(entry_df[entry_df["word"] == word]["category_ids"].values[0])
        
        words_steamed.append(_query_by_similarity(entry_df, word))
        
    return words_steamed