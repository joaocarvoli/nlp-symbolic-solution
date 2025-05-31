import pandas as pd

def evaluate_sentiment_results(df: pd.DataFrame, sentiment_col: str, rating_col: str = 'numeric_rating', 
                              rating_threshold: float = 2.5) -> tuple:
    """
    Evaluate sentiment analysis results against ratings.
    
    Args:
        df: Dataframe with sentiment predictions and actual ratings
        sentiment_col: Column containing sentiment predictions (-1, 0, 1)
        rating_col: Column containing numeric ratings
        rating_threshold: Threshold to consider a rating as positive/negative
        
    Returns:
        Tuple of (overall accuracy, positive accuracy, negative accuracy)
    """
    # Filter out neutral sentiment predictions
    df_non_neutral = df.loc[df[sentiment_col] != 0]
    
    # Count total valid predictions
    total_reviews = df_non_neutral.shape[0]
    
    # Count reviews by rating
    bad_reviews = df_non_neutral.loc[df_non_neutral[rating_col] <= rating_threshold].shape[0]
    good_reviews = df_non_neutral.loc[df_non_neutral[rating_col] > rating_threshold].shape[0]
    
    # Count correct predictions
    bad_review_and_sentiment = df_non_neutral.loc[
        (df_non_neutral[rating_col] <= rating_threshold) & 
        (df_non_neutral[sentiment_col] == -1)
    ].shape[0]
    
    good_review_and_sentiment = df_non_neutral.loc[
        (df_non_neutral[rating_col] > rating_threshold) & 
        (df_non_neutral[sentiment_col] == 1)
    ].shape[0]
    
    # Calculate accuracies
    overall_accuracy = (bad_review_and_sentiment + good_review_and_sentiment) / total_reviews * 100
    positive_accuracy = good_review_and_sentiment / good_reviews * 100
    negative_accuracy = bad_review_and_sentiment / bad_reviews * 100
    
    return overall_accuracy, positive_accuracy, negative_accuracy