import pandas as pd
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, PolynomialFeatures
import numpy as np

def normalize_data(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize numerical columns in a DataFrame."""
    scaler = MinMaxScaler()
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    return df

def one_hot_encode(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Perform one-hot encoding on a specified column."""
    encoder = OneHotEncoder(sparse=False, drop='first')
    encoded = encoder.fit_transform(df[[column]])
    encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out([column]))
    return df.join(encoded_df).drop(column, axis=1)

def log_transform(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """Applies log transformation to selected columns."""
    for col in columns:
        df[col] = np.log1p(df[col])  # log(1 + x) to handle zeros
    return df

def create_polynomial_features(df: pd.DataFrame, degree: int) -> pd.DataFrame:
    """Generates polynomial features up to a specified degree."""
    poly = PolynomialFeatures(degree)
    poly_features = poly.fit_transform(df)
    return pd.DataFrame(poly_features, columns=poly.get_feature_names(df.columns))

def bin_data(df: pd.DataFrame, column: str, bins: int, labels=None) -> pd.DataFrame:
    """Bins data into discrete intervals."""
    df[column + '_binned'] = pd.cut(df[column], bins=bins, labels=labels)
    return df
