import pytest
import pandas as pd
from datasience_methods.utils import similarity_merge

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
        thresholds={'name': 80, 'address': 80}
    )
    
    # Check if the result is a DataFrame
    assert isinstance(result, pd.DataFrame)
    
    # Check if the number of rows is correct (should be 3 in this case)
    assert len(result) == 3
    
    # Check if all columns from both DataFrames are present
    expected_columns = set(left_df.columns) | set(right_df.columns) | {'similarity'}
    assert set(result.columns) == expected_columns
    
    # Check if the merge was performed correctly
    assert result.loc[0, 'name'] == 'John Doe'
    assert result.loc[0, 'company_name'] == 'John Doe Inc'
    
    # Check if similarity scores are present and within the expected range
    assert 'similarity' in result.columns
    assert all(result['similarity'] >= 80)

def test_similarity_merge_no_matches(sample_dataframes):
    left_df, right_df = sample_dataframes
    
    result = similarity_merge(
        left_df,
        right_df,
        left_on=['name', 'address'],
        right_on=['company_name', 'company_address'],
        thresholds={'name': 100, 'address': 100}  # Set very high thresholds
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
            thresholds={'name': 80}
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