import pandas as pd
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from category_encoders import TargetEncoder, BinaryEncoder, HashingEncoder
import logging
import numpy as np

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def apply_onehot_encoding(df, cols):
    """
    Apply One-Hot Encoding to categorical columns.
    """
    logger.info(f"Applying One-Hot Encoding to columns: {cols}")
    encoder = OneHotEncoder(sparse=False, drop='first')  # Drop first to avoid multicollinearity
    transformed = encoder.fit_transform(df[cols])
    df_encoded = pd.DataFrame(transformed, columns=encoder.get_feature_names_out(cols))
    df = df.drop(cols, axis=1)
    df = pd.concat([df, df_encoded], axis=1)
    return df

def apply_label_encoding(df, cols):
    """
    Apply Label Encoding to categorical columns.
    """
    logger.info(f"Applying Label Encoding to columns: {cols}")
    for col in cols:
        encoder = LabelEncoder()
        df[col] = encoder.fit_transform(df[col])
    return df

def apply_target_encoding(df, cols, target_col):
    """
    Apply Target Encoding to categorical columns based on the target variable.
    """
    logger.info(f"Applying Target Encoding to columns: {cols} based on target: {target_col}")
    encoder = TargetEncoder(cols=cols)
    df[cols] = encoder.fit_transform(df[cols], df[target_col])
    return df

def apply_frequency_encoding(df, cols):
    """
    Apply Frequency Encoding to categorical columns by replacing categories with their frequency in the dataset.
    """
    logger.info(f"Applying Frequency Encoding to columns: {cols}")
    for col in cols:
        freq_encoding = df[col].value_counts() / len(df)
        df[col] = df[col].map(freq_encoding)
    return df

def apply_binary_encoding(df, cols):
    """
    Apply Binary Encoding to categorical columns.
    """
    logger.info(f"Applying Binary Encoding to columns: {cols}")
    encoder = BinaryEncoder(cols=cols)
    df = encoder.fit_transform(df)
    return df

def apply_hashing_encoding(df, cols, n_components=8):
    """
    Apply Hashing Encoding to categorical columns.
    """
    logger.info(f"Applying Hashing Encoding to columns: {cols} with {n_components} components.")
    encoder = HashingEncoder(cols=cols, n_components=n_components)
    df = encoder.fit_transform(df)
    return df

def apply_mean_encoding(df, cols, target_col):
    """
    Apply Mean Encoding to categorical columns by replacing categories with the mean of the target variable.
    """
    logger.info(f"Applying Mean Encoding to columns: {cols} based on target: {target_col}")
    for col in cols:
        mean_encoding = df.groupby(col)[target_col].mean()
        df[col] = df[col].map(mean_encoding)
    return df

def apply_woe_encoding(df, cols, target_col):
    """
    Apply Weight of Evidence (WOE) Encoding to categorical columns.
    
    WOE replaces categories with log(odds) based on the target variable.
    """
    logger.info(f"Applying WOE Encoding to columns: {cols} based on target: {target_col}")
    for col in cols:
        woe_encoding = {}
        for cat in df[col].unique():
            positive_rate = len(df[(df[col] == cat) & (df[target_col] == 1)])
            negative_rate = len(df[(df[col] == cat) & (df[target_col] == 0)])
            if positive_rate == 0:
                woe_encoding[cat] = 0
            else:
                woe = np.log((positive_rate + 1e-5) / (negative_rate + 1e-5))  # Avoid divide-by-zero
                woe_encoding[cat] = woe
        df[col] = df[col].map(woe_encoding)
    return df

def recommend_encoding_strategy(df, target_col=None):
    """
    Recommend encoding strategies based on the dataset's categorical columns.
    """
    recommendations = {}
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        unique_vals = df[col].nunique()
        if unique_vals <= 10:
            recommendations[col] = 'onehot'
            logger.info(f"Recommended One-Hot Encoding for '{col}' (few unique values).")
        elif unique_vals > 10 and unique_vals < 50:
            recommendations[col] = 'label'
            logger.info(f"Recommended Label Encoding for '{col}' (moderate number of unique values).")
        elif unique_vals >= 50 and target_col:
            recommendations[col] = 'target'
            logger.info(f"Recommended Target or Mean Encoding for '{col}' (high cardinality) based on target.")
        elif unique_vals >= 50 and not target_col:
            recommendations[col] = 'hashing'
            logger.info(f"Recommended Hashing Encoding for '{col}' (high cardinality).")
    
    return recommendations