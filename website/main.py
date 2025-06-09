import torch
torch.classes = None

import streamlit as st
import pandas as pd
from symbolic.src.scraping.crawler import get_movie_reviews
from symbolic.src.sentiment.sentiment import analyze_sentiment
from symbolic.src.sentiment.analyzer import SentimentAnalyzer
from symbolic.src.preprocessing.cleaner import preprocess_dataframe
from symbolic.src.utils.dictionary import DictionaryLoader
from symbolic.src.utils.constants import ERROR_IMAGE, PREPROCESSING_COLUMN, SENTIMENT_COLUMN, SENTIMENT_IMAGES, DEFAULT_MOVIE
from symbolic.src.sentiment.visualization import get_sentiment_pie
from neural.model import tokenizer, model

def display_error(e: Exception):
    print(e)
    st.header('Houve um erro')
    col1, col2 = st.columns(2)
    with col1:
        st.image(ERROR_IMAGE)
    with col2:
        st.subheader('''Tivemos um problema ao buscar este filme no Letterboxd. 
Tente novamente ou experimente outro título.''')
        st.write(f"Detalhe do erro: {e}") 

def post_processing(movies_pt):
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

    category = st.selectbox(label='Selecione uma categoria:',
                    options = ['Todos', 'Não recomendado', 'Neutro', 'Recomendado'])
    
    category_num = {
        'Não recomendado': -1,
        'Neutro': 0,
        'Recomendado': 1
    }
    
    sentiment_map = {
        1: "😊 Positivo",
        -1: "😞 Negativo",
        0: "😐 Neutro"
    }

    with st.expander("Mostrar comentários"):
        if category == 'Todos':
            comments_to_show = movies_pt[movies_pt[SENTIMENT_COLUMN].notnull()]
        else:
            comments_to_show = movies_pt[movies_pt[SENTIMENT_COLUMN] == category_num[category]]
        for idx, row in comments_to_show.head(20).iterrows():
            sentiment_label = sentiment_map.get(row[SENTIMENT_COLUMN], "N/A")
            st.markdown(
                f"**{row['username']}** &nbsp;|&nbsp; ⭐ {row['numeric_rating']} &nbsp;|&nbsp; {sentiment_label}<br>"
                f"{row['comment']}",
                unsafe_allow_html=True
            )


if __name__ == '__main__':
    dict_loader = DictionaryLoader()
    categories_df, entries_df = dict_loader.load()

    st.title('Avaliação de filmes via Letterboxd')
    st.text('''Nosso sistema avalia os sentimentos presentes nos 100 comentários em português mais relevantes de um filme no Letterboxd.

Ele informa se o sentimento geral inclina para o positivo ou negativo.''')

    movie = st.text_input('Nome do filme', value=DEFAULT_MOVIE)
    buscar = st.button('Buscar')
    on = st.toggle("Modo IA")

    if buscar or 'movies_pt' not in st.session_state or st.session_state.get('last_movie') != movie:
        try:
            poster_url, rating, comments = get_movie_reviews(movie)
            movies_pt = pd.DataFrame(comments)
            if 'comment' not in movies_pt.columns or movies_pt.empty:
                raise ValueError("Não foi possível encontrar comentários em português para este filme.")
            st.session_state['movies_pt'] = movies_pt
            st.session_state['poster_url'] = poster_url
            st.session_state['last_movie'] = movie
        except Exception as e:
            display_error(e)
            st.stop()
    else:
        movies_pt = st.session_state['movies_pt']
        poster_url = st.session_state['poster_url']

    if on:
        try:
            inputs = tokenizer(
                movies_pt['comment'].tolist(), 
                truncation=True, 
                padding='max_length', 
                max_length=256, 
                return_tensors='pt'
            )

            model.eval()

            with torch.no_grad():
                outputs = model(**inputs)
                logits = outputs.logits
                preds = torch.argmax(logits, dim=1)
            
            results = preds.cpu().numpy()
            movies_pt[SENTIMENT_COLUMN] = results
            movies_pt[SENTIMENT_COLUMN] = movies_pt[SENTIMENT_COLUMN].replace(0, -1)
            post_processing(movies_pt)
        except Exception as e:
            display_error(e)
            st.stop()

    else:
        try:
            movies_pt = preprocess_dataframe(movies_pt, 'comment', PREPROCESSING_COLUMN)
            analyzer = SentimentAnalyzer(entries_df)
            movies_pt = analyzer.analyze_dataframe(movies_pt, PREPROCESSING_COLUMN, SENTIMENT_COLUMN)
            post_processing(movies_pt)

        except Exception as e:
            display_error(e)
            st.stop()