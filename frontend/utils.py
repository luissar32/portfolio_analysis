import pandas as pd

def format_data(df):
    """Ensure DataFrame is in correct format for analysis."""
    if df is None or df.empty or df.isna().all().all():
        raise ValueError("El DataFrame está vacío o contiene solo valores nulos.")
    df.index = pd.to_datetime(df.index)
    df = df.dropna()
    if df.empty:
        raise ValueError("El DataFrame está vacío después de eliminar valores nulos.")
    return df