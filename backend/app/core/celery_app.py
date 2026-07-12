"""
Celery App for QuantumPilot AI - Background Jobs
- Space Weather fetch every 10 min (NOAA kp + neutron cosmic ray strength) - LIVE
- Calibration refresh every 1 hour (IBM Quantum backends)
- Drift prediction every 30 min (LSTM)
"""

from celery import Celery
from celery.schedules import crontab
import os

# Use Redis as broker via env, fallback to RabbitMQ
broker_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
# If using RabbitMQ as broker, use RABBITMQ_URL
if os.getenv("RABBITMQ_URL"):
    broker_url = os.getenv("RABBITMQ_URL")

# For production, use Redis for broker and backend
celery_app = Celery(
    "quantumpilot",
    broker=broker_url,
    backend=os.getenv("REDIS_URL", "redis://redis:6379/0"),
    include=["app.core.tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    beat_schedule={
        # Space Weather every 10 minutes - fetches live kp_index + neutron_flux for NeuralUCB 22-D
        "fetch-space-weather-every-10m": {
            "task": "app.core.tasks.fetch_space_weather",
            "schedule": 600.0,  # 600 seconds = 10 minutes
        },
        # Calibration refresh every 1 hour - fetches live T1/T2/RO/CZ from IBM Quantum fez/marrakesh/kingston
        "refresh-calibration-every-1h": {
            "task": "app.core.tasks.refresh_calibration",
            "schedule": 3600.0,
        },
        # Drift prediction every 30 min - LSTM predicts T1 after 2h
        "predict-drift-every-30m": {
            "task": "app.core.tasks.predict_drift",
            "schedule": 1800.0,
        },
    }
)

if __name__ == "__main__":
    celery_app.start()
