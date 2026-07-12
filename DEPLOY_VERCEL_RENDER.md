# Deploy QuantumPilot AI - Public URL - Vercel + Render - One Click

## Goal: Get https://quantumpilot-ai.vercel.app live

We have built Docker Prod 6 services, now deploy to cloud for public usage.

### Option 1: Vercel (Frontend) + Render (Backend) - Recommended - Free Tier

#### Step 1: Deploy Backend to Render.com (5 min)

1. Go to https://dashboard.render.com/ -> New -> Blueprint -> Connect Repo `ahmedzogly/QuantumPilot-AI`
2. Render will detect `render.yaml` - it contains:
   - `quantumpilot-backend` Docker Python 3.11 with Mitiq + FastAPI + NeuralUCB 8847 ctx + SpaceWeather LIVE NOAA
   - `quantumpilot-postgres` Starter Postgres 15
   - `quantumpilot-redis` Starter Redis 7
   - `quantumpilot-frontend-ssr` Node SSR for Recharts
3. Set Environment Variables in Render Dashboard:
   ```
   IBM_TOKEN=YOUR_IBM_TOKEN_HERE (or use live data already fetched fez 135.6us etc)
   IBM_CRN=YOUR_IBM_CRN_HERE
   HF_TOKEN=YOUR_HF_TOKEN_HERE (optional, has mock fallback)
   SECRET_KEY=random-32-chars
   ```
4. Deploy -> Wait 5 min -> Backend will be at `https://quantumpilot-backend.onrender.com`
5. Test: `https://quantumpilot-backend.onrender.com/api/v1/health` -> {"status":"ok"}
   `https://quantumpilot-backend.onrender.com/api/v1/backends` -> fez 156q live
   `https://quantumpilot-backend.onrender.com/api/v1/spaceweather/live` -> NOAA kp 2.0 live + neutron 94.6
   `https://quantumpilot-backend.onrender.com/api/v1/copilot/plan` POST {"intent_text":"نفذ بأقل تكلفة"} -> plan

#### Step 2: Deploy Frontend to Vercel (2 min)

1. Go to https://vercel.com/new -> Import `ahmedzogly/QuantumPilot-AI` -> Select `frontend` as Root Directory
2. Vercel will detect Next.js - it uses `frontend/vercel.json` + `frontend/next.config.js`
3. Set Environment Variable:
   ```
   NEXT_PUBLIC_API_URL=https://quantumpilot-backend.onrender.com/api/v1
   ```
4. Deploy -> Wait 2 min -> Frontend will be at `https://quantumpilot-ai.vercel.app` (or your vercel domain)
5. Open: You will see Dashboard with:
   - SpaceWeatherChart LIVE (kp 2.0 Unsettled, neutron 94.6, solar 74.65°)
   - BackendChart (fez 135.6us, kingston 231us BEST)
   - TrainingChart (loss 0.3224->0.0028 from 8847 contexts)
   - T1vsKpChart Scatter (NOVELTY space weather correlation -0.197)
   - MitigationChart (S-ZNE 1.2x vs ZNE 5x = 76% saving)
   - CopilotChat: Type "نفذ بأقل تكلفة" -> Build Plan button -> Shows backend kingston Opt1 Mit s_zne Shots 1024 Fid 0.95 + explanation AR

#### Step 3: Connect Frontend to Backend

- In Vercel Dashboard -> Settings -> Environment Variables -> NEXT_PUBLIC_API_URL = your Render backend URL
- Redeploy Frontend
- Now CopilotChat and all Recharts fetch from live backend + live NOAA

### Option 2: All on Render (Simplest)

- Use `render.yaml` that defines both backend Docker and frontend Node SSR
- One click deploy button: [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/ahmedzogly/QuantumPilot-AI)
- Both services in same region Oregon for low latency

### Option 3: Local Docker (Already Working)

```bash
cp .env.example .env
# Edit IBM_TOKEN, IBM_CRN, HF_TOKEN
docker-compose -f docker-compose.prod.yml up --build -d
# Backend http://localhost:8000/docs
# Frontend http://localhost:3000
# RabbitMQ http://localhost:15672 guest/guest
# SpaceWeather logs ./logs/spaceweather_latest.json
```

### Environment Variables Needed

#### Backend (Render)
- POSTGRES_HOST, USER, PASS, DB -> auto from Render database
- REDIS_URL -> auto from Render Redis
- IBM_TOKEN, IBM_CRN -> Your IBM Quantum CRN DIGI (or use live data already fetched)
- HF_TOKEN -> Optional, has mock fallback for Granite
- SECRET_KEY -> Generate random 32 chars

#### Frontend (Vercel)
- NEXT_PUBLIC_API_URL -> https://quantumpilot-backend.onrender.com/api/v1

### Cost

- **Vercel Frontend**: Free 100GB bandwidth
- **Render Backend Starter**: $7/month + Postgres Starter $7 + Redis Starter $10 = ~$24/month for 24/7
- **Alternative Free**: Use Render Free tier (spins down after 15 min idle) + Supabase Postgres free + Upstash Redis free = $0 but slower cold start

### Verification Checklist

- [ ] Backend /health returns ok
- [ ] /backends returns fez 135.6us, marrakesh 170.9us, kingston 231us
- [ ] /spaceweather/live returns NOAA kp 2.0 live + neutron 94.6 cosmic ray strength
- [ ] /copilot/plan with "نفذ بأقل تكلفة" returns backend kingston opt1 mit s_zne
- [ ] Frontend shows 6 Recharts + SpaceWeatherChart LIVE + CopilotChat with Arabic examples
- [ ] SpaceWeather background job every 10 min fetches NOAA

### Public URLs After Deploy

- Frontend: https://quantumpilot-ai.vercel.app (or your vercel.app)
- Backend: https://quantumpilot-backend.onrender.com/api/v1/docs
- Backend Health: https://quantumpilot-backend.onrender.com/api/v1/health
- Space Weather Live: https://quantumpilot-backend.onrender.com/api/v1/spaceweather/live
- Copilot: POST https://quantumpilot-backend.onrender.com/api/v1/copilot/plan

### Current Status

- Code pushed to https://github.com/ahmedzogly/QuantumPilot-AI main branch
- CI SUCCESS: 5 jobs lint, docs-check 20 files, research-validation drift_50k 1.8M + clifford 100 + reward_net_deep 80K, security-scan, docker-build-test
- Docker files ready: backend/Dockerfile Python 3.11 for Mitiq, frontend/Dockerfile Node 20
- Live data: ibm_fez 135.6us etc + 8M drift 50k sample + 8847 aggregated contexts + 100 clifford + QCalEval 243 + models 80K
- Ready for one-click deploy via render.yaml + vercel.json

