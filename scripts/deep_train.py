import pandas as pd, numpy as np, sys
from pathlib import Path
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "backend"))

import torch
import torch.nn as nn
import duckdb, json, random

DATASET_ROOT = ROOT / "datasets"
parquet_path = DATASET_ROOT / "calibration_drift" / "drift_50k.parquet"
con = duckdb.connect()

query = f"""
SELECT 
    backend,
    observed_time,
    AVG(CASE WHEN property='T1' THEN value END) as T1_mean,
    AVG(CASE WHEN property='T2' THEN value END) as T2_mean,
    AVG(CASE WHEN property='readout_error' THEN value END) as RO_mean,
    AVG(CASE WHEN property LIKE '%cz%error%' OR property='cz_error' THEN value END) as CZ_mean,
    AVG(CASE WHEN property LIKE '%sx%error%' THEN value END) as SX_mean,
    AVG(calibration_age_seconds) as cal_age_mean,
    AVG(temperature_c) as temp_mean,
    AVG(kp_index) as kp_mean,
    AVG(neutron_flux) as neutron_mean,
    AVG(solar_zenith_deg) as solar_mean,
    COUNT(*) as n
FROM parquet_scan('{parquet_path}')
GROUP BY backend, observed_time
ORDER BY observed_time
LIMIT 10000
"""
df_context = con.execute(query).fetch_df()
print(f"Aggregated {df_context.shape}")

# Fill NaN with means
for col in ['T1_mean','T2_mean','RO_mean','CZ_mean','SX_mean','cal_age_mean','temp_mean','kp_mean','neutron_mean','solar_mean']:
    df_context[col] = df_context[col].fillna(df_context[col].mean())

def to_us(val):
    return val*1e6 if pd.notna(val) and val < 0.01 else val

df_context['T1_mean_us'] = df_context['T1_mean'].apply(to_us)
df_context['T2_mean_us'] = df_context['T2_mean'].apply(to_us)
print(f"T1 us min {df_context['T1_mean_us'].min():.1f} max {df_context['T1_mean_us'].max():.1f} mean {df_context['T1_mean_us'].mean():.1f}")

def build_full_context(row):
    T1_norm = float(np.clip(row['T1_mean_us']/300.0, 0, 2))
    T2_norm = float(np.clip(row['T2_mean_us']/300.0, 0, 2))
    RO = float(np.clip((row['RO_mean'] or 0.02)*10, 0, 1))
    CZ = float(np.clip((row['CZ_mean'] or 0.03)*10, 0, 1))
    SX = float(np.clip((row['SX_mean'] or 0.01)*10, 0, 1))
    queue = float(np.random.uniform(0, 50)/100.0)
    pending = float(np.random.uniform(0, 20)/100.0)
    cal_age = float(np.clip((row['cal_age_mean'] or 3600)/3600.0, 0, 5))
    backend_ctx = [T1_norm, T2_norm, RO, CZ, SX, queue, pending, cal_age]
    # Circuit 7 random
    num_qubits = random.randint(3, 20)
    depth = random.randint(5, 100)
    circuit_ctx = [num_qubits/156.0, depth/500.0, num_qubits/156.0, random.uniform(0,20)/1000.0, random.uniform(0,1), 1.0 if random.random()>0.5 else 0.0, 1.0 if random.random()>0.7 else 0.0]
    hist = [float(np.clip(0.8 + (T1_norm*0.1) - RO*0.2,0,1)), float(queue*100), float(0.9 + random.uniform(-0.1,0.1))]
    kp_norm = float(np.clip((row['kp_mean'] or 2)/9.0,0,1))
    temp_norm = float(np.clip(((row['temp_mean'] or 20)+20)/60.0,0,1))
    opt_mit = [random.uniform(0,1), random.uniform(0,1)]
    env_extra = [kp_norm, temp_norm]
    full = backend_ctx + circuit_ctx + hist + opt_mit + env_extra
    if len(full) < 22:
        full = full + [0.0]*(22-len(full))
    return full[:22]

contexts=[]
for _, row in df_context.iterrows():
    contexts.append(build_full_context(row))
contexts = np.array(contexts, dtype=np.float32)
print(f"Contexts {contexts.shape}")

rewards=[]
for ctx in contexts:
    T1,T2,RO,CZ = ctx[0],ctx[1],ctx[2],ctx[3]
    queue, cal_age = ctx[5], ctx[7]
    kp = ctx[20]
    fidelity_proxy = (T1*0.3 + T2*0.3) - RO*0.5 - CZ*0.5
    fidelity_proxy = np.clip(fidelity_proxy,0,1)
    reward = 0.5*fidelity_proxy - queue*0.2 - cal_age*0.05 - kp*0.1*0.1 + np.random.normal(0,0.05)
    rewards.append(float(np.clip(reward,-1,1)))
