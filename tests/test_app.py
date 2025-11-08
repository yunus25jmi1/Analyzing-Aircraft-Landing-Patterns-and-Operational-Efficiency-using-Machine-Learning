"""
Unit tests for the Aircraft Landing Analysis API
"""

import pytest
from fastapi.testclient import TestClient
from app import app
import os

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Aircraft Landing Analysis API" in response.json()["message"]

def test_forecast():
    request_data = {"months": 6}
    response = client.post("/forecast", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "dates" in data
    assert "predictions" in data
    assert len(data["dates"]) == 6
    assert len(data["predictions"]) == 6

def test_anomaly():
    request_data = {"value": 10000.0}
    response = client.post("/anomaly", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "is_anomaly" in data
    assert "score" in data
    assert isinstance(data["is_anomaly"], bool)
    assert isinstance(data["score"], float)

def test_trend():
    response = client.get("/trend")
    assert response.status_code == 200
    data = response.json()
    assert "slope" in data
    assert isinstance(data["slope"], float)

def test_forecast_invalid_months():
    request_data = {"months": -1}
    response = client.post("/forecast", json=request_data)
    assert response.status_code == 400

def test_anomaly_invalid_value():
    request_data = {"value": "invalid"}
    response = client.post("/anomaly", json=request_data)
    assert response.status_code == 422  # Validation error

# Test model loading
def test_models_loaded():
    from app import trend_model, prophet_model, anomaly_model
    assert trend_model is not None
    assert prophet_model is not None
    assert anomaly_model is not None