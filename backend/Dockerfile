FROM python:3.11-slim

WORKDIR /app

# System deps for building numpy, etc + curl for healthcheck
RUN apt-get update && apt-get install -y gcc g++ curl libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy requirements first for cache
COPY requirements.txt .
# Install torch CPU first to avoid heavy build
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt
# Mitiq requires Python 3.11 - now will work (was failing on 3.13)
RUN pip install --no-cache-dir mitiq

# Copy app code
COPY . .

# Create non-root user
RUN useradd -m quantumpilot && chown -R quantumpilot /app
USER quantumpilot

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:8000/api/v1/health || exit 1

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
