# IBM_RUNTIME - QuantumPilot AI - Live Integration

## Live Data Pulled Today (Verified 2026-07-12)

### IBM Quantum Account
- **CRN:** crn:v1:bluemix:public:quantum-computing:us-east:a/abd845cfd9bc4a37898488294645cbc3:cdf67559-abcb-4675-8486-cf736ffe4e3c:: (Name: DIGI, Region us-east, State active, Created 2026-07-11)
- **Token:** 9ac9duxenBehY3CqCjHEJ8Eivbk4J0T6ZvU5Tcn-zcLo (IBM Cloud API Key, used for IAM token exchange)
- **CRN Discovery:** Via resource-controller.cloud.ibm.com/v2/resource_instances -> 1 instance found DIGI
- **IAM Exchange:** https://iam.cloud.ibm.com/identity/token grant_type apikey -> access_token with IBMid, email, account bss

### Backends Operational (via QiskitRuntimeService channel ibm_cloud)

**From backend.properties() to_dict() - Full JSON 1.1MB each:**

#### ibm_fez - 156q Heron R2 - Best for T1? Actually kingston best
- **Version:** 1.3.37, **Last Update:** 2026-07-11 15:52:49+00:00
- **Basis Gates:** ['cz', 'id', 'rz', 'sx', 'x'] + ['rzz'] in gates list
- **Qubits:** 156 entries, each with T1, T2, readout_error, prob_meas0_prep1, prob_meas1_prep0, readout_length, anharmonicity, frequency (in older - now not)
- **Stats:** T1 mean 135.6us, T2 mean 106.3us, RO mean 2.23%, CZ count 352 mean 3.33% median 0.29% max 100% for [72,73] faulty
- **Gates:** 1796 total: cz 352, rzz 352, id 156, rx 156, rz 156, sx 156, x 156, reset 156, measure 156 - each with gate_error, gate_length 68ns for cz, 24ns for id
- **Files Saved:** ibm_fez_properties.json 1.1M, ibm_fez_qubits_full.csv 14K (qubit,T1,T2,RO,prob...), ibm_fez_cz_errors.csv 13K, ibm_live_noise_model.json 17M (NoiseModel.from_backend)

#### ibm_marrakesh - 156q
- Last Update: 2026-07-11 16:12:14+00:00
- T1 mean 170.9us, T2 100.4us, RO 2.73%, CZ mean 4.52% median 0.29%
- Similar structure

#### ibm_kingston - 156q BEST
- Last Update: 2026-07-11 16:39:51+00:00
- T1 mean 231.0us, T2 159.7us, RO 2.18%, CZ mean 2.92% median 0.20% - BEST
- This is chosen for highest_fidelity intent

### QiskitRuntimeService Usage

```python
from qiskit_ibm_runtime import QiskitRuntimeService
# With CRN discovered via resource-controller
service = QiskitRuntimeService(channel="ibm_cloud", token=TOKEN, instance=CRN)
backends = service.backends(simulator=False, operational=True)
# Returns [ibm_fez, ibm_marrakesh, ibm_kingston] operational (3)
backend = service.backend("ibm_fez")
props = backend.properties() # BackendProperties
config = backend.configuration().to_dict()
status = backend.status().to_dict() # operational True, pending 0
```

### NoiseModel

```python
from qiskit_aer.noise import NoiseModel
noise_model = NoiseModel.from_backend(backend)
# Basis gates: ['cz', 'delay', 'id', 'if_else', 'measure', 'reset', 'rz', 'sx', 'x']
# Instructions with noise: ['id', 'sx', 'x', 'measure', 'reset', 'cz']
# Qubits with noise: [0..155]
# Specific errors: 156 id, 156 sx, 156 x, 156 reset, 352 cz, 156 measure
```

### Historical Drift Dataset - phanerozoic/qiskit-calibration-drift

- 8,042,108 rows 45MB parquet original at /home/user/.cache/huggingface/.../train-00000-of-00001.parquet
- Sampled 50k via DuckDB -> drift_50k.parquet 1.8M + drift_50k.csv 12M + drift_agg.csv
- Columns: backend (fez, marrakesh, kingston, torino), property_family (T1, T2, readout_error, sx_error, cz_error...), property (T1, T2, readout_error...), qubit_a 0-155, qubit_b, value, unit, scope, is_failure_ceiling, observed_time timestamp, calibrated_time, snapshot_update_time, calibration_age_seconds, is_new_measurement, chipwide_recal_event_id, latitude 41.27, longitude -73.78, solar_zenith_deg, temperature_c, pressure_hpa, humidity_pct, bz_gsm_nt, neutron_flux, kp_index, ap_index, Ap_daily, SN, f107, dst_nt
- Used for: Drift Predictor LSTM, NeuralUCB context, Space Weather correlation, T1 vs kp -0.197 p=0.00047

### Calibration Refresh Job

- Celery Beat every 1h: refresh_calibration task -> QiskitRuntimeService -> properties -> Postgres backend_calibrations + Redis
- File: backend/app/core/tasks.py

### Frontend Integration

- BackendChart shows T1 135.6us, T2 106.3us live
- DriftChart shows T1 vs time from drift_50k 100 points
- SpaceWeatherChart shows live kp 2.0 today + neutron 94.6

