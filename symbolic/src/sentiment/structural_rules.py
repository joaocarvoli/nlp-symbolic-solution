from typing import List, Set
import pandas as pd
from symbolic.src.custom_types.strategy import WordStrategy, WORD_STRATEGY

def apply_clause_rule(tokens: List[str], conjunctions: Set[str], entries_df: pd.DataFrame, strategy: WordStrategy = WordStrategy.STEM) -> float:
    clauses = []
    split_indices = [-1]
    
    for i, token in enumerate(tokens):
        if token in conjunctions:
            split_indices.append(i)

    if len(split_indices) == 1:
        return 0.0

    split_indices.append(len(tokens))
    for i in range(len(split_indices) - 1):
        start = split_indices[i] + 1
        end = split_indices[i+1]
        clause_tokens = tokens[start:end]
        if clause_tokens:
            clauses.append(clause_tokens)

    if len(clauses) < 2:
        return 0.0

    clause_scores = []
    for clause in clauses:
        score = sum(WORD_STRATEGY[strategy](token, entries_df, strategy) for token in clause)
        clause_scores.append(score)

    combined_score = clause_scores[0] + 1.5 * clause_scores[-1]

    return combined_score

def apply_comparison_rule(tokens: List[str], entries_df: pd.DataFrame) -> float:
    adjustment = 0.0
    for i in range(len(tokens) - 2):
        first = tokens[i]
        second = tokens[i + 1]
        third = tokens[i + 2]

        if first in {"melhor", "pior"} and second == "que":
            next_sentiment = WORD_STRATEGY[WordStrategy.STEM](third, entries_df)
            if first == "melhor" and next_sentiment < 0:
                adjustment += 0.5
            elif first == "pior" and next_sentiment > 0:
                adjustment -= 0.5
    return adjustment