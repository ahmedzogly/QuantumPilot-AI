"""
Train Drift Transformer + Ensemble for QuantumPilot AI - Strengthening LSTM
Uses 8847 contexts from drift 8M with 8 features: T1,T2,kp,neutron,temp,solar,RO,CZ
"""
import pandas as pd, numpy as np, torch, torch.nn as nn, sys
from pathlib import Path
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "backend"))

import duckdb

# Load drift data
parquet_path = ROOT / "datasets/calibration_drift/drift_50k.parquet"
con = duckdb.connect()
df = con.execute(f"""
SELECT 
    backend,
    observed_time,
    AVG(CASE WHEN property='T1' THEN value END)*1e6 as T1_us,
    AVG(CASE WHEN property='T2' THEN value END)*1e6 as T2_us,
    AVG(CASE WHEN property='readout_error' THEN value END) as RO,
    AVG(CASE WHEN property LIKE '%cz%error%' THEN value END) as CZ,
    AVG(kp_index) as kp,
    AVG(neutron_flux) as neutron,
    AVG(temperature_c) as temp,
    AVG(solar_zenith_deg) as solar
FROM parquet_scan('{parquet_path}')
GROUP BY backend, observed_time
HAVING T1_us IS NOT NULL
ORDER BY observed_time
LIMIT 2000
""").fetch_df()

print(f"Loaded {df.shape} rows for Transformer training")
df = df.fillna(df.mean(numeric_only=True))
# Normalize T1 for training stability
df['T1_norm'] = (df['T1_us'] - df['T1_us'].mean()) / (df['T1_us'].std()+1e-6)

# Build sequences: history 10 -> future 1, with 8 features
features = ['T1_us','T2_us','kp','neutron','temp','solar','RO','CZ']
# Normalize features
for col in features:
    if col in df.columns:
        df[col] = df[col].fillna(df[col].mean())
        df[col+'_norm'] = (df[col] - df[col].mean()) / (df[col].std()+1e-6)

feature_cols = [c+'_norm' for c in features if c+'_norm' in df.columns]
print(f"Feature cols: {feature_cols}")

# Create sequences
seq_len = 10
X_seq, y_seq = [], []
for i in range(len(df)-seq_len):
    seq = df[feature_cols].iloc[i:i+seq_len].values.astype(np.float32)
    target = df['T1_norm'].iloc[i+seq_len]
    X_seq.append(seq)
    y_seq.append(target)

X_seq = np.array(X_seq)
y_seq = np.array(y_seq)
print(f"Sequences: X {X_seq.shape} y {y_seq.shape} - Features {len(feature_cols)} - This is input_dim for Transformer")

# Train Transformer
from backend.app.infrastructure.ai.neuralucb.drift_transformer import DriftTransformer, DriftPredictorEnsemble

device = "cpu"
input_dim = len(feature_cols)

# Split
from sklearn.model_selection import train_test_split
X_train, X_val, y_train, y_val = train_test_split(X_seq, y_seq, test_size=0.2, random_state=42)

train_ds = torch.utils.data.TensorDataset(torch.from_numpy(X_train), torch.from_numpy(y_train).unsqueeze(1))
val_ds = torch.utils.data.TensorDataset(torch.from_numpy(X_val), torch.from_numpy(y_val).unsqueeze(1))
train_loader = torch.utils.data.DataLoader(train_ds, batch_size=32, shuffle=True)
val_loader = torch.utils.data.DataLoader(val_ds, batch_size=32)

# Transformer
model = DriftTransformer(input_dim=input_dim, d_model=64, nhead=4, num_layers=2, dim_feedforward=128)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.MSELoss()

best_val = float('inf')
print("\n=== Training Drift Transformer (8 features: T1,T2,kp,neutron,temp,solar,RO,CZ) ===")
for epoch in range(60):
    model.train()
    t_losses = []
    for xb, yb in train_loader:
        optimizer.zero_grad()
        pred = model(xb)
        loss = criterion(pred, yb)
        loss.backward()
        optimizer.step()
        t_losses.append(loss.item())
    
    model.eval()
    v_losses = []
    with torch.no_grad():
        for xb, yb in val_loader:
            pred = model(xb)
            v_losses.append(criterion(pred, yb).item())
    
    tl = np.mean(t_losses)
    vl = np.mean(v_losses)
    if epoch % 10 == 0:
        print(f"Epoch {epoch:03d} train {tl:.4f} val {vl:.4f}")
    
    if vl < best_val:
        best_val = vl
        torch.save(model.state_dict(), str(ROOT / "models/neuralucb/drift_transformer.pt"))
        print(f"  -> Saved best val {best_val:.4f}")

