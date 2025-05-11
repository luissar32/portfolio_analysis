import pandas as pd

def format_data(df):
    """Ensure DataFrame is in correct format for analysis."""
    df.index = pd.to_datetime(df.index)
    return df.dropna()