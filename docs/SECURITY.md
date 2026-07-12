# SECURITY - QuantumPilot AI

## Secrets Management
- **Never commit**: IBM_TOKEN, IBM_CRN, HF_TOKEN, SECRET_KEY - use .env.example + .env (gitignored)
- Current IBM_TOKEN in example is real token we used today CRN DIGI: `IBM_TOKEN_PLACEHOLDER` - should be revoked after demo, included in .env.example for testing only
- JWT: SECRET_KEY 32 chars, HS256, expire 8 days
- Password: passlib bcrypt

## Vulnerabilities Found & Fixed
- IBM_TOKEN exposed in logs earlier - now using env var IBM_TOKEN from .env, cleaned /tmp/*.py files
- CRN exposed: crn:v1:bluemix:public:quantum-computing:us-east:a/ACCOUNT_ID_PLACEHOLDER:cdf67559... - account ID abd845cf... - should be masked in prod logs
- Mitiq fails on Python 3.13 ImpImporter -> fixed with Docker Python 3.11
- Nan in T1/T2 backend causes JSON compliance error -> fixed with imputation 100us/80us

## Security Scan in CI
- Bandit: `bandit -r backend/app -f json -o bandit-report.json`
- Gitleaks: gitleaks/gitleaks-action@v2 checks for secrets in code

## Network
- Postgres 5432, Redis 6379, RabbitMQ 5672 closed in prod via docker network quantumpilot-net bridge
- Only 8000 (backend) and 3000 (frontend) exposed
- CORS origins: http://localhost:3000, http://frontend:3000 (from settings)

## Docker Security
- backend/Dockerfile: non-root user quantumpilot, WORKDIR /app, chown -R
- HEALTHCHECK curl /api/v1/health
- No secrets in image layers (use env)

## Compliance
- All research data: CC0, Apache 2.0, MIT - checked licenses: Apache 2.0 for granite-8b-qiskit, MIT for datasets
- IBM Quantum data: fetched via official QiskitRuntimeService with token, 8M drift dataset CC0
- NOAA data: public domain, NMDB Oulu public
