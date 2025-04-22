import pandas as pd
import os

from preprocessing.cleaner import preprocess_dataframe
from sentiment.analyzer import SentimentAnalyzer
from utils.dictionary import DictionaryLoader
from utils.evaluation import evaluate_sentiment_results
from utils.visualization import plot_accuracy_metrics, plot_sentiment_distribution
from utils.constants import PREPROCESSING_COLUMN, SENTIMENT_COLUMN
    
if __name__ == '__main__':
    dict_loader = DictionaryLoader()
    categories_df, entries_df = dict_loader.load()

    print(f"Type of categories_df after load: {type(categories_df)}")
    print(f"Type of entries_df after load: {type(entries_df)}")
    if not isinstance(entries_df, pd.DataFrame) or entries_df.empty:
        raise TypeError(f"SentimentAnalyzer expects a non-empty DataFrame for entries_df, but received {type(entries_df)}")

    data_file = 'movie_reviews_with_language.csv'
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    movie_path = os.path.join(base_path, 'data', data_file)

    print(f"Attempting to load movie data from: {movie_path}")

    try:
        movies = pd.read_csv(movie_path)
    except FileNotFoundError:
        print(f"Error: Could not find data file at {movie_path}")
        print(f"Current Working Directory: {os.getcwd()}")
        exit()

    movies_pt = movies[movies['language'] == 'pt'].copy()
    if movies_pt.empty:
        print("Warning: No Portuguese reviews found in the dataset.")
    else:
        movies_pt = preprocess_dataframe(movies_pt, 'comment', PREPROCESSING_COLUMN)

        analyzer = SentimentAnalyzer(entries_df)
        movies_pt = analyzer.analyze_dataframe(movies_pt, PREPROCESSING_COLUMN, SENTIMENT_COLUMN)

        output_dir = os.path.join(base_path, 'results')
        os.makedirs(output_dir, exist_ok=True)
        dist_plot_path = os.path.join(output_dir, 'sentiment_distribution.png')
        acc_plot_path = os.path.join(output_dir, 'accuracy_metrics.png')


        plot_sentiment_distribution(movies_pt, SENTIMENT_COLUMN, dist_plot_path)
        print(f"Sentiment distribution plot saved to: {dist_plot_path}")

        overall, positive, negative = evaluate_sentiment_results(movies_pt, SENTIMENT_COLUMN)

        print(f"Overall accuracy: {overall:.2f}%")
        print(f"Positive review accuracy: {positive:.2f}%")
        print(f"Negative review accuracy: {negative:.2f}%")

        plot_accuracy_metrics(overall, positive, negative, acc_plot_path)
        print(f"Accuracy metrics plot saved to: {acc_plot_path}")

        print("Analysis complete. Plots saved.")