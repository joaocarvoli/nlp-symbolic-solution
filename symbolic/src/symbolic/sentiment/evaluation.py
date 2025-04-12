import pandas as pd

def results(df: pd.DataFrame, sentiment_col: str):
    # Number of reviews with sentiment != 0
    total_reviews = df.loc[(df[sentiment_col] != 0)].shape[0]

    # Number of reviews with numeric_rating <= 2.5 and sentiment != 0
    bad_reviews = df.loc[(df['numeric_rating'] <= 2.5) & (df[sentiment_col] != 0)].shape[0]

    # Number of reviews with numeric_rating > 2.5 and sentiment != 0
    good_reviews = df.loc[(df['numeric_rating'] > 2.5) & (df[sentiment_col] != 0)].shape[0]

    # Number of reviews with numeric_rating <= 2.5 and sentiment == -1
    bad_review_and_sentiment = df.loc[(df['numeric_rating'] <= 2.5) & (df[sentiment_col] == -1)].shape[0]

    # Number of reviews with numeric_rating > 2.5 and sentiment == 1
    good_review_and_sentiment = df.loc[(df['numeric_rating'] > 2.5) & (df[sentiment_col] == 1)].shape[0]

    return (bad_review_and_sentiment + good_review_and_sentiment)/total_reviews*100, \
        good_review_and_sentiment/good_reviews*100, \
        bad_review_and_sentiment/bad_reviews*100