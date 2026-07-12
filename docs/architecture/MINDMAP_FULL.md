# QuantumPilot AI - الخريطة الذهنية الكاملة للتنفيذ
## Mind Map - Production & Research Grade

> هذه الخريطة هي المرجع الوحيد لتنفيذ المنصة - كل شيء مترابط

```mermaid
mindmap
  root((QuantumPilot AI<br/>NeuralUCB Autopilot))
    Domain_Core[Domain Core - DDD]
      Circuit_Entity
        QASM
        Qiskit Code
        Profile[Cw,Cd,Gc1q,Gc2q,Dpe,Depth,Width,Entanglement]
        AlgorithmType[VQE,QAOA,Grover,QFT,Custom]
      BackendCalibration
        Live_fez__marrakesh__kingston[T1_mean: 135-231us<br/>T2_mean: 100-159us<br/>RO: 2.2%<br/>CZ: 2.9% mean]
        Drift_8M[phanerozoic 8.04M<br/>50k Sample<br/>+ Space Weather<br/>kp_index, neutron_flux, solar_zenith]
        Context_Vector_22D[8 backend + 7 circuit + 3 history + 2 opt/mit + 2 pad]
      ExecutionDecision
        backend_id
        opt_level[0,1,2,3]
        mitigation[S_ZNE,ZNE,PEC,CDR,TREX,NNAS,Transformer,DAEM]
        confidence_UCB
      Reward
        Fidelity_0.5
        Time_0.2
        Queue_0.2
        Cost_0.1
    AI_Engine[AI Engine - The Brain]
      NeuralUCB_Classical
        RewardNet[22->128->128->1 Xavier]
        A_grad_covariance[lambda*I + sum g g^T]
        UCB_score[ f_theta + alpha*sqrt(g^T A^-1 g) ]
        Warmup_10_random
        Buffer_32_recent
      QNTK_UCB_Future[arXiv:2601.02870<br/>Omega((TK)^3) vs (TK)^8<br/>Frozen QNN + Kernel Ridge]
      Drift_Predictor_LSTM[Input: T1 history + kp_index + temperature<br/>Output: T1 after 2h]
      Granite_8B_Code_Assistant[Qiskit/granite-8b-qiskit<br/>46.5% HumanEval<br/>Code Gen + Fix Deprecated<br/>RAG: Neura-parse 113k]
    Mitigation_Factory[Error Mitigation Manager - Factory]
      Mitiq_Wrapper
        ZNE[Linear,Richardson,Exp<br/>fold_global, local, random]
        PEC[Pauli-Lindblad sparse]
        CDR[vnCDR near-Clifford]
        REM[Confusion Matrix]
        LRE[Layerwise Richardson]
        TREX[Readout Extinction exp]
      S_ZNE_Constant_Overhead[weiyouLiao paper<br/>100q Ising/Heisenberg<br/>Only constant measurement<br/>truncation=2]
      NNAS_Physics_Inspired[arXiv:2501.04558<br/>Noise Accumulation Surrogate<br/>Layer-wise error<br/>-50% error, -10x data]
      Transformer_Seq2Seq[arXiv:2601.14226<br/>Attention best for 5q IBM<br/>No retrain across similar QPUs]
      Noise_Agnostic_DAEM[Nature 2025<br/>Quantum Augmentation<br/>No noise model, no clean data]
      Clifford_Training_Generator[arXiv:2606.02697<br/>80% Clifford + 20% RZ<br/>100 pairs ideal vs noisy]
      AVPP[Adaptive Variational<br/>Kaggle]
    Infrastructure
      Qiskit_Runtime
        Backend_Repository[QiskitRuntimeService<br/>CRN DIGI<br/>fez, marrakesh, kingston]
        NoiseModel_from_backend
        Transpiler[opt_level 0-3]
      Persistence
        Postgres[users, projects, circuits, decisions, results]
        Redis[Calibration Cache<br/>Queue Length]
        RabbitMQ[Execution Jobs]
        Parquet[Datasets]
          drift_50k.parquet[50k]
          clifford_100[ideal vs noisy]
          szne_repo[Fig2 predictions]
          qcaleval_243[DRAG images]
      Messaging_EventDriven[ExecutionCompleted -> LearningEngine]
    Application_UseCases
      AnalyzeCircuit[QASM -> Profile]
      SelectBackend[Filter by T1>30,T2>20,RO<5%]
      MakeDecision[NeuralUCB.select(contexts 72 arms)]
      ExecuteAndLearn[Orchestrator]
      AdaptiveRecovery[Retry, Switch Backend, Change Mitigation]
    Presentation_API
      FastAPI_v1
        health
        backends[GET live calibration]
        analyze[POST QASM -> Profile]
        decide[POST -> DecisionResponse]
        execute[POST -> job id]
        dashboard[WebSocket queue]
        generate[Granite code gen]
    Frontend_NextJS
      Dashboard
        BackendHealth[T1/T2 charts Recharts]
        DriftChart[Time vs T1 + kp_index correlation]
        DecisionFlow[UCB scores]
        ExperimentTracking
      Admin
      Analytics[Reward history]
    16_Modules_Checklist
      1_Auth[JWT]
      2_Project_Mgmt[CRUD]
      3_Circuit_Analyzer[Done 80%]
      4_Backend_Selection[Done: live fez]
      5_NeuralUCB_Engine[Done: RewardNet]
      6_Circuit_Optimization[Granite]
      7_Mitigation_Manager[Factory S-ZNE+Mitiq]
      8_Runtime_Execution[Qiskit Runtime]
      9_Execution_Monitor[QCalEval Vision]
      10_Adaptive_Recovery[Retry logic]
      11_Learning_Engine[Online update A]
      12_Analytics_Dashboard[Recharts]
      13_Experiment_Tracking[MLflow style]
      14_API[FastAPI Done 50%]
      15_Admin_Dashboard
      16_Notification[Email/Webhook]
    Research_Novelty
      MultiObjective[Accuracy + Queue + Cost]
      ConstantOverhead_S_ZNE
      SpaceWeather_Correlation[kp, neutron, solar]
      QNTK_UCB_QuantumAdvantage
      Comparison[IBM least_busy vs Q-LEAR 25% vs MQT vs Ours]
    DevOps_Production
      DockerCompose[postgres, redis, rabbitmq, backend, frontend]
      GitHub_Actions[pytest, black, isort, ruff]
      Logging[structlog]
      Security[JWT, SECRET_KEY]
      Testing[Unit, Integration, e2e]
    Sprints
      Sprint1_MVP[Auth, Project, Analyzer, BackendRepo, FastAPI 50% Done]
      Sprint2_Brain[NeuralUCB train on 50k+100 + Mitigation Factory + Granite]
      Sprint3_Prod[Frontend + Monitor + Recovery + Docker + Docs 20 files]
```

