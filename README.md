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

## Dashboard

- A Dash-based dashboard is available at `dashboard.py`. It reads `data/cleaned_data.csv` and provides:
	- Data overview and sample table
	- Visualizations (monthly landings, distribution, aircraft types)
	- Buttons to call the API endpoints for forecast, anomaly detection, and trend analysis

Run the dashboard locally (make sure the API is running):
```powershell
# Activate venv (PowerShell)
C:\Users\Yunus\Downloads\Internship\.venv\Scripts\Activate.ps1

# Start API in one terminal
python -m uvicorn app:app --reload

# Start dashboard in another terminal
python dashboard.py

# Open http://127.0.0.1:8050 in your browser
```

## Docker / Deployment

- A `Dockerfile` and `docker-compose.yml` are included to run the API and dashboard as containers.

To run locally with Docker Compose:
```powershell
# Build and start services
docker-compose up --build

# API -> http://localhost:8000
# Dashboard -> http://localhost:8050
```

## Continuous Integration

- A GitHub Actions workflow is configured at `.github/workflows/ci.yml` to run tests on push/pull requests to `main`.

## Run full pipeline

- A helper script `run_pipeline.py` is provided to run the data pipeline scripts in order. Use:
```powershell
python run_pipeline.py
```

## Tests

- Run unit & integration tests with:
```powershell
python -m pytest -q
```

## Running Tests
Run unit tests: `pytest tests/`

## Pipeline
1. Load and clean data
2. Explore and visualize key patterns
3. Perform statistical or ML-based trend analysis
4. Predict landing volume or detect anomalies
5. Generate final plots and report-ready insights