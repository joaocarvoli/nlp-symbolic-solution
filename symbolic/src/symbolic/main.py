import pandas as pd
import matplotlib.pyplot as plt

from utils.reader import dic_reader
from utils.preprocessing import comment_preprocessing
from utils.constants import PREPROCESSING_COLUMN, SENTIMENT_COLUMN
from utils.sentiment import dataframe_sentiment
from utils.evaluation import results
    
if __name__ == '__main__':
    # Reading
    symbols, words = dic_reader()
    data_file = 'movie_reviews_with_language.csv'
    movie_path = '../../data/' + data_file
    movies = pd.read_csv(movie_path)

    # Processing
    
    movies_pt = movies[movies['language'] == 'pt'].copy()
    movies_pt = comment_preprocessing(movies_pt, PREPROCESSING_COLUMN)
    movies_pt = dataframe_sentiment(movies_pt, PREPROCESSING_COLUMN, SENTIMENT_COLUMN, words)
    #movies_pt, distribution = dataframe_sentiment(movies_pt, PREPROCESSING_COLUMN, SENTIMENT_COLUMN, words)

    # count_positive, count_negative, count_zero = 0,0,0
    # for dist in distribution:
    #     count_positive += sum(1 for x in dist if x>0)
    #     count_negative += sum(1 for x in dist if x<0)
    #     count_zero += sum(1 for x in dist if x==0)

    # counts = [count_positive, count_negative, count_zero]
    # plt.bar(['positive', 'negative', 'neutral'], counts)
    # plt.savefig('Test.png')

    # Evaluation
    overall, good, bad = results(movies_pt, SENTIMENT_COLUMN)

    print("Overall accuracy: %.2f%%" % overall)
    print("Good review accuracy: %.2f%%" % good)
    print("Bad review accuracy: %.2f%%" % bad)