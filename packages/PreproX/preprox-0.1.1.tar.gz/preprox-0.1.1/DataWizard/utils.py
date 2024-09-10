import pandas as pd
import numpy as np
from sklearn.preprocessing import Normalizer
from sklearn.model_selection import train_test_split
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_missing_values(df):
    """
    Check for missing values in the dataset and return a summary.
    """
    logger.info("Checking for missing values in the dataset.")
    missing_count = df.isnull().sum()
    missing_percentage = (missing_count / len(df)) * 100
    missing_data = pd.DataFrame({"Missing Values": missing_count, "Percentage": missing_percentage})
    missing_data = missing_data[missing_data["Missing Values"] > 0]
    return missing_data

def check_outliers(df, cols=None, method='iqr'):
    """
    Detect outliers in numerical columns using the Interquartile Range (IQR) or Z-score method.
    """
    logger.info(f"Detecting outliers using {method} method.")
    outliers = {}
    
    if cols is None:
        cols = df.select_dtypes(include=[np.number]).columns
    
    for col in cols:
        if method == 'iqr':
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers[col] = df[(df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))]
        elif method == 'zscore':
            mean_col = df[col].mean()
            std_col = df[col].std()
            z_scores = (df[col] - mean_col) / std_col
            outliers[col] = df[np.abs(z_scores) > 3]
    
    return outliers

def check_data_types(df):
    """
    Check the data types of each column in the dataset and return a summary.
    """
    logger.info("Checking data types of the dataset columns.")
    return df.dtypes

def calculate_basic_statistics(df, cols=None):
    """
    Calculate basic statistics for numerical columns such as mean, median, variance, and standard deviation.
    """
    logger.info("Calculating basic statistics for numerical columns.")
    if cols is None:
        cols = df.select_dtypes(include=[np.number]).columns
    
    stats = {
        'mean': df[cols].mean(),
        'median': df[cols].median(),
        'variance': df[cols].var(),
        'std_dev': df[cols].std()
    }
    
    return pd.DataFrame(stats)

def format_column_names(df):
    """
    Format column names by removing leading/trailing spaces, converting to lowercase, and replacing spaces with underscores.
    """
    logger.info("Formatting column names to be consistent.")
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    return df

def detect_constant_columns(df):
    """
    Detect columns that have constant values across all rows.
    
    Returns:
    list
        List of columns that contain constant values.
    """
    logger.info("Detecting constant columns in the dataset.")
    constant_columns = [col for col in df.columns if df[col].nunique() == 1]
    return constant_columns

def detect_duplicates(df):
    """
    Detect duplicate rows in the dataset.
    
    Returns:
    pd.DataFrame
        DataFrame with duplicate rows.
    """
    logger.info("Detecting duplicate rows in the dataset.")
    duplicates = df[df.duplicated()]
    return duplicates

def detect_highly_correlated_features(df, threshold=0.9):
    """
    Detect pairs of features that are highly correlated with each other.
    
    Parameters:
    df : pd.DataFrame
        The dataset.
    threshold : float, optional
        Correlation threshold to detect highly correlated features (default is 0.9).
    
    Returns:
    list of tuple
        List of pairs of features that are highly correlated.
    """
    logger.info(f"Detecting highly correlated features with correlation greater than {threshold}.")
    corr_matrix = df.corr().abs()
    upper_triangle = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    
    highly_correlated_pairs = [
        (col1, col2) for col1 in upper_triangle.columns for col2 in upper_triangle.columns 
        if upper_triangle.loc[col1, col2] > threshold
    ]
    
    return highly_correlated_pairs

def convert_categorical_to_category(df):
    """
    Convert object-type columns to the category data type to optimize memory usage.
    
    Returns:
    pd.DataFrame
        DataFrame with object columns converted to category data type.
    """
    logger.info("Converting object columns to category data type for memory optimization.")
    categorical_cols = df.select_dtypes(include=['object']).columns
    df[categorical_cols] = df[categorical_cols].astype('category')
    return df

def normalize_numerical_data(df, cols=None, norm='l2'):
    """
    Normalize numerical data using L1 or L2 normalization.
    
    Parameters:
    df : pd.DataFrame
        The dataset.
    cols : list, optional
        List of columns to normalize. If None, all numerical columns are normalized.
    norm : str, optional
        The normalization technique to use ('l1' or 'l2'). Default is 'l2'.
    
    Returns:
    pd.DataFrame
        DataFrame with normalized numerical columns.
    """
    logger.info(f"Normalizing numerical data using {norm} normalization.")
    if cols is None:
        cols = df.select_dtypes(include=[np.number]).columns
    
    normalizer = Normalizer(norm=norm)
    df[cols] = normalizer.fit_transform(df[cols])
    return df


def count_unique_values(df):
    """
    Count unique values in each column of the dataset.
    
    Returns:
    pd.Series
        Series with the count of unique values for each column.
    """
    logger.info("Counting unique values in each column of the dataset.")
    return df.nunique()