rewards = np.array(rewards, dtype=np.float32)
print(f"Rewards mean {rewards.mean():.3f}")

# Train RewardNet
from backend.app.infrastructure.ai.neuralucb.engine import RewardNet
device="cpu"
model=RewardNet(22, hidden_dim=128).to(device)
optimizer=torch.optim.Adam(model.parameters(), lr=1e-3)
criterion=nn.MSELoss()
from sklearn.model_selection import train_test_split
X_train,X_val,y_train,y_val = train_test_split(contexts, rewards, test_size=0.2, random_state=42)
train_ds=torch.utils.data.TensorDataset(torch.from_numpy(X_train), torch.from_numpy(y_train).unsqueeze(1))
val_ds=torch.utils.data.TensorDataset(torch.from_numpy(X_val), torch.from_numpy(y_val).unsqueeze(1))
train_loader=torch.utils.data.DataLoader(train_ds, batch_size=64, shuffle=True)
val_loader=torch.utils.data.DataLoader(val_ds, batch_size=64)

best=float('inf')
for epoch in range(100):
    model.train()
    t_losses=[]
    for xb,yb in train_loader:
        optimizer.zero_grad()
        pred=model(xb)
        loss=criterion(pred,yb)
        loss.backward()
        optimizer.step()
        t_losses.append(loss.item())
    model.eval()
    v_losses=[]
    with torch.no_grad():
        for xb,yb in val_loader:
            pred=model(xb)
            v_losses.append(criterion(pred,yb).item())
    tl=np.mean(t_losses); vl=np.mean(v_losses)
    if epoch%10==0:
        print(f"Epoch {epoch} train {tl:.4f} val {vl:.4f}")
    if vl<best:
        best=vl
        torch.save(model.state_dict(), str(ROOT / "models/neuralucb/reward_net_deep.pt"))

print(f"Best {best:.4f} saved")

# LSTM Drift
print("\n=== LSTM Drift Predictor ===")
df_fez = df_context[df_context['backend']=='ibm_fez'].sort_values('observed_time')
if len(df_fez)>50:
    series=df_fez['T1_mean_us'].values
    series_norm=(series-series.mean())/(series.std()+1e-6)
    seq_len=10
    X_seq,y_seq=[],[]
    for i in range(len(series_norm)-seq_len):
        X_seq.append(series_norm[i:i+seq_len])
        y_seq.append(series_norm[i+seq_len])
    X_seq=np.array(X_seq,dtype=np.float32); y_seq=np.array(y_seq,dtype=np.float32)
    class DriftLSTM(nn.Module):
        def __init__(self):
            super().__init__()
            self.lstm=nn.LSTM(1,32,batch_first=True)
            self.fc=nn.Linear(32,1)
        def forward(self,x):
            out,_=self.lstm(x)
            return self.fc(out[:,-1,:])
    lstm=DriftLSTM()
    opt=torch.optim.Adam(lstm.parameters(), lr=1e-3)
    X_t=torch.from_numpy(X_seq).unsqueeze(-1)
    y_t=torch.from_numpy(y_seq).unsqueeze(-1)
    ds=torch.utils.data.TensorDataset(X_t,y_t)
    loader=torch.utils.data.DataLoader(ds,batch_size=32,shuffle=True)
    for epoch in range(50):
        lstm.train()
        losses=[]
        for xb,yb in loader:
            opt.zero_grad()
            pred=lstm(xb)
            loss=criterion(pred,yb)
            loss.backward()
            opt.step()
            losses.append(loss.item())
        if epoch%10==0:
            print(f"LSTM epoch {epoch} loss {np.mean(losses):.4f}")
    torch.save(lstm.state_dict(), str(ROOT / "models/neuralucb/drift_lstm.pt"))
    print("Saved drift_lstm.pt")

# Final eval
from backend.app.domain.services.mitigation import MitigationFactory
factory=MitigationFactory()
for T1_example in [50,135,231]:
    decay=0.1 + (300-T1_example)/300*0.2
    noisy_vals=[0.9 - decay*f for f in [0,1,2,3,4]]
    zne_val=factory.create("zne").mitigate(noisy_vals)
    szne_val=factory.create("s_zne").mitigate(noisy_vals)
    print(f"T1={T1_example}us noisy {noisy_vals[0]:.2f}->{noisy_vals[-1]:.2f} ZNE->{zne_val:.3f} S-ZNE->{szne_val:.3f} overhead 5x vs 1.2x")
