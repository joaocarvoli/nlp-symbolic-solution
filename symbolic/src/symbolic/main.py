import pandas as pd

from utils.reader import dic_reader
from utils.preprocessing import comment_preprocessing
from utils.constants import PREPROCESSING_COLUMN, SENTIMENT_COLUMN
from utils.sentiment import dataframe_sentiment
from utils.evaluation import results
    
if __name__ == '__main__':
    # Reading
    symbols, words = dic_reader()
    movies = pd.read_csv('/Users/jv/Desktop/uni/nlp-symbolic-solution/symbolic/data/movie_reviews_with_language.csv')

    # Processing
    
    movies_pt = movies[movies['language'] == 'pt'].copy()
    movies_pt = comment_preprocessing(movies_pt, PREPROCESSING_COLUMN)
    movies_pt = dataframe_sentiment(movies_pt, PREPROCESSING_COLUMN, SENTIMENT_COLUMN, symbols, words)

    # Evaluation
    overall, good, bad = results(movies_pt, SENTIMENT_COLUMN)

    print("Overall accuracy: %.2f%%" % overall)
    print("Good review accuracy: %.2f%%" % good)
    print("Bad review accuracy: %.2f%%" % bad)