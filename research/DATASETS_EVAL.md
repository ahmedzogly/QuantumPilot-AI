# Evaluation of All Sources for QuantumPilot AI

## Date: 2026-07-11
## Data Already Pulled Live:
- ibm_fez, marrakesh, kingston calibration (T1, T2, readout, CZ errors)
- phanerozoic/qiskit-calibration-drift 8M rows -> 50k sample + agg
- weiyouLiao S-ZNE repo
- nvidia/QCalEval 243 images

---

## New Sources from User's AI Mode Conversation

### 1. Error Mitigation Dataset Definition (arXiv 2311.01727, 2511.03556)
**Structure:** Noisy Outputs + Ideal Labels + Hardware Metadata (T1,T2,fidelities)
**Use for QuantumPilot:** This is exactly our Domain Model - BackendCalibration (metadata) + ExecutionResult (counts/shots) + Statevector simulation (ideal). Confirm our architecture is correct.

### 2. Neura-parse/quantum-error-mitigation-and-benchmarking (HF, 113k rows)
**Content type:** Not numeric counts, but educational corpus: concepts (ZNE folding G->G(G†G)^n, Richardson vs exponential), CDR near-Clifford, PEC Pauli-Lindblad, Symmetry verification. 102k train, 11.4k test.
**Usefulness:** HIGH for LLM
- Fine-tune granite-8b-qiskit with RAG
- Auto-generate docs/ERROR_MITIGATION.md
- Use as knowledge base for Granite assistant in API
- NOT useful as numerical training for NeuralUCB

### 3. QNTK-UCB: Quantum-Enhanced Neural Contextual Bandit (arXiv:2601.02870, 2026)
**Key finding:** By freezing QNN at random init and using QNTK kernel for ridge regression, they achieve parameter scaling Ω((TK)^3) vs classical NeuralUCB Ω((TK)^8) for same regret. Superior sample efficiency low-data.
**Usefulness:** VERY HIGH - Future upgrade
- Our current NeuralUCB uses classical RewardNet. QNTK-UCB is drop-in replacement for low-data regime (first 100 executions).
- Can implement as `infrastructure/ai/neuralucb/qntk_engine.py` alternative
- Proves quantum advantage for bandits.

### 4. Quantum Contextual Bandits and Recommender (arXiv:2301.13524)
**Idea:** Observable = context, unknown quantum states = actions, low-energy recommendation = classifying phase of Hamiltonian (Ising, cluster model).
**Usefulness:** MEDIUM - Theoretical foundation
- Justifies our formulation: Hamiltonian/Context -> Backend recommendation
- Could add phase-classifier as feature in CircuitProfile

### 5. Deep Learning Approaches to QEM (arXiv:2601.14226, 48 pages, 2026)
**Key finding:** Systematic comparison: Fully Connected vs Transformers. Sequence-to-sequence attention models best for 5 qubit IBM QPU data. Generalization across similar devices works without full retrain.
**Usefulness:** HIGH
- For Mitigation Manager: Instead of linear regression (S-ZNE), use Transformer seq2seq for count distribution correction
- Input features they tested: circuit, device properties, noisy stats - exactly our context vector
- Suggests we should add transformer-based mitigator as option alongside S-ZNE

### 6. Physics-inspired ML for QEM - NNAS (arXiv:2501.04558)
**Key finding:** Neural Noise Accumulation Surrogate incorporates noise accumulation structural characteristics across layers. Reduces dataset by 10x and errors by >50% for deep circuits.
**Usefulness:** CRITICAL for Deep Circuit Handling
- Our current ExecutionDecision does not model layer-wise accumulation
- NNAS architecture: we should add layer index as feature to RewardNet
- Implement as `infrastructure/ai/mitigation/nnas.py` - captures how error grows with depth

### 7. ML-based QEM for Variational Algorithms (arXiv:2606.02697, n=12 VQE SK Hamiltonian)
**Key finding:** Generates training data by simulating (near-)Clifford circuits (80% Clifford + few non-Clifford). Model selection + training, transfers across Hamiltonians of similar structure. Several-fold suppression, beats ZNE in high-noise regime.
**Usefulness:** VERY HIGH for VQE/QAOA
- Exactly our use case: Project Management has VQE experiments
- Training data generation protocol: we can reuse our Aer simulator to generate near-Clifford circuits
- Implement as training pipeline in `scripts/generate_clifford_training.py`

