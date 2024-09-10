## **PreproX**  
_A Python library for comprehensive data preprocessing with recommendations._

### **Overview**

PreproX is a Python library that automates the process of data preprocessing. It offers suggestions for handling common preprocessing tasks like encoding categorical variables, imputing missing values, outlier detection, scaling, and more. PreproX is designed to help users streamline the preprocessing stage of machine learning pipelines with minimal manual intervention, while still allowing for customization and control.

---

### **Key Features**

- **Automatic Encoding Recommendations**: Suggests the best encoding methods (e.g., OneHotEncoding, LabelEncoding, Target Encoding, etc.) based on the characteristics of categorical data.
- **Imputation of Missing Values**: Automatically detects missing data and suggests appropriate imputation strategies such as mean, median, or mode imputation.
- **Outlier Detection**: Identifies outliers using both the Z-score and IQR (Interquartile Range) methods.
- **Scaling & Normalization**: Recommends scaling techniques such as MinMaxScaler, StandardScaler, or RobustScaler based on the dataset’s characteristics.
- **Visualization Utilities**: Offers multiple ways to visualize data, such as histograms, box plots, scatter plots, correlation matrices, and more.
- **Logging**: Tracks and logs the preprocessing steps taken for transparency and reproducibility.

---

### **Installation**

You can install **PreproX** via pip:

```bash
pip install preprox
```

---

### **Usage**

Here’s a step-by-step guide on how to use PreproX:

#### **1. Basic Preprocessing Recommendations**

You can start by loading your dataset and letting PreproX suggest preprocessing strategies.

```python
import PreproX as preprox
import pandas as pd

# Load your dataset
df = pd.read_csv('your_dataset.csv')

# Get preprocessing recommendations
recommendations = preprox.recommend_preprocessing(df)

# Print the recommendations
print(recommendations)
```

#### **2. Visualizing Your Data**

PreproX also provides a variety of visualization options to better understand your data.

```python
# Visualize your dataset
preprox.visualize_data(df)
```

Supported visualizations include:
- Histograms
- Bar plots for categorical columns
- Box plots for outliers
- Pair plots for relationships between columns
- Correlation heatmaps
- Violin plots
- Scatter plots

#### **3. Applying Preprocessing**

After getting recommendations, you can automatically apply the suggested preprocessing steps.

```python
# Apply recommended preprocessing
df_preprocessed = preprox.apply_preprocessing(df, recommendations)

# Preview the processed data
print(df_preprocessed.head())
```

This will apply encoding, imputation, scaling, and other recommendations as per the analysis of your dataset.

#### **4. Categorical Data Handling**

PreproX helps in handling categorical data with a variety of encoding strategies. For example:

```python
# Encoding recommendations and application
encoding_recommendations = preprox.recommend_encoding_strategy(df, target_col='target')
df_encoded = preprox.apply_encoding(df, encoding_recommendations)

# Check the encoded data
print(df_encoded.head())
```

Available encoding strategies include:
- **OneHotEncoding**
- **LabelEncoding**
- **TargetEncoding**
- **BinaryEncoding**
- **HashingEncoding**

#### **5. Handling Missing Data**

PreproX can suggest the best methods to handle missing data based on the column type:

```python
# Handle missing values
df_imputed = preprox.impute_missing_values(df)
```

Common imputation strategies include:
- **Mean Imputation**
- **Median Imputation**
- **Mode Imputation**
- **K-Nearest Neighbors Imputation (for advanced cases)**

#### **6. Outlier Detection and Handling**

PreproX offers outlier detection using methods like IQR and Z-score.

```python
# Detect outliers using IQR method
outliers = preprox.detect_outliers(df, method='iqr')

# Handle outliers based on recommendations
df_cleaned = preprox.handle_outliers(df, outliers)
```

---

### **Advanced Customization**

Although PreproX automates much of the preprocessing, it also allows advanced users to customize steps as needed. You can fine-tune how different strategies are applied to various columns of your dataset.

For example, you can customize scaling methods:

```python
scaling_strategies = {
    'numerical_column1': 'standard',
    'numerical_column2': 'minmax'
}

df_scaled = preprox.apply_scaling(df, scaling_strategies)
```

---

### **Modules Overview**

1. **Encoding**:
   - Handles automatic encoding of categorical variables.
   - Supports OneHot, Label, Target, Binary, and Hashing encoding.

2. **Imputation**:
   - Detects missing data and applies imputation strategies based on the data type.
   - Suggests appropriate imputation based on numerical vs categorical columns.

3. **Outlier Detection**:
   - Identifies outliers using methods such as Z-score and IQR.
   - Provides recommendations for how to handle outliers (e.g., removal or transformation).

4. **Scaling**:
   - Suggests appropriate scaling methods such as MinMaxScaler, StandardScaler, RobustScaler, and more.

5. **Visualization**:
   - A variety of visualization techniques to explore the dataset.

6. **Logging**:
   - Logs preprocessing steps taken on the dataset to ensure reproducibility.

---

### **FAQ**

#### **Q1: Can I customize the preprocessing steps?**
Yes, while PreproX provides automated suggestions, you can override any recommendation and specify your preferred encoding, imputation, or scaling strategy.

#### **Q2: Does PreproX handle large datasets efficiently?**
PreproX is designed to work efficiently with small and moderately large datasets. However, for extremely large datasets, it is recommended to optimize memory usage using specialized tools or preprocessing steps outside the scope of PreproX.

#### **Q3: Can I use PreproX for real-time data?**
PreproX is primarily intended for preprocessing static datasets. Real-time data processing would require additional tools and architecture outside of this library’s scope.

---

### **Contributing**

Contributions are welcome! If you'd like to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push the branch and open a pull request.

---

### **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### **Contact**

For any questions, feel free to open an issue on GitHub or contact me at **your.email@example.com**.
