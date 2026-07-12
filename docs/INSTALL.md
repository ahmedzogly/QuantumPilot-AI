# INSTALL - QuantumPilot AI

## Prerequisites
- Docker & Docker Compose
- Python 3.11 (for Mitiq compatibility, Python 3.13 fails ImpImporter)
- Node 20
- IBM Quantum Account (CRN DIGI) - we used crn:v1:bluemix:public:quantum-computing:us-east:a/...:cdf67559... for live fetch
- HuggingFace Token (optional, for Granite-8B API 0GB)

## Quick Start - Production One Command

```bash
git clone https://github.com/your-org/QuantumPilot-AI.git
cd QuantumPilot-AI
cp .env.example .env
# Edit .env: IBM_TOKEN, IBM_CRN, HF_TOKEN, SECRET_KEY
docker-compose -f docker-compose.prod.yml up --build -d
```

## Verify

```bash
curl http://localhost:8000/api/v1/health
# {"status":"ok","service":"QuantumPilot AI","version":"0.1.0"}

curl http://localhost:8000/api/v1/backends
# [{"backend_name":"ibm_fez","num_qubits":156,"T1_mean":135.6,...}, ...] - Live data pulled today 2026-07-11

curl http://localhost:8000/api/v1/spaceweather/live
# {"kp_index":2.0,"source":"NOAA_1m","status":"live","neutron_flux":94.6,"cosmic_ray_strength":0.945, "solar_zenith_deg":74.65}

curl http://localhost:8000/api/v1/copilot/plan -X POST -H "Content-Type: application/json" -d '{"intent_text":"نفذ بأقل تكلفة"}'
# Returns backend ibm_kingston opt1 mit s_zne shots 1024 fidelity 0.95
```

## Development Mode (Without Docker)

```bash
cd backend
pip install -r requirements.txt
# Torch CPU
pip install torch --index-url https://download.pytorch.org/whl/cpu
# For Mitiq, must use Python 3.11: pip install mitiq (fails on 3.13)

# Run FastAPI
uvicorn app.main:app --reload --port 8000

# In another terminal, Celery Worker for SpaceWeather every 10 min
celery -A app.core.celery_app worker --loglevel=info
celery -A app.core.celery_app beat --loglevel=info

# Frontend
cd ../frontend
npm install
npm run dev
# http://localhost:3000
```

## Datasets Setup (Already Pulled)

We have already pulled:
- `datasets/calibration_drift/drift_50k.parquet` 1.8M (50k sample of 8M)
- `datasets/szne/repo` Fig2 100q predictions
- `datasets/qcaleval` 243 test images
- `datasets/clifford_training/clifford_training_100.json` 44K ideal vs noisy
- Live: `ibm_fez_properties.json` 1.1MB + `ibm_fez_qubits_full.csv` 14K + 352 CZ gates mean 3.33%

To repull:
```bash
python scripts/pull_datasets.py
python scripts/generate_clifford_training.py
python scripts/deep_train.py # Trains RewardNet 22->128->128->1 8847 contexts loss 0.3224->0.0028 -> reward_net_deep.pt 80K + drift_lstm.pt 21K
python scripts/prepare_frontend_data.py # Creates frontend/public/*.json
```

## Live Data Fetch (Verified Today)

- NOAA Kp: https://services.swpc.noaa.gov/json/planetary_k_index_1m.json -> kp=2.0 live 2026-07-12T10:58 UTC
- NMDB Neutron: https://cosmicrays.oulu.fi/nowcastapi/ -> Oulu station + Forbush model fallback
- IBM Quantum: QiskitRuntimeService CRN DIGI -> fez 156q T1 135.6us

## Models

- `models/neuralucb/reward_net_deep.pt` 80K (8847 contexts, best val 0.0028)
- `models/neuralucb/drift_lstm.pt` 21K (seq 10 -> next T1)
- Granite-8B: HF Inference API 0GB local (16GB FP16 original, 4.9GB Q4_K_M GGUF alternative)

## Frontend Build

```bash
cd frontend
npm run build
npm start
# http://localhost:3000 Dashboard with 6 Recharts + SpaceWeatherChart LIVE + CopilotChat
```

## Tests

```bash
cd backend
pytest tests/unit -v --cov=app
pytest tests/integration -v
```

## Troubleshooting

- **Mitiq fails on Python 3.13**: Use Docker Python 3.11 - we fixed with Dockerfile FROM python:3.11-slim
- **DuckDB missing**: pip install duckdb
- **Torch missing**: pip install torch --index-url https://download.pytorch.org/whl/cpu
- **QASM3 import**: pip install qiskit-qasm3-import
