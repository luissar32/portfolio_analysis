import pandas as pd


def format_data(df):
    """Ensure DataFrame is in correct format for analysis."""
    if df is None or df.empty or df.isna().all().all():
        raise ValueError("El DataFrame está vacío o contiene solo valores nulos.")

    # Validar y convertir el índice a fechas
    try:
        df.index = pd.to_datetime(df.index, format="mixed", errors="raise")
    except ValueError as e:
        raise ValueError(
            f"Error en el formato de las fechas: {str(e)}. Asegúrate de que la columna 'Date' tenga el formato YYYY-MM-DD.")

    # Eliminar valores nulos
    df = df.dropna()
    if df.empty:
        raise ValueError("El DataFrame está vacío después de eliminar valores nulos.")

    return df