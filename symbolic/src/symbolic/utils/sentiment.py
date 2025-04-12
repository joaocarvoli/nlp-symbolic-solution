import pandas as pd

# Defines how a word is evaluated according to its sentiment
def word_sentiment(word: str, words: dict[str, list[int]]):
    if word not in words or 30 not in words[word]:
        return 0
    elif 31 in words[word]:
        return 1
    elif {32, 33, 34, 35} & set(words[word]):
        return -1
    else:
        return 0
    
def reduce_neutrality(word_list: list[str], words: dict[str, list[int]]):
    words_sentiments = [word_sentiment(word, words) for word in word_list]
    result_list = words_sentiments[:]
    i = 0
    while i < len(words_sentiments):
        if words_sentiments[i] == 0:
            start = i
            while i < len(words_sentiments) and words_sentiments[i] == 0:
                i += 1
            end = i

            if start > 0 and end < len(words_sentiments):
                if words_sentiments[start - 1] == words_sentiments[end] and words_sentiments[start - 1] in [-1, 1]:
                    for j in range(start, end):
                        result_list[j] = words_sentiments[start - 1]
        else:
            i += 1
    return sum(result_list)

def evaluate_phrase(word_list: list[str], words: dict[str, list[int]]):
    sentiment_words = {
        'negative': {'não', 'n', 'nao', 'mas', 'entanto'},
        'intensity': {'muito', 'demais', 'bastante', 'tanto', 'mais'}
    }

    # word_set = set(word_list)
    # word_directions = dict()
    # for word in word_set:
    #     for sentiment in sentiment_words['negative'] or sentiment in sentiment_words['intensity']: 
    #         word_directions[word] = context_flags_with_direction(word_list, word, sentiment)
    # print(word_directions)
    # sentiment = 0
    general_sentiment = 0
    partial_sentiments = []
    if is_quoted_phrase(word_list):
        general_sentiment = 1
    else: 
        for i in range(len(word_list)):
            sentiment = word_sentiment(word_list[i], words)
            if sentiment != 0:

                context_intensity = context_flags_with_direction(word_list, word_list[i], sentiment_words['intensity'])
                for tuple0 in context_intensity:
                    if tuple0[0]:
                        sentiment *= 2
                        context_intensity_negative = context_flags_with_direction(word_list, word_list[i], sentiment_words['negative'])
                        for tuple1 in context_intensity_negative:
                            if tuple1[1] == 'after':
                                sentiment *= 0.5
                            elif tuple1[1] == 'before':
                                sentiment *= -1

                context_negative = context_flags_with_direction(word_list, word_list[i], sentiment_words['negative'])
                for tuple in context_negative:
                    if tuple[0]: 
                        if tuple[1] == 'after':
                            sentiment *= 0.5
                        elif tuple[1] == 'before':
                            sentiment *= -1
            general_sentiment += sentiment
            partial_sentiments.append(sentiment)

    return general_sentiment, partial_sentiments


def evaluate_phrase2(word_list: list[str], words: dict[str, list[int]]):
    sentiment_words = {
        'negative': {'não', 'n', 'nao', 'mas', 'entanto'},
        'intensity': {'muito', 'demais', 'bastante', 'tanto', 'mais'}
    }

    general_sentiment = 0
    negation = False
    for word in word_list:
        sentiment = word_sentiment(word, words)
        if word in sentiment_words['negative']:
            negation = not negation
        if word in sentiment_words['intensity']:
            sentiment *= 2

        if negation:
            sentiment *= -1

        general_sentiment += sentiment

    return general_sentiment


def dataframe_sentiment(df: pd.DataFrame, preprocessing_col: str, sentiment_col: str, words: dict[str, list[int]]):
    gen_sent = []
    sentiment_dists = []
    for row in df[preprocessing_col].items():
        x = evaluate_phrase(row[1], words)
        gen_sent.append(x[0])
        sentiment_dists.append(x[1])
    #df[sentiment_col] = pd.DataFrame(gen_sent)

    df[sentiment_col] = df[preprocessing_col].apply(lambda words_list: reduce_neutrality(words_list, words))

    df.loc[df[sentiment_col] < 0, sentiment_col] = -1
    df.loc[df[sentiment_col] > 0, sentiment_col] = 1

    return df, sentiment_dists

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