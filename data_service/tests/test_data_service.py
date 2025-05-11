from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_asset_history():
    response = client.get("/assets/AAPL/history?days=30")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_asset_list():
    response = client.get("/assets/list")
    assert response.status_code == 200
    assert "AAPL" in response.json()