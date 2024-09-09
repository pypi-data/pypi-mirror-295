import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def plot_correlation_matrix(df: pd.DataFrame) -> None:
    """Plots the correlation matrix using a heatmap."""
    corr = df.corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
    plt.show()

def plot_histograms(df: pd.DataFrame, columns: list) -> None:
    """Plots histograms for selected columns."""
    df[columns].hist(bins=20, figsize=(10, 8))
    plt.show()
