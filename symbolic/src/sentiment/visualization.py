import pandas as pd
import plotly.express as px

def get_sentiment_pie(df: pd.DataFrame):
    # Count occurrences of each sentiment
    sentiment_counts = df['sentiment'].value_counts().sort_index()

    # Map numerical values to labels
    labels = {-1: 'Não recomendado', 0: 'Neutro', 1: 'Recomendado'}
    df_counts = pd.DataFrame({
        'Sentiment': [labels[k] for k in sentiment_counts.index],
        'Count': sentiment_counts.values
    })

    # Create pie chart
    return px.pie(df_counts, names='Sentiment', values='Count', title='Distribuição de sentimento')