import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

def missing_how_type(df, alpha=0.05):
    """
    This function will analyze and print out a report of missing values and the type of missingness in the dataset.

    There are three types of missing data:
    - MCAR: Missing completely at random, which can be tested using the chi-squared function from the SciPy package. 
    The chi-squared function helps test the independence of the columns in the dataset to determine whether 
    the missingness is completely independent of each other
    - MAR: Missing at random. If the missingness is not MCAR, it may be MAR; 
    however, further domain knowledge is required to make this determination.
    - MNAR: Missing not at random. Domain expertise is required to determine whether this type of missingness is present.

    Parameters
    ----------
    df: pandas.DataFrames
        A pandas dataframe to analyze missingness.

    alpha: float, default=0.05
        The significant level to test the p.value that result from the chi-squared test

    Returns
    -------
    pandas.DataFrame
        The table contains two columns: one shows the names of the columns in the dataset, and the other indicates whether each column is MCAR, MAR, or MNAR.
        If the value is True, the column is MCAR. If the value is False, the column is either MAR or MNAR.

    Examples
    --------
    >>> df = pd.DataFrame({'age': [25, np.nan, 35], 'income': [50000, 60000, np.nan]})
    >>> missing_how_type(df, alpha=0.05)
    This data frame have 2 missing values, below is the number of missing values for each column:
    age             1
    income          1
    dtype: int64

    Columns with True value is Missing Completely at Random (MCAR)
    Columns with False value are either Missing at Random (MAR) or Missing Not at Random (MNAR)
    Since MAR and MNAR cannot be tested statistically and formally, additional domain expertise is needed for further investigation

    pd.DataFrame # a pandas dataframe that show whether each column have MCAR or not

    """
    
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Your df is not a pandas DataFrame.")
    
    if not (0 < alpha < 1):
        raise ValueError("Your alpha value must be between 0 and 1.")

    results = []

    if df.isna().sum().sum() == 0:
        print("The data set has no missing values.")
        return

    for target in df.columns:

        if df[target].isna().sum() == 0:
            results.append({"target": target,
                            "MCAR": "No Missing Value"})
            continue

        for other_target in df.columns:
            if target == other_target:
                continue

            missing = df[target].isna()
            table = pd.crosstab(missing, df[other_target])

            if table.shape[1] < 2:
                continue
            
            try:
                p = chi2_contingency(table)[1]
            except ValueError:
                raise ValueError(
                    f"Chi-square test failed for column {target} and {other_target}"
                )

            results.append({
                "target": target,
                "other_target": other_target,
                "p.value": p,
                "MCAR": p > alpha
            })
    
    print(f"This data frame have {df.isna().sum().sum()} missing values, below is the number of missing values for each column:")
    print(df.isna().sum())
    print("\nColumns with True value is Missing Completely at Random (MCAR)")
    print("Columns with False value are either Missing at Random (MAR) or Missing Not at Random (MNAR)")
    print("Since MAR and MNAR cannot be tested statistically and formally, additional domain expertise is needed for further investigation")

    return pd.DataFrame(results).groupby("target")[["MCAR"]].all()   