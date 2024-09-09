import pandas as pd

def data_summary(df: pd.DataFrame) -> None:
    """Prints a summary of the data including null values and data types."""
    print(f"Data Types:\n{df.dtypes}\n")
    print(f"Missing Values:\n{df.isnull().sum()}\n")
    print(f"Basic Statistics:\n{df.describe()}\n")
