import streamlit as st
import pandas as pd
from scraping.crawler import get_movie_reviews
from sentiment.sentiment import analyze_sentiment
from sentiment.analyzer import SentimentAnalyzer
from preprocessing.cleaner import preprocess_dataframe
from utils.dictionary import DictionaryLoader
from utils.constants import ERROR_IMAGE, PREPROCESSING_COLUMN, SENTIMENT_COLUMN, SENTIMENT_IMAGES, DEFAULT_MOVIE
from sentiment.visualization import get_sentiment_pie


if __name__ == '__main__':
    dict_loader = DictionaryLoader()
    categories_df, entries_df = dict_loader.load()

    st.title('Avaliação de filmes via Letterboxd')
    st.text('''Nosso sistema avalia os sentimentos presentes nos 100 comentários em português mais relevantes de um filme no Letterboxd.

Ele informa se o sentimento geral inclina para o positivo ou negativo.''')

    movie = st.text_input('Nome do filme', value=DEFAULT_MOVIE)
    try:
        poster_url, rating, comments = get_movie_reviews(movie)

        movies_pt = pd.DataFrame(comments)
        movies_pt = preprocess_dataframe(movies_pt, 'comment', PREPROCESSING_COLUMN)
        analyzer = SentimentAnalyzer(entries_df)
        movies_pt = analyzer.analyze_dataframe(movies_pt, PREPROCESSING_COLUMN, SENTIMENT_COLUMN)
        sentiment = analyze_sentiment(movies_pt, SENTIMENT_COLUMN)
        pie = get_sentiment_pie(movies_pt)
        movie_title = movies_pt.iloc[0]['movie_title']

        col1, col2 = st.columns(2)
        with col1:
            st.header(movie_title)
            st.image(poster_url)
        with col2:
            st.subheader(SENTIMENT_IMAGES[sentiment]['label'])
            st.image(SENTIMENT_IMAGES[sentiment]['image'])
            st.plotly_chart(pie)

    except Exception as e:
        print(e)
        st.header('Houve um erro')
        col1, col2 = st.columns(2)
        with col1:
            st.image(ERROR_IMAGE)
        with col2:
            st.subheader('''Tivemos um problema ao buscar este filme no Letterboxd. 

Tente novamente ou experimente outro título.''')