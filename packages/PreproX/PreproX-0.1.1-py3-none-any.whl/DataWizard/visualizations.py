import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def recommend_visualizations(df):
    """
    Recommend visualizations based on the dataset.
    
    Parameters:
    df : pd.DataFrame
        The dataset.
    
    Returns:
    dict
        Dictionary of recommended visualizations for the dataset.
    """
    recommendations = {}
    numeric_cols = df.select_dtypes(include=[float, int]).columns
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    
    # Check for categorical columns
    if len(categorical_cols) > 0:
        recommendations['categorical'] = ['Bar Plot', 'Class Balance Plot']
    
    # Check for numerical columns
    if len(numeric_cols) > 0:
        recommendations['numerical'] = ['Histograms', 'Box Plots', 'Scatter Plots', 'Correlation Heatmap']
    
    # Check for high-dimensional data
    if len(numeric_cols) > 3:
        recommendations['dimensionality_reduction'] = ['PCA Plot', 't-SNE Plot']
    
    # Check for time-series data (assuming time-like columns are detected)
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            recommendations['time_series'] = ['Time-Series Plot']
            break

    logger.info("Generated visualization recommendations.")
    return recommendations

def plot_histograms(df, cols=None, bins=20):
    """
    Plot histograms for numerical columns.
    
    Parameters:
    df : pd.DataFrame
        The dataset.
    cols : list, optional
        List of columns to plot. If None, all numerical columns will be plotted.
    bins : int, optional
        Number of bins for the histogram (default is 20).
    
    Returns:
    None
    """
    logger.info("Plotting histograms for numerical columns.")
    if cols is None:
        cols = df.select_dtypes(include=[float, int]).columns
    
    df[cols].hist(bins=bins, figsize=(12, 10), color='skyblue', edgecolor='black')
    plt.suptitle('Histograms of Numerical Features', fontsize=16)
    plt.show()

def plot_bar(df, cols):
    """
    Plot bar plots for categorical columns.
    
    Parameters:
    df : pd.DataFrame
        The dataset.
    cols : list
        List of categorical columns to plot.
    
    Returns:
    None
    """
    logger.info("Plotting bar plots for categorical columns.")
    for col in cols:
        plt.figure(figsize=(8, 5))
        sns.countplot(y=col, data=df, palette='viridis')
        plt.title(f'Distribution of {col}')
        plt.show()

def plot_correlation_heatmap(df):
    """
    Plot a correlation heatmap for numerical columns.
    
    Parameters:
    df : pd.DataFrame
        The dataset.
    
    Returns:
    None
    """
    logger.info("Plotting correlation heatmap for numerical columns.")
    numeric_cols = df.select_dtypes(include=[float, int]).columns
    if len(numeric_cols) > 1:
        corr_matrix = df[numeric_cols].corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
        plt.title('Correlation Heatmap of Numerical Features')
        plt.show()

def plot_pca(df, cols=None, n_components=2):
    """
    Plot a PCA projection of the data for dimensionality reduction and visualization.
    
    Parameters:
    df : pd.DataFrame
        The dataset.
    cols : list, optional
        List of numerical columns to include in PCA. If None, all numerical columns are used.
    n_components : int, optional
        The number of components for PCA (default is 2).
    
    Returns:
    None
    """
    logger.info(f"Plotting PCA with {n_components} components.")
    if cols is None:
        cols = df.select_dtypes(include=[float, int]).columns
    
    pca = PCA(n_components=n_components)
    pca_result = pca.fit_transform(df[cols])
    
    if n_components == 2:
        plt.figure(figsize=(8, 6))
        plt.scatter(pca_result[:, 0], pca_result[:, 1], alpha=0.7)
        plt.title('2D PCA Plot')
        plt.xlabel('PC1')
        plt.ylabel('PC2')
    elif n_components == 3:
        from mpl_toolkits.mplot3d import Axes3D
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(pca_result[:, 0], pca_result[:, 1], pca_result[:, 2], alpha=0.7)
        ax.set_title('3D PCA Plot')
        ax.set_xlabel('PC1')
        ax.set_ylabel('PC2')
        ax.set_zlabel('PC3')
    
    plt.show()

def plot_tsne(df, cols=None, n_components=2, perplexity=30, n_iter=1000):
    """
    Plot a t-SNE projection of the data for complex data visualization.
    
    Parameters:
    df : pd.DataFrame
        The dataset.
    cols : list, optional
        List of numerical columns to include in t-SNE. If None, all numerical columns are used.
    n_components : int, optional
        The number of dimensions for t-SNE (default is 2).
    perplexity : int, optional
        The perplexity for t-SNE (default is 30).
    n_iter : int, optional
        The number of iterations for optimization (default is 1000).
    
    Returns:
    None
    """
    logger.info(f"Plotting t-SNE with {n_components} components.")
    if cols is None:
        cols = df.select_dtypes(include=[float, int]).columns
    
    tsne = TSNE(n_components=n_components, perplexity=perplexity, n_iter=n_iter)
    tsne_result = tsne.fit_transform(df[cols])
    
    if n_components == 2:
        plt.figure(figsize=(8, 6))
        plt.scatter(tsne_result[:, 0], tsne_result[:, 1], alpha=0.7)
        plt.title('2D t-SNE Plot')
        plt.xlabel('t-SNE1')
        plt.ylabel('t-SNE2')
        plt.show()

def plot_time_series(df, time_col, value_col, title="Time Series Plot"):
    """
    Plot a time series for the given value column.
    
    Parameters:
    df : pd.DataFrame
        The dataset.
    time_col : str
        The column representing time.
    value_col : str
        The column representing the value to plot over time.
    title : str, optional
        Title of the plot (default is 'Time Series Plot').
    
    Returns:
    None
    """
    logger.info(f"Plotting time series for '{value_col}' over '{time_col}'.")
    plt.figure(figsize=(10, 6))
    plt.plot(df[time_col], df[value_col], marker='o')
    plt.title(title)
    plt.xlabel(time_col)
    plt.ylabel(value_col)
    plt.grid(True)
    plt.show()

def plot_combined_hist_kde(df, col):
    """
    Plot a combined histogram and KDE plot for a numerical column.
    
    Parameters:
    df : pd.DataFrame
        The dataset.
    col : str
        The name of the column to plot.
    
    Returns:
    None
    """
    logger.info(f"Plotting combined histogram and KDE plot for column: {col}")
    plt.figure(figsize=(8, 6))
    sns.histplot(df[col], kde=True, color='blue')
    plt.title(f'Histogram and KDE Plot for {col}')
    plt.show()
