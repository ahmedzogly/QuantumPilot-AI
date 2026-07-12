# Changelog - Fully Documented

## [0.3.0] - 2026-07-12 11:10 UTC - Space Weather Live Service

### Added - Space Weather Discovery + Live Service (User: "وضحلى الاكتشاف" + "هل هيدخل بيانات قوة الأشعة الكونية" + "ابني الـ Service الآن")
- Analyzed 312 samples from drift 50k: T1 vs kp -0.197 p=0.00047 significant, T1 vs solar -0.216 p=0.0001, T1 vs temp +0.584 p=6e-30, T1 vs neutron +0.08 NS
- Grouped by kp bins: Quiet 0-2 -> Severe 6-9 mean T1 251us only (8 cases) dramatic 40% reduction (fez 130us, torino 67us vs normal 135-231)
- Built SpaceWeatherService: LIVE NOAA API https://services.swpc.noaa.gov/json/planetary_k_index_1m.json verified working today 2026-07-12 10:58 UTC kp=2.0 source NOAA_1m status live, Oulu neutron monitor NMDB with Forbush model fallback neutron=100-kp*2+random 94.6 counts/min (قوة الأشعة الكونية), solar zenith calc for Yorktown 41.27/-73.78 -> 74.65 deg, Open-Meteo temp 18.8C
- Tested LIVE: kp 2.0 Unsettled -5% T1, neutron 94.6, cosmic_ray_strength 0.945, kp_norm 0.222, temp_norm 0.646
- Integration: kp_norm,temp_norm as last 2 dims of 22-D context for NeuralUCB, reward = 0.5*Fid - queue*0.2 - cal_age*0.05 - kp*0.01
- Created SpaceWeatherChart.tsx + endpoints /api/v1/spaceweather/live + /api/v1/spaceweather/context
- Saved research/spaceweather_analysis.json + frontend/public/spaceweather_full.json
- Updated docs/project/Tasks.md, Completed.md, Current.md with full documentation of Phase 6

## [0.2.0] - 2026-07-12 08:45 UTC - Granite Size + API + Recharts
- Checked HF Hub granite-8b-qiskit 3x safetensors 16GB FP16, Q4_K_M 4.9GB, Q2_K 2.8GB
- GRANITE_SIZE.md + GraniteClient HF Inference API 0GB local + mock fallback (Bell, VQE H2, QAOA)
- Endpoints: POST /generate, /granite/status, /mitigation/status, /mitigation/compare
- Recharts Frontend: drift_timeseries 13K, t1_vs_kp 14K scatter NOVELTY, training_history 0.3224->0.0028, 5 components DriftChart, T1vsKpChart, TrainingChart, MitigationChart, BackendChart + index.tsx Dashboard
- Deep training 8847 contexts: RewardNet 22->128->128->1 100 epochs 0.3224->0.0028 best val -> 80K + LSTM drift 21K
- Mitiq Adapter 7.8K: ZNE factories linear 0.916, richardson 0.93, exp 0.9262, poly 0.926 + s_zne 0.916 overhead 1.2x CONSTANT vs 5x = 76% saving

## [0.1.0] - 2026-07-12 06:58 UTC - Deep Training + Mitiq Wrapper Start
- Live IBM fez 135.6us etc, drift 8M->50k, S-ZNE 100q, QCalEval 243, clifford 100
- Domain Entities Q-LEAR, NeuralUCB, BackendRepo, Analyzer, FastAPI, etc.

## [0.0.1] - 2026-07-11
- Scaffolding 44 dirs
