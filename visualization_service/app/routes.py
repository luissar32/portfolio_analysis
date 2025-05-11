from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
import plotly.express as px
import plotly.io as pio
import pandas as pd
import requests
import os

router = APIRouter()

@router.get("/portfolio/plot/efficient-frontier", response_class=HTMLResponse)
async def plot_efficient_frontier(tickers: str):  # Ejemplo: tickers=AAPL,MSFT
    try:
        # Obtener datos del servicio de análisis
        analysis_service_url = os.getenv("ANALYSIS_SERVICE_URL", "http://localhost:8002")
        tickers_list = tickers.split(",")
        response = requests.post(
            f"{analysis_service_url}/portfolio/optimize",
            json={"tickers": tickers_list}
        )
        response.raise_for_status()
        portfolio_data = response.json()

        # Simular frontera eficiente (puedes usar utils.py)
        df = pd.DataFrame({
            "Return": [portfolio_data["return"]],
            "Volatility": [portfolio_data["volatility"]]
        })

        # Crear gráfico con Plotly
        fig = px.scatter(df, x="Volatility", y="Return", title="Efficient Frontier")
        return pio.to_html(fig, full_html=False)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
