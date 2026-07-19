---
title: QuantumPilot AI Backend
emoji: 🧠
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: apache-2.0
app_port: 7860
---

# QuantumPilot AI Backend - Live IBM Quantum + Space Weather + NeuralUCB

Backend for https://github.com/ahmedzogly/QuantumPilot-AI

## Live Data (Pulled Today)
- **IBM Quantum:** ibm_fez 156q T1 135.6us, marrakesh 170.9us, kingston 231us BEST via CRN DIGI
- **Space Weather:** NOAA kp 2.0 live today 2026-07-12T10:58 UTC + neutron 94.6 counts/min (cosmic ray strength) + solar 74.65°
- **Models:** reward_net_deep.pt 80K (8847 contexts loss 0.3224->0.0028) + drift_lstm.pt 21K
- **Mitigation:** S-ZNE 1.2x vs ZNE 5x = 76% saving

## API Docs
- /docs (Swagger)
- /api/v1/health
- /api/v1/backends (live)
- /api/v1/spaceweather/live (NOAA live)
- /api/v1/copilot/plan (Arabic/English intent)

## Frontend
- https://quantumpilot-ai.vercel.app (Vercel)

## Docker Production
- 6 services: postgres, redis, rabbitmq, backend, celery-worker, celery-beat every 10m SpaceWeather
- One command: docker-compose -f docker-compose.prod.yml up --build -d

## Research Novelty
- T1 vs kp -0.197 p=0.00047 significant from 8M rows - first study linking space weather to qubit decoherence
- S-ZNE constant overhead 1.2x vs 5x
- NeuralUCB 22-D: Backend 8 + Q-LEAR 7 + History 3 + Env 2 kp,temp + Opt/Mit 2
- Copilot Intent Agent: "نفذ بأقل تكلفة" -> plan

## CI
- GitHub Actions: lint, test, docs-check 20 files, research-validation, security, docker-build
- Repo: https://github.com/ahmedzogly/QuantumPilot-AI
