import pandas as pd
from fuzzywuzzy import fuzz
from typing import List, Dict, Union

def similarity_merge(
    left_df: pd.DataFrame,
    right_df: pd.DataFrame,
    left_on: Union[str, List[str]],
    right_on: Union[str, List[str]],
    thresholds: Dict[str, float],
    method: str = 'token_sort_ratio'
) -> pd.DataFrame:
    """
    Merge two DataFrames based on similarity between specified columns.

    Args:
        left_df (pd.DataFrame): Left DataFrame
        right_df (pd.DataFrame): Right DataFrame
        left_on (str or List[str]): Column(s) from left_df to use for matching
        right_on (str or List[str]): Column(s) from right_df to use for matching
        thresholds (Dict[str, float]): Dictionary of column names and their similarity thresholds
        method (str): Fuzzy matching method to use (default: 'token_sort_ratio')

    Returns:
        pd.DataFrame: Merged DataFrame
    """
    if isinstance(left_on, str):
        left_on = [left_on]
    if isinstance(right_on, str):
        right_on = [right_on]

    if len(left_on) != len(right_on):
        raise ValueError("left_on and right_on must have the same number of columns")

    merged_df = pd.DataFrame()

    for left, right in zip(left_on, right_on):
        if left not in thresholds or right not in thresholds:
            raise ValueError(f"Threshold not specified for columns {left} or {right}")

        threshold = thresholds[left]  # Assuming same threshold for corresponding columns

        # Cross join
        cross = left_df[[left]].merge(right_df[[right]], how='cross')

        # Calculate similarity
        cross['similarity'] = cross.apply(
            lambda row: getattr(fuzz, method)(str(row[left]), str(row[right])),
            axis=1
        )

        # Filter based on threshold
        cross = cross[cross['similarity'] >= threshold]

        # Merge with original DataFrames
        if merged_df.empty:
            merged_df = pd.merge(left_df, cross, on=left)
            merged_df = pd.merge(merged_df, right_df, left_on=right, right_on=right, suffixes=('', '_right'))
        else:
            merged_df = pd.merge(merged_df, cross, on=left)
            merged_df = pd.merge(merged_df, right_df, left_on=right, right_on=right, suffixes=('', '_right'))

    # Drop duplicate columns and rename
    cols_to_drop = [col for col in merged_df.columns if col.endswith('_right')]
    merged_df = merged_df.drop(columns=cols_to_drop)

    return merged_df