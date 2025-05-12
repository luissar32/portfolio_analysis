import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
import numpy as np
import sys
import os
from datetime import datetime, date
import time

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from utils import format_data

def fetch_stock_data(tickers, start_date, end_date, max_retries=3):
    """Fetch stock data from Yahoo Finance with retries."""
    for attempt in range(max_retries):
        try:
            data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=True)["Close"]
            if data.empty or data.isna().all().all():
                raise ValueError("No se encontraron datos para los tickers y fechas especificados.")
            return data
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(1)
                continue
            raise ValueError(f"Error al obtener datos de Yahoo Finance tras {max_retries} intentos: {str(e)}")

def calculate_returns(df):
    returns = df.pct_change().dropna()
    if returns.empty or returns.isna().all().all():
        raise ValueError("No hay retornos válidos para calcular.")
    return returns

def calculate_sharpe_ratio(returns, risk_free_rate):
    if returns.empty:
        raise ValueError("No hay retornos para calcular el Sharpe ratio.")
    mean_return = returns.mean() * 252
    std_return = returns.std() * np.sqrt(252)
    sharpe = (mean_return - risk_free_rate) / std_return
    return sharpe.mean() if isinstance(sharpe, pd.Series) else sharpe

def optimize_portfolio(returns, risk_free_rate):
    if returns.empty:
        raise ValueError("No hay retornos para optimizar el portafolio.")
    num_assets = len(returns.columns)
    weights = np.ones(num_assets) / num_assets
    mean_returns = returns.mean() * 252
    std_returns = returns.std() * np.sqrt(252)
    min_return = mean_returns.min() if mean_returns.any() and not np.isnan(mean_returns.min()) else 0.0
    max_return = mean_returns.max() if mean_returns.any() and not np.isnan(mean_returns.max()) else 0.1
    min_vol = std_returns.min() if std_returns.any() and not np.isnan(std_returns.min()) else 0.0
    max_vol = std_returns.max() if std_returns.any() and not np.isnan(std_returns.max()) else 0.2
    frontier = pd.DataFrame({
        "Return": np.linspace(min_return, max_return, 10),
        "Volatility": np.linspace(min_vol, max_vol, 10)
    })
    return pd.Series(weights, index=returns.columns, name="Weight"), frontier

st.set_page_config(page_title="Portfolio Analysis Microservice", layout="wide")

try:
    with open(os.path.join(os.path.dirname(__file__), "assets", "style.css")) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("No se encontró style.css.")

st.title("Portfolio Analysis Microservice")
st.markdown("Analiza y optimiza portafolios de inversión con datos financieros en tiempo real.")

with st.sidebar:
    st.header("Configuración del Portafolio")
    tickers = st.text_input("Tickers de Acciones (separados por comas)", "AAPL,MSFT,GOOGL")
    start_date = st.date_input("Fecha de Inicio", value=pd.to_datetime("2023-01-01"), max_value=date.today())
    end_date = st.date_input("Fecha de Fin", value=pd.to_datetime("2024-05-01"), max_value=date.today())
    risk_free_rate = st.number_input("Tasa Libre de Riesgo (%)", min_value=0.0, max_value=10.0, value=2.0, step=0.1) / 100
    uploaded_file = st.file_uploader("Subir CSV (opcional)", type=["csv"])

tickers_list = [t.strip() for t in tickers.split(",") if t.strip()]
if not tickers_list and not uploaded_file:
    st.warning("Por favor, ingrese tickers válidos o suba un CSV.")
elif start_date > end_date:
    st.error("La fecha de inicio debe ser anterior a la fecha de fin.")
elif end_date > date.today():
    st.error("La fecha de fin no puede ser futura.")
else:
    if st.button("Analizar Portafolio"):
        try:
            if uploaded_file:
                df = pd.read_csv(uploaded_file, index_col=0, parse_dates=True)
                if df.empty or df.isna().all().all():
                    raise ValueError("El CSV subido está vacío o contiene solo valores nulos.")
                df = format_data(df)
            else:
                if not tickers_list:
                    raise ValueError("Por favor, ingrese al menos un ticker válido.")
                df = fetch_stock_data(tickers_list, start_date, end_date)
                df = format_data(df)

            if df.empty or df.isna().all().all():
                raise ValueError("No hay datos válidos después de procesar.")

            st.subheader("Datos del Portafolio")
            st.dataframe(df.tail())

            returns = calculate_returns(df)
            sharpe_ratio = calculate_sharpe_ratio(returns, risk_free_rate)

            col1, col2 = st.columns(2)
            with col1:
                annualized_return = returns.mean() * 252 * 100
                st.metric("Retorno Anualizado", f"{annualized_return.mean():.2f}%")
            with col2:
                st.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")

            st.subheader("Retornos Acumulativos")
            cumulative_returns = (1 + returns).cumprod() - 1
            fig_returns = px.line(cumulative_returns, title="Retornos Acumulativos", template="simple_white")
            fig_returns.update_layout(xaxis_title="Fecha", yaxis_title="Retorno Acumulativo")
            st.plotly_chart(fig_returns, use_container_width=True)

            st.subheader("Frontera Eficiente")
            weights, frontier = optimize_portfolio(returns, risk_free_rate)
            fig_frontier = px.scatter(x=frontier["Volatility"] * 100,
                                     y=frontier["Return"] * 100,
                                     title="Frontera Eficiente",
                                     template="simple_white")
            fig_frontier.update_layout(xaxis_title="Volatilidad Anualizada (%)",
                                      yaxis_title="Retorno Anualizado (%)")
            st.plotly_chart(fig_frontier, use_container_width=True)

            st.subheader("Pesos Óptimos del Portafolio")
            weights_df = pd.DataFrame(weights, columns=["Peso"])
            st.dataframe(weights_df.style.format("{:.2%}"))

        except Exception as e:
            st.error(f"Error al analizar el portafolio: {str(e)}")

    else:
        st.info("Ingresa tickers o sube un CSV y haz clic en 'Analizar Portafolio'.")
        if st.button("Cargar Datos de Ejemplo"):
            try:
                sample_path = os.path.join(os.path.dirname(__file__), "assets", "sample_data.csv")
                df = pd.read_csv(sample_path, index_col=0, parse_dates=True)
                if df.empty or df.isna().all().all():
                    raise ValueError("El archivo sample_data.csv está vacío o contiene solo valores nulos.")
                st.session_state["uploaded_file"] = df
                st.experimental_rerun()
            except FileNotFoundError:
                st.error("No se encontró sample_data.csv.")
            except Exception as e:
                st.error(f"Error al cargar datos de ejemplo: {str(e)}")