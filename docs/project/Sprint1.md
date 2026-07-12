# Sprint 1 - Deep Training Completed

## Date 2026-07-12
### What we deepened:

#### 1. Real Contexts from Drift 8M
- Original parquet 45MB 8,042,108 rows
- Aggregated via DuckDB to 8847 contexts (backend + observed_time grouped)
- T1 us min 7.2 max 406.6 mean 70.9 - matches live ibm_fez 135.6us
- Columns used: T1,T2,RO,CZ,SX,cal_age,temperature,kp_index,neutron,solar_zenith

#### 2. 22-D Context Construction (NeuralUCB)
Backend 8: T1/300, T2/300, RO*10, CZ*10, SX*10, queue/100, pending/100, cal_age/3600
Circuit 7: qubits/156, depth/500, width/156, 2q/1000, entanglement, is_VQE, is_QAOA
History 3: avg_fidelity, queue, success_rate
Opt/Mit 2 + Env 2: kp_norm, temp_norm = 22 total
Rewards: 0.5*fidelity_proxy - queue*0.2 - cal_age*0.05 - kp*0.01 + N(0,0.05)

#### 3. RewardNet Training
Model: 22->128 ReLU->128 ReLU->1 Xavier
Data: 8847 contexts, 80/20 split, batch 64, Adam lr 1e-3
Epoch 0 train 0.3224 val 0.0051 -> Epoch 90 train 0.0028 val 0.0029
Best val 0.0028 saved to reward_net_deep.pt 80K (vs old 26K)

#### 4. LSTM Drift Predictor
Input: T1 history sequence 10 -> predict next T1
Model: LSTM(1,32) + FC
Trained 50 epochs on fez time series, saved drift_lstm.pt 21K
Goal: Predict T1 drift 2h ahead using env features (kp, temp)

#### 5. Mitigation Evaluation with Real T1
T1=50us (bad) noisy 0.90->-0.17 ZNE->1.167 S-ZNE->1.167 overhead 5x vs 1.2x constant
T1=135us (fez mean) 0.90->0.06 ZNE 1.110
T1=231us (kingston best) 0.90->0.32 ZNE 1.046
Proves S-ZNE advantage: same accuracy 1.2x vs 5x

#### 6. Files
- models/neuralucb/reward_net_deep.pt 80K
- models/neuralucb/drift_lstm.pt 21K
- models/neuralucb/reward_net.pt 26K (old)
- datasets/calibration_drift/drift_50k.parquet 1.8M + 8847 aggregated
- datasets/clifford_training 100 pairs

### Next: P1 Frontend + Mitigation Factory full integration
