import pandas as pd

def target_encode(df: pd.DataFrame, column: str, target: str) -> pd.DataFrame:
    """Encodes a categorical column with the mean of the target variable."""
    target_mean = df.groupby(column)[target].mean()
    df[column + '_encoded'] = df[column].map(target_mean)
    return df
