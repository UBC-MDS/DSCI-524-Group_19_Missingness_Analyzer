def generate_missing_report(df):
    """
   This function calculates the total number of missing values 
   ​​and the percentage of missing values ​​in each column of the input pandas DataFrame. 
   It then organizes these results into a well-structured table, providing a more intuitive view of 
   the distribution of missing values.

    Parameters
    df : pd.DataFrame
        A pandas DataFrame containing the data for which missingness
        should be summarized.

    Returns
    pd.DataFrame
        Returns a DataFrame, with each column corresponding to a variable in the original data,
        and provides information such as 'number of missing data' and 'proportion of missing data'.
    """