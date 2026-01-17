import os
import sys
import pytest
import pandas as pd
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.missingness_analyzer.type_of_missing_and_how import missing_how_type

@pytest.fixture
def the_df():
    data_path = os.path.join(
        os.path.dirname(__file__),
        "synthetic_dataset.csv"
    )
    return pd.read_csv(data_path)

def test_number_of_truefalse():
    """This test is too see whether the function identify the correct number of columsn that have MCAR"""

    df = pd.read_csv("tests/synthetic_dataset.csv")
    result = missing_how_type(df)

    assert (result["MCAR"] == False).sum() == 3
    assert (result["MCAR"] == True).sum() == 2

def test_raises_error_if_not_dataframe():
    """This test is to see whether the defending raise ValueError display if the input data is not a pandas.dataframe"""

    try:
        missing_how_type("A string")
        assert False, "TypeError should be displayed if there is a wrong input type"
    except TypeError:
        assert True


def test_if_alpha_is_optional():

    df = pd.read_csv("tests/synthetic_dataset.csv")
    result = missing_how_type(df)

    try:
        missing_how_type(df, alpha=1.2)
        assert False, "Expected ValueError for invalid alpha"
    except ValueError:
        assert True


def test_returns_none_if_no_missing_values():
    df = pd.DataFrame({
        "A": [1, 2, 3],
        "B": ["x", "y", "z"]
    })

    out = missing_how_type(df)
    assert out is None


def test_returns_dataframe_when_missing_exists():
    df = pd.DataFrame({
        "A": [1, None, 3, None, 5],
        "B": ["x", "y", "x", "y", "x"]
    })

    out = missing_how_type(df)

    assert isinstance(out, pd.DataFrame)
    assert "MCAR" in out.columns
    assert "A" in out.index

def test_random_missing_can_be_mcar():
    rng = np.random.default_rng(0)
    n = 400

    df = pd.DataFrame({
        "A": rng.normal(size=n),
        "B": rng.choice(["x", "y"], size=n)
    })

    mask = rng.random(n) < 0.2
    df.loc[mask, "A"] = np.nan

    out = missing_how_type(df)

    # Should return a boolean
    assert out.loc["A", "MCAR"] in [True, False]


