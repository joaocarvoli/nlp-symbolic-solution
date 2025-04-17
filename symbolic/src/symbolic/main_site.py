import streamlit as st
import pandas as pd
from scraping.crawler import get_movie_reviews
from sentiment.reader import dic_reader
from sentiment.preprocessing import comment_preprocessing
from sentiment.sentiment import dataframe_sentiment, analyze_sentiment
from utils.constants import PREPROCESSING_COLUMN, SENTIMENT_COLUMN, SENTIMENT_IMAGES, DEFAULT_MOVIE
from sentiment.visualization import get_sentiment_pie


if __name__ == '__main__':
    symbols, words = dic_reader()
    st.title('Avaliação de filmes via Letterboxd')
    st.text('''Nosso sistema avalia os sentimentos presentes nos 100 comentários em português mais relevantes de um filme no Letterboxd.

Ele informa se o sentimento geral inclina para o positivo ou negativo.''')

    movie = st.text_input('Nome do filme', value=DEFAULT_MOVIE)
    poster_url, rating, comments = get_movie_reviews(movie)

    comments = pd.DataFrame(comments)
    movies_pt = comment_preprocessing(comments, PREPROCESSING_COLUMN)
    movies_pt = dataframe_sentiment(movies_pt, PREPROCESSING_COLUMN, SENTIMENT_COLUMN, symbols, words)
    sentiment = analyze_sentiment(movies_pt, SENTIMENT_COLUMN)
    pie = get_sentiment_pie(movies_pt)

    col1, col2 = st.columns(2)
    with col1:
        st.image(poster_url)
    with col2:
        st.header(SENTIMENT_IMAGES[sentiment]['label'])
        st.image(SENTIMENT_IMAGES[sentiment]['image'])
        st.plotly_chart(pie)
