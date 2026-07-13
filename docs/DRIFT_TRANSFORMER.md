# Drift Transformer - Strengthening LSTM - Not Replacing NeuralUCB

## ReasoningBrain Analysis - لا تستبدل، ادمج الاثنين 🔥

**NeuralUCB و LSTM/Transformer يحلون مشكلتين مختلفتين:**

| المكون | الوظيفة |
|---|---|
| **LSTM/Transformer** | يتنبأ بـ "كيف ستكون صحة الكيوبت بعد 10-30 دقيقة؟" (Forecasting) |
| **NeuralUCB** | يقرر "أي إعداد أختار الآن بناءً على الوضع الحالي؟" (Decision-Making) |

**الهيكل المثالي (المنفذ في QuantumPilot AI):**

```
بيانات T1/T2 التاريخية + Kp-index + Neutron Flux + Solar + RO + CZ (8 features)
        ↓
   LSTM (يتنبأ قصير المدى 10-20 دقيقة) + Transformer (يتنبأ طويل المدى 30-60 دقيقة مع Attention)
        ↓
   Ensemble weighting (متعلم)
        ↓
   التنبؤات المستقبلية لـ T1 كـ Features إضافية
        ↓
   NeuralUCB (22-D Context + Future T1)
   (يتخذ قرار Backend + Optimization + Mitigation)
        ↓
   التنفيذ الأمثل
```

**لماذا هذا أقوى من الاستبدال؟**

- **بدون LSTM/Transformer:** NeuralUCB يرى الحالة الحالية فقط. لو T1 ممتاز الآن لكن عاصفة شمسية قادمة بعد 20 دقيقة (والمهمة تحتاج 30 دقيقة)، سيختار قراراً خاطئاً.

- **مع LSTM/Transformer:** NeuralUCB يرى الحالة الحالية + التوقع المستقبلي، فيقرر مثلاً: "أؤجل التنفيذ 45 دقيقة" أو "أختار جهازاً أقل تأثراً بالعاصفة".

## Implementation in QuantumPilot AI

### Models Created (Today)

1. **drift_lstm.pt** 21KB (Existing - Short-term)
   - Input: T1 history seq 10, 1 feature
   - LSTM(1,32) + FC
   - Seq 10 -> Next T1, 50 epochs, loss 0.99
   - Good for recent trends, low memory

2. **drift_transformer.pt** 1.5MB (NEW - Long-term with Attention)
   - Input: 8 features (T1,T2,kp,neutron,temp,solar,RO,CZ) seq 10
   - Architecture: Input Projection 8->64 + Positional Encoding + TransformerEncoder 2 layers nhead 4 dim_feedforward 128 + FC 64->32->1
   - Positional Encoding: sin/cos for temporal order
   - Attention over all past points: Captures space weather influence better than LSTM sequential
   - Training: 263 sequences from drift_50k (filtered to 2000 rows with T1 not null), 8 features normalized, 80/20 split batch 32 Adam 1e-3 60 epochs
   - Best val loss 0.1548 saved
   - Good for long-range dependencies 30-60 min, space weather

3. **drift_ensemble.pt** 1.6MB (NEW - Combined)
   - LSTM (short-term 10-20 min) + Transformer (long-term 30-60 min)
   - Ensemble weighting learnable softmax [LSTM weight, Trans weight] -> final prediction
   - Training: 40 epochs, best val 0.1215 weights LSTM 0.49 Trans 0.51 (balanced, slightly more Transformer)
   - Robust: LSTM for short-term, Transformer for long-term

### Training Data

- Source: drift_50k.parquet 50k sample of 8M, filtered to 2000 rows with T1 not null, then 273 rows for Transformer (after grouping and filtering)
- Features: T1_us, T2_us, kp, neutron, temp, solar, RO, CZ - all normalized (mean/std)
- Sequences: history 10 -> future 1, 263 sequences, shape X (263,10,8) y (263,)
- Input_dim for Transformer: 8

### Results

- **LSTM alone:** loss ~0.99 (not great due to small data 167-1000 points)
- **Transformer alone:** val loss 0.1548 best (much better - attention helps)
- **Ensemble:** val loss 0.1215 best (best of both - 0.49 LSTM + 0.51 Transformer)

### Integration with NeuralUCB

```python
# Historical 8 features
historical = [T1_hist[0..9], T2, kp, neutron, temp, solar, RO, CZ]  # 8 features

# LSTM predicts short-term future
future_T1_lstm = lstm_model(historical)  # T1 after 15 min

# Transformer predicts long-term with attention to kp
future_T1_transformer = transformer_model(historical_with_env)  # T1 after 30 min, attention to kp spike

# Ensemble
future_T1 = 0.49*future_T1_lstm + 0.51*future_T1_transformer

# Feed as extra feature to NeuralUCB
context_22d = [
  T1_now/300, T2/300, RO*10, CZ*10, ... # 8 backend
  + Q-LEAR 7 + History 3 + Opt/Mit 2
  + kp_norm, temp_norm, future_T1_norm  # 3 env + future - Now 23-D? Actually we keep 22-D with future replacing one pad
]
decision = NeuralUCB.select(contexts)  # Decision aware of future
```

### Why Strengthening, Not Replacing?

- **NeuralUCB** = Decision-Making: Which backend/opt/mitigation to choose NOW based on current + future predicted state
- **LSTM/Transformer** = Forecasting: What will T1 be in 10-30 min?
- Together: Optimal Execution - If future T1 predicted low due to incoming storm kp 7, NeuralUCB can decide to delay 45 min or switch to less affected backend

Without LSTM: NeuralUCB sees current T1 excellent but storm coming in 20 min (task needs 30 min) -> wrong decision
With LSTM/Transformer: NeuralUCB sees current + future -> correct decision: delay or switch

### Files

- backend/app/infrastructure/ai/neuralucb/drift_transformer.py 3.5K: DriftTransformer + DriftPredictorEnsemble + PositionalEncoding
- models/neuralucb/drift_lstm.pt 21K (short-term)
- models/neuralucb/drift_transformer.pt 1.5MB (long-term attention)
- models/neuralucb/drift_ensemble.pt 1.6MB (combined)
- scripts/train_drift_transformer.py: Training on 273 sequences 8 features 60 epochs + 40 epochs ensemble

### Future

- Add more env features: pressure, humidity, bz_gsm, ap_index, solar_flux for better Transformer attention
- Use Transformer decoder for multi-step forecasting (10,20,30 min ahead)
- Add uncertainty estimation: Transformer attention weights show which past time points and which env features influenced prediction most (explainability)
- Deploy ensemble as microservice for real-time T1 forecasting every 10 min via Celery Beat

