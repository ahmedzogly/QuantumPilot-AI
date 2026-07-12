# TESTING - QuantumPilot AI

## Test Structure (Clean Architecture)

```
backend/tests/
├── unit/
│   ├── test_circuit_analyzer.py - Q-LEAR Cw,Cd,Gc1q,Gc2q,Dpe
│   ├── test_backend_calibration.py - T1_mean, context_vector 8-D, NaN handling
│   ├── test_neuralucb.py - RewardNet 22->128->128->1, UCB, build_context 22-D
│   ├── test_mitigation_factory.py - ZNE 0.916 5x vs S-ZNE 1.2x constant
│   ├── test_spaceweather_service.py - NOAA kp live 2.0, neutron 94.6
│   └── test_copilot_agent.py - CHEAPEST "أقل تكلفة", HIGHEST_FIDELITY "Fidelity >95%"
├── integration/
│   ├── test_backend_repository.py - Loads live ibm_fez 135.6us etc from CSVs
│   ├── test_drift_dataset.py - DuckDB 8847 contexts from 8M
│   └── test_api_endpoints.py - FastAPI TestClient /health, /backends, /spaceweather/live, /copilot/plan
└── e2e/
    └── test_full_flow.py - Circuit -> Analyzer -> Decide (72 arms) -> Mitigate -> Reward
```

## Running Tests

```bash
cd backend
# Unit
pytest tests/unit -v --cov=app --cov-report=xml
# Integration
pytest tests/integration -v
# E2E
pytest tests/e2e -v

# All with coverage
pytest tests/ -v --cov=app --cov-report=html
```

## Coverage Goals

- Unit: >80% for domain entities, use cases
- Integration: BackendRepository loads live CSVs, drift 50k
- E2E: Full flow from QASM to Decision with live space weather kp 2.0

## Test Data (Real Data We Pulled Today)

- Live calibration: ibm_fez_properties.json 1.1MB, ibm_fez_qubits_full.csv 14K, 352 CZ mean 3.33%
- Drift: drift_50k.parquet 1.8M, 8847 aggregated contexts T1 7.2-406.6 mean 70.9us
- Clifford: clifford_training_100.json 44K ideal vs noisy fidelity 94.3% avg
- Space Weather: NOAA kp 1m API live verified 2026-07-12 10:58 UTC kp=2.0, neutron 94.6

## Mock Strategy

- For IBM Quantum: use Fake backends (FakeBrisbane etc) with real properties snapshot when no token
- For NOAA: mock with historical mean 2.2 if API fails, Forbush model for neutron
- For Granite-8B: mock fallback with plausible Qiskit templates (Bell, VQE H2, QAOA) when HF API not available (transformers missing)

## CI Integration

- GitHub Actions CI: 5 jobs lint, test, docker-build-test, security-scan, docs-check, research-validation
- Tests run with Postgres 15-alpine and Redis 7-alpine services
- Docker build test for backend Python 3.11 (Mitiq) + frontend Node 20

## Example Test

```python
def test_circuit_analyzer_qlear():
    from app.application.use_cases.analyze_circuit import CircuitAnalyzer
    from qiskit import QuantumCircuit
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cx(0,1)
    analyzer = CircuitAnalyzer()
    profile = analyzer._from_qiskit(qc, "VQE")
    assert profile.Cw == 3
    assert profile.Gc2q == 1
    assert profile.qlear_feature_vector == [3, depth, ...]

def test_neuralucb_context_22d():
    # Backend 8 + Circuit 7 Q-LEAR + History 3 + Env 2 + Opt/Mit 2 =22
    assert len(context) == 22
    assert context[0] == T1/300 etc.
```

## Live Testing

- test_api.py: FastAPI TestClient /health, /backends (live fez 135.6us), /spaceweather/live (NOAA kp 2.0 live)
- Scripts: scripts/deep_train.py trains RewardNet 8847 contexts loss 0.3224->0.0028 best val -> 80K
- Scripts: scripts/prepare_frontend_data.py creates frontend/public/*.json for Recharts
