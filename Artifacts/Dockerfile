FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# Install build dependencies needed for scientific stack
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src ./src
COPY data ./data
COPY streamlit_app.py ./streamlit_app.py
COPY run_server.py ./run_server.py
COPY scripts ./scripts

# Expose API port; Streamlit can be enabled with alternate command
EXPOSE 8000

# Allow platforms like Render/Fly to provide port via PORT env var
CMD ["sh", "-c", "uvicorn src.api.main:app --host 0.0.0.0 --port ${PORT:-8000}"]

