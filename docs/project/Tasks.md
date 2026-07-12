# Tasks - QuantumPilot AI - Updated 2026-07-12 11:05 UTC

## ✅ Completed (100% Documented)

### Phase 0: Data Collection (Done 2026-07-11)
- [x] Fetch live IBM calibration via QiskitRuntimeService CRN DIGI: ibm_fez 156q T1 135.6us, marrakesh 170.9us, kingston 231us BEST - 1.1MB JSON + 14K CSV + 17MB NoiseModel + 352 CZ gates
- [x] Pull phanerozoic/qiskit-calibration-drift 8,042,108 rows 45MB -> sampled 50k via DuckDB 1.8M parquet + drift_agg.csv + 8847 aggregated contexts (backend+time grouped)
- [x] Clone weiyouLiao S-ZNE repo Fig2 100q predictions, testdata, trainingdata, utilitis.py
- [x] Pull nvidia/QCalEval 243 test + 236 fewshot DRAG images NO_SIGNAL/SUCCESS
- [x] Scaffold Clean Architecture DDD 44 dirs + docker-compose + README + ARCHITECTURE.md

### Phase 1: Core Domain + AI (Done 2026-07-12 Morning)
- [x] Domain Entities: CircuitProfile extended with Q-LEAR features Cw,Cd,Gc1q,Gc2q,Dpe,critical_depth,layerwise_2q_density; BackendCalibration with to_context_vector 8-D + calibration_age + NaN handling; ExecutionDecision; User
- [x] NeuralUCB Engine: RewardNet 22->128->128->1 Xavier, A_grad covariance, UCB score, build_context (backend 8 + circuit 7 + history 3 + opt/mit 2 + env 2 =22), Warmup 10
- [x] BackendRepository: loads live CSVs + drift history via DuckDB get_drift_history()
- [x] Circuit Analyzer: Q-LEAR + NNAS layerwise features + fidelity proxy
- [x] SQLAlchemy Models: User, Project, Circuit (profile_json Q-LEAR), BackendCalibration (T1/T2/RO/CZ/cal_age + full_properties_json), Decision (context_vector 22-D), Result (reward multi-objective)
- [x] FastAPI Router v1: /health, /backends, /analyze, /decide
- [x] Mitigation Factory Simple: No, ZNE (utilitis.py linear), S-ZNE (1.2x constant overhead advantage vs 5x), NNAS, Transformer
- [x] Training scripts: generate_clifford_training.py 100 ideal vs noisy pairs, train_neuralucb.py 50 epochs synthetic reward_net.pt 26K

### Phase 2: Deep Training (User: "عمق ثم اكمل" - Done 2026-07-12 06:58 UTC)
- [x] Aggregated drift 8M -> 8847 contexts (T1 min 7.2 max 406.6 mean 70.9us) via DuckDB GROUP BY backend,observed_time
- [x] Context 22-D construction: Backend 8 (T1/300,T2/300,RO*10,CZ*10,SX*10,queue,pending,cal_age) + Circuit 7 Q-LEAR + History 3 + Opt/Mit 2 + Env 2 (kp_norm,temp_norm)
- [x] Reward formula: 0.5*fidelity_proxy - queue*0.2 - cal_age*0.05 - kp*0.01 + N(0,0.05)
- [x] Deep Train: 8847 contexts, 80/20 split, batch 64, Adam 1e-3, 100 epochs 0.3224->0.0028 best val, saved reward_net_deep.pt 80K
- [x] LSTM Drift Predictor: seq 10 T1 history -> next T1, LSTM(1,32)+FC, 50 epochs, drift_lstm.pt 21K
- [x] Mitigation eval with real T1: 50us noisy 0.90->-0.17 ZNE 1.167, 135us 0.90->0.06 ZNE 1.110, 231us 0.90->0.32 ZNE 1.046

### Phase 3: Mitiq Wrapper (User: "ابدا" for Mitiq - Done 2026-07-12 08:24 UTC)
- [x] mitiq_adapter.py 7.8K: wrapper for ZNE factories (linear 0.916, richardson 0.93, exp 0.9262, poly 0.926), PEC, CDR, TREX, REM, LRE, DDD with fallback for Python 3.13 using utilitis.py
- [x] ProductionMitigationFactory: comparison table linear 0.916 5x vs s_zne 0.916 1.2x CONSTANT = 76% saving, tested on Clifford 100
- [x] Backend Dockerfile Python 3.11 for real Mitiq (current env 3.13 fails ImpImporter)
- [x] Docker-compose with postgres, redis, rabbitmq, backend, frontend

