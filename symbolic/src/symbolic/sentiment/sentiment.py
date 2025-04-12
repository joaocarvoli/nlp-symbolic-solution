import pandas as pd

# Defines how a word is evaluated according to its sentiment
def word_sentiment(word: str, symbols: dict[int, str], words: dict[str, list[int]]):
    if word not in words or 30 not in words[word]:
        return 0
    elif 31 in words[word]:
        return 1
    elif 32 in words[word]:
        return -1
    else:
        return 0
    
def dataframe_sentiment(df: pd.DataFrame, preprocessing_col: str, sentiment_col: str, symbols: dict[int, str], words: dict[str, list[int]]):
    df[sentiment_col] = df[preprocessing_col].apply(lambda words_list: sum(word_sentiment(word, symbols, words) for word in words_list))

    df.loc[df[sentiment_col] < 0, sentiment_col] = -1
    df.loc[df[sentiment_col] > 0, sentiment_col] = 1

    return df

def analyze_sentiment(df: pd.DataFrame, sentiment_col: str):
    sentiment_counts = df[sentiment_col].value_counts()

    positive = sentiment_counts.get(1, 0)
    negative = sentiment_counts.get(-1, 0)

    if positive > negative:
        return 'Positive'
    elif negative > positive:
        return 'Negative'
    else:
        return 'Neutral'
