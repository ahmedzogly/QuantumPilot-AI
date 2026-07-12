# NeuralUCB Engine - Design Doc

## Why NeuralUCB not PPO/DQN
Quantum execution is contextual bandit: each decision independent, immediate reward (fidelity, queue, cost). No long MDP. PPO would waste quantum seconds on exploration.

## Context Vector 22-D
Backend part (8) from live ibm_fez fetch:
- T1_mean/300, T2_mean/300, readout_error_mean*10, cz_error_mean*10, cz_error_std*10, queue/100, pending/100, calibration_age/3600

Circuit part (7) from Circuit Analyzer:
- num_qubits/156, depth/500, width/156, num_2q/1000, entanglement_ratio, is_VQE, is_QAOA

History (3):
- avg_fidelity_last_10, avg_queue_last_10, success_rate

Opt/Mitigation (2) encoded per arm + 2 padding = 22

## Arms
72 arms = 3 backends (fez,marrakesh,kingston) * 4 opt_levels * 6 mitigations (none,zne,s_zne,trex,pec,noise_agnostic)

## UCB Formula
score = f_theta(context) + alpha * sqrt(g^T A^{-1} g)
g = grad last layer w.r.t context

## Training
- Buffer 32 recent (context,reward)
- Adam lr 1e-3
- A_grad = lambda*I + sum(g g^T)
- Cold start: warmup 10 random + pretrain on drift_agg.csv

## Reward
R = 0.5*Fidelity -0.2*Time/10s -0.2*Queue/60s -0.1*Cost/600s
If fail: -1

## Implementation Path
File: backend/app/infrastructure/ai/neuralucb/engine.py
Model: RewardNet 22->128->128->1
Device CPU for MVP, GPU later

## Future
- Use drift dataset to predict T1 drift with LSTM and feed as feature
- Multi-objective Pareto UCB
