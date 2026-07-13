# Deploy QuantumPilot Backend on Deta Space - Free No Visa - 100% Free

## Why Deta Space?
- **Free**: 1GB RAM per micro, no credit card, no PRO required
- **No Visa**: Unlike Render, Koyeb, HuggingFace Docker PRO
- **Public URL**: https://quantumpilot-backend.deta.app automatically
- **One Command**: space push

## Quick Start (2 minutes)

### 1. Install Deta Space CLI (No Visa)
```bash
# Linux/Mac
curl -fsSL https://get.deta.dev/space-cli.sh | sh

# Windows (PowerShell)
iwr https://get.deta.dev/space-cli.ps1 -useb | iex

# Verify
space --version
```

### 2. Login (Browser, No Visa)
```bash
space login
# Opens browser -> Login with GitHub/Google -> Copy code -> Paste in terminal
# No credit card required
```

### 3. Create New Project on Deta Space Dashboard
- Go to https://deta.space
- Click "New Project" -> Name: quantumpilot
- Click "Create"

### 4. Push Backend (From QuantumPilot-AI root)

```bash
cd QuantumPilot-AI

# First time: link project
space link --id <your-project-id> --name quantumpilot
# Project ID from Deta dashboard URL: https://deta.space/builder/<id>

# Push (builds Docker Python 3.11 + FastAPI + NeuralUCB 8847 ctx)
space push

# Wait 3-5 min building...
# Backend will be at: https://quantumpilot-backend.deta.app
# Docs: https://quantumpilot-backend.deta.app/docs
```

### 5. Test Live Endpoints

```bash
curl https://quantumpilot-backend.deta.app/api/v1/health
# {"status":"ok"}

curl https://quantumpilot-backend.deta.app/api/v1/backends
# [{"backend_name":"ibm_fez","T1_mean":135.6,...}] - Live data

curl https://quantumpilot-backend.deta.app/api/v1/spaceweather/live
# {"kp_index":2.0,"source":"NOAA_1m","status":"live","neutron_flux":94.6,"cosmic_ray_strength":0.945}

curl -X POST https://quantumpilot-backend.deta.app/api/v1/copilot/plan -H "Content-Type: application/json" -d '{"intent_text":"نفذ بأقل تكلفة"}'
# {"intent":{"type":"cheapest"},"plan":{"backend_name":"ibm_kingston","optimization_level":1,"mitigation_strategy":"s_zne","shots":1024}}
```

### 6. Connect Frontend Vercel to Deta Backend

- Go to https://vercel.com/dashboard -> Your project quantumpilot-ai -> Settings -> Environment Variables
- Key: NEXT_PUBLIC_API_URL
- Value: https://quantumpilot-backend.deta.app/api/v1
- Save -> Redeploy Frontend

Now https://quantumpilot-ai.vercel.app will fetch live data from Deta backend!

### Files for Deta

- **Spacefile**: Defines 2 micros: backend Python 3.11 + frontend Node 18
- **.spaceignore**: Ignores large datasets (drift_50k.csv 12M, qcaleval 22M, models *.pt large) to stay under 1GB limit - keeps essential: drift_50k.parquet 1.8M, reward_net_deep.pt 80K
- **backend/Dockerfile.deta**: Lightweight Dockerfile for Deta

### Live Data We Have

- ibm_fez 156q T1 135.6us, marrakesh 170.9us, kingston 231us BEST via CRN DIGI
- Drift 8M -> 8847 contexts T1 7.2-406.6 mean 70.9us
- Models: reward_net_deep.pt 80K loss 0.3224->0.0028 + drift_lstm.pt 21K
- Mitigation: S-ZNE 1.2x vs ZNE 5x = 76% saving
- SpaceWeather: NOAA kp 2.0 live today 2026-07-12T10:58 UTC + neutron 94.6 (قوة الأشعة الكونية) + correlation -0.197 p=0.00047

### Troubleshooting

- If push fails due to size: check .spaceignore - we ignore large CSVs and keep only parquet 1.8M
- If build fails: check logs via `space logs`
- If backend needs Postgres/Redis: Deta has built-in NoSQL Base (free) - we use memory:// fallback for Redis and SQLite for Postgres in Spacefile env

### Alternative: Deta Space Discovery

- Browse other Quantum projects: https://deta.space/discovery
- Docs: https://deta.space/docs

### Cost

- **Free**: 1GB RAM per micro, 10GB storage, 100k requests/day, no credit card, no PRO
- **Vs Render**: Render required Visa, Deta does not
- **Vs HuggingFace**: HF Docker requires PRO $9/month, Deta free
- **Vs Koyeb**: Koyeb free tier now requires Visa, Deta does not

