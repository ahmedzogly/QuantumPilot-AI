# QuantumPilot AI
### AI Orchestrator for Quantum Computing - NeuralUCB-Based Autonomous Decision Engine for Adaptive Quantum Execution

**Production-ready research project** that acts as Autopilot for IBM Quantum.

## What it does
Automatically: Analyze circuits → Select best backend (ibm_fez, marrakesh, kingston) based on live T1/T2/readout/CZ errors + calibration drift (8M rows) → Choose transpiler settings → Choose mitigation (S-ZNE from weiyouLiao paper, ZNE, TREX, Noise-agnostic from Nature 2025) → Monitor → Retry intelligently → Learn via NeuralUCB.

## Live Data Pulled
- **ibm_fez 156q**: T1 mean 135.6us, last update 2026-07-11
- **ibm_marrakesh 156q**: T1 170.9us
- **ibm_kingston 156q**: T1 231us (best)
- **Datasets**: 
  - phanerozoic/qiskit-calibration-drift 8.04M rows sampled to 50k (drift_50k.parquet)
  - S-ZNE repo (Sample-efficient QEM via classical learning surrogates)
  - nvidia/QCalEval 243 calibration images

## Architecture
Clean Architecture + DDD + SOLID + Repository Pattern
Backend: Python FastAPI Qiskit Qiskit Runtime Pydantic SQLAlchemy Redis RabbitMQ Postgres
AI: NeuralUCB (context 22-D: T1,T2,readout,gate_error,queue,depth,width,algo_type)
Frontend: React Next.js Tailwind TypeScript Recharts

## Quick Start
```bash
docker-compose up --build
# API docs at http://localhost:8000/docs
```

## API Endpoints (MVP)
- GET /api/v1/health
- GET /api/v1/backends -> returns live calibration from ibm_fez etc
- POST /api/v1/analyze -> circuit profile
- POST /api/v1/decide -> NeuralUCB decision

## Research Novelty
- First NeuralUCB for multi-objective backend selection (fidelity+queue+cost)
- Integrates S-ZNE constant-overhead mitigation
- Uses real drift dataset with environmental features (solar, kp_index)
- Comparison vs IBM least_busy, Q-LEAR, MQT

## Docs
See docs/ARCHITECTURE.md, docs/project/Tasks.md