### 8. Q-LEAR (FSE 2024, IBM 8 quantum computers)
**Features:** Circuit-level: Cw (width), Cd (depth), Gc1q, Gc2q, plus Dpe features from subcircuits. Output-level: counts. Achieved 25% avg improvement over QRAFT baseline on real IBM hardware.
**Usefulness:** HIGH - Feature Engineering Gold
- Their feature set should be merged into our CircuitProfile + BackendCalibration context
- Q-LEAR's subcircuit division for Dpe is novel - we can add to Backend Selection Engine
- Comparison baseline: we must compare NeuralUCB vs Q-LEAR in research/ResearchNotes.md

### 9. Mitiq (Unitary Fund) - THE Standard
**Modules:** ZNE (zne), PEC (pec), CDR (cdr), DDD (ddd), REM (rem), QSE (qse), LRE (lre), experimental TREX, VD, Shadows
**Usefulness:** CRITICAL - Must Integrate
- Do NOT reinvent ZNE/PEC - wrap mitiq.zne.construct_circuits and combine_results
- Our Error Mitigation Manager should be a factory that delegates to Mitiq + S-ZNE + NNAS + Noise-agnostic
- Provides benchmarking utilities we need for Testing

### 10. Qruise (Germany) + 1QB NEM
**Focus:** Pulse-level ML control, raw waveforms, CNN/RNN for hardware-level mitigation
**Usefulness:** LOW for MVP, HIGH for future
- Pulse waveforms not available in our current Qiskit Runtime API (need pulse access)
- Keep as research/ideas/Ideas.md for Phase 3

---

## Decision Matrix for QuantumPilot AI

| Source | Type | Rows/Size | Module | Priority | Action |
|--------|------|-----------|--------|----------|--------|
| phanerozoic drift 8M | Parquet | 8.04M -> 50k sampled | NeuralUCB context + Drift Predictor | P0 | Already pulled, use DuckDB |
| ibm_fez live | JSON | 1.1MB | BackendCalibration | P0 | Already pulled live today |
| weiyouLiao S-ZNE | npy | 100+ files 100q | Mitigation Manager Strategy S_ZNE | P0 | Already cloned |
| QCalEval | Parquet | 243 images | Execution Monitor Vision | P1 | Already pulled |
| Neura-parse 113k | Text/Code | 113k | Granite RAG + Docs | P1 | Pull via HF (small) |
| Mitiq | Library | Code | Mitigation Manager backend | P0 | pip install mitiq, wrap |
| Q-LEAR features | Paper | Feature list | CircuitProfile + Context | P0 | Add Cw,Cd,Gc1q,Gc2q,Dpe |
| NNAS | Paper | Architecture | Deep circuit handling | P1 | Add layer-wise features |
| Deep Learning Seq2Seq Transformer | Paper | 48p | Mitigation Transformer | P2 | Implement after S-ZNE |
| QNTK-UCB | Paper | Theory | NeuralUCB Q variant | P2 | Future upgrade |
| Clifford training (2606.02697) | Protocol | 12 qubits | Training data gen | P0 | Implement generator script |
| Noise-agnostic Nature 2025 | Paper | DAEM | Mitigation fallback | P1 | Already in roadmap |

## Revised Architecture Additions

1. **CircuitProfile** extended with Q-LEAR features: Cw, Cd, Gc1q, Gc2q, Dpe
2. **BackendCalibration.to_context_vector()** extended with calibration_age from drift dataset
3. **Mitigation Manager** now factory:
   - ZNE -> mitiq.zne
   - S_ZNE -> weiyouLiao surrogate
   - PEC -> mitiq.pec
   - NNAS -> physics-inspired (layer accumulation)
   - Transformer -> Seq2Seq attention (from 2601.14226)
   - Noise-agnostic -> DAEM

4. **NeuralUCB** has two implementations: Classical (current) and QNTK-UCB (future)

5. **Granite Assistant** uses Neura-parse corpus as RAG.

## Next Steps Agreed

Based on this evaluation, we will:
- Keep existing pulled data (drift 50k, live fez, szne, qcaleval)
- Integrate Mitiq as mitigation backend (pip install)
- Extend context vector with Q-LEAR features
- Implement Clifford training data generator
- Continue building MVP with these additions