---

## الخريطة النصية التفصيلية (للتنفيذ الفوري)

### 1. القلب - Domain Layer (اللي اتبنى 60%)
```
Circuit (Entity)
├── id: uuid
├── name: VQE-H2
├── profile: CircuitProfile (Q-LEAR features)
│   ├── Cw: width (circuit width)
│   ├── Cd: depth
│   ├── Gc1q: #1q gates
│   ├── Gc2q: #2q gates (entanglement source)
│   ├── Dpe: subcircuit error (from Q-LEAR)
│   ├── entanglement_ratio: 2q/(1q+2q)
│   └── algorithm_type: VQE/QAOA/Grover
└── qasm/qiskit_code

BackendCalibration (Entity) - من البيانات الحية اللي سحبناها اليوم
├── backend_name: ibm_fez (156q, Heron R2)
├── last_update: 2026-07-11 15:52 UTC (Live!)
├── T1_mean: 135.6us [fez] / 170.9 [marrakesh] / 231 [kingston best]
├── T2_mean: 106.3us
├── readout_error_mean: 2.23%
├── cz_error_mean: 3.33% (median 0.29%, max 100% for faulty [72,73])
├── queue_length: from IBM API
├── calibration_age_seconds: from drift dataset
├── to_context_vector() -> 8-D normalized
└── qubits: List[QubitCalibration (is_good if RO<5% && T1>30us)]

ExecutionDecision (Aggregate Root) - ناتج NeuralUCB
├── backend_name: ibm_kingston (chosen)
├── optimization_level: 0-3
├── mitigation_strategy: S_ZNE (from S-ZNE paper constant overhead)
├── shots: 4096
├── expected_fidelity: from proxy
├── confidence: UCB bonus
└── context_vector: 22-D full

ExecutionResult + Reward
├── fidelity: Hellinger
├── execution_time, queue_time, cost
└── reward = 0.5*fidelity -0.2*time -0.2*queue -0.1*cost (multi-objective)
```

### 2. المخ - AI Engine

