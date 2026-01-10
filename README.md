# DSCI_524_Group_19_Missingness_Analyzer

Canada, Vancouver

Creation of a data-science related package for DSCI 524 (Collaborative Software Development); a course in the Master of Data Science program at the University of British Columbia. 2025-2026.

## **Contributors**

Rocco Lee, Nguyen Nguyen, Shuhang Li

## **About**

Missing data imputation/handling is one of the most common forms of data cleaning that needs to happen in any analysis project. Large amounts of missing data can heavily skew the distribution of data or labels within the dataset, or invalidate large portions of rwos in the dataset if an imputation strategy is not defined. The vision for this package is to not only give surface level analysis of how much missing data there is in a given dataset, but also to identify potential patterns to the missing data, such as Missing Completely At Random (MCAR), Missing At Random (MAR) or Missing Not At Random (MNAR), and use machine learning algorithms to give a sensible suggestion to the imputation strategy that would make sense to be used in ceertain contexts.

## **List of Functions**

* <Function 1 Name Here>

  * This function describes the amount of missing data in the dataset and attempts to identify the type of missingness (MCAR, MAR or MNAR)

* suggest\_imputation

  * This function takes in the dataset and the type of missingness and passes those to a logistic regression algorithm which attempts to suggest an imputation strategy that would be best suited

## **Python Ecosystem**

Below is a summary of existing packages related to our topic:

**scikit-na** (https://pypi.org/project/scikit-na/)
This is a package that contains functions for statistical analysis, building visuals and export capabilities for helping data scientists understand and handle missing values in their datasets.

**mdatagen** (https://github.com/ArthurMangussi/pymdatagen)
This GitHub repo contains a project for artificially generating data for missing fields.

**Other Existing Packages** (e.g. deepchecks)
Other packages like deepchecks have functions that can be used to write tests to detect if the amount of missing data in a dataset passes a set threshold.