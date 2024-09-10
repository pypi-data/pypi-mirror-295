import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def apply_log_transformation(df, cols):
    """
    Apply logarithmic transformation to numerical columns.
    
    Parameters:
    df : pd.DataFrame
        The dataset.
    cols : list
        List of columns to apply the log transformation to.
    
    Returns:
    pd.DataFrame
        DataFrame with log-transformed columns.
    """
    logger.info(f"Applying log transformation to columns: {cols}")
    df[cols] = df[cols].apply(lambda x: np.log1p(x))  # log1p avoids log(0) by applying log(1 + x)
    return df

def generate_polynomial_features(df, cols, degree=2, interaction_only=False):
    """
    Generate polynomial and interaction features for the given numerical columns.
    
    Parameters:
    df : pd.DataFrame
        The dataset.
    cols : list
        List of numerical columns to generate polynomial features from.
    degree : int, optional
        The degree of the polynomial features (default is 2).
    interaction_only : bool, optional
        Whether to generate only interaction features (default is False).
    
    Returns:
    pd.DataFrame
        DataFrame containing the original and polynomial features.
    """
    logger.info(f"Generating polynomial features for columns: {cols} with degree={degree}")
    poly = PolynomialFeatures(degree=degree, interaction_only=interaction_only, include_bias=False)
    poly_features = poly.fit_transform(df[cols])
    poly_feature_names = poly.get_feature_names_out(cols)
    
    poly_df = pd.DataFrame(poly_features, columns=poly_feature_names, index=df.index)
    df = pd.concat([df, poly_df], axis=1)
    
    return df

def binning(df, col, bins, labels=None):
    """
    Perform binning on a numerical column (discretization).
    
    Parameters:
    df : pd.DataFrame
        The dataset.
    col : str
        The name of the column to bin.
    bins : int or list-like
        The number of bins or bin edges.
    labels : list, optional
        The labels for the bins.
    
    Returns:
    pd.DataFrame
        DataFrame with the binned column.
    """
    logger.info(f"Performing binning on column: {col}")
    df[f'{col}_binned'] = pd.cut(df[col], bins=bins, labels=labels)
    return df

def apply_sqrt_transformation(df, cols):
    """
    Apply square root transformation to numerical columns.
    
    Parameters:
    df : pd.DataFrame
        The dataset.
    cols : list
        List of columns to apply the square root transformation to.
    
    Returns:
    pd.DataFrame
        DataFrame with square root transformed columns.
    """
    logger.info(f"Applying square root transformation to columns: {cols}")
    df[cols] = df[cols].apply(lambda x: np.sqrt(x))
    return df

def apply_boxcox_transformation(df, cols):
    """
    Apply Box-Cox transformation to numerical columns (requires positive values).
    
    Parameters:
    df : pd.DataFrame
        The dataset.
    cols : list
        List of columns to apply the Box-Cox transformation to.
    
    Returns:
    pd.DataFrame
        DataFrame with Box-Cox transformed columns.
    """
    from scipy import stats
    
    logger.info(f"Applying Box-Cox transformation to columns: {cols}")
    for col in cols:
        # Ensure all values are positive for Box-Cox
        if (df[col] <= 0).any():
            raise ValueError(f"Column '{col}' contains non-positive values, cannot apply Box-Cox transformation.")
        
        df[col], _ = stats.boxcox(df[col])
    
    return df

def target_encode(df, col, target_col):
    """
    Apply target encoding to a categorical column based on the mean of the target variable.
    
    Parameters:
    df : pd.DataFrame
        The dataset.
    col : str
        The name of the categorical column to target encode.
    target_col : str
        The target column for calculating the mean encoding.
    
    Returns:
    pd.DataFrame
        DataFrame with the target-encoded column.
    """
    logger.info(f"Applying target encoding to column: {col} based on target column: {target_col}")
    mean_encoding = df.groupby(col)[target_col].mean()
    df[f'{col}_target_encoded'] = df[col].map(mean_encoding)
    
    return df

def apply_inverse_transformation(df, cols):
    """
    Apply inverse transformation (1/x) to numerical columns.
    
    Parameters:
    df : pd.DataFrame
        The dataset.
    cols : list
        List of columns to apply the inverse transformation to.
    
    Returns:
    pd.DataFrame
        DataFrame with inverse transformed columns.
    """
    logger.info(f"Applying inverse transformation to columns: {cols}")
    df[cols] = df[cols].apply(lambda x: 1 / x)
    return df