print(f"\nBest Transformer val loss {best_val:.4f} saved to drift_transformer.pt")

# Also train Ensemble LSTM+Transformer
print("\n=== Training Ensemble LSTM+Transformer ===")
from torch.nn import LSTM

class SimpleLSTM(nn.Module):
    def __init__(self, input_dim=8, hidden=32):
        super().__init__()
        self.lstm = nn.LSTM(input_dim, hidden, batch_first=True)
        self.fc = nn.Linear(hidden, 1)
    def forward(self, x):
        out,_ = self.lstm(x)
        return self.fc(out[:,-1,:])

lstm_model = SimpleLSTM(input_dim=input_dim, hidden=32)
ensemble_transformer = DriftTransformer(input_dim=input_dim, d_model=64, nhead=4, num_layers=2)

# Load best transformer weights
ensemble_transformer.load_state_dict(torch.load(str(ROOT / "models/neuralucb/drift_transformer.pt")))

# Ensemble training - learn weights
ensemble_weight = torch.nn.Parameter(torch.tensor([0.5, 0.5]))
optimizer_ens = torch.optim.Adam(list(lstm_model.parameters()) + list(ensemble_transformer.parameters()) + [ensemble_weight], lr=1e-3)

best_ens = float('inf')
for epoch in range(40):
    lstm_model.train()
    ensemble_transformer.train()
    t_losses = []
    for xb, yb in train_loader:
        optimizer_ens.zero_grad()
        lstm_pred = lstm_model(xb)
        trans_pred = ensemble_transformer(xb)
        weights = torch.softmax(ensemble_weight, dim=0)
        ensemble_pred = weights[0]*lstm_pred + weights[1]*trans_pred
        loss = criterion(ensemble_pred, yb)
        loss.backward()
        optimizer_ens.step()
        t_losses.append(loss.item())
    
    lstm_model.eval()
    ensemble_transformer.eval()
    v_losses = []
    with torch.no_grad():
        for xb, yb in val_loader:
            lstm_pred = lstm_model(xb)
            trans_pred = ensemble_transformer(xb)
            weights = torch.softmax(ensemble_weight, dim=0)
            ensemble_pred = weights[0]*lstm_pred + weights[1]*trans_pred
            v_losses.append(criterion(ensemble_pred, yb).item())
    
    tl = np.mean(t_losses)
    vl = np.mean(v_losses)
    if epoch % 10 == 0:
        w = torch.softmax(ensemble_weight, dim=0)
        print(f"Ensemble Epoch {epoch:03d} train {tl:.4f} val {vl:.4f} weights LSTM {w[0]:.2f} Trans {w[1]:.2f}")
    
    if vl < best_ens:
        best_ens = vl
        torch.save({
            'lstm': lstm_model.state_dict(),
            'transformer': ensemble_transformer.state_dict(),
            'weights': ensemble_weight
        }, str(ROOT / "models/neuralucb/drift_ensemble.pt"))

print(f"\nBest Ensemble val {best_ens:.4f} saved to drift_ensemble.pt")
print(f"\n=== Architecture for QuantumPilot AI ===")
print(f"Historical T1/T2 + Kp + Neutron + Temp + Solar + RO + CZ (8 features)")
print(f"        ↓")
print(f"   LSTM (short-term 10-20 min) + Transformer (long-term 30-60 min with attention)")
print(f"        ↓")
print(f"   Ensemble weighting (learned)")
print(f"        ↓")
print(f"   Future T1 prediction as extra feature")
print(f"        ↓")
print(f"   NeuralUCB (Decision: Backend + Optimization + Mitigation)")
print(f"        ↓")
print(f"   Optimal Execution - Strengthening, not replacing NeuralUCB")
