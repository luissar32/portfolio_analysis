import streamlit as st
import pandas as pd
import plotly.express as px
from src.data.fetch_data import fetch_stock_data
from src.utils.metrics import calculate_returns, calculate_sharpe_ratio
from src.models.portfolio_optimization import optimize_portfolio
from visualization.utils import format_data

# Page configuration
st.set_page_config(page_title="Portfolio Analysis Microservice", layout="wide")

# Custom CSS
with open("visualization/assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Title and description
st.title("Portfolio Analysis Microservice")
st.markdown("Analyze and optimize investment portfolios with real-time financial data. Calculate key metrics and visualize the efficient frontier.")

# Sidebar for user inputs
with st.sidebar:
    st.header("Portfolio Configuration")
    tickers = st.text_input("Stock Tickers (comma-separated)", "AAPL,MSFT,GOOGL")
    start_date = st.date_input("Start Date", value=pd.to_datetime("2023-01-01"))
    end_date = st.date_input("End Date", value=pd.to_datetime("2025-05-01"))
    risk_free_rate = st.number_input("Risk-Free Rate (%)", min_value=0.0, max_value=10.0, value=2.0, step=0.1) / 100
    uploaded_file = st.file_uploader("Upload CSV (optional)", type=["csv"])

# Main content
if st.button("Analyze Portfolio"):
    if uploaded_file:
        df = pd.read_csv(uploaded_file, index_col=0, parse_dates=True)
        df = format_data(df)
    else:
        tickers_list = [t.strip() for t in tickers.split(",")]
        df = fetch_stock_data(tickers_list, start_date, end_date)
        df = format_data(df)

    # Display raw data
    st.subheader("Portfolio Data")
    st.dataframe(df.tail())

    # Calculate metrics
    returns = calculate_returns(df)
    sharpe_ratio = calculate_sharpe_ratio(returns, risk_free_rate)

    # Display metrics
    col1, col2 = st.columns(2)
    with col1:
        annualized_return = returns.mean() * 252 * 100
        st.metric("Annualized Return", f"{annualized_return.mean():.2f}%")
    with col2:
        st.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")

    # Visualize returns
    st.subheader("Cumulative Returns")
    cumulative_returns = (1 + returns).cumprod() - 1
    fig_returns = px.line(cumulative_returns, title="Cumulative Returns", template="simple_white")
    fig_returns.update_layout(xaxis_title="Date", yaxis_title="Cumulative Return")
    st.plotly_chart(fig_returns, use_container_width=True)

    # Portfolio optimization
    st.subheader("Efficient Frontier")
    weights, frontier = optimize_portfolio(returns, risk_free_rate)
    fig_frontier = px.scatter(x=frontier["Volatility"] * np.sqrt(252) * 100,
                             y=frontier["Return"] * 252 * 100,
                             title="Efficient Frontier",
                             template="simple_white")
    fig_frontier.update_layout(xaxis_title="Annualized Volatility (%)",
                              yaxis_title="Annualized Return (%)")
    st.plotly_chart(fig_frontier, use_container_width=True)

    # Optimal weights
    st.subheader("Optimal Portfolio Weights")
    weights_df = pd.DataFrame(weights, index=df.columns, columns=["Weight"])
    st.dataframe(weights_df.style.format("{:.2%}"))

else:
    st.info("Enter tickers or upload a CSV and click 'Analyze Portfolio' to begin.")
    if st.button("Load Sample Data"):
        df = pd.read_csv("visualization/assets/sample_data.csv", index_col=0, parse_dates=True)
        st.session_state["uploaded_file"] = df
        st.experimental_rerun()