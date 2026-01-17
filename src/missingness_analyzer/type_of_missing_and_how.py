import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

def missing_how_type_(df, alpha=0.05):
    """
    Print out a report that contain the number of missing data in the data set, and also identify and print out the type of missigness.
    There are 3 types of missingness: Missing completely at random (MCAR), 
    Missing at random (MAR), Missing Not at random (MNAR)

    Parameters
    ----------
    df(pd.DataFrames) : A pandas dataframe to analyze missingness.

    Returns
    -------
    A data frame that show boolean value of which columns are MCAR or MAR and MNAR

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