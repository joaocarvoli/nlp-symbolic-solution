import pandas as pd

# Defines how a word is evaluated according to its sentiment
def word_sentiment(word: str, symbols: dict[int, str], words: dict[str, list[int]]):
    if word not in words or 30 not in words[word]:
        return 0
    elif 31 in words[word]:
        return 1
    elif {32, 33, 34, 35} & set(words[word]):
        return -1
    else:
        return 0

def evaluate_phrase(word_list: list[str]):
    sentiment_words = {
        'negative': {'não', 'n', 'nao', 'mas', 'entanto'},
        'intensity': {'muito', 'demais'}
    }
    word_set = set(word_list)
    word_directions = dict()
    for word in word_set:
        for sentiment in sentiment_words['negative'] or sentiment in sentiment_words['intensity']: 
            word_directions[word] = context_flags_with_direction(word_list, word, sentiment)
    print(word_directions)
    return 0
    
def dataframe_sentiment(df: pd.DataFrame, preprocessing_col: str, sentiment_col: str, symbols: dict[int, str], words: dict[str, list[int]]):
    df[sentiment_col] = df[preprocessing_col].apply(lambda words_list: evaluate_phrase(words_list))

    df.loc[df[sentiment_col] < 0, sentiment_col] = -1
    df.loc[df[sentiment_col] > 0, sentiment_col] = 1

    return df

def is_quoted_phrase(word_list):
    if not word_list:
        return False
    return word_list[0] == '"' and word_list[-1] == '"'

def context_flags_with_direction(phrase, target_word, element):
    results = []
    for index, word in enumerate(phrase):
        if word == target_word:
            before_indices = range(max(0, index - 2), index)
            after_indices = range(index + 1, min(len(phrase), index + 3))

            direction = None
            found = False

            # Check before
            for i in before_indices:
                if phrase[i] == element:
                    found = True
                    direction = "before"
                    break

            # Check after only if not already found
            if not found:
                for i in after_indices:
                    if phrase[i] == element:
                        found = True
                        direction = "after"
                        break

            results.append((found, direction))
    return results