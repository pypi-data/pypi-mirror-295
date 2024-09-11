import pandas as pd
import numpy as np
from typing import Union, List, Dict, Callable
from fuzzywuzzy import fuzz
import jellyfish
from difflib import SequenceMatcher
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_bipartite_matching

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

    # Pre-compute all similarity scores using chunking
    chunk_size = 1000  # Adjust based on available memory
    num_left = len(left_df)
    num_right = len(right_df)
    
    similarity_matrices = []
    for left_col, right_col in zip(left_on, right_on):
        similarity_matrix = np.zeros((num_left, num_right))
        for i in range(0, num_left, chunk_size):
            left_chunk = left_df[left_col].iloc[i:i+chunk_size].astype(str).values
            for j in range(0, num_right, chunk_size):
                right_chunk = right_df[right_col].iloc[j:j+chunk_size].astype(str).values
                chunk_sim = np.vectorize(similarity_func)(left_chunk[:, np.newaxis], right_chunk)
                similarity_matrix[i:i+chunk_size, j:j+chunk_size] = chunk_sim
        similarity_matrices.append(similarity_matrix)

    # Combine similarity scores
    combined_similarity = np.mean(similarity_matrices, axis=0)

    # Apply thresholds
    threshold_mask = np.all([sim >= thresholds[col] for sim, col in zip(similarity_matrices, left_on)], axis=0)
    combined_similarity[~threshold_mask] = 0

    # Convert to sparse matrix for memory efficiency
    sparse_similarity = csr_matrix(combined_similarity)

    if limit:
        matches = []
        for i in range(num_left):
            row = sparse_similarity.getrow(i)
            top_k = min(limit, row.nnz)  # number of non-zero elements
            if top_k > 0:
                top_indices = np.argpartition(-row.data, top_k-1)[:top_k]
                matches.extend([(i, row.indices[j], row.data[j]) for j in top_indices if row.data[j] > 0])
        matches = sorted(matches, key=lambda x: x[2], reverse=True)
    else:
        # Use maximum bipartite matching for optimal 1-to-1 matching
        graph = (sparse_similarity > 0).astype(int)
        matching = maximum_bipartite_matching(graph, perm_type='column')
        matches = [(i, j, combined_similarity[i, j]) for i, j in enumerate(matching) if j >= 0]

    # Create result DataFrame
    left_indices, right_indices, similarities = zip(*matches) if matches else ([], [], [])
    left_data = left_df.iloc[list(left_indices)].reset_index(drop=True)
    right_data = right_df.iloc[list(right_indices)].reset_index(drop=True)
    result_df = pd.concat([left_data, right_data], axis=1)
    result_df['similarity_score'] = similarities

    # Remove duplicate columns
    result_df = result_df.loc[:, ~result_df.columns.duplicated()]

    return result_df

def get_similarity_function(method: Union[str, Callable]) -> Callable:
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