# AI_ENGINE - QuantumPilot AI - The Brain

## Overview
AI Engine is the brain: NeuralUCB (72 arms decision) + Drift Predictor LSTM + Granite Code Assistant + SpaceWeather Feature

## Components (Detailed in docs/NEURALUCB.md, docs/GRANITE_SIZE.md, docs/DECISION_ENGINE.md)

### 1. NeuralUCB - Main Decision Engine
- Context 22-D: Backend 8 (T1/300,T2/300,RO*10,CZ*10,SX*10,queue,pending,cal_age) + Circuit 7 Q-LEAR + History 3 + Env 2 kp,temp + Opt/Mit 2
- Model RewardNet 22->128->128->1 Xavier, A_grad = lambda*I + sum(g g^T), UCB = f_theta + alpha*sqrt(g^T A^-1 g)
- Training: 8847 contexts from drift 8M, loss 0.3224->0.0028 best val -> reward_net_deep.pt 80K + drift_lstm.pt 21K
- Reward: 0.5*Fidelity -0.2*Time -0.2*Queue -0.1*Cost, with -kp*0.01 for space weather

### 2. QNTK-UCB Future (arXiv:2601.02870)
- Scaling (TK)^3 vs (TK)^8 classical, quantum advantage low-data

### 3. Drift Predictor LSTM
- Seq 10 T1 history + env kp,temp,neutron -> next T1, LSTM(1,32)+FC

### 4. Granite-8B Code Assistant 0GB API
- Qiskit/granite-8b-qiskit 8B 46.5% HumanEval, FP16 16GB vs Q4 4.9GB vs API 0GB, client mock fallback Bell/VQE/QAOA

### 5. SpaceWeather Feature (NOVELTY)
- 8M dataset includes kp_index, neutron_flux, solar_zenith, temperature, pressure, bz_gsm_nt
- Correlation T1 vs kp -0.197 p=0.00047 significant, T1 vs solar -0.216, Severe kp>=6 T1 251us 40% drop
- Live Service NOAA 1m API + Oulu NMDB + Forbush model + Open-Meteo + solar calc 74.65°

### Files
- engine.py RewardNet + NeuralUCB
- drift_lstm, granite/client.py, spaceweather_service.py, copilot_agent.py

### Research Novelty
- First to use kp, neutron, solar as features for backend selection
- Space weather correlation -0.197
- S-ZNE constant overhead 1.2x vs 5x = 76% saving
