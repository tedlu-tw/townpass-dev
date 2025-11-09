FROM python:3.11-slim

WORKDIR /app

# Install CA certificates and other system dependencies for MongoDB SSL/TLS
RUN apt-get update && apt-get install -y \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port 8080 (Cloud Run default)
EXPOSE 8080

# Use gunicorn for production
CMD exec gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 wsgi:app
