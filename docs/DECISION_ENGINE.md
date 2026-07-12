# DECISION_ENGINE - QuantumPilot AI - NeuralUCB + Copilot Intent Agent

## Overview
Decision Engine is the brain that makes autonomous decisions: which backend, which optimization level, which mitigation, how many shots, etc. It has two parts: NeuralUCB for backend selection and Copilot Intent Agent for natural language intent.

## NeuralUCB - Backend Selection (72 Arms)

### Problem Formulation: Contextual Bandit

- **Context:** 22-D vector per decision: backend 8-D (T1,T2,RO,CZ,SX,queue,pending,cal_age) + circuit 7-D Q-LEAR (Cw,Cd,Gc1q,Gc2q,Dpe,entanglement,is_VQE,is_QAOA) + history 3 (avg_fidelity, queue, success) + opt/mit 2 + env 2 (kp_norm,temp_norm)
- **Action:** Choose one of 72 arms: 3 backends (fez 135.6us, marrakesh 170.9us, kingston 231us BEST) *4 optimization levels (0-3) *6 mitigations (none,zne,s_zne,trex,pec,nnas,transformer)
- **Reward:** Multi-objective: R = 0.5*Fidelity -0.2*Time -0.2*Queue -0.1*Cost. If fail -1. Specifically from deep training: 0.5*fidelity_proxy - queue*0.2 - cal_age*0.05 - kp*0.01 + N(0,0.05). fidelity_proxy = (T1*0.3+T2*0.3)-RO*0.5-CZ*0.5

### Model: RewardNet

- Architecture: 22->128 ReLU->128 ReLU->1 Xavier init
- Hidden 128 (config NEURALUCB_HIDDEN_DIM)
- Loss MSE, Adam lr 1e-3, buffer 32 recent
- A_grad = lambda*I + sum(g g^T) where g = grad last layer w.r.t context
- UCB: score = f_theta(ctx) + alpha * sqrt(g^T A^{-1} g), alpha 1.0 (NEURALUCB_ALPHA), lambda 1.0
- Warmup 10 random arms
- Training: On 8847 real contexts from drift 8M (T1 7.2-406.6 mean 70.9us) aggregated via DuckDB GROUP BY backend,observed_time, 80/20 split batch 64, 100 epochs loss 0.3224->0.0028 best val -> reward_net_deep.pt 80K (vs old 26K for 50 contexts)
- Also: drift_lstm.pt 21K LSTM seq 10 T1 history -> next T1, 50 epochs

### Selection

```python
from backend.app.infrastructure.ai.neuralucb.engine import NeuralUCB
engine = NeuralUCB(context_dim=22, hidden_dim=128, alpha=1.0)
contexts = [build_context for each of 72 arms] # each 22-D
chosen_idx, ucb_scores = engine.select(contexts) # argmax UCB
backend, opt, mit = arm_meta[chosen_idx] # e.g., ibm_kingston, 2, s_zne
```

### Update (Online Learning)

```python
# After execution: reward = fidelity - time - queue - cost
loss = engine.update(context, reward) # Updates A_grad += g g^T and trains RewardNet on buffer 32
```

### Files
- backend/app/infrastructure/ai/neuralucb/engine.py: RewardNet + NeuralUCB with select(), update(), build_context(), _get_grad_features()

## Copilot Intent Agent - Natural Language Intent (9.5/10 Feature)

### Problem: User writes natural language, not config

Instead of UI with many settings, user writes:
- Arabic: "نفذ بأقل تكلفة", "اختر الجهاز الذي يحقق Fidelity أعلى من 95%", "تجنب التنفيذ وقت العاصفة الشمسية"
- English: "Execute with lowest cost", "Choose backend with fidelity >95%", "Avoid space weather storm"

Agent should build execution plan automatically and explain why.

### Implementation: backend/app/application/services/copilot_agent.py 350 lines

**IntentType Enum:**
- CHEAPEST: أقل تكلفة, cheapest, cost low
- HIGHEST_FIDELITY: أعلى دقة, fidelity >95%, 95%
- FASTEST: أسرع, fastest, low queue
- BALANCED: متوازن, balanced
- AVOID_SPACE_WEATHER: تجنب طقس فضائي, avoid space weather, cosmic ray
- HIGH_KP_AVOID: kp عالي, high kp, geomagnetic
- SPECIFIC_BACKEND: ibm_fez, kingston etc.
- AUTO: default

