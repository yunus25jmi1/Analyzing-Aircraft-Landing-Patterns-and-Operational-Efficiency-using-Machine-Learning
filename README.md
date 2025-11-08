# Analyzing Aircraft Landing Patterns and Operational Efficiency using Machine Learning

This is a 4-week academic aerospace project analyzing air traffic landing data from San Francisco International Airport using machine learning techniques.

## Project Structure
- `data/`: Contains the dataset files
- `scripts/`: Python scripts for data processing, analysis, and modeling
- `notebooks/`: Jupyter notebooks for exploratory analysis
- `models/`: Saved machine learning models
- `docs/`: Additional documentation and outputs
- `app.py`: FastAPI backend for serving predictions
- `tests/`: Unit tests for the API

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Place the "Air Traffic Landings" dataset from Kaggle in the `data/` folder
3. Run the scripts in order: `data_loading.py`, `exploratory_analysis.py`, `trend_analysis.py`, `predictions.py`, `final_insights.py`

## Running the Backend
1. Start the API server: `uvicorn app:app --reload`
2. Access the API documentation at `http://127.0.0.1:8000/docs`

## API Endpoints
- `GET /`: API status
- `POST /forecast`: Forecast landings for next N months
- `POST /anomaly`: Check if a value is an anomaly
- `GET /trend`: Get trend slope

## Running Tests
Run unit tests: `pytest tests/`

## Pipeline
1. Load and clean data
2. Explore and visualize key patterns
3. Perform statistical or ML-based trend analysis
4. Predict landing volume or detect anomalies
5. Generate final plots and report-ready insights