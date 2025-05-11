from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_plot_efficient_frontier():
    response = client.get("/portfolio/plot/efficient-frontier?tickers=AAPL,MSFT")
    assert response.status_code == 200
    assert "<div" in response.text  # Verifica que sea HTML con un gráfico