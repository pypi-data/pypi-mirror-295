import pandas as pd

def export_to_csv(df: pd.DataFrame, filename: str) -> None:
    """Exports DataFrame to CSV file."""
    df.to_csv(filename, index=False)

def export_to_excel(df: pd.DataFrame, filename: str) -> None:
    """Exports DataFrame to Excel file."""
    df.to_excel(filename, index=False)

def read_from_csv(filename: str) -> pd.DataFrame:
    """Reads data from a CSV file."""
    return pd.read_csv(filename)

def read_from_excel(filename: str) -> pd.DataFrame:
    """Reads data from an Excel file."""
    return pd.read_excel(filename)
