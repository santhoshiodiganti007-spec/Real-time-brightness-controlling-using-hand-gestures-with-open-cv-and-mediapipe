# Multi-Stage Dockerfile for Touchless Brightness Control Dashboard / Cloud Mode
FROM python:3.11-slim as backend-builder

WORKDIR /app

# Install system dependencies for OpenCV and MediaPipe
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend ./backend
COPY config ./config

# Expose FastAPI port
EXPOSE 8000

ENV DEMO_MODE=true
ENV API_HOST=0.0.0.0
ENV API_PORT=8000

CMD ["python", "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
