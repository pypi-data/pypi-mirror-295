from .encoding import (apply_onehot_encoding, apply_label_encoding, apply_target_encoding,
                       apply_frequency_encoding, apply_binary_encoding, apply_hashing_encoding)
from .imputation import (impute_mean, impute_median, impute_mode, impute_knn, impute_iterative, impute_constant)
from .scaling import (apply_standard_scaling, apply_minmax_scaling, apply_robust_scaling, 
                      apply_maxabs_scaling, apply_quantile_transform, apply_power_transform)
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def apply_preprocessing(df, encoding_strategies=None, imputation_strategies=None, scaling_strategies=None):
    """
    Apply the specified preprocessing steps (encoding, imputation, scaling) to the dataset.
    
    Parameters:
    df : pd.DataFrame
        The dataset to be preprocessed.
    encoding_strategies : dict, optional
        A dictionary specifying the encoding strategies for each categorical column.
        Format: { 'column_name': 'encoding_type' }
    imputation_strategies : dict, optional
        A dictionary specifying the imputation strategies for each column with missing values.
        Format: { 'column_name': 'imputation_type' }
    scaling_strategies : dict, optional
        A dictionary specifying the scaling strategies for each numerical column.
        Format: { 'column_name': 'scaling_type' }
    
    Returns:
    pd.DataFrame
        The preprocessed DataFrame.
    """
    logger.info("Starting preprocessing steps...")
    
    # Apply Encoding Strategies
    if encoding_strategies:
        logger.info("Applying encoding strategies...")
        for col, strategy in encoding_strategies.items():
            if strategy == 'onehot':
                df = apply_onehot_encoding(df, [col])
            elif strategy == 'label':
                df = apply_label_encoding(df, [col])
            elif strategy == 'target':
                df = apply_target_encoding(df, [col], target_col='target')  # Adjust 'target' as needed
            elif strategy == 'frequency':
                df = apply_frequency_encoding(df, [col])
            elif strategy == 'binary':
                df = apply_binary_encoding(df, [col])
            elif strategy == 'hashing':
                df = apply_hashing_encoding(df, [col])
    
    # Apply Imputation Strategies
    if imputation_strategies:
        logger.info("Applying imputation strategies...")
        for col, strategy in imputation_strategies.items():
            if strategy == 'mean':
                df = impute_mean(df, [col])
            elif strategy == 'median':
                df = impute_median(df, [col])
            elif strategy == 'mode':
                df = impute_mode(df, [col])
            elif strategy == 'knn':
                df = impute_knn(df, [col])
            elif strategy == 'iterative':
                df = impute_iterative(df, [col])
            elif strategy == 'constant':
                df = impute_constant(df, [col], fill_value=-999)
    
    # Apply Scaling Strategies
    if scaling_strategies:
        logger.info("Applying scaling strategies...")
        for col, strategy in scaling_strategies.items():
            if strategy == 'standard':
                df = apply_standard_scaling(df, [col])
            elif strategy == 'minmax':
                df = apply_minmax_scaling(df, [col])
            elif strategy == 'robust':
                df = apply_robust_scaling(df, [col])
            elif strategy == 'maxabs':
                df = apply_maxabs_scaling(df, [col])
            elif strategy == 'quantile':
                df = apply_quantile_transform(df, [col])
            elif strategy == 'power':
                df = apply_power_transform(df, [col])
    
    logger.info("Finished preprocessing steps.")
    return df
