import functools
import pandas as pd
from typing import List

from sentiment.word_level import get_word_categories, is_quoted_phrase, word_sentiment, word_sentiment_with_stemming
from sentiment.context_rules import apply_negation_rule, apply_intensifier_rule, apply_punctuation_rule
from sentiment.structural_rules import apply_clause_rule, apply_comparison_rule
from custom_types.strategy import register_word_sentiment_functions

register_word_sentiment_functions(word_sentiment, word_sentiment_with_stemming)

class SentimentAnalyzer:
    def __init__(self, entries_df: pd.DataFrame):
        if not isinstance(entries_df, pd.DataFrame) or entries_df.empty:
             raise ValueError("A valid Pandas DataFrame for entries must be provided.")
        required_cols = ['word', 'is_wildcard', 'category_ids']
        if not all(col in entries_df.columns for col in required_cols):
            raise ValueError(f"Entries DataFrame must contain columns: {required_cols}")

        self.entries_df = entries_df.copy()
        self.negations = {"não", "nunca", "jamais", "nem", "sem"}
        self.intensifiers = {
            "muito": 1.5, "extremamente": 2.0, "demais": 1.5,
            "super": 1.5, "bastante": 1.3
        }
        self.conjunctions = {"mas", "porém", "contudo", "entretanto", "todavia", "no entanto"}
        self.negative_context_words = {"ruim", "péssimo", "terrível", "mau", "horrível"}
        self.positive_context_words = {"bom", "ótimo", "excelente", "maravilhoso", "fantástico"}


    @functools.lru_cache(maxsize=10000)
    def _get_word_categories_cached(self, word: str) -> tuple[int, ...]:
        result = get_word_categories(word, self.entries_df)
        return tuple(sorted(result))

    @functools.lru_cache(maxsize=10000)
    def get_sentiment_for_word(self, word: str) -> float:
         categories = self._get_word_categories_cached(word)
         is_positive = 31 in categories
         is_negative = any(cat in categories for cat in [32, 33, 34, 35])

         if is_positive and not is_negative:
             return 1.0
         elif is_negative and not is_positive:
             return -1.0
         elif is_positive and is_negative:
             return 0.0
         else:
             return 0.0

    def analyze(self, tokens: List[str]) -> float:
        if not tokens:
            return 0.0

        if is_quoted_phrase(tokens):
            return 1.0

        token_sentiments = [self.get_sentiment_for_word(token) for token in tokens]
        base_score = sum(token_sentiments)

        clause_override_score = None
        if any(conj in tokens for conj in self.conjunctions):
             clause_score = apply_clause_rule(tokens, self.conjunctions, self.entries_df)
             if clause_score != 0.0:
                 clause_override_score = clause_score

        negation_adjustment = apply_negation_rule(tokens, token_sentiments, self.negations)
        intensifier_adjustment = apply_intensifier_rule(tokens, token_sentiments, self.intensifiers)
        comparison_adjustment = apply_comparison_rule(tokens, self.entries_df)

        attenuation_adjustment = 0.0
        for i in range(len(tokens) - 2):
            if tokens[i] == "não" and tokens[i + 1] in {"é", "está"}:
                target = tokens[i + 2]
                if target in self.negative_context_words:
                    attenuation_adjustment += 1.0
                elif target in self.positive_context_words:
                    attenuation_adjustment -= 1.0

        current_score = clause_override_score if clause_override_score is not None else base_score

        final_score = current_score + negation_adjustment + intensifier_adjustment \
                      + comparison_adjustment + attenuation_adjustment

        punctuation_multiplier = apply_punctuation_rule(tokens)
        final_score *= punctuation_multiplier

        return final_score

    def analyze_dataframe(self, df: pd.DataFrame, tokens_column: str,
                         sentiment_column: str) -> pd.DataFrame:
        if tokens_column not in df.columns:
            raise ValueError(f"Column '{tokens_column}' not found in DataFrame.")

        df = df.copy()
        raw_score_col = f"{sentiment_column}_raw"
        df[raw_score_col] = df[tokens_column].apply(self.analyze)

        df[sentiment_column] = 0
        df.loc[df[raw_score_col] > 0, sentiment_column] = 1
        df.loc[df[raw_score_col] < 0, sentiment_column] = -1

        return df