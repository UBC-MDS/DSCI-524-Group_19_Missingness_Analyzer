import sys
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))
from missingness_analyzer.missing_correlation_matrix import (missing_correlation_matrix,)

def test_missing_corr_returns_dataframe():
    """Result should be a pandas DataFrame when using synthetic_dataset."""
    df = pd.read_csv("tests/synthetic_dataset.csv")

    result = missing_correlation_matrix(df)

    assert isinstance(result, pd.DataFrame)


def test_missing_corr_labels_match_input():
    """Row and column labels should match column names of synthetic_dataset."""
    df = pd.read_csv("tests/synthetic_dataset.csv")

    result = missing_correlation_matrix(df)

    assert list(result.index) == list(df.columns)
    assert list(result.columns) == list(df.columns)


def test_missing_corr_diagonal():
    """Diagonal entries should be 1 for each variable's own missingness."""
    df = pd.read_csv("tests/synthetic_dataset.csv")

    result = missing_correlation_matrix(df)
    assert np.allclose(np.diag(result.values), 1.0)

