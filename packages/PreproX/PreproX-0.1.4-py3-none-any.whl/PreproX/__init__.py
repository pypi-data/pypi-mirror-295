# Import encoding functions
from .encoding import (
    apply_onehot_encoding,
    apply_label_encoding,
    apply_target_encoding,
    apply_frequency_encoding,
    apply_binary_encoding,
    apply_hashing_encoding
)

# Import imputation functions
from .imputation import (
    impute_mean,
    impute_median,
    impute_mode,
    impute_knn,
    impute_iterative,
    impute_constant
)

# Import scaling functions
from .scaling import (
    apply_standard_scaling,
    apply_minmax_scaling,
    apply_robust_scaling,
    apply_maxabs_scaling,
    apply_quantile_transform,
    apply_power_transform
)

# Import transformers
from .transformers import (
    apply_log_transformation,
    generate_polynomial_features,
    binning,
    apply_sqrt_transformation,
    apply_boxcox_transformation,
    target_encode,
    apply_inverse_transformation
)

# Import utility functions
from .utils import (
    check_missing_values,
    check_outliers,
    check_data_types,
    calculate_basic_statistics,
    format_column_names,
    detect_constant_columns,
    detect_duplicates,
    detect_highly_correlated_features,
    convert_categorical_to_category,
    normalize_numerical_data,
    count_unique_values
)

# Import logging functions
from .logging import (
    setup_logging,
    set_logging_level,
    log_to_file,
    disable_logging,
    log_custom_message,
    log_timed_event,
    log_memory_usage,
    log_dataframe_shape,
    enable_console_logging,
    disable_console_logging
)

# Import visualization functions
from .visualizations import (
    plot_histograms,
    plot_bar,
    plot_scatter,
    plot_correlation_heatmap,
    plot_boxplots,
    plot_pairplot,
    plot_pca,
    plot_tsne,
    plot_time_series,
    plot_combined_hist_kde,
    recommend_visualizations
)

# Import exceptions
from .exceptions import (
    PreprocessingError,
    MissingColumnError,
    InvalidEncodingStrategyError,
    InvalidImputationStrategyError,
    InvalidScalingStrategyError,
    DataTypeMismatchError,
    OutlierDetectionError,
    MissingValueImputationError,
    UnsupportedDataTypeError,
    InvalidFeatureSelectionError
)

# Import preprocessing function
from .preprocessing import apply_preprocessing
