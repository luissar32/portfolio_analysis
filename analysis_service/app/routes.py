from fastapi import APIRouter, HTTPException
import numpy as np
import pandas as pd
import requests
from pydantic import BaseModel
import os

router = APIRouter()
class PortfolioInput(BaseModel):
    tickers: list[str]
    weights: list[float] = None    # Opcional, si no se proporcionan datos

@router.post("/portfolio/optimize")
async def optimize_portfolio(portfolio: PortfolioInput):
    try:
        # Intentar traer la data.
        data_service_url = os.getenv("DATA_SERVICE_URL", "http://localhost:8001")
        historical_data = []
        for ticker in portfolio.tickers:
            try:
                response = requests.get(f"{data_service_url}/assets/{ticker}/history")
                response.raise_for_status()  # Lanza excepción para errores HTTP
                data = response.json()
                if not data:  # Verifica si la respuesta está vacía
                    raise HTTPException(status_code=404, detail=f"No data found for ticker {ticker}")
                historical_data.append(pd.DataFrame(data))
            except requests.exceptions.HTTPError as e:
                raise HTTPException(status_code=500, detail=f"Error al obtener datos para {ticker}: {e}")

        # Procesamiento de datos.
        returns = pd.concat([df["Close"].rename(ticker) for df, ticker in zip(historical_data, portfolio.tickers)], axis=1).pct_change().dropna()
        mean_retorno = returns.mean() * 252
        cov_matrix = returns.cov() * 252

        # En caso de que los weights estén vacíos.
        if portfolio.weights is None:
            num_assets = len(portfolio.tickers)
            weights = np.random.random(num_assets)
            weights = weights / np.sum(weights)
        else:
            weights = np.array(portfolio.weights)
            if len(weights) != len(portfolio.tickers) or abs(sum(weights) - 1.0) > 0.01:
                raise HTTPException(status_code=400, detail="weights requieren sumar al menos 1 y coincidir con el ticker")
        portfolio_return = np.sum(mean_retorno * weights) * 100
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix * 100, weights)))
        sharpe_ratio = portfolio_return / portfolio_volatility

        return {
            "tickers": portfolio.tickers,
            "weights": weights.tolist(),
            "return": portfolio_return,
            "volatility": portfolio_volatility,
            "sharpe_ratio": sharpe_ratio
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
