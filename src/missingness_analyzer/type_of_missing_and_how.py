def missing_how_type_(df):
    """
    Print out a report that contain the number of missing data in the data set, and also identify and print out the type of missigness.
    There are 3 types of missingness: Missing completely at random (MCAR), 
    Missing at random (MAR), Missing Not at random (MNAR)

    Parameters
    ----------
    df(pd.DataFrames) : A pandas dataframe to analyze missingness.

    Returns
    -------
    None

    """

    results = []

    if df.isna().sum().sum() == 0:
        print("The data set have no missing values.")
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

            chi2, p, dof, exp = chi2_contingency(table)

            results.append({
                "target": target,
                "other_target": other_target,
                "p_value": p,
                "MCAR": p > alpha
            })
    
    print("\nColumns with True value is Missing Completely at Random (MCAR)")
    print("Columns with False value are either Missing at Random (MAR) or Missing Not at Random (MNAR)")
    print("Since MAR and MNAR cannot be tested statistically and formally, additional domain expertise is needed for further investigation")

    return pd.DataFrame(results).groupby("target")[["MCAR"]].all()   