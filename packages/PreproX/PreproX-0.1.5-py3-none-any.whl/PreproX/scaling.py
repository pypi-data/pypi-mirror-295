import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, MaxAbsScaler, QuantileTransformer, PowerTransformer
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def apply_standard_scaling(df, cols):
    """
    Apply Standard Scaling (zero mean, unit variance) to numerical columns.
    
    Parameters:
    df : pd.DataFrame
        The dataset.
    cols : list
        List of columns to scale.
    
    Returns:
    pd.DataFrame
        DataFrame with scaled columns.
    """
    logger.info(f"Applying Standard Scaling to columns: {cols}")
    scaler = StandardScaler()
    df[cols] = scaler.fit_transform(df[cols])
    return df

def apply_minmax_scaling(df, cols, feature_range=(0, 1)):
    """
    Apply Min-Max Scaling to numerical columns.
    
    Parameters:
    df : pd.DataFrame
        The dataset.
    cols : list
        List of columns to scale.
    feature_range : tuple, optional
        Desired range of transformed data (default is (0, 1)).
    
    Returns:
    pd.DataFrame
        DataFrame with scaled columns.
    """
    logger.info(f"Applying Min-Max Scaling to columns: {cols} with range {feature_range}")
    scaler = MinMaxScaler(feature_range=feature_range)
    df[cols] = scaler.fit_transform(df[cols])
    return df

def apply_robust_scaling(df, cols):
    """
    Apply Robust Scaling (based on median and IQR) to numerical columns, robust to outliers.
    
    Parameters:
    df : pd.DataFrame
        The dataset.
    cols : list
        List of columns to scale.
    
    Returns:
    pd.DataFrame
        DataFrame with scaled columns.
    """
    logger.info(f"Applying Robust Scaling to columns: {cols}")
    scaler = RobustScaler()
    df[cols] = scaler.fit_transform(df[cols])
    return df

def apply_maxabs_scaling(df, cols):
    """
    Apply MaxAbs Scaling (scales data by the maximum absolute value) to numerical columns.
    
    Parameters:
    df : pd.DataFrame
        The dataset.
    cols : list
        List of columns to scale.
    
    Returns:
    pd.DataFrame
        DataFrame with scaled columns.
    """
    logger.info(f"Applying MaxAbs Scaling to columns: {cols}")
    scaler = MaxAbsScaler()
    df[cols] = scaler.fit_transform(df[cols])
    return df

def apply_quantile_transform(df, cols, output_distribution='uniform'):
    """
    Apply Quantile Transformation to numerical columns to transform data to follow
    a uniform or normal distribution.
    
    Parameters:
    df : pd.DataFrame
        The dataset.
    cols : list
        List of columns to scale.
    output_distribution : str, optional
        Desired output distribution ('uniform' or 'normal'). Default is 'uniform'.
    
    Returns:
    pd.DataFrame
        DataFrame with transformed columns.
    """
    logger.info(f"Applying Quantile Transformation to columns: {cols} with output distribution '{output_distribution}'")
    scaler = QuantileTransformer(output_distribution=output_distribution)
    df[cols] = scaler.fit_transform(df[cols])
    return df

def apply_power_transform(df, cols, method='yeo-johnson'):
    """
    Apply Power Transformation to numerical columns to make data more Gaussian-like.
    Supports Box-Cox and Yeo-Johnson methods.
    
    Parameters:
    df : pd.DataFrame
        The dataset.
    cols : list
        List of columns to scale.
    method : str, optional
        The transformation method ('box-cox' or 'yeo-johnson'). Default is 'yeo-johnson'.
        Note: Box-Cox requires positive values.
    
    Returns:
    pd.DataFrame
        DataFrame with transformed columns.
    """
    logger.info(f"Applying Power Transformation ({method}) to columns: {cols}")
    scaler = PowerTransformer(method=method)
    df[cols] = scaler.fit_transform(df[cols])
    return df

def recommend_scaling_strategy(df):
    """
    Recommend scaling strategies based on the distribution and properties of the data.
    
    Parameters:
    df : pd.DataFrame
        The dataset.
    
    Returns:
    dict
        Dictionary with recommended scaling strategies for each numerical column.
    """
    recommendations = {}
    numeric_cols = df.select_dtypes(include=['float', 'int']).columns
    
    logger.info("Analyzing numerical data for scaling recommendations...")
    for col in numeric_cols:
        col_range = df[col].max() - df[col].min()
        col_skewness = df[col].skew()

        # Recommend based on the range and skewness of the data
        if col_range > 1000:
            recommendations[col] = 'minmax'
            logger.info(f"Recommended Min-Max Scaling for '{col}' (large range).")
        elif abs(col_skewness) > 1:
            recommendations[col] = 'robust'
            logger.info(f"Recommended Robust Scaling for '{col}' (high skewness).")
        else:
            recommendations[col] = 'standard'
            logger.info(f"Recommended Standard Scaling for '{col}' (normal range, low skewness).")
    
    return recommendations
