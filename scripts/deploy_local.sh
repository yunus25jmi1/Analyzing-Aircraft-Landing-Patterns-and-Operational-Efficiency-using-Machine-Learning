#!/usr/bin/env bash
set -euo pipefail

# Start API and dashboard in background (Linux/macOS)
PYTHON=${PYTHON:-python}

echo "Starting API: $PYTHON -m uvicorn app:app --host 0.0.0.0 --port 8000"
nohup $PYTHON -m uvicorn app:app --host 0.0.0.0 --port 8000 > api.log 2>&1 &

echo "Starting Dashboard: $PYTHON dashboard.py"
nohup $PYTHON dashboard.py > dashboard.log 2>&1 &

echo "Started. API -> http://localhost:8000 , Dashboard -> http://localhost:8050"
