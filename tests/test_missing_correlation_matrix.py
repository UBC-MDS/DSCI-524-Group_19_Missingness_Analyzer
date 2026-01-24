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


def test_missing_corr_returns_dataframe(the_df):
    """Result should be a pandas DataFrame when using synthetic_dataset."""

    result = missing_correlation_matrix(the_df)

    assert isinstance(result, pd.DataFrame)


def test_missing_corr_labels_match_input(the_df):
    """Row and column labels should match column names of synthetic_dataset."""

    result = missing_correlation_matrix(the_df)

    assert list(result.index) == list(the_df.columns)
    assert list(result.columns) == list(the_df.columns)


def test_missing_corr_diagonal(the_df):
    """Diagonal entries should be 1 for each variable's own missingness."""

    result = missing_correlation_matrix(the_df)
    assert np.allclose(np.diag(result.values), 1.0)

def test_correlation_values_between_one_minusone(the_df):
    """Make sure all correlation values are between -1 and 1."""

    result = missing_correlation_matrix(the_df)
    
    assert (result >= -1.0).all().all(), "Correlation values cannot be less than -1"
    assert (result <= 1.0).all().all(), "Correlation values cannot be bigger than 1"

def test_correlation_matrix_square_shape(the_df):
    """Correlation matrix should be square (same number of rows and columns)."""
    
    result = missing_correlation_matrix(the_df)
    
    n_rows, n_cols = result.shape
    assert n_rows == n_cols, f"Matrix should be square but got shape {result.shape}"
    
    # Also verify it matches the number of columns in input
    assert n_rows == len(the_df.columns)
    assert n_cols == len(the_df.columns)

