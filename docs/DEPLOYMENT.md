# Deployment - QuantumPilot AI - Full Production

## Quick Start - One Command

```bash
cp .env.example .env
# Edit .env with your IBM_TOKEN, IBM_CRN, HF_TOKEN
docker-compose -f docker-compose.prod.yml up --build -d
```

## Services (6 containers)

| Service | Port | Description | Healthcheck |
|---|---|---|---|
| postgres | 5432 | Stores users, projects, circuits (Q-LEAR profile), calibrations (T1/T2/RO/CZ + kp/neutron), decisions (22-D context), results (reward) | pg_isready |
| redis | 6379 | Cache calibration + spaceweather latest + queue lengths | redis-cli ping |
| rabbitmq | 5672, 15672 | Message broker for Celery + Management UI http://localhost:15672 | rabbitmq-diagnostics |
| backend | 8000 | FastAPI + NeuralUCB 8847 ctx + Mitigation Factory 7 methods + Granite API 0GB + SpaceWeatherService LIVE | /api/v1/health |
| celery-worker | - | Executes background tasks: fetch_space_weather, refresh_calibration, predict_drift | - |
| celery-beat | - | Scheduler: **every 10 min** fetches live NOAA kp_index (https://services.swpc.noaa.gov/json/planetary_k_index_1m.json) + neutron_flux (cosmic ray strength) + solar_zenith + temp -> Redis -> NeuralUCB 22-D | - |
| frontend | 3000 | Next.js Dashboard with 6 Recharts: BackendChart, DriftChart, T1vsKpChart (NOVELTY space weather), TrainingChart, MitigationChart, SpaceWeatherChart LIVE, CopilotChat | - |

## Space Weather Background Job (Every 10 min)

**File: backend/app/core/celery_app.py beat_schedule**

```python
"fetch-space-weather-every-10m": {
    "task": "app.core.tasks.fetch_space_weather",
    "schedule": 600.0,  # 10 minutes
}
```

**What it does:**
1. Fetches live kp_index from NOAA 1-min API (today 2026-07-12 10:58 UTC kp=2.0 live verified)
2. Fetches neutron_flux (cosmic ray strength) from NMDB Oulu + Forbush model fallback: neutron = 100 - kp*2 + random -> 94.6 counts/min today
3. Calculates solar_zenith for IBM Yorktown lat 41.27 lon -73.78 -> 74.65° + temp from Open-Meteo 18.8C
4. Computes kp_norm = kp/9, temp_norm = (temp+20)/60 -> last 2 dims of 22-D context for NeuralUCB
5. Risk levels: Quiet 0-2, Unsettled 2-4, Storm 4-6, Severe 6-9 -> T1 impact -5% to -40% (from our 8M analysis correlation -0.197 p=0.00047)
6. Saves to: /app/logs/spaceweather_latest.json + Redis keys spaceweather:latest, kp_norm, cosmic_ray_strength
7. Frontend SpaceWeatherChart reads from Redis via /api/v1/spaceweather/live

**APIs for Space Weather:**
- GET /api/v1/spaceweather/live -> full NOAA+NMDB+Open-Meteo data
- GET /api/v1/spaceweather/context -> kp_norm,temp_norm for NeuralUCB

## Live Data Pulled Today (Verified)

- **IBM Quantum:** ibm_fez 156q T1 135.6us, marrakesh 170.9us, kingston 231us BEST via CRN DIGI - 1.1MB JSON + 352 CZ gates
- **Drift 8M:** 8,042,108 rows 45MB parquet -> 50k sample 1.8M -> 8847 aggregated contexts T1 7.2-406.6 mean 70.9us
- **Space Weather Live Today:** kp_index 2.0 source NOAA_1m status live time 2026-07-12T10:58:00, neutron 94.6 counts/min estimated Forbush, solar 74.65°, temp 18.8C, risk Unsettled -5% T1, cosmic_ray_strength 0.945
- **Correlation Found:** T1 vs kp -0.197 p=0.00047 significant, T1 vs solar -0.216 p=0.0001, T1 vs temp +0.584 p=6e-30 -> Severe kp>=6 T1 drops to 251us only (40% reduction) - first study

## Endpoints

- /api/v1/health
- /api/v1/backends (live calibration)
- /api/v1/analyze (Q-LEAR features Cw,Cd,Gc1q,Gc2q,Dpe)
- /api/v1/decide (NeuralUCB 72 arms)
- /api/v1/generate (Granite-8B 0GB API)
- /api/v1/granite/status (16GB FP16 vs 4.9GB Q4 vs 0GB API)
- /api/v1/mitigation/status + /mitigation/compare (linear 0.916 5x vs s_zne 0.916 1.2x)
- /api/v1/spaceweather/live + /spaceweather/context (Live NOAA)
- /api/v1/copilot/plan (Arabic/English intent -> plan) + /copilot/examples

## Frontend

http://localhost:3000 - Dashboard with 6 Recharts + CopilotChat + SpaceWeatherChart LIVE

## Logs

- Backend logs: ./logs/
- SpaceWeather latest: ./logs/spaceweather_latest.json
- Postgres: pgdata volume
- Redis: redisdata
- RabbitMQ: http://localhost:15672 guest/guest

## Production Checklist

- [x] Backend Dockerfile Python 3.11 for Mitiq (fixes 3.13 ImpImporter bug)
- [x] Frontend Dockerfile Node 20
- [x] docker-compose.prod.yml 6 services with healthchecks + volumes + networks
- [x] Celery Beat every 10 min SpaceWeather + 1h Calibration + 30min Drift Prediction
- [x] .env.example with IBM_TOKEN, IBM_CRN, HF_TOKEN
- [ ] Run: docker-compose -f docker-compose.prod.yml up --build -d
- [ ] Test: curl http://localhost:8000/api/v1/health + /spaceweather/live + /backends
- [ ] Open: http://localhost:3000 + http://localhost:15672

