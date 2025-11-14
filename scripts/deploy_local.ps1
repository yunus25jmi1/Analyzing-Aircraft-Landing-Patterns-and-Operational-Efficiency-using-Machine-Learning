#!/usr/bin/env pwsh

# Start API and Dashboard locally in the background (Windows PowerShell).
# Usage: Open PowerShell in the repo root and run: `.	ools\deploy_local.ps1` or `.	ools\deploy_local.ps1 -Start`.

$ErrorActionPreference = 'Stop'

# Locate Python in .venv if present
$venvPython = Join-Path $PSScriptRoot '..\.venv\Scripts\python.exe'
if (Test-Path $venvPython) {
    $python = $venvPython
} else {
    $python = 'python'
}

Write-Host "Using Python: $python"

Write-Host "Starting API (uvicorn) in background..."
Start-Process -FilePath $python -ArgumentList '-m uvicorn app:app --host 0.0.0.0 --port 8000' -WindowStyle Hidden

Write-Host "Starting Dashboard (Dash) in background..."
Start-Process -FilePath $python -ArgumentList 'dashboard.py' -WindowStyle Hidden

Write-Host "Started: API -> http://localhost:8000 , Dashboard -> http://localhost:8050"
