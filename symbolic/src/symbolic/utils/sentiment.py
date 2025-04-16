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


## teste das ideias do amigo gpt

def analyze_sentiment(tokens: list[str], words: dict[str, list[int]]) -> float:
    """
    Calcula a pontuação de sentimento de um comentário, aplicando regras simbólicas:
      - Cálculo base usando word_sentiment
      - Repetição de palavras-chave
      - Expansão do escopo de negação
      - Intensificação via intensificadores e advérbios
      - Pontuação (ex.: múltiplos pontos de exclamação)
      - Análise de cláusulas com coordenação (ex.: "mas")
      - Comparações implícitas (ex.: "melhor que", "pior que")
      - Atenuação contextualizada (ex.: "não é ruim")
    """
    # Listas para palavras auxiliares
    negations = {"não", "nunca", "jamais", "nem", "sem"}
    # Intensificadores e advérbios de modo com seus multiplicadores
    intensifiers = {
        "muito": 1.5,
        "extremamente": 2.0,
        "demais": 1.5,
        "super": 1.5,
        "bastante": 1.3
    }
    # Conjunções que indicam contraste ou separação de cláusulas
    coord_conjunctions = {"mas", "porém", "contudo", "entretanto", "todavia", "no entanto"}





    base_score = 0.0
    token_sentiments = [word_sentiment(token.lower(), words) for token in tokens]
    
    # --- Regra Base: soma dos sentimentos individuais ---
    for s in token_sentiments:
        base_score += s

    # --- Regra 1: Repetição de Palavras-Chave ---
    # Se a mesma palavra de sentimento aparece várias vezes, adicione um bônus.
    repetition_bonus = 0.0
    repetition_counts = {}
    for i, token in enumerate(tokens):
        token_lower = token.lower()
        s = word_sentiment(token_lower, words)
        if s != 0:
            repetition_counts[token_lower] = repetition_counts.get(token_lower, 0) + 1
    # Para cada palavra repetida, adiciona um bônus arbitrário (por exemplo, 0.1 para cada ocorrência extra)
    for token, count in repetition_counts.items():
        if count > 1:
            repetition_bonus += 0.1 * (count - 1)
    
    # --- Regra 2: Expansão do Escopo de Negação ---
    # Se um termo de negação aparece, inverter o sinal das palavras de sentimento em uma janela maior
    negation_adjustment = 0.0
    window_neg = 4  # janela de 4 tokens após a negação
    for i, token in enumerate(tokens):
        if token.lower() in negations:
            # Para cada token na janela seguinte, se for palavra de sentimento, inverte o seu efeito
            for j in range(i + 1, min(i + 1 + window_neg, len(tokens))):
                s = word_sentiment(tokens[j].lower(), words)
                if s != 0:
                    # Como o valor já foi somado, subtrai duas vezes o valor para inverter
                    negation_adjustment -= 2 * s

    # --- Regra 3: Intensificação por Intensificadores/Advérbios ---
    # Se um intensificador aparece imediatamente antes de uma palavra de sentimento
    intensification_adjustment = 0.0
    for i, token in enumerate(tokens):
        token_lower = token.lower()
        if token_lower in intensifiers:
            multiplier = intensifiers[token_lower]
            # Se o próximo token é uma palavra de sentimento, amplifica seu valor
            if i + 1 < len(tokens):
                s_next = word_sentiment(tokens[i + 1].lower(), words)
                if s_next != 0:
                    # Adiciona a diferença causada pelo intensificador
                    intensification_adjustment += (multiplier - 1) * s_next

    # --- Regra 4: Pontuação e Formatação ---
    # Procura por tokens que contenham múltiplos pontos de exclamação ou repetições de caracteres (ex.: "!!!", "muuuito")
    punctuation_amplifier = 1.0
    for token in tokens:
        if "!" in token:
            count_ex = token.count("!")
            # Cada ponto de exclamação extra aumenta o multiplicador em 10%
            punctuation_amplifier += 0.1 * count_ex
        # Exemplo: se houver letras repetidas, podemos fazer uma checagem simples
        # (essa regra é simplificada; pode-se melhorar com expressões regulares)
        for char in set(token):
            if token.count(char) > 2 and char.isalpha():
                punctuation_amplifier += 0.05

    # --- Regra 5: Subordinadas e Coordenação + Contraste Explícito ---
    # Se houver conjunções de contraste, separe as cláusulas e dê maior peso (por exemplo, à última cláusula)
    clauses = []
    current_clause = []
    for token in tokens:
        if token.lower() in coord_conjunctions:
            if current_clause:
                clauses.append(current_clause)
            current_clause = []
        else:
            current_clause.append(token)
    if current_clause:
        clauses.append(current_clause)
    
    # Se houver duas ou mais cláusulas, podemos ajustar o score
    clause_scores = []
    for clause in clauses:
        cs = sum(word_sentiment(tok.lower(), words) for tok in clause)
        clause_scores.append(cs)
    # Se houver contraste, por exemplo, dar mais ênfase à última cláusula
    clause_adjustment = 0.0
    if len(clause_scores) >= 2:
        # Uma estratégia: combinar o score da primeira cláusula com 1.5x o score da última
        clause_adjustment = clause_scores[0] + 1.5 * clause_scores[-1]
        # Essa substituição pode ser feita ou somada ao score base, conforme teste.
        # Aqui optamos por substituir o score base para casos com contraste.
        base_score = clause_adjustment

    # --- Regra 6: Comparações Implícitas ---
    # Procura padrões como "melhor que" ou "pior que" que podem indicar amplificação da polaridade
    comparison_adjustment = 0.0
    for i in range(len(tokens) - 2):
        first = tokens[i].lower()
        second = tokens[i + 1].lower()
        third = tokens[i + 2].lower()
        if first in {"melhor", "pior"} and second == "que":
            next_sent = word_sentiment(third, words)
            if first == "melhor" and next_sent < 0:
                comparison_adjustment += 0.5
            elif first == "pior" and next_sent > 0:
                comparison_adjustment -= 0.5

    # --- Regra 7: Negação ou Atenuação Contextualizada ---
    # Detecta frases como "não é ruim" ou "não está bom" e ajusta o sentimento para ser menos extremo.
    attenuation_adjustment = 0.0
    for i in range(len(tokens) - 2):
        if tokens[i].lower() == "não" and tokens[i + 1].lower() in {"é", "está"}:
            target = tokens[i + 2].lower()
            if target in {"ruim", "péssimo", "terrível"}:
                # "não é ruim" tende para positivo ou pelo menos neutro
                attenuation_adjustment += 1.0
            elif target in {"bom", "ótimo", "excelente"}:
                # "não é bom" tende para diminuir a positividade
                attenuation_adjustment -= 1.0

    # --- Soma dos ajustes ---
    final_score = base_score
    final_score += repetition_bonus
    final_score += negation_adjustment
    final_score += intensification_adjustment
    final_score += comparison_adjustment
    final_score += attenuation_adjustment
    # Aplica amplificação determinada pela pontuação e formatação
    final_score *= punctuation_amplifier

    if is_quoted_phrase(tokens):
        final_score = 1.0

    return final_score










def dataframe_sentiment(df: pd.DataFrame, preprocessing_col: str, sentiment_col: str, words: dict[str, list[int]]):
    # gen_sent = []
    # sentiment_dists = []
    # for row in df[preprocessing_col].items():
    #     x = evaluate_phrase(row[1], words)
    #     gen_sent.append(x[0])
    #     sentiment_dists.append(x[1])
    #df[sentiment_col] = pd.DataFrame(gen_sent)

    df[sentiment_col] = df[preprocessing_col].apply(lambda words_list: analyze_sentiment(words_list, words))

    df.loc[df[sentiment_col] < 0, sentiment_col] = -1
    df.loc[df[sentiment_col] > 0, sentiment_col] = 1

    return df#, sentiment_dists

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