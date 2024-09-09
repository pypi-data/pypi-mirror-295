def group_and_aggregate(df: pd.DataFrame, group_col: str, agg_col: str, agg_func='mean') -> pd.DataFrame:
    """Groups data by a column and applies an aggregation function."""
    return df.groupby(group_col)[agg_col].agg(agg_func).reset_index()
