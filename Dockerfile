FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY backend ./backend
COPY cli ./cli
COPY frontend ./frontend
COPY data ./data

# Create necessary directories
RUN mkdir -p data/raw data/wiki data/output

# Copy environment template as default
COPY .env.example .env

# Expose ports
EXPOSE 8000 5173

# Default command runs the backend
CMD ["python", "backend/main.py"]
