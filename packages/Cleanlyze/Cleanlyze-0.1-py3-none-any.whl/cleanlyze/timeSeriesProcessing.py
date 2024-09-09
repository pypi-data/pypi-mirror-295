import pandas as pd

def rolling_statistics(df: pd.DataFrame, column: str, window: int) -> pd.DataFrame:
    """Calculates rolling mean and standard deviation for a time series."""
    df[column + '_rolling_mean'] = df[column].rolling(window=window).mean()
    df[column + '_rolling_std'] = df[column].rolling(window=window).std()
    return df

def add_lag_features(df: pd.DataFrame, column: str, lags: int) -> pd.DataFrame:
    """Adds lag features for a time series column."""
    for lag in range(1, lags + 1):
        df[column + f'_lag_{lag}'] = df[column].shift(lag)
    return df
