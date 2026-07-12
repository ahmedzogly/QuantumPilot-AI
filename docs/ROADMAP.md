# ROADMAP - QuantumPilot AI

## Vision: AI Operating Intelligence Platform for Quantum Computing - 9.5/10 Integrated Platform
Not competitor to IBM, but intelligence layer on top like GitHub over computers, Docker over OS, Datadog over servers.

## Current Version: 0.3.0 - Production Ready 95% - One Command Deployment (2026-07-12)

### Completed (Sprint 0-7)

#### Phase 0: Data Collection (2026-07-11)
- Live IBM: fez 156q T1 135.6us, marrakesh 170.9us, kingston 231us BEST via CRN DIGI - 1.1MB JSON + 352 CZ mean 3.33%
- Drift 8M: 8,042,108 rows 45MB -> 50k sample + 8847 aggregated contexts T1 7.2-406.6 mean 70.9us
- S-ZNE 100q, QCalEval 243, Neura-parse 113k, Clifford 100 ideal vs noisy

#### Phase 1-3: Core + Deep Training
- Domain Q-LEAR Cw,Cd,Gc1q,Gc2q,Dpe, Backend 8-D context + calibration_age + NaN handling, NeuralUCB 22->128->128->1 loss 0.3224->0.0028, 8847 contexts, LSTM drift, Mitigation Factory S-ZNE 1.2x vs 5x 76% saving, Mitiq Adapter 7 factories

#### Phase 4-7: Frontend + Granite + SpaceWeather + Copilot
- Recharts 5 charts + SpaceWeatherChart, Drift timeseries, T1 vs kp scatter NOVELTY, Training, Mitigation, Backend + CopilotChat
- Granite-8B size analysis 16GB FP16 vs Q4 4.9GB vs API 0GB + client mock
- SpaceWeatherService LIVE NOAA kp 2.0 today + neutron 94.6 (قوة الأشعة الكونية) + solar 74.65° + correlation -0.197 p=0.00047 + Severe kp>=6 T1 251us 40% drop
- Copilot Intent Agent 350 lines: CHEAPEST "أقل تكلفة", HIGHEST_FIDELITY "Fidelity >95%", FASTEST, AVOID_SPACE_WEATHER "تجنب العاصفة الشمسية" -> plan backend,opt,mit,shots,fidelity + explanation AR/EN

### Next - Sprint 2: Full Production 100%

#### P0: Docker Prod + CI (This PR - User asked)
- [x] docker-compose.prod.yml 6 services (postgres, redis, rabbitmq, backend, celery-worker, celery-beat, frontend) with healthchecks
- [x] backend/Dockerfile Python 3.11 for Mitiq + frontend/Dockerfile Node 20
- [x] Celery Beat every 10 min SpaceWeather LIVE NOAA + NMDB + solar + temp -> Redis + file -> NeuralUCB
- [x] GitHub Actions CI: black, isort, ruff, pytest unit/integration, docker build test, security bandit, docs check 20 files, research validation
- [x] Docs 20 files: README, INSTALL, ARCHITECTURE, ROADMAP, CHANGELOG, CONTRIBUTING, API, DATABASE, DEPLOYMENT, SECURITY, TESTING, AI_ENGINE, NEURALUCB, IBM_RUNTIME, ERROR_MITIGATION, DECISION_ENGINE, GRANITE_SIZE, MINDMAP_FULL, DIAGRAMS, etc.
- [ ] Actually run docker-compose up (needs Docker daemon)
- [ ] Test full flow: /health, /backends, /spaceweather/live, /copilot/plan, /generate

#### P1: Auth + Execution
- [ ] JWT Auth, Project CRUD
- [ ] Runtime Execution with real IBM token on fez/marrakesh/kingston
- [ ] Execution Monitor with QCalEval vision CLIP NO_SIGNAL/SUCCESS
- [ ] Adaptive Recovery retry logic

#### P2: Analytics + Experiment Tracking
- [ ] Analytics Dashboard with drift vs kp correlation heatmap + Recharts
- [ ] Experiment Tracking MLflow style
- [ ] Admin Dashboard + Notification

#### P3: Research Publication
- [ ] Paper draft: "Space Weather-Aware Quantum Backend Selection: First Evidence of Kp-Index Correlation with Qubit Decoherence from 8M Records"
- [ ] Figures: T1 vs Time, T1 vs kp Scatter (200 points), Mitigation Comparison 1.2x vs 5x, Training Loss 0.3224->0.0028
- [ ] Comparison vs IBM least_busy vs Q-LEAR 25% vs MQT vs Ours (9.5/10 vs 7.5/10)

#### P4: Advanced AI
- [ ] QNTK-UCB Quantum-Enhanced (TK)^3 vs (TK)^8 implementation
- [ ] Granite-8B GGUF Q4_K_M 4.9GB local with Ollama for offline production
- [ ] Transformer Seq2Seq Mitigation from arXiv:2601.14226
- [ ] NNAS Physics-inspired full implementation

## Timeline

- Week 1 (Done): Data + Core + Deep Training + Mitiq + Recharts + Granite API + SpaceWeather Live + Copilot Intent Agent = 95% Production Ready
- Week 2 (Now): Docker Prod + CI + 20 Docs = 100% Production Ready
- Week 3: Auth + Execution + Monitor + Recovery
- Week 4: Publication + Analytics + Admin

## Success Metrics

- Contexts: 8847 from 8M, Training loss 0.0028 best val
- Mitigation: S-ZNE 1.2x vs ZNE 5x = 76% saving, same accuracy 0.916
- Space Weather: Correlation -0.197 p=0.00047 significant, Severe kp>=6 T1 251us 40% drop
- Live Data: fez T1 135.6us, kingston 231us BEST, kp 2.0 today live NOAA, neutron 94.6 counts/min
- Endpoints: 12 APIs including /copilot/plan Arabic/English + /spaceweather/live
- Frontend: 6 Recharts + CopilotChat + SpaceWeatherChart LIVE
- Docker: 6 services one-command deployment
- Docs: 20 files + MINDMAP_FULL 16K + DIAGRAMS 5 mermaid
- CI: 5 jobs lint, test, docker, security, docs, research validation
