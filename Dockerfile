FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install system dependencies for OpenCV, Tesseract OCR, PyMuPDF, and PostgreSQL
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    tesseract-ocr \
    tesseract-ocr-eng \
    libgl1-mesa-glx \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy application files
COPY . .

# Generate historical dataset & train model if not present
RUN python data/seed_generator.py && \
    python models/train_xgboost.py

# Expose FastAPI (8000) and Streamlit (8501)
EXPOSE 8000 8501

# Default command launches FastAPI backend
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
