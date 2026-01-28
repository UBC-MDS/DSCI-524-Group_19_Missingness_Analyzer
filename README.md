# DSCI_524_Group_19_Missingness_Analyzer

Canada, Vancouver

Creation of a data-science related package for DSCI 524 (Collaborative Software Development); a course in the Master of Data Science program at the University of British Columbia. 2025-2026.

## **Contributors**

Rocco Lee, Nguyen Nguyen, Shuhang Li

## **About**

Missing data imputation/handling is one of the most common forms of data cleaning that needs to happen in any analysis project. Large amounts of missing data can heavily skew the distribution of data or labels within the dataset, or invalidate large portions of rwos in the dataset if an imputation strategy is not defined. The vision for this package is to not only give surface level analysis of how much missing data there is in a given dataset, but also to identify potential patterns to the missing data, such as Missing Completely At Random (MCAR), Missing At Random (MAR) or Missing Not At Random (MNAR), and use machine learning algorithms to give a sensible suggestion to the imputation strategy that would make sense to be used in ceertain contexts.

## Setting Up 

Here's how to setup missingness_analyzer for local development:

1. Fork the repository: https://github.com/UBC-MDS/DSCI-524-Group_19_Missingness_Analyzer

2. Clone the fork locally using:

```bash 
git clone git@github.com:your_name_here/missingness_analyzer.git
```

3. Create the virtual environment with:
```bash 
conda env create -f environment.yml
```

4. Once the environment is created, activiate it with:
```bash
conda activate 524-Group-19
```

5. Install the package with:
```bash
pip install -e .
```

6. Develop Away!
  * Make sure to document your changes with comments
  * If you are adding new functions in new python files, ensure that the docstring for those functions are written with Numpy formatting.

## Publishing Your Code

After fixing bugs or developing new features, here's how you can deploy your changes

1. Verify that all tests still pass with (run in terminal):
```bash
pytest
```

2. Once you have verified that all tests pass, commit and push your changes to the remote repository and create a pull request

3. This should automatically trigger a Github Workflow which automatically updates the HTML site containing documentation for this package, builds an artifact and deploys the changes to PyPI
  * The updated documentation can be found [here] (https://ubc-mds.github.io/DSCI-524-Group_19_Missingness_Analyzer/CONTRIBUTING.html)

## **List of Functions**

* type\_of\_missing\_and\_how

  * This function describes the amount of missing data in the dataset and attempts to identify the type of missingness (MCAR, MAR or MNAR)

  * Unit tests written for this function are: 

     * the_df()

     * the_result()

     * test_number_of_truefalse()

     * test_raises_error_if_not_dataframe()

     * test_if_alpha_is_optional(the_df, the_result)

     * test_if_alpha_matter(the_df)

     * test_return_none_if_no_missing()

* suggest\_imputation

  * This function takes in the dataset and the type of missingness and parses the amount of missingness and datatypes in the dataframe to suggest an imputation strategy that would be best suited. The best suited method and reasoning is returned to the user in a dictionary format.

  * Unit tests written for this function are: 

     * test_missingness_amount()

     * test_no_missing()

     * test_duplicate_col_names()

     * test_whole_column_missing()

* missing\_correlation\_matrix

  * This function takes a pandas dataframe as an argument and returns a correlation matrix of the amount of missingness to help identify the type of missingness

  * Unit tests written for this function are: 

     * test_missing_corr_returns_dataframe()

     * test_missing_corr_labels_match_input()

     * test_missing_corr_diagonal()

## **Python Ecosystem**

Below is a summary of existing packages related to our topic:

**scikit-na** (https://pypi.org/project/scikit-na/)
This is a package that contains functions for statistical analysis, building visuals and export capabilities for helping data scientists understand and handle missing values in their datasets.

**mdatagen** (https://github.com/ArthurMangussi/pymdatagen)
This GitHub repo contains a project for artificially generating data for missing fields.

**Other Existing Packages** (e.g. deepchecks)
Other packages like deepchecks have functions that can be used to write tests to detect if the amount of missing data in a dataset passes a set threshold.
What differentiates our package from existing ones is the implementation of a smart imputation function which suggests an imputation method based on notonly the type of missingness present in the dataframe, but also takes into account the datatypes of the columns in the dataframe. Also included are two helper functions which aid the user in identifying the type of missingness present in the input as well as a handy function to display a correlation matrix of the missing data.