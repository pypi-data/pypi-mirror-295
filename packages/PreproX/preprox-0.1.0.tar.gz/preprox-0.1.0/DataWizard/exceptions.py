class PreprocessingError(Exception):
    """
    Base class for exceptions in the preprocessing library.
    """
    def __init__(self, message="An error occurred during preprocessing."):
        self.message = message
        super().__init__(self.message)


class MissingColumnError(PreprocessingError):
    """
    Exception raised when a required column is missing from the dataset.
    """
    def __init__(self, column_name):
        self.message = f"The required column '{column_name}' is missing from the dataset."
        super().__init__(self.message)


class InvalidEncodingStrategyError(PreprocessingError):
    """
    Exception raised when an invalid encoding strategy is provided.
    """
    def __init__(self, strategy):
        self.message = f"The encoding strategy '{strategy}' is invalid or not supported."
        super().__init__(self.message)


class InvalidImputationStrategyError(PreprocessingError):
    """
    Exception raised when an invalid imputation strategy is provided.
    """
    def __init__(self, strategy):
        self.message = f"The imputation strategy '{strategy}' is invalid or not supported."
        super().__init__(self.message)


class InvalidScalingStrategyError(PreprocessingError):
    """
    Exception raised when an invalid scaling strategy is provided.
    """
    def __init__(self, strategy):
        self.message = f"The scaling strategy '{strategy}' is invalid or not supported."
        super().__init__(self.message)


class DataTypeMismatchError(PreprocessingError):
    """
    Exception raised when there is a mismatch between expected and actual data types.
    """
    def __init__(self, expected_type, actual_type, column_name):
        self.message = f"Expected data type '{expected_type}' for column '{column_name}', but got '{actual_type}'."
        super().__init__(self.message)


class OutlierDetectionError(PreprocessingError):
    """
    Exception raised during the outlier detection process.
    """
    def __init__(self, column_name):
        self.message = f"An error occurred while detecting outliers in column '{column_name}'."
        super().__init__(self.message)


class MissingValueImputationError(PreprocessingError):
    """
    Exception raised when there is an error during missing value imputation.
    """
    def __init__(self, column_name):
        self.message = f"An error occurred during missing value imputation in column '{column_name}'."
        super().__init__(self.message)


class UnsupportedDataTypeError(PreprocessingError):
    """
    Exception raised when an unsupported data type is encountered.
    """
    def __init__(self, data_type):
        self.message = f"Data type '{data_type}' is unsupported for the current operation."
        super().__init__(self.message)


class InvalidFeatureSelectionError(PreprocessingError):
    """
    Exception raised when invalid or unsupported feature selection criteria are provided.
    """
    def __init__(self, criteria):
        self.message = f"The feature selection criteria '{criteria}' is invalid or unsupported."
        super().__init__(self.message)
