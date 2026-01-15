import pandas as pd
import numpy as np

from missingness_analyzer.missing_correlation_matrix import missing_correlation_matrix  


def test_missing_corr_basic_shape_and_labels():
    df = pd.DataFrame(
        {
            "a": [1, None, 3, None],
            "b": [None, 2, 3, 4],
            "c": [1, 2, 3, 4]
        }
    )

    result = missing_correlation_matrix(df)

    assert isinstance(result, pd.DataFrame)
    assert list(result.index) == ["a", "b", "c"]
    assert list(result.columns) == ["a", "b", "c"]
    assert np.allclose(np.diag(result.values), 1.0)
