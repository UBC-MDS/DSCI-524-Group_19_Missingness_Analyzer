import os
import sys
import pytest
import pandas as pd
import numpy as np
from pathlib import Path

# #sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
# ROOT = Path(__file__).resolve().parents[1]
# sys.path.append(str(ROOT / "src"))
from missingness_analyzer import missing_how_type

@pytest.fixture
def the_df():
    "This is the data set to test on"
    return pd.read_csv("tests/synthetic_dataset.csv")

@pytest.fixture
def the_result():
    "This is the result table of the function"
    df = pd.read_csv("tests/synthetic_dataset.csv")
    return missing_how_type(df, alpha = 0.05)

def test_number_of_truefalse(the_result):
    """This test is too see whether the function identify the correct number of columsn that have MCAR"""

    assert (the_result["MCAR"] == False).sum() == 3
    assert (the_result["MCAR"] == True).sum() == 2

def test_raises_error_if_not_dataframe():
    """This test is to see whether the defending raise ValueError display if the input data is not a pandas.dataframe"""

    try:
        missing_how_type("A string")
        assert False, "TypeError should be displayed if there is a wrong input type"
    except TypeError:
        assert True

def test_if_alpha_is_optional(the_df, the_result):
    """This test is to see whether the alpha input is actually default = 0.05 and optional or not"""

    assert the_result.equals(missing_how_type(the_df))

def test_if_alpha_matter(the_df):
    """This test check whether alpha actually do affect the final result or not"""

    result1 = missing_how_type(the_df, alpha=0.01)
    result2 = missing_how_type(the_df, alpha=0.5)

    assert not result1.equals(result2)

def test_return_none_if_no_missing():
    df = pd.DataFrame({
        "A": [1, 2, 3],
        "B": ["i", "j", "z"]
    })

    assert missing_how_type(df) is None
