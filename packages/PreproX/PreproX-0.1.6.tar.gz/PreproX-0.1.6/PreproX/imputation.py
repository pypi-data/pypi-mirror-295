import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def impute_mean(df, cols):
    """
    Impute missing values with the mean of each column.
    
    Parameters:
    df : pd.DataFrame
        The dataset.
    cols : list
        List of columns to impute.
    
    Returns:
    pd.DataFrame
        DataFrame with imputed values.
    """
    logger.info(f"Imputing mean for columns: {cols}")
    imputer = SimpleImputer(strategy='mean')
    df[cols] = imputer.fit_transform(df[cols])
    return df

def impute_median(df, cols):
    """
    Impute missing values with the median of each column.
    
    Parameters:
    df : pd.DataFrame
        The dataset.
    cols : list
        List of columns to impute.
    
    Returns:
    pd.DataFrame
        DataFrame with imputed values.
    """
    logger.info(f"Imputing median for columns: {cols}")
    imputer = SimpleImputer(strategy='median')
    df[cols] = imputer.fit_transform(df[cols])
    return df

def impute_mode(df, cols):
    """
    Impute missing values with the most frequent value (mode) of each column.
    
    Parameters:
    df : pd.DataFrame
        The dataset.
    cols : list
        List of columns to impute.
    
    Returns:
    pd.DataFrame
        DataFrame with imputed values.
    """
    logger.info(f"Imputing mode for columns: {cols}")
    imputer = SimpleImputer(strategy='most_frequent')
    df[cols] = imputer.fit_transform(df[cols])
    return df

def impute_knn(df, cols, n_neighbors=5):
    """
    Impute missing values using K-Nearest Neighbors (KNN) imputation.
    
    Parameters:
    df : pd.DataFrame
        The dataset.
    cols : list
        List of columns to impute.
    n_neighbors : int, optional
        Number of neighbors to use for KNN imputation.
    
    Returns:
    pd.DataFrame
        DataFrame with imputed values.
    """
    logger.info(f"Imputing using KNN for columns: {cols} with {n_neighbors} neighbors.")
    imputer = KNNImputer(n_neighbors=n_neighbors)
    df[cols] = imputer.fit_transform(df[cols])
    return df

def impute_iterative(df, cols):
    """
    Impute missing values using Iterative Imputation.
    
    Parameters:
    df : pd.DataFrame
        The dataset.
    cols : list
        List of columns to impute.
    
    Returns:
    pd.DataFrame
        DataFrame with imputed values.
    """
    logger.info(f"Imputing iteratively for columns: {cols}")
    imputer = IterativeImputer()
    df[cols] = imputer.fit_transform(df[cols])
    return df

def impute_constant(df, cols, fill_value=-999):
    """
    Impute missing values with a constant value.
    
    Parameters:
    df : pd.DataFrame
        The dataset.
    cols : list
        List of columns to impute.
    fill_value : int/float, optional
        The constant value to use for imputation (default: -999).
    
    Returns:
    pd.DataFrame
        DataFrame with imputed values.
    """
    logger.info(f"Imputing constant value {fill_value} for columns: {cols}")
    imputer = SimpleImputer(strategy='constant', fill_value=fill_value)
    df[cols] = imputer.fit_transform(df[cols])
    return df

def recommend_imputation_strategy(df):
    """
    Recommend imputation strategies based on the missing data in the dataset.
    
    Parameters:
    df : pd.DataFrame
        The dataset.
    
    Returns:
    dict
        Dictionary with recommended imputation strategies for each column.
    """
    recommendations = {}
    missing_data = df.isnull().sum()
    missing_percentage = (df.isnull().sum() / df.shape[0]) * 100
    
    logger.info("Analyzing missing data for imputation recommendations...")
    for col in df.columns:
        missing_pct = missing_percentage[col]
        if missing_pct == 0:
            continue
        elif missing_pct < 5:
            recommendations[col] = 'mean'
            logger.info(f"Recommended Mean Imputation for '{col}' (missing: {missing_pct:.2f}%).")
        elif 5 <= missing_pct < 20:
            recommendations[col] = 'median'
            logger.info(f"Recommended Median Imputation for '{col}' (missing: {missing_pct:.2f}%).")
        elif missing_pct >= 20:
            recommendations[col] = 'knn'
            logger.info(f"Recommended KNN Imputation for '{col}' (missing: {missing_pct:.2f}%).")
    
    return recommendations
