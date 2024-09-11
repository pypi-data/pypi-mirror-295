import pandas as pd
from typing import Union, List, Dict, Callable
from fuzzywuzzy import fuzz
import jellyfish
from difflib import SequenceMatcher

def similarity_merge(
    left_df: pd.DataFrame,
    right_df: pd.DataFrame,
    left_on: Union[str, List[str]],
    right_on: Union[str, List[str]],
    thresholds: Union[float, Dict[str, float]],
    method: Union[str, Callable] = 'token_sort_ratio',
    limit: int = None,
    best_match: bool = False
) -> pd.DataFrame:
    """
    Merge two DataFrames based on similarity between specified columns.

    Args:
        left_df (pd.DataFrame): Left DataFrame
        right_df (pd.DataFrame): Right DataFrame
        left_on (str or List[str]): Column(s) from left_df to use for matching
        right_on (str or List[str]): Column(s) from right_df to use for matching
        thresholds (float or Dict[str, float]): Similarity threshold(s)
        method (str or Callable): Fuzzy matching method or custom function
        limit (int, optional): Max number of matches per left row
        best_match (bool): If True, return only the best match for each left row

    Returns:
        pd.DataFrame: Merged DataFrame
    """
    if isinstance(left_on, str):
        left_on = [left_on]
    if isinstance(right_on, str):
        right_on = [right_on]

    if len(left_on) != len(right_on):
        raise ValueError("left_on and right_on must have the same number of columns")

    if isinstance(thresholds, float):
        thresholds = {col: thresholds for col in left_on}
    elif isinstance(thresholds, dict):
        if not all(col in thresholds for col in left_on):
            raise ValueError("Thresholds must be specified for all columns")
    else:
        raise ValueError("thresholds must be a float or a dictionary")

    similarity_func = get_similarity_function(method)

    merged_rows = []

    for _, (_, left_row) in enumerate(left_df.iterrows()):
        matches = []
        for _, right_row in right_df.iterrows():
            column_similarities = []
            for left_col, right_col in zip(left_on, right_on):
                col_similarity = similarity_func(str(left_row[left_col]), str(right_row[right_col]))
                column_similarities.append(col_similarity)

            # Check if all column similarities meet their respective thresholds
            if all(sim >= thresholds[col] for sim, col in zip(column_similarities, left_on)):
                # Calculate average similarity as the match score
                match_score = sum(column_similarities) / len(column_similarities)
                matches.append((match_score, right_row))

        matches.sort(key=lambda x: x[0], reverse=True)
        
        if best_match:
            matches = matches[:1]
        elif limit:
            matches = matches[:limit]

        for match_score, right_row in matches:
            merged_row = {**left_row.to_dict(), **right_row.to_dict(), 'similarity_score': match_score}
            merged_rows.append(merged_row)

    result_df = pd.DataFrame(merged_rows)

    result_df = result_df.loc[:, ~result_df.columns.duplicated()]

    return result_df

def get_similarity_function(method: Union[str, Callable]) -> Callable:
    """
    Get the similarity function based on the specified method.

    Args:
        method (str or Callable): The similarity method to use

    Returns:
        Callable: The similarity function
    """
    if callable(method):
        return method
    elif isinstance(method, str):
        if method in dir(fuzz):
            return lambda s1, s2: getattr(fuzz, method)(s1, s2) / 100.0  # Normalize to [0, 1]
        elif method == 'levenshtein':
            return lambda s1, s2: 1 - (jellyfish.levenshtein_distance(s1, s2) / max(len(s1), len(s2)))
        elif method == 'jaro_winkler':
            return jellyfish.jaro_winkler_similarity
        elif method == 'sequence_matcher':
            return lambda s1, s2: SequenceMatcher(None, s1, s2).ratio()
        else:
            raise ValueError(f"Unknown similarity method: {method}")
    else:
        raise ValueError("method must be a string or a callable")

# Example usage:
# left_df = pd.DataFrame(...)
# right_df = pd.DataFrame(...)
# result = similarity_merge(
#     left_df, right_df,
#     left_on=['name', 'address'],
#     right_on=['company_name', 'company_address'],
#     thresholds={'name': 0.8, 'address': 0.7},
#     method='token_sort_ratio',
#     limit=3,
#     best_match=False
# )

# For best match only:
# result_best = similarity_merge(
#     left_df, right_df,
#     left_on=['name', 'address'],
#     right_on=['company_name', 'company_address'],
#     thresholds={'name': 0.8, 'address': 0.7},
#     method='token_sort_ratio',
#     best_match=True
# )