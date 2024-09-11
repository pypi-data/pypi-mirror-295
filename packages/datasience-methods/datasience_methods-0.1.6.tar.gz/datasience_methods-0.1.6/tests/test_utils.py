from datasience_methods.utils import similarity_merge
import pytest
import pandas as pd

@pytest.fixture
def sample_dataframes():
    left_df = pd.DataFrame({
        'name': ['John Doe', 'Jane Smith', 'Mike Johnson'],
        'address': ['123 Main St', '456 Elm St', '789 Oak St'],
        'age': [30, 25, 35]
    })
    
    right_df = pd.DataFrame({
        'company_name': ['John Doe Inc', 'Jane Smyth LLC', 'Michael Johnson Co'],
        'company_address': ['123 Main Street', '456 Elm Street', '789 Oak Avenue'],
        'revenue': [100000, 75000, 120000]
    })
    
    return left_df, right_df

def test_similarity_merge(sample_dataframes):
    left_df, right_df = sample_dataframes
    
    result = similarity_merge(
        left_df,
        right_df,
        left_on=['name', 'address'],
        right_on=['company_name', 'company_address'],
        thresholds={'name': 0.8, 'address': 0.8}
    )
    
    # Check if the result is a DataFrame
    assert isinstance(result, pd.DataFrame)
    
    # Check if the result is not empty
    assert len(result) > 0
    
    # Check if all columns from both DataFrames are present
    expected_columns = set(left_df.columns) | set(right_df.columns) | {'similarity_score'}
    assert set(result.columns) == expected_columns
    
    # Check if the merge was performed correctly
    assert 'John Doe' in result['name'].values
    assert 'John Doe Inc' in result['company_name'].values
    
    # Check if similarity scores are present and within the expected range
    assert 'similarity_score' in result.columns
    assert all(result['similarity_score'] >= 0.64)  # 0.8 * 0.8 = 0.64

def test_similarity_merge_no_matches(sample_dataframes):
    left_df, right_df = sample_dataframes
    
    result = similarity_merge(
        left_df,
        right_df,
        left_on=['name', 'address'],
        right_on=['company_name', 'company_address'],
        thresholds={'name': 1.0, 'address': 1.0}  # Set very high thresholds
    )
    
    # Check if the result is an empty DataFrame
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 0

def test_similarity_merge_invalid_input():
    left_df = pd.DataFrame({'name': ['John']})
    right_df = pd.DataFrame({'company_name': ['John Inc']})
    
    # Test with mismatched column lists
    with pytest.raises(ValueError):
        similarity_merge(
            left_df,
            right_df,
            left_on=['name'],
            right_on=['company_name', 'extra_column'],
            thresholds={'name': 0.8}
        )
    
    # Test with missing threshold
    with pytest.raises(ValueError):
        similarity_merge(
            left_df,
            right_df,
            left_on=['name'],
            right_on=['company_name'],
            thresholds={}
        )

def test_similarity_merge_with_limit(sample_dataframes):
    left_df, right_df = sample_dataframes
    
    result = similarity_merge(
        left_df,
        right_df,
        left_on=['name', 'address'],
        right_on=['company_name', 'company_address'],
        thresholds={'name': 0.7, 'address': 0.7},
        limit=2
    )
    
    # Check if the result is not empty
    assert len(result) > 0
    
    # Check if the number of matches per left row is limited
    assert len(result.groupby('name')) <= 2

def test_similarity_merge_custom_method(sample_dataframes):
    left_df, right_df = sample_dataframes
    
    def custom_similarity(s1, s2):
        return 1 if s1.lower() in s2.lower() or s2.lower() in s1.lower() else 0
    
    result = similarity_merge(
        left_df,
        right_df,
        left_on=['name'],
        right_on=['company_name'],
        thresholds=0.9,
        method=custom_similarity
    )
    
    # Check if the result is not empty
    assert len(result) > 0
    
    # Check if the custom method was applied correctly
    assert all(result['similarity_score'].isin([0, 1]))

def test_similarity_merge_single_threshold(sample_dataframes):
    left_df, right_df = sample_dataframes
    
    result = similarity_merge(
        left_df,
        right_df,
        left_on=['name', 'address'],
        right_on=['company_name', 'company_address'],
        thresholds=0.7
    )
    
    # Check if the result is not empty
    assert len(result) > 0
    
    # Check if the single threshold was applied correctly
    assert all(result['similarity_score'] >= 0.49)  # 0.7 * 0.7 = 0.49