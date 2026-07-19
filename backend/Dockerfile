FROM python:3.11-slim-bookworm

WORKDIR /app

# Copy requirements first for cache
COPY requirements.txt .
# Install torch CPU first to avoid GPU wheels and heavy CUDA downloads
RUN pip install --no-cache-dir torch==2.13.0+cpu --extra-index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt
# Keep Mitiq on a NumPy 1.x compatible line for transformers/scikit-learn.
RUN pip install --no-cache-dir "mitiq==0.41.0" "numpy==1.26.4"

# Copy app code
COPY . .

# Create non-root user
RUN useradd -m quantumpilot && chown -R quantumpilot /app
USER quantumpilot

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/v1/health', timeout=5).read()" || exit 1

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
