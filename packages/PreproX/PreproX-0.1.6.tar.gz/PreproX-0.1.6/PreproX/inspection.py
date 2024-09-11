import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import skew

def inspect_data(df, target_col=None):
    """
    Inspect the dataset and provide comprehensive insights such as data types, missing values,
    outliers, skewness, correlations, class balance, and more.
    
    Parameters:
    df : pd.DataFrame
        The dataset to inspect.
    target_col : str, optional
        The target column for classification tasks. If provided, class balance will be checked.
    
    Returns:
    None
    """
    print("======== Dataset Inspection ========")
    
    # 1. Basic Information
    print("\n1. Dataset Shape:")
    print(f"The dataset contains {df.shape[0]} rows and {df.shape[1]} columns.")
    
    print("\n2. Column Data Types and Basic Stats:")
    print(df.dtypes)
    print("\nBasic Statistics:")
    print(df.describe())

    # 2. Missing Values
    print("\n3. Missing Values:")
    missing_values = df.isnull().sum()
    missing_percentage = (df.isnull().sum() / df.shape[0]) * 100
    missing_data = pd.DataFrame({"Missing Values": missing_values, "Percentage": missing_percentage})
    missing_data = missing_data[missing_data["Missing Values"] > 0]
    
    if missing_data.empty:
        print("No missing values detected.")
    else:
        print(missing_data)
        
        # Missing value heatmap
        plt.figure(figsize=(10, 6))
        sns.heatmap(df.isnull(), cbar=False, cmap='viridis')
        plt.title('Missing Value Heatmap')
        plt.show()

    # 3. Duplicates
    print("\n4. Duplicate Rows:")
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        print(f"Warning: {duplicates} duplicate rows found!")
    else:
        print("No duplicate rows detected.")
    
    # 4. Outlier Detection (using IQR)
    print("\n5. Outlier Detection (IQR Method):")
    for col in df.select_dtypes(include=[np.number]):
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = df[(df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))]
        if not outliers.empty:
            print(f"Outliers detected in '{col}'.")
        else:
            print(f"No significant outliers detected in '{col}'.")
    
    # 5. Skewness
    print("\n6. Skewness of Numerical Columns:")
    skewness_values = df.select_dtypes(include=[np.number]).apply(lambda x: skew(x.dropna()))
    skewed_columns = skewness_values[abs(skewness_values) > 1]
    if skewed_columns.empty:
        print("No highly skewed columns detected.")
    else:
        print(f"Highly skewed columns (|skewness| > 1):\n{skewed_columns}")
    
    # 6. Variance and Standard Deviation
    print("\n7. Variance and Standard Deviation of Numerical Columns:")
    variance = df.select_dtypes(include=[np.number]).var()
    std_dev = df.select_dtypes(include=[np.number]).std()
    print(f"Variance:\n{variance}")
    print(f"Standard Deviation:\n{std_dev}")

    # 7. High Cardinality Columns
    print("\n8. High Cardinality Categorical Columns (more than 50 unique values):")
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        unique_vals = df[col].nunique()
        if unique_vals > 50:
            print(f"Column '{col}' has {unique_vals} unique values. Consider handling high cardinality.")

    # 8. Correlation Matrix for Numerical Columns
    print("\n9. Correlation Matrix:")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 1:
        corr_matrix = df[numeric_cols].corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
        plt.title('Correlation Matrix for Numerical Columns')
        plt.show()
    else:
        print("Not enough numerical columns for a correlation matrix.")
    
    # 9. Class Balance Check (for classification tasks)
    if target_col and df[target_col].dtype == 'object':
        print("\n10. Class Balance Check:")
        class_counts = df[target_col].value_counts()
        class_percentage = df[target_col].value_counts(normalize=True) * 100
        print(f"Class distribution for target column '{target_col}':\n{class_counts}")
        plt.figure(figsize=(8, 5))
        sns.barplot(x=class_counts.index, y=class_counts.values, palette='coolwarm')
        plt.title(f'Class Balance for {target_col}')
        plt.show()
    
    print("\n======== End of Inspection ========")

