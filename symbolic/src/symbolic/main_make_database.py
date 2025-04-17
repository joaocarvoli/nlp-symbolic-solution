import pandas as pd
import os
import re
import csv

from scraping.crawler import get_movie_reviews
from sentiment.preprocessing import comment_preprocessing
from sentiment.sentiment import dataframe_sentiment, analyze_sentiment
from sentiment.reader import dic_reader
from utils.constants import PREPROCESSING_COLUMN, SENTIMENT_COLUMN

with open('./data/movies.txt', encoding='utf-8') as f:
    symbols, words = dic_reader()
    for movie_name in f.readlines():
        movie_name = movie_name.strip()
        print(movie_name)
        
        try:
            _, rating, comments = get_movie_reviews(movie_name)
            comments = pd.DataFrame(comments)
            movies_pt = comment_preprocessing(comments, PREPROCESSING_COLUMN)
            movies_pt = dataframe_sentiment(movies_pt, PREPROCESSING_COLUMN, SENTIMENT_COLUMN, symbols, words)
            sentiment = analyze_sentiment(movies_pt, SENTIMENT_COLUMN)

            movie_title = comments.iloc[0]['movie_title'].lower()
            movie_title = re.sub(r'[^\w\s]', '', movie_title)
            movie_title = movie_title.replace(' ', '_')
            print(movie_title)

            comments.to_csv(f'./data/movies/{movie_title}.csv', index=False)
            
            all_exists = os.path.isfile('./data/all_comments.csv')
            comments.to_csv('./data/all_comments.csv', mode='a', index=False, header=not all_exists)

            match = (rating <= 2.5 and sentiment == -1) or (rating > 2.5 and sentiment == 1)
            recommendation_df = pd.DataFrame([{'movie_title': comments.iloc[0]['movie_title'], 'average_rating': rating, 'recommendation': sentiment, 'match': match}])
            write_header = not os.path.exists('./data/movie_recommendation.csv')

            recommendation_df.to_csv('./data/movie_recommendation.csv', mode='a', header=write_header, index=False)

        except:
            with open('./data/wrong_movies.txt', 'a', encoding='utf-8') as f:
                f.write(f'{movie_name}\n')