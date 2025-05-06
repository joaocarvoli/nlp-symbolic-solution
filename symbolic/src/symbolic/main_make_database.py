import pandas as pd
import os
import re

from scraping.crawler import get_movie_reviews
from sentiment.sentiment import analyze_sentiment
from preprocessing.cleaner import preprocess_dataframe
from sentiment.analyzer import SentimentAnalyzer
from utils.dictionary import DictionaryLoader
from utils.constants import PREPROCESSING_COLUMN, SENTIMENT_COLUMN

with open('./data/movies.txt', encoding='utf-8') as f:
    dict_loader = DictionaryLoader()
    categories_df, entries_df = dict_loader.load()
    os.makedirs('./data/movies', exist_ok=True)

    for movie_name in f.readlines():
        movie_name = movie_name.strip()
        print(movie_name)
        
        try:
            _, rating, movies_pt = get_movie_reviews(movie_name)
            movies_pt = pd.DataFrame(movies_pt)

            movies_pt = preprocess_dataframe(movies_pt, 'comment', PREPROCESSING_COLUMN)
            analyzer = SentimentAnalyzer(entries_df)
            movies_pt = analyzer.analyze_dataframe(movies_pt, PREPROCESSING_COLUMN, SENTIMENT_COLUMN)
            sentiment = analyze_sentiment(movies_pt, SENTIMENT_COLUMN)

            movie_title = movies_pt.iloc[0]['movie_title'].lower()
            movie_title = re.sub(r'[^\w\s]', '', movie_title)
            movie_title = movie_title.replace(' ', '_')

            movies_pt.to_csv(f'./data/movies/{movie_title}.csv', index=False)
            
            all_exists = os.path.isfile('./data/all_comments.csv')
            movies_pt.to_csv('./data/all_comments.csv', mode='a', index=False, header=not all_exists)

            recommendation_df = pd.DataFrame([{'movie_title': movies_pt.iloc[0]['movie_title'], 'average_rating': rating, 'recommendation': sentiment}])
            write_header = not os.path.exists('./data/movie_recommendation.csv')

            recommendation_df.to_csv('./data/movie_recommendation.csv', mode='a', header=write_header, index=False)

        except:
            with open('./data/wrong_movies.txt', 'a', encoding='utf-8') as f:
                f.write(f'{movie_name}\n')