**Parsing:**
- Regex Arabic+English patterns
- Fidelity threshold extraction: (\d+)% or fidelity >0.
- Backend preference: contains fez, kingston, marrakesh
- Language detection: Arabic if ord>127 or contains Arabic keywords

**Plan Building:**
- Based on intent type, sets reward weights:
  - cheapest: fidelity 0.2, cost 0.5, queue 0.2, time 0.1 -> S-ZNE 1.2x + 1024 shots + lowest queue backend (kingston queue 5) -> fidelity 0.95
  - highest_fidelity: fidelity 0.7, cost 0.1, queue 0.1, time 0.1 -> kingston T1 231us + opt 3 + pec + 8192 shots -> fidelity 0.97
  - fastest: fidelity 0.2, cost 0.1, queue 0.6, time 0.1 -> no mit + opt 0 + lowest queue
  - avoid_space_weather: checks live kp 2.0 Unsettled vs 7 Severe -> if kp>=6 recommends delay, else kingston + S-ZNE + advice about cosmic ray 94.6 counts/min
- Chooses backend: if preference set use it, else cheapest/fastest -> lowest queue, else highest_fidelity/balanced -> highest fidelity_proxy (kingston 0.92)
- Expected fidelity: backend fidelity_proxy + mitigation bonus (s_zne +0.05, pec +0.08)
- Expected cost: overhead * shots/4096
- Expected queue: backend queue *10 seconds

**Explanation:**
- AR + EN + space_weather_advice + qiskit_code_suggestion via Granite + reward_weights + confidence 0.85-0.92

**Tested:**
- "نفذ بأقل تكلفة" -> cheapest -> kingston Opt1 Mit s_zne Shots 1024 Fid 0.95 Weights cost 0.5
- "اختر الجهاز الذي يحقق Fidelity أعلى من 95%" -> highest_fidelity threshold 0.95 -> kingston Opt3 Mit pec Shots 8192 Fid 0.97
- "تجنب التنفيذ وقت العاصفة الشمسية" -> avoid_space_weather -> kingston Opt2 Mit s_zne Shots 4096 Fid 0.95 + explanation about kp 2.5 Unsettled safe
- "Execute with lowest cost" -> cheapest English works too

**API:**
- POST /api/v1/copilot/plan {intent_text, kp_index=2.0, neutron_flux=94.6} -> intent + plan + space_weather + novelty note
- GET /copilot/examples -> 5 Arabic + 5 English examples + intent_types list

**Frontend:**
- CopilotChat.tsx with example buttons, input, Build Plan button, shows plan backend, opt, mit, shots, fidelity, explanation AR, weights, space weather kp, neutron, risk, novelty note

**Integration:**
- Uses live SpaceWeatherService NOAA kp 2.0 + neutron 94.6 + solar 74.65° + temp 18.8C -> kp_norm 0.222, temp_norm 0.646 as last 2 dims of 22-D context
- Uses GraniteClient for Qiskit code suggestion: Build VQE for H2 etc.

### Combined Decision Flow

1. User writes intent in CopilotChat: "نفذ بأقل تكلفة"
2. Frontend calls POST /copilot/plan with intent_text + live kp from /spaceweather/live
3. CopilotIntentAgent.parse_intent -> type CHEAPEST language ar
4. Copilot builds plan with reward weights cost 0.5 etc + chooses backend kingston (lowest queue) + mit s_zne 1.2x + shots 1024
5. Plan includes explanation AR: "اخترت أقل تكلفة: S-ZNE 1.2x بدل 5x توفير 76%..."
6. If user wants to execute, Frontend calls POST /decide or /execute with plan details
7. Backend uses NeuralUCB with context including kp_norm,temp_norm from live SpaceWeatherService to make final decision - if kp high, it will adjust reward -kp*0.01 and maybe switch backend
8. Execution -> Result with reward -> NeuralUCB.update -> A_grad

### Files
- copilot_agent.py 350 lines
- CopilotChat.tsx 5.2K
- router.py + /copilot/plan + /copilot/examples

### Novelty
First quantum platform to parse Arabic intent + space weather aware + explainable + NeuralUCB 22-D (Backend 8 + Q-LEAR 7 + Env 2 kp,temp) as per ChatGPT analysis of 9.5/10 Integrated Platform
