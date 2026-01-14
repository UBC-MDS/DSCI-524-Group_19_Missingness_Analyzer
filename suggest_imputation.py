def suggest_imputation(df, missingness_type)
"""
Prints a suggested imputation strategy for handling missing data in a dataset based the datatypes in the dataframe and the amount of missingness.

Parameters:
    df (pd.DataFrame): A pandas dataframe to analyze missingness for
    missingness_type (str): The type of missingness present in the function

Returns:
    dict : Single imputation recommendation for the dataframe

"""
# Structure and parts of the code written with Claude AI

# Get columns with missing data
cols_with_missing = df.columns[df.isnull().any()].tolist()

if not cols_with_missing:
    return {
        'method': 'none',
        'reasoning': ['No missing data detected'],
        'warnings': []
    }

# Calculate overall missing percentage
total_missing = df.isnull().sum().sum()
total_cells = df.size
missing_pct = (total_missing / total_cells) * 100

# Analyze dataframe characteristics
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()

has_numeric = len([c for c in cols_with_missing if c in numeric_cols]) > 0
has_categorical = len([c for c in cols_with_missing if c in categorical_cols]) > 0

# Score different methods
method_scores = {}
reasoning = []
warnings = []

# Rule 1: High overall missingness
if missing_pct > 30:
    warnings.append(f"High overall missingness ({missing_pct:.1f}%) - results may be unreliable")
    method_scores['mice'] = method_scores.get('mice', 0) + 20
    method_scores['knn'] = method_scores.get('knn', 0) + 15

# Rule 2: Low overall missingness - simple methods work
if missing_pct < 5:
    reasoning.append("Low missingness allows simple imputation")
    method_scores['simple'] = 40

# Rule 3: Mixed data types
if has_numeric and has_categorical:
    reasoning.append("Mixed data types present")
    method_scores['mice'] = method_scores.get('mice', 0) + 35
    method_scores['knn'] = method_scores.get('knn', 0) + 25
elif has_numeric:
    reasoning.append("Primarily numeric data")
    method_scores['knn'] = method_scores.get('knn', 0) + 30
    method_scores['simple'] = method_scores.get('simple', 0) + 20
else:
    reasoning.append("Primarily categorical data")
    method_scores['simple'] = method_scores.get('simple', 0) + 30

# Rule 4: Missingness pattern
if missingness_type:
    if 'MCAR' in missingness_type:
        reasoning.append("MCAR pattern: simple methods are valid")
        method_scores['simple'] = method_scores.get('simple', 0) + 25
    elif 'MAR' in missingness_type:
        reasoning.append("MAR pattern: multivariate methods recommended")
        method_scores['mice'] = method_scores.get('mice', 0) + 40
        method_scores['knn'] = method_scores.get('knn', 0) + 35
    elif 'MNAR' in missingness_type:
        warnings.append("MNAR suspected: all imputation methods may introduce bias")
        method_scores['mice'] = method_scores.get('mice', 0) + 20

# Rule 5: Time series detection
if df.index.dtype == 'datetime64[ns]':
    reasoning.append("Time series data detected")
    method_scores['interpolation'] = 50

# Select best method
if method_scores:
    best_method = max(method_scores.items(), key=lambda x: x[1])[0]
else:
    best_method = 'simple'

# Map to specific implementation
method_mapping = {
    'simple': 'SimpleImputer (mean for numeric, most_frequent for categorical)',
    'knn': 'KNNImputer (k=5)',
    'mice': 'IterativeImputer (MICE algorithm)',
    'interpolation': 'Time-based interpolation'
}

return {
    'method': method_mapping.get(best_method, best_method),
    'reasoning': reasoning,
    'warnings': warnings,
    'missing_percentage': round(missing_pct, 2)
}