FROM python:3.11-slim AS builder

# Install build dependencies to compile any packages that need it
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements-pinned.txt ./

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements-pinned.txt

########################################
# Final image
FROM python:3.11-slim

WORKDIR /app

# Copy installed Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy project files
COPY . /app

EXPOSE 8000 8050

CMD ["/bin/bash","-c","echo 'To run: use docker-compose or run uvicorn app:app --host 0.0.0.0 --port 8000' && sleep infinity"]
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
