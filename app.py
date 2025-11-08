"""
Aircraft Landing Analysis Backend API

A FastAPI application providing endpoints for aircraft landing predictions,
anomaly detection, and trend analysis.
"""

import warnings
warnings.filterwarnings("ignore", message="Importing plotly failed")

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
import pickle
from datetime import datetime, timedelta
import os
from contextlib import asynccontextmanager

# Load models at import time
trend_model = joblib.load(os.path.join("models", "trend_model.pkl"))
with open(os.path.join("models", "prophet_model.pkl"), "rb") as f:
    prophet_model = pickle.load(f)
anomaly_model = joblib.load(os.path.join("models", "anomaly_model.pkl"))

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Models already loaded
    yield

app = FastAPI(title="Aircraft Landing Analysis API", version="1.0.0", lifespan=lifespan)

# Pydantic models for request/response
class ForecastRequest(BaseModel):
    months: int = 12

class AnomalyRequest(BaseModel):
    value: float

class ForecastResponse(BaseModel):
    dates: list[str]
    predictions: list[float]

class AnomalyResponse(BaseModel):
    is_anomaly: bool
    score: float

class TrendResponse(BaseModel):
    slope: float

@app.get("/")
async def root():
    return {"message": "Aircraft Landing Analysis API", "status": "running"}

@app.post("/forecast", response_model=ForecastResponse)
async def forecast(request: ForecastRequest):
    if request.months <= 0:
        raise HTTPException(status_code=400, detail="Months must be positive")
    if prophet_model is None:
        raise HTTPException(status_code=500, detail="Prophet model not loaded")

    # Create future dataframe
    last_date = pd.to_datetime("2018-09-01")  # Last date in data
    future_dates = pd.date_range(start=last_date, periods=request.months + 1, freq='ME')[1:]

    future_df = pd.DataFrame({"ds": future_dates})
    forecast = prophet_model.predict(future_df)

    return ForecastResponse(
        dates=[d.strftime("%Y-%m-%d") for d in forecast["ds"]],
        predictions=forecast["yhat"].tolist()
    )

@app.post("/anomaly", response_model=AnomalyResponse)
async def check_anomaly(request: AnomalyRequest):
    if anomaly_model is None:
        raise HTTPException(status_code=500, detail="Anomaly model not loaded")

    # Create DataFrame with proper column name to match training
    input_df = pd.DataFrame([[request.value]], columns=['landings'])
    prediction = anomaly_model.predict(input_df)[0]
    score = anomaly_model.decision_function(input_df)[0]

    return AnomalyResponse(
        is_anomaly=prediction == -1,
        score=score
    )

@app.get("/trend", response_model=TrendResponse)
async def get_trend():
    if trend_model is None:
        raise HTTPException(status_code=500, detail="Trend model not loaded")

    slope = trend_model.coef_[0]
    return TrendResponse(slope=slope)