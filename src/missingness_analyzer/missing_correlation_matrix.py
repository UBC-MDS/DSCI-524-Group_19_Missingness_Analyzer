import warnings
def missing_correlation_matrix(df):
    """
    Calculate correlations between variables' missingness patterns.

    For each column in `df`, this function constructs a binary indicator
    (1 = value is missing, 0 = value is observed) and computes the
    pairwise correlation matrix of these indicators. High positive
    correlations flag variables that tend to be missing at the same time,
    which can reveal shared data-collection issues or common missingness mechanisms.

    Parameters
    ----------
    df : pd.DataFrame
        A pandas DataFrame for which the pairwise correlations of missing
        values across columns should be computed.

    Returns
    -------
    pd.DataFrame
        A square DataFrame whose rows and columns correspond to the original
        variables, and whose entries give the correlation between their
        missingness indicators.   

    Examples
    --------
    >>> df = pd.DataFrame({'age': [25, np.nan, 35], 'income': [50000, 60000, np.nan]})
    >>> result = missing_correlation_matrix(df)
                    age	    income
        age	        1.0	    -0.5
        income	   -0.5	    1.0

    
    """
    try:
        missing_indicators = df.isna().astype(float)
        corr_matrix = missing_indicators.corr()
        corr_matrix = corr_matrix.loc[df.columns, df.columns]
        return corr_matrix
    except:
        warnings.warn("Cannot compute missing correlations: invalid input")
        return pd.DataFrame()