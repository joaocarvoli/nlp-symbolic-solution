import torch
torch.classes = None

import pandas as pd

from symbolic.src.utils.constants import SENTIMENT_COLUMN
from symbolic.src.utils.evaluation import evaluate_sentiment_results
from symbolic.src.sentiment.sentiment import analyze_sentiment
from symbolic.src.utils.dictionary import DictionaryLoader
from sklearn.model_selection import train_test_split
from neural.model import tokenizer, model

def analyze_sentiment(count_dict):
    positive = count_dict[0]
    negative = count_dict[1]

    if positive > negative:
        return 1
    elif negative > positive:
        return -1
    else:
        return 0


if __name__ == '__main__':
    movie_path = './data/all_comments.csv'
    movies = pd.read_csv(movie_path)
    movies = movies[['movie_title', "comment", "numeric_rating", "sentiment"]]
    movies.rename(columns={"comment":"review_text"}, inplace=True)
    SEED = 42
    movies_FT, movies_test = train_test_split(
        movies, test_size=2704/7704, stratify=movies['numeric_rating'], random_state=SEED
    )

    overall, positive, negative = evaluate_sentiment_results(movies_test, SENTIMENT_COLUMN)

    print(f"Overall accuracy of symbolic solution: {overall:.2f}%")
    print(f"Positive review accuracy of symbolic solution: {positive:.2f}%")
    print(f"Negative review accuracy of symbolic solution: {negative:.2f}%")

    inputs = tokenizer(
        movies_test['review_text'].tolist(),
        truncation=True, 
        padding='max_length', 
        max_length=256, 
        return_tensors='pt'
    )

    model.eval()

    print('Inputs ready!')

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        preds = torch.argmax(logits, dim=1)

    print("torch.no_grad finished")
    
    results = preds.cpu().numpy()
    print("Results finished")

    movies_test[f'{SENTIMENT_COLUMN}_ia'] = results
    movies_test[f'{SENTIMENT_COLUMN}_ia'] = movies_test[f'{SENTIMENT_COLUMN}_ia'].replace(0, -1)
    
    overall_ia, positive_ia, negative_ia = evaluate_sentiment_results(movies_test, f'{SENTIMENT_COLUMN}_ia')

    print(f"Overall accuracy of AI solution: {overall_ia:.2f}%")
    print(f"Positive review accuracy of AI solution: {positive_ia:.2f}%")
    print(f"Negative review accuracy of AI solution: {negative_ia:.2f}%")

    final_dict = {}

    for movie, group in movies_test.groupby('movie_title'):
        contagem_ia = group[f'{SENTIMENT_COLUMN}_ia'].value_counts().sort_index().to_dict()
        contagem_symbolic = group[SENTIMENT_COLUMN].value_counts().sort_index().to_dict()
        media_rating = group['numeric_rating'].mean()

        if media_rating > 2.5:
            movie_sentiment = 1
        else:
            movie_sentiment = -1

        final_dict[movie] = {
            'count_ia': contagem_ia,
            'count_symbolic': contagem_symbolic,
            'numeric_rating': round(media_rating, 2),  # arredondado para 2 casas
            'movie_sentiment_ia': analyze_sentiment(contagem_ia),
            'movie_sentiment_symbolic': analyze_sentiment(contagem_symbolic),
            'movie_sentiment': movie_sentiment
        }

    print(final_dict)