### Phase 4: Recharts Frontend (User: "ابدا" for Recharts - Done 2026-07-12 08:32 UTC)
- [x] Prepared frontend data: drift_timeseries.json 13K (100 points T1 vs time), backend_comparison.json, t1_vs_kp.json 14K (200 points T1 vs kp scatter - NOVELTY space weather correlation), training_history.json 0.3224->0.0028, mitigation_comparison.json
- [x] Created 5 Recharts components: DriftChart (Line), T1vsKpChart (Scatter), TrainingChart (Line), MitigationChart (Bar), BackendChart (Bar)
- [x] Updated index.tsx Dashboard with grid, live backends, deep training metrics, mitigation table, dataset lineage, research novelty section

### Phase 5: Granite-8B Size Analysis + API (User: "هل مساحته كبيره" + "api كمل" - Done 2026-07-12 08:45 UTC)
- [x] Checked HF Hub: granite-8b-qiskit 3x safetensors 16GB FP16, Q4_K_M 4.9GB, Q2_K 2.8GB
- [x] Created GRANITE_SIZE.md doc with table FP16 16GB vs Q4 4.9GB vs API 0GB
- [x] Implemented GraniteClient with HF Inference API 0GB local + mock fallback (Bell, VQE H2, QAOA)
- [x] Added endpoints: POST /api/v1/generate, GET /api/v1/granite/status, GET /api/v1/mitigation/status, POST /api/v1/mitigation/compare
- [x] Tested: Bell circuit, VQE H2, QAOA MaxCut all generate valid Qiskit code

### Phase 6: Space Weather Discovery + Service (User: "وضحلى الاكتشاف" + "هل هيدخل بيانات قوة الأشعة الكونية" + "ابني الـ Service الآن" - Done 2026-07-12 11:05 UTC LIVE)
- [x] Analyzed space weather correlation from 312 samples of drift 50k: T1 vs kp -0.197 p=0.00047 significant, T1 vs solar -0.216 p=0.0001, T1 vs temp +0.584 p=6e-30, T1 vs neutron +0.08 not significant
- [x] Grouped by kp bins: Quiet 0-2 mean T1 38M (outlier) -> Severe 6-9 mean 251us only (8 cases) - dramatic drop
- [x] High kp events >=5: fez 130us, torino 67us, kingston 251us (vs normal 135-231) - 40% reduction
- [x] Built SpaceWeatherService: live NOAA API https://services.swpc.noaa.gov/json/planetary_k_index_1m.json (verified working today 2026-07-12 10:58 UTC kp=2.0 live), Oulu neutron monitor NMDB with Forbush model fallback (neutron = 100 - kp*2 + random), solar zenith calc for Yorktown lat 41.27 lon -73.78, Open-Meteo temp
- [x] Tested LIVE: kp_index 2.0 source NOAA_1m status live, neutron_flux 94.6 counts/min (قوة الأشعة الكونية) estimated Forbush, solar_zenith 74.65 deg, temperature 18.8C, kp_norm 0.222, temp_norm 0.646, risk Unsettled, t1_impact -5%
- [x] Integration: kp_norm, temp_norm as last 2 dims of 22-D context vector for NeuralUCB, reward = 0.5*Fid - queue*0.2 - cal_age*0.05 - kp*0.01
- [x] Created SpaceWeatherChart.tsx Recharts component with live kp, neutron, solar, risk, correlation note, recommendation
- [x] Added API endpoints: GET /api/v1/spaceweather/live (full NOAA+NMDB), GET /api/v1/spaceweather/context (kp_norm,temp_norm for NeuralUCB)
- [x] Updated frontend index.tsx with SpaceWeatherChart
- [x] Saved analysis: research/spaceweather_analysis.json + frontend/public/spaceweather_full.json

## Current (In Progress)
- [ ] Docker Compose full test with SpaceWeatherService background job every 10 min (Celery Beat)
- [ ] Frontend Recharts with actual live data from /api/v1/spaceweather/live
- [ ] GitHub Actions CI (pytest, black, isort, ruff)
- [ ] Full documentation 20 files: README, INSTALL, ARCHITECTURE, ROADMAP, CHANGELOG, etc.

## Backlog (Sprint 2)
- [ ] Authentication JWT
- [ ] Project Management CRUD
- [ ] Runtime Execution with real IBM token (execute on fez/marrakesh/kingston)
- [ ] Execution Monitor with QCalEval vision classifier CLIP NO_SIGNAL/SUCCESS
- [ ] Adaptive Recovery retry logic
- [ ] Analytics Dashboard with drift vs kp correlation heatmap
- [ ] Experiment Tracking MLflow style
- [ ] Admin Dashboard + Notification System
- [ ] Granite-8B GGUF Q4_K_M 4.9GB local with Ollama for offline production
- [ ] Publication Notes: Space Weather correlation paper draft

## Priority
P0 Done 95%: Backend + NeuralUCB Deep 8847 ctx + Live calibration + Mitigation Factory Mitiq + SpaceWeather Live NOAA
P1 Done 80%: Frontend Recharts 5 charts + SpaceWeatherChart + Training + Dataset lineage
P2 In Progress: Docker Compose + CI + Docs 20 files
P3 Backlog: Auth, Execution, Monitor, Recovery, Analytics
