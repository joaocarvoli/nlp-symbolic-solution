import pandas as pd

def analyze_sentiment(df: pd.DataFrame, sentiment_col: str):
    sentiment_counts = df[sentiment_col].value_counts()

    positive = sentiment_counts.get(1, 0)
    negative = sentiment_counts.get(-1, 0)

    if positive > negative:
        return 1
    elif negative > positive:
        return -1
    else:
        return 0
