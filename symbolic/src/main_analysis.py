import pandas as pd

from preprocessing.cleaner import preprocess_dataframe
from sentiment.analyzer import SentimentAnalyzer
from utils.constants import PREPROCESSING_COLUMN, SENTIMENT_COLUMN
from utils.evaluation import evaluate_sentiment_results
from utils.dictionary import DictionaryLoader


if __name__ == '__main__':
    dict_loader = DictionaryLoader()
    categories_df, entries_df = dict_loader.load()
    movie_path = '../../data/all_comments.csv'
    movies = pd.read_csv(movie_path)
    overall, positive, negative = evaluate_sentiment_results(movies, SENTIMENT_COLUMN)

    print(f"Overall accuracy: {overall:.2f}%")
    print(f"Positive review accuracy: {positive:.2f}%")
    print(f"Negative review accuracy: {negative:.2f}%")