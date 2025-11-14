import pytest
from fastapi.testclient import TestClient
from app import app
import json

client = TestClient(app)


def test_api_and_models_loaded():
    # Basic health
    r = client.get("/")
    assert r.status_code == 200
    data = r.json()
    assert data.get("status") == "running"


def test_forecast_and_anomaly_and_trend():
    # Forecast (POST)
    r = client.post("/forecast", json={"months": 2})
    assert r.status_code == 200
    f = r.json()
    assert "dates" in f and "predictions" in f
    assert len(f["dates"]) == 2

    # Anomaly (POST)
    r2 = client.post("/anomaly", json={"value": 100.0})
    assert r2.status_code == 200
    a = r2.json()
    assert "is_anomaly" in a and "score" in a

    # Trend (GET)
    r3 = client.get("/trend")
    assert r3.status_code == 200
    t = r3.json()
    assert "slope" in t
