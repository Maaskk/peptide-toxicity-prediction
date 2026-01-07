# Dockerfile for standalone Python ML environment
# Use this for training models or running ML scripts independently

FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy ML code
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY data/ ./data/
COPY results/ ./results/

# Create necessary directories
RUN mkdir -p /app/data/raw /app/data/processed /app/results

# Set Python path
ENV PYTHONPATH=/app

# Default command (can be overridden)
CMD ["python3", "scripts/train_pipeline.py"]

