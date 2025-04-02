import re
import pandas as pd

from utils.constants import punctuation

# Removes punctuation from words that not all characters are punctuations (enables emojis, for example)
def word_cleaning(word: str):
    cleaned_word = re.sub(r"^[\W_]+|[\W_]+$", "", word, flags=re.UNICODE)
    return cleaned_word if cleaned_word else word

def comment_preprocessing(df: pd.DataFrame, preprocessing_col: str):
    df[preprocessing_col] = df['comment'].apply(lambda x: [
        word_cleaning(word).lower() for word in x.split() 
        if (word not in punctuation)
    ])

    return df