from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_optimize_portfolio():
    carga = {"tickers": ["AAPL", "MSFT"], "weights": [0.5, 0.5]}
    response = client.post("/portfolio/optimize", json=carga)
    assert response.status_code == 200
    assert "tickers" in response.json()
    assert "sharpe_ratio" in response.json()