import os
import sys
import pytest
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.missingness_analyzer.suggest_imputation import suggest_imputation

def test_missingness_identification():
    """Testing to see if fucntion accurately identifies the amount of missingness in the dataset"""

    df = pd.read_csv("tests\synthetic_dataset.csv")
    result = suggest_imputation(df)
    assert result["missingness_amount"] == 30.8