import pandas as pd
import numpy as np
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
    limit: int = None
) -> pd.DataFrame:
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

    # Pre-compute all similarity scores
    similarity_matrices = []
    for left_col, right_col in zip(left_on, right_on):
        left_values = left_df[left_col].astype(str).values
        right_values = right_df[right_col].astype(str).values
        similarity_matrix = np.vectorize(similarity_func)(left_values[:, np.newaxis], right_values)
        similarity_matrices.append(similarity_matrix)

    # Combine similarity scores
    combined_similarity = np.mean(similarity_matrices, axis=0)

    # Apply thresholds
    threshold_mask = np.all([sim >= thresholds[col] for sim, col in zip(similarity_matrices, left_on)], axis=0)
    combined_similarity[~threshold_mask] = 0

    # Get top matches
    if limit:
        top_k = min(limit, combined_similarity.shape[1])
        top_indices = np.argpartition(-combined_similarity, top_k, axis=1)[:, :top_k]
        row_indices = np.arange(combined_similarity.shape[0])[:, np.newaxis]
        top_similarities = combined_similarity[row_indices, top_indices]
        
        # Flatten the indices and similarities
        left_indices = np.repeat(np.arange(len(left_df)), top_k)
        right_indices = top_indices.flatten()
        similarities = top_similarities.flatten()
        
        # Remove pairs with zero similarity
        mask = similarities > 0
        left_indices = left_indices[mask]
        right_indices = right_indices[mask]
        similarities = similarities[mask]
    else:
        nonzero_indices = np.nonzero(combined_similarity)
        left_indices, right_indices = nonzero_indices
        similarities = combined_similarity[nonzero_indices]

    # Create merged DataFrame
    left_data = left_df.iloc[left_indices].reset_index(drop=True)
    right_data = right_df.iloc[right_indices].reset_index(drop=True)
    result_df = pd.concat([left_data, right_data], axis=1)
    result_df['similarity_score'] = similarities

    # Remove duplicate columns
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
#     limit=3
# )