```
NeuralUCB (backend/app/infrastructure/ai/neuralucb/engine.py - Done)
├── RewardNet: 22 -> 128 ReLU -> 128 ReLU -> 1 (Xavier init)
├── A_grad: lambda*I + sum(grad * grad^T) (exploration covariance)
├── select(contexts[72 arms]) -> chosen_idx, UCB_scores
│   ├── contexts = 3 backends * 4 opt * 6 mitigation = 72
│   ├── 72 context = backend[8] + circuit[7] + history[3] + opt/mit[2] + pad[2]
│   └── UCB = f_theta(ctx) + alpha * sqrt(g^T A^-1 g)
├── update(context, reward): online Adam + update A_grad + buffer 32
├── build_context(circuit_profile, backend, history): 22-D
└── Warmup: 10 random arms

QNTK-UCB (Future - arXiv:2601.02870)
├── Frozen QNN random init -> QNTK kernel
├── Ridge regression with static kernel
├── Scaling (TK)^3 vs (TK)^8 classical -> quantum advantage low-data
└── qntk_engine.py

Drift Predictor (New from 8M dataset)
├── Dataset: phanerozoic 8M rows: T1 history + temperature, pressure, kp_index, neutron_flux, solar_zenith
├── Model: LSTM input (T1(t-10..t) + env features) -> T1(t+2h)
└── Feature: calibration_age_seconds critical for NeuralUCB

Granite-8B (LLM for Qiskit)
├── Model: Qiskit/granite-8b-qiskit 8B params, 46.5% Qiskit HumanEval
├── Use: Code gen, Fix deprecated code, Transpilation suggestions
├── RAG: Neura-parse 113k corpus (ZNE folding, PEC Lindblad, CDR)
└── Service: vLLM sidecar /api/v1/generate
```

### 3. مصنع تخفيف الأخطاء - Mitigation Factory (التميز البحثي)

```
MitigationManager (factory pattern)
├── Mitiq Wrapper (Python 3.11 Docker - currently Python 3.13 fails)
│   ├── ZNE: fold_global, fold_local, fold_random, Linear/Richardson/Exp Factory
│   ├── PEC: sparse Pauli-Lindblad model
│   ├── CDR: near-Clifford training
│   ├── REM: confusion matrix
│   ├── LRE: Layerwise Richardson (2402.04000)
│   └── TREX, VD (experimental)
├── S-ZNE (weiyouLiao repo - Done cloned)
│   ├── Surrogate: classical learning h(x,O,lambda)
│   ├── Constant overhead: only constant measurement for family of circuits
│   └── Theorem: error ≤ zeta^2 + O(L^2 u B^2 / M) same as ZNE
├── NNAS (arXiv:2501.04558) - Physics-inspired
│   ├── Captures noise accumulation across layers
│   ├── -50% error, -10x data for deep circuits
│   └── Implement: layer index + noise accumulation pattern
├── Transformer Seq2Seq (arXiv:2601.14226)
│   ├── Attention best for 5q IBM data
│   └── Generalization across similar QPUs without retrain
├── Noise-agnostic DAEM (Nature 2025)
│   └── Quantum augmentation, no noise model, no clean data
├── Clifford Generator (arXiv:2606.02697 + our script)
│   ├── 80% Clifford (h,s,x,cx) + 20% RZ arbitrary
│   ├── Generates ideal vs noisy counts pairs (done: 100 pairs)
│   └── Transfers across Hamiltonians
└── AVPP (Kaggle)
    └── VQC post-processing V(θ)|ψ> ≈ E^-1 |ψ>
```

### 4. البيانات - Datasets (تم سحبها فعلاً)

```
Live Calibration (from your CRN DIGI today)
├── ibm_fez_properties.json 1.1MB last 2026-07-11
├── ibm_fez_qubits_full.csv 14K: qubit, T1, T2, RO, prob_meas0_prep1
├── ibm_fez_cz_errors.csv 13K: 352 CZ gates mean 3.33%
├── marrakesh, kingston similarly
└── noise_model 17MB

Historical Drift (phanerozoic)
├── 8,042,108 rows total 45MB parquet original
├── 50k sample drift_50k.parquet (1.8MB) + 12M CSV via DuckDB
├── drift_agg.csv: backend, property_family, mean, std
├── Columns: backend, property, qubit_a, value, observed_time, calibrated_time, calibration_age_seconds, is_new_measurement, chipwide_recal_event_id, latitude 41.3, longitude -73.78, solar_zenith, temperature_c, pressure_hpa, humidity, bz_gsm, neutron_flux, kp_index, ap, SN, f107
└── Use: Pretrain NeuralUCB + Drift Predictor + Space weather correlation novelty

S-ZNE Repo (weiyouLiao)
├── Fig2/predictions: heisen_100q_-0.1J_-0.5h_depo predictions 10-200 sample
├── Fig2/testdata + trainingdata + vqa_loss
├── Fig3 + SM
├── utilitis.py: extrapolation methods linear, quadratic, cubic, spline, exponential, richardson
└── Notebooks 1_fig2.ipynb, 2_fig3.ipynb

QCalEval (nvidia)
├── test 243 rows + fewshot 236 rows: id, experiment_type (drag), images list, q1-q6 prompts, answers, expected_status NO_SIGNAL/SUCCESS
└── Use: Vision Monitor to classify calibration plots

Neura-parse (113k)
├── train 102k, test 11.4k: concept, definition, formulas, code, framework
├── Topics: qemb-zero-noise-extrapolation, pec-pauli-lindblad, cdr, symmetry verification
└── Use: RAG for Granite

Clifford Training (Generated today)
├── clifford_training_100.json 44K: depth, num_qubits, ideal_counts, noisy_counts
└── Example: ideal {'00000':2065,'00010':2031} vs noisy with spread
```

### 5. تدفق التنفيذ الكامل (Flow)

```
User -> Frontend (Next.js) 
  -> POST /api/v1/analyze {qasm} 
    -> CircuitAnalyzer -> CircuitProfile(Cw,Cd,Gc1q,Gc2q,Dpe,Depth,Width)
  -> GET /api/v1/backends 
    -> BackendRepository: live fez/marrakesh/kingston (T1,T2,RO,CZ,Queue) + drift history + calibration_age
  -> POST /api/v1/decide
    -> For each of 72 arms: build_context = backend[8] + circuit[7] + history[3] + opt/mit[2] + pad[2] = 22-D
    -> NeuralUCB.select(contexts) -> UCB scores -> chosen arm (backend, opt_level, mitigation=S_ZNE)
    -> DecisionResponse {backend_name: ibm_kingston, opt_level:2, mitigation:S_ZNE, confidence:0.87}
  -> POST /api/v1/execute {decision_id}
    -> Qiskit Runtime: transpile with opt_level, apply mitigation factory (S-ZNE surrogate or Mitiq ZNE)
    -> ExecutionMonitor: poll job, check QCalEval vision classifier for calibration image
    -> If fail: AdaptiveRecovery -> retry with different backend or mitigation
    -> ExecutionResult: counts, fidelity, time, queue, cost
    -> Reward = 0.5*fidelity -0.2*time -0.2*queue -0.1*cost
    -> LearningEngine: NeuralUCB.update(context, reward) -> update A_grad + train RewardNet on buffer 32
    -> Postgres + Redis + Experiment Tracking
  -> Analytics Dashboard: Recharts for T1 drift vs kp_index, Reward history, UCB scores
```

### 6. الـ Tech Stack Mapping

```
Backend: FastAPI + Pydantic + SQLAlchemy + Alembic + Redis + RabbitMQ + PostgreSQL + Qiskit + Qiskit Runtime + Aer + Torch + Transformers + Datasets + DuckDB
Frontend: Next.js + Tailwind + TypeScript + Recharts + WebSocket
AI: NeuralUCB (RewardNet 22->128->128->1) + QNTK-UCB (future) + Granite-8B + LSTM Drift Predictor + Transformer Mitigator + NNAS
Mitigation: Mitiq (ZNE,PEC,CDR,TREX) + S-ZNE + NNAS + DAEM
DevOps: Docker Compose (postgres, redis, rabbitmq, backend py3.11 for Mitiq, frontend) + GitHub Actions (pytest, black, isort, ruff) + Logs + JWT + Black/isort/ruff
Docs: 20 files ARCHITECTURE.md, NEURALUCB.md, ERROR_MITIGATION.md, etc + Mermaid diagrams
```

### 7. خطة Sprints المحدثة بعد الفحص

```
Sprint1 MVP (Done 60% today):
- [x] Live calibration fetch fez/marrakesh/kingston
- [x] Drift 50k + agg + S-ZNE + QCalEval + Clifford 100
- [x] Domain Entities + NeuralUCB + BackendRepo + Analyzer + FastAPI router
- [ ] Add Q-LEAR features Cw,Cd,Gc1q,Gc2q to CircuitProfile
- [ ] SQLAlchemy models + Alembic migration
- [ ] Mitiq wrapper in Python 3.11 Docker

Sprint2 Brain:
- [ ] Train NeuralUCB on 50k + 100 cliff + live: pretrain -> online
- [ ] Implement Mitigation Factory: S-ZNE surrogate (utilitis.py) + Mitiq ZNE + NNAS layer accumulation
- [ ] Granite-8B microservice + Neura-parse RAG
- [ ] Drift Predictor LSTM with kp_index

Sprint3 Production & Research:
- [ ] Frontend Next.js: BackendHealth (T1/T2 charts), DriftChart (time vs T1 + solar), DecisionFlow (UCB), ExperimentTracking
- [ ] Execution Monitor with QCalEval vision (CLIP classify NO_SIGNAL/SUCCESS)
- [ ] Adaptive Recovery + Notification
- [ ] Full Docs 20 files + Mermaid + Comparison vs IBM least_busy vs Q-LEAR 25% vs MQT
- [ ] Publication Notes: Space Weather correlation novelty
```

---

هذه الخريطة هي **الـ Blueprint النهائي** - كل موديول له مصدر بياناته الحية اللي سحبناها اليوم والورقة البحثية المرتبطة.
