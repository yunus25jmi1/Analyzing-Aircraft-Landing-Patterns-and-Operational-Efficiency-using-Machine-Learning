FROM python:3.11-slim
WORKDIR /app

# Install system deps for a minimal runtime
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000 8050

# Default command shows help; user should run uvicorn or dashboard as needed via docker-compose
CMD ["/bin/bash", "-c", "echo 'Start services via docker-compose or run uvicorn app:app --host 0.0.0.0 --port 8000' && sleep infinity"]
