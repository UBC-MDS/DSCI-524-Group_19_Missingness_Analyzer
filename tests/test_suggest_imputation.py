import os
import sys
import pytest
import pandas as pd
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.missingness_analyzer.suggest_imputation import suggest_imputation

def test_missingness_amount():
    """Testing to see if function accurately identifies the amount of missingness in the dataset"""
    """The synthetic dataset contains 5 columns of categoric and numeric data with varying percentages of missingness. Overall the amount of empty cells in the dataframe versus filled cells is ~30.8%"""

    df = pd.read_csv("tests/synthetic_dataset.csv")
    
    result = suggest_imputation(df)
    
    assert abs(result["missingness_amount"] - 30.8) < 0.1

def test_no_missing():
    """Testing whether function can handle a dataframe with nothing missing"""
    """Expected behaviour is that "none" method is returned, with no warnings, "No missing data detected" as the reasoning and missingness_amount should be 0"""

    none_missing = pd.DataFrame({"col1": [0, 0, 0], "col2": ["test1", "test2", "test3"]})
    
    result = suggest_imputation(none_missing)
    
    assert result["method"] == 'none'
    assert result["reasoning"] == ['No missing data detected']
    assert result["warnings"] ==  []
    assert result['missingness_amount'] == 0
    
def test_duplicate_col_names():
    """Testing to see if function can handle duplicate column names in the input dataframe without failing"""
    """Expected behaviour is for the function to treat the duplicate column as any other column and process regularly"""
    df_with_dupes = pd.read_csv("tests/synthetic_dataset.csv")
    df_with_dupes = pd.concat([df_with_dupes, df_with_dupes["Category"]], axis = 1)
    
    result = suggest_imputation(df_with_dupes)

    assert result["method"] != "none"

def test_whole_column_missing():
    """Testing to see if function can handle a dataframe with an entire column of missing data"""
    """Expected behaviour is for missingness amount to be equal to 100%"""
    df_whole_col = pd.DataFrame({'all_missing': [np.nan]*100})

    result = suggest_imputation(df_whole_col)

    assert result["missingness_amount"] == 100