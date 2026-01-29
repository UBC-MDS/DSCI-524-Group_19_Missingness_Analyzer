import sys
from pathlib import Path
import pandas as pd
import numpy as np
import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))
from missingness_analyzer.missing_correlation_matrix import (missing_correlation_matrix,)

@pytest.fixture
def the_df():
    "This is the data set to test on"
    return pd.read_csv("tests/synthetic_dataset.csv")

@pytest.fixture
def the_result():
    "This is the result table of the function"
    df = pd.read_csv("tests/synthetic_dataset.csv")
    return missing_correlation_matrix(df)

def test_missing_corr_returns_dataframe(the_result):
    """Result should be a pandas DataFrame when using synthetic_dataset."""

    assert isinstance(the_result, pd.DataFrame)


def test_missing_corr_labels_match_input(the_df, the_result):
    """Row and column labels should match column names of synthetic_dataset."""

    assert list(the_result.index) == list(the_df.columns)
    assert list(the_result.columns) == list(the_df.columns)


def test_missing_corr_diagonal(the_result):
    """Diagonal entries should be 1 for each variable's own missingness."""

    assert np.allclose(np.diag(the_result.values), 1.0)

def test_correlation_values_between_one_minusone(the_result):
    """Make sure all correlation values are between -1 and 1."""
    
    assert (the_result >= -1.0).all().all(), "Correlation values cannot be less than -1"
    assert (the_result <= 1.0).all().all(), "Correlation values cannot be bigger than 1"

def test_correlation_matrix_square_shape(the_df, the_result):
    """Correlation matrix should be square (same number of rows and columns)."""
        
    rows, cols = the_result.shape
    assert rows == cols, f"Matrix is not square with {the_result.shape}, please fix!"
    assert rows == len(the_df.columns)
    assert cols == len(the_df.columns)

def test_if_function_give_correct_answer():
    """This test tests whether the function work as expected with other random data"""

    df = pd.DataFrame({'age': [25, np.nan, 35], 'income': [50000, 60000, np.nan]})
    result = missing_correlation_matrix(df)

    assert result.iloc[0, 0] == 1
    assert result.iloc[0, 1] == -0.5
    assert result.iloc[1, 0] == -0.5
    assert result.iloc[1, 1] == 1

def test_if_all_missing():
    """This test that if a dataset have a column that fully missing, 
    it will throw NA to prevent doing correlation (because there is no variance)"""
    
    df = pd.DataFrame({
    'col1': [np.nan, np.nan],
    'col2': [1, 2],
    })

    result = missing_correlation_matrix(df)

    assert pd.isna(result.loc['col1', 'col2'])

def test_if_no_missing():
    """This test aims to confirm that the function is able to handle dataframes with no missing values"""

    df = pd.DataFrame({
    'col1': [1, 2],
    'col2': [1, 2],
    })

    result = missing_correlation_matrix(df)

    assert result.empty

def test_non_dataframe_input():
    """This is a test for correct handling of the input not being a dataframe"""

    df = "hi"

    with pytest.warns(UserWarning, match="Cannot compute missing correlations"):
        result = missing_correlation_matrix(df)
    
    assert result.empty