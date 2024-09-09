import pandas as pd

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate rows from a DataFrame."""
    return df.drop_duplicates()

def fill_missing_values(df: pd.DataFrame, value: str = '') -> pd.DataFrame:
    """Fill missing values in a DataFrame with a specified value."""
    return df.fillna(value)

def handle_outliers(df: pd.DataFrame, method='remove', threshold=1.5) -> pd.DataFrame:
    """Removes or caps outliers based on IQR method or Z-score."""
    if method == 'remove':
        Q1 = df.quantile(0.25)
        Q3 = df.quantile(0.75)
        IQR = Q3 - Q1
        df_cleaned = df[~((df < (Q1 - threshold * IQR)) | (df > (Q3 + threshold * IQR))).any(axis=1)]
    elif method == 'cap':
        # Cap outliers
        df_cleaned = df.clip(lower=df.quantile(0.01), upper=df.quantile(0.99), axis=1)
    return df_cleaned

def impute_missing_values(df: pd.DataFrame, strategy='mean') -> pd.DataFrame:
    """Imputes missing values using 'mean', 'median', or 'mode'."""
    if strategy == 'mean':
        return df.fillna(df.mean())
    elif strategy == 'median':
        return df.fillna(df.median())
    elif strategy == 'mode':
        return df.fillna(df.mode().iloc[0])
