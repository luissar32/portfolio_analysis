from fastapi import APIRouter, HTTPException
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/assets/{ticker}/history")
async def get_asset_history(ticker: str, days: int = 30):
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        stock = yf.Ticker(ticker)
        data = stock.history(start=start_date, end=end_date)
        if data.empty:
            raise HTTPException(status_code=404, detail="No data found for ticker")
        return data.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/assets/list")
async def get_asset_list():
    # ticker lists for example use.
    return ["AAPL", "MSFT", "GOOGL", "TSLA